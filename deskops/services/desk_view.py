"""Read-only views of one desk for the deskops UI.

Each view composes existing operations (``show_task``, ``verify_task_closeout``,
``next_action_report``, the drawer and inbox readers, the Herdr runtime and the
run index) into one JSON-ready dict. Nothing here writes: a reference that does
not resolve lands in the view's ``errors`` list with its cause, never as data.

The contract of every view is written in ``docs/deskops-ui.md``.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shlex
from typing import Any, Callable

from deskops import lifecycle
from deskops.models import BoardDoc
from deskops.models import InboxNoteDoc
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations

CONTRACT_VERSION = 1
BOARD_REF = Path("desk") / "tasks" / "Board.md"
RUN_INDEX = Path("runs") / "subagents" / "index.jsonl"
DEFAULT_RUNS_LIMIT = 20
EXCERPT_LINES = 3
_TEMPLATE_HINT = re.compile(r"^_.*_$")
_NOTE_STAMP = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-")


class DeskViewError(RuntimeError):
    """The view cannot be produced at all (no desk, unknown task)."""


def task_revision(board_path: Path, task_path: Path) -> str:
    """The advance guard: sha256 of Board.md bytes, a NUL byte, and the task file bytes.

    Same formula as graph_ui's ``DeskRoutes.detail``.
    """
    return hashlib.sha256(board_path.read_bytes() + b"\0" + task_path.read_bytes()).hexdigest()


def note_revision(path: Path) -> str:
    """The guard for inbox actions: sha256 of the note file bytes."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DeskView:
    def __init__(
        self,
        root: Path,
        *,
        operations: DeskopsOperations | None = None,
        runs_limit: int = DEFAULT_RUNS_LIMIT,
        herdr: str = "herdr",
        workers_provider: Callable[[], list[dict[str, Any]]] | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.board_path = self.root / BOARD_REF
        if not self.board_path.is_file():
            raise DeskViewError(f"No desk board at {self.board_path}; run 'deskops init' first.")
        self.ops = operations or DeskopsOperations(self.root)
        self.runs_limit = runs_limit
        self.herdr = herdr
        self._workers_provider = workers_provider
        self._spec = lifecycle.load_lifecycle_spec()

    # ------------------------------------------------------------ helpers
    def _rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return str(path)

    @staticmethod
    def _error(errors: list[dict[str, str]], reference: str, cause: str, task: str | None = None) -> None:
        item = {"reference": reference, "cause": cause}
        if task:
            item["task"] = task
        if item not in errors:
            errors.append(item)

    def _lifecycle_nodes(self) -> list[dict[str, Any]]:
        nodes = []
        for state in self._spec.states:
            node = str(state.get("current_node") or "")
            if not node or node == lifecycle.COMPLETE:
                continue
            nodes.append(
                {
                    "node": node,
                    "phase": str(state.get("phase") or ""),
                    "purpose": str(state.get("purpose") or ""),
                }
            )
        known = {item["node"] for item in nodes}
        for node in self._spec.rituals:
            if node not in known:
                nodes.append({"node": node, "phase": "", "purpose": ""})
        return nodes

    def _board_payload(self) -> dict[str, Any]:
        return self.ops._read_doc(self.board_path, BoardDoc)

    def _board_task_paths(self, errors: list[dict[str, str]]) -> list[Path]:
        tasks_dir = (self.root / "desk" / "tasks").resolve()
        paths: list[Path] = []
        for ref in self._board_payload().get("tasks") or []:
            path = (self.root / str(ref)).resolve()
            if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md":
                self._error(errors, str(ref), "Board reference is outside desk/tasks/ or is not a task file.")
                continue
            if not path.is_file():
                self._error(errors, str(ref), "Board reference points to a missing task file.")
                continue
            if path in paths:
                self._error(errors, str(ref), "Task listed twice in the Board.")
                continue
            paths.append(path)
        return paths

    def _resolve_pill(self, pill_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.pill", pill_id)
        except Exception:
            return None

    def _resolve_atom(self, atom_id: str) -> dict[str, Any] | None:
        try:
            return self.ops.show_artifact("artifact.atom", atom_id)
        except Exception:
            return None

    def _pills(
        self, refs: list[tuple[str, str]], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        pills = []
        for pill_id, source in refs:
            doc = self._resolve_pill(pill_id)
            if doc is None:
                self._error(
                    errors,
                    pill_id,
                    f"Pill referenced by the {source} does not resolve to a PillDoc.",
                    task if source == "task" else None,
                )
                continue
            item = {"id": pill_id, "title": str(doc.get("title") or ""), "source": source}
            if detail:
                item.update({key: str(doc.get(key) or "") for key in ("what", "when", "how_not")})
            pills.append(item)
        return pills

    def _atoms(
        self, ids: list[str], errors: list[dict[str, str]], *, detail: bool, task: str | None = None
    ) -> list[dict[str, Any]]:
        atoms = []
        for atom_id in ids:
            doc = self._resolve_atom(atom_id)
            if doc is None:
                self._error(errors, atom_id, "Atom referenced by the task does not resolve to an AtomDoc.", task)
                continue
            item = {"id": atom_id, "title": str(doc.get("title") or "")}
            if detail:
                item["question"] = str(doc.get("five_wh_one_plus") or "")
                item["answer"] = str(doc.get("answer") or "")
            atoms.append(item)
        return atoms

    @staticmethod
    def _atom_ids(payload: dict[str, Any]) -> list[str]:
        ids = [str(item) for item in payload.get("effective_atoms") or payload.get("atoms") or []]
        ids += [
            str(ref)
            for ref in payload.get("effective_references") or payload.get("references") or []
            if str(ref).startswith("atom-")
        ]
        return list(dict.fromkeys(ids))

    def _closeout(self, task_id: str, node: str, errors: list[dict[str, str]]) -> dict[str, Any] | None:
        try:
            report = self.ops.verify_task_closeout(task_id)
        except Exception as exc:
            self._error(errors, task_id, f"verify_task_closeout failed: {exc}")
            return None
        at_closeout = node == "ritual-closeout"
        evidence = []
        for name, gate in report.get("gates", {}).items():
            state = "holds" if gate.get("ok") else ("failing" if at_closeout else "pending")
            evidence.append(
                {
                    "gate": name,
                    "state": state,
                    "evidence": list(gate.get("evidence") or []),
                    "findings": list(gate.get("findings") or []),
                }
            )
        for finding in report.get("findings", []):
            if finding.get("code") == "unknown_closeout_evidence":
                evidence.append({"gate": "unknown", "state": "failing", "evidence": [], "findings": [finding]})
        return {
            "ok": bool(report.get("ok")),
            "declared": list(report.get("declared") or []),
            "found": list(report.get("found") or []),
            "summary": report.get("summary"),
            "implicit_code": bool(report.get("implicit_code")),
            "alerts": list(report.get("alerts") or []),
            "evidence": evidence,
        }

    def _card(
        self, path: Path, board_pills: list[str], errors: list[dict[str, str]], *, detail: bool = False
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        stem = path.stem
        payload = self.ops._resolve_task_payload(stem)
        task_id = str(payload.get("id") or stem)
        task, gates = self.ops.show_task(stem)
        node = str(payload.get("current_node") or "")
        if task is not None and not gates and node and node != lifecycle.COMPLETE:
            try:
                self.ops._transitions_from(node)
                cause = f"The desk lifecycle graph declares no transition leaving {node}."
            except Exception as exc:
                cause = f"Lifecycle gates unavailable: {exc}"
            self._error(errors, task_id, cause)
        pill_refs = [(str(p), "task") for p in payload.get("effective_pills") or payload.get("pills") or []]
        pill_refs += [(p, "board") for p in board_pills if p not in {ref for ref, _ in pill_refs}]
        card = {
            "id": task_id,
            "title": str(payload.get("title") or ""),
            "status": str(payload.get("status") or ""),
            "current_node": node,
            "task_type": str(payload.get("task_type") or ""),
            "path": self._rel(path),
            "gates": [dict(gate) for gate in gates],
            "gates_holding": sum(1 for gate in gates if gate.get("holds")),
            "gates_total": len(gates),
            "closeout": self._closeout(stem, node, errors),
            "pills": self._pills(pill_refs, errors, detail=detail, task=task_id),
            "atoms": self._atoms(self._atom_ids(payload), errors, detail=detail, task=task_id),
        }
        return card, payload

    # ------------------------------------------------------------ views
    def board(self) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._board_view()

    def _board_view(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        board = self._board_payload()
        board_pills = [str(p) for p in board.get("pills") or []]
        nodes = self._lifecycle_nodes()
        columns = {item["node"]: {**item, "in_lifecycle": True, "count": 0, "tasks": []} for item in nodes}
        for path in self._board_task_paths(errors):
            try:
                card, _ = self._card(path, board_pills, errors)
            except Exception as exc:
                self._error(errors, self._rel(path), f"Task does not load: {exc}")
                continue
            node = card["current_node"]
            if node not in columns:
                self._error(errors, card["id"], f"current_node '{node}' is not a node of the task lifecycle.")
                columns[node] = {"node": node, "phase": "", "purpose": "", "in_lifecycle": False, "count": 0, "tasks": []}
            columns[node]["tasks"].append(card)
            columns[node]["count"] += 1
        cards = [card for column in columns.values() for card in column["tasks"]]
        return {
            "view": "board",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "board": {
                "path": self._rel(self.board_path),
                "pills": self._pills([(p, "board") for p in board_pills], errors, detail=False),
            },
            "columns": list(columns.values()),
            "counts": {
                "tasks": len(cards),
                "by_node": {node: column["count"] for node, column in columns.items()},
                "gates_holding": sum(card["gates_holding"] for card in cards),
                "gates_total": sum(card["gates_total"] for card in cards),
            },
            "errors": errors,
        }

    def task(self, selector: str) -> dict[str, Any]:
        with self.ops.read_snapshot():
            return self._task_view(selector)

    def _task_view(self, selector: str) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        try:
            path = self.ops._resolve_artifact_selector("artifact.task", self.ops.desk_root / "tasks", selector)
        except (FileNotFoundError, ValueError) as exc:
            raise DeskViewError(f"Task '{selector}' does not resolve: {exc}") from exc
        board_paths = self._board_task_paths([])
        board_pills = [str(p) for p in self._board_payload().get("pills") or []]
        card, payload = self._card(path, board_pills, errors, detail=True)
        try:
            report = self.ops.next_action_report(path.stem)
            next_info = {
                "phase": report.get("phase", ""),
                "ritual": report.get("ritual", ""),
                "next_actions": list(report.get("next_actions") or []),
                "advance_when": list(report.get("advance_when") or []),
            }
        except Exception as exc:
            next_info = None
            self._error(errors, card["id"], f"next_action_report failed: {exc}")
        return {
            "view": "task",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "task": {
                **card,
                "on_board": path.resolve() in board_paths,
                "why": str(payload.get("why") or ""),
                "goal": str(payload.get("goal") or ""),
                "scope": str(payload.get("scope") or ""),
                "implementation_path": str(payload.get("implementation_path") or ""),
                "validation": [str(v) for v in payload.get("effective_validation") or payload.get("validation") or []],
                "done_when": str(payload.get("effective_done_when") or payload.get("done_when") or ""),
                "references": [str(r) for r in payload.get("effective_references") or payload.get("references") or []],
                "files": [str(f) for f in payload.get("files") or []],
                "depends_on": [str(d) for d in payload.get("depends_on") or []],
                "inherits_from": [str(i) for i in payload.get("inherits_from") or []],
                "from_drawer": str(payload.get("from_drawer") or ""),
                "history": [str(h) for h in payload.get("history") or []],
            },
            "next": next_info,
            "revision": task_revision(self.board_path, path),
            "errors": errors,
        }

    def drawer(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        drawer_dir = self.root / "desk" / "drawer" / "tasks"
        index_files = self.ops.drawer.DRAWER_INDEX_FILES
        entries = []
        files = sorted(p for p in drawer_dir.glob("*.md") if p.name not in index_files) if drawer_dir.is_dir() else []
        for path in files:
            rel = self._rel(path)
            try:
                text = self.ops.drawer._read_markdown(path)
            except Exception as exc:
                self._error(errors, rel, f"Drawer file does not parse: {exc}")
                continue
            try:
                doc = self.ops._read_doc(path, TaskDoc)
            except Exception as exc:
                doc = {}
                self._error(errors, rel, f"Drawer file is not a valid TaskDoc: {exc}")
            lines = [
                line.strip()
                for line in text["body"].splitlines()
                if line.strip() and not line.lstrip().startswith("#") and not _TEMPLATE_HINT.match(line.strip())
            ]
            entries.append(
                {
                    "id": str(doc.get("id") or path.stem),
                    "markdown": path.read_text(encoding="utf-8"),
                    "title": text["title"],
                    "status": str(doc["status"]) if doc.get("status") else None,
                    "excerpt": lines[:EXCERPT_LINES],
                    "path": rel,
                    "command": "deskops add task --root . --from-drawer "
                    + shlex.quote(rel)
                    + " --title "
                    + shlex.quote(text["title"]),
                }
            )
        return {
            "view": "drawer",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "tasks": entries,
            "count": len(entries),
            "errors": errors,
        }

    def inbox(self) -> dict[str, Any]:
        from deskops.cli.commands.message import MessageCLI

        errors: list[dict[str, str]] = []
        reader = MessageCLI()
        notes = []
        for path in reader._iter_notes(self.root / "desk"):
            rel = self._rel(path)
            try:
                detail = reader._note_detail(path)
            except Exception as exc:
                self._error(errors, rel, f"Inbox note does not parse: {exc}")
                continue
            try:
                body = str(self.ops._read_doc(path, InboxNoteDoc).get("body") or "")
            except Exception as exc:
                body = str(detail.get("body") or "")
                self._error(errors, rel, f"Inbox note is not a valid InboxNoteDoc; body shown raw: {exc}")
            match = _NOTE_STAMP.match(path.name)
            date = "{}-{}-{}T{}:{}:{}".format(*match.groups()) if match else None
            if date is None:
                self._error(errors, rel, "Inbox note filename carries no YYYYMMDD-HHMMSS stamp.")
            status = str(detail.get("status") or "")
            notes.append(
                {
                    "id": path.stem,
                    "path": rel,
                    "kind": str(detail.get("kind") or ""),
                    "title": str(detail.get("title") or ""),
                    "sender": str(detail.get("sender_project") or ""),
                    "target": str(detail.get("target_project") or ""),
                    "date": date,
                    "status": status,
                    "acknowledged": status == "closed",
                    "acknowledged_by": detail.get("acknowledged_by"),
                    "acknowledged_at": detail.get("acknowledged_at"),
                    "body": body,
                    "revision": note_revision(path),
                }
            )
        return {
            "view": "inbox",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "notes": notes,
            "count": len(notes),
            "open": sum(1 for note in notes if not note["acknowledged"]),
            "errors": errors,
        }

    def _list_workers(self) -> list[dict[str, Any]]:
        if self._workers_provider is not None:
            agents = self._workers_provider()
        else:
            from deskops.runtime.herdr import HerdrClient, HerdrProvider

            agents = HerdrProvider(HerdrClient(self.herdr)).list_agents()
        from deskops.cli.commands.runtime import RuntimeCLI

        return [RuntimeCLI._project_agent(agent) for agent in agents]

    def agents(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        workers: list[dict[str, Any]] | None
        workers_error = None
        try:
            workers = self._list_workers()
        except Exception as exc:
            workers = None
            workers_error = f"{type(exc).__name__}: {exc}"
            self._error(errors, "runtime workers", f"Herdr runtime unavailable: {workers_error}")
        board_ids = set()
        for path in self._board_task_paths([]):
            try:
                board_ids.add(str(self.ops._read_doc(path, TaskDoc).get("id") or path.stem))
            except Exception:
                continue
        runs: list[dict[str, Any]] = []
        index = self.root / RUN_INDEX
        total = 0
        if index.is_file():
            lines = index.read_text(encoding="utf-8").splitlines()
            parsed = []
            for number, line in enumerate(lines, start=1):
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    if not isinstance(entry, dict):
                        raise ValueError("entry is not an object")
                except ValueError as exc:
                    self._error(errors, f"{RUN_INDEX.as_posix()}:{number}", f"Run index line does not parse: {exc}")
                    continue
                parsed.append(entry)
            total = len(parsed)
            for entry in reversed(parsed[-self.runs_limit :] if self.runs_limit > 0 else []):
                task_id = str(entry.get("task_id") or "")
                runs.append(
                    {
                        "task_id": task_id,
                        "run_id": entry.get("run_id"),
                        "run_dir": entry.get("run_dir"),
                        "commit": entry.get("commit"),
                        "mode": entry.get("mode"),
                        "on_board": task_id in board_ids,
                    }
                )
        return {
            "view": "agents",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "workers": workers,
            "workers_error": workers_error,
            "live_workers": None if workers is None else len(workers),
            "runs": runs,
            "runs_total": total,
            "runs_limit": self.runs_limit,
            "errors": errors,
        }


# ---------------------------------------------------------------- text rendering
def _errors_text(view: dict[str, Any]) -> list[str]:
    return [f"! {item['reference']}: {item['cause']}" for item in view.get("errors") or []]


def render_text(view: dict[str, Any]) -> str:
    kind = view.get("view")
    lines: list[str] = []
    if kind == "board":
        for column in view["columns"]:
            lines.append(f"{column['node']} ({column['count']})")
            for card in column["tasks"]:
                lines.append(f"  {card['id']} [{card['status']}] gates {card['gates_holding']}/{card['gates_total']} - {card['title']}")
    elif kind == "task":
        task = view["task"]
        lines += [f"{task['id']} [{task['status']}] {task['current_node']}", task["title"], f"revision {view['revision']}"]
        for gate in task["gates"]:
            lines.append(f"  gate {gate['relation_type']} -> {gate['target']}: {'holds' if gate['holds'] else 'pending'} ({gate['condition'] or 'no condition'})")
        for item in (task.get("closeout") or {}).get("evidence", []):
            lines.append(f"  evidence {item['gate']}: {item['state']}")
    elif kind == "drawer":
        for entry in view["tasks"]:
            lines.append(f"{entry['id']} [{entry['status'] or '-'}] {entry['title']}")
    elif kind == "inbox":
        for note in view["notes"]:
            lines.append(f"{note['id']} [{'ack' if note['acknowledged'] else 'open'}] {note['sender']} -> {note['target']}: {note['title']}")
    elif kind == "agents":
        if view["workers"] is None:
            lines.append(f"workers unavailable: {view['workers_error']}")
        else:
            lines.append(f"live workers: {view['live_workers']}")
            for worker in view["workers"]:
                lines.append(f"  {worker.get('pane')} | {worker.get('kind')} | {worker.get('status')} | {worker.get('cwd') or ''}")
        lines.append(f"runs (latest {len(view['runs'])} of {view['runs_total']}):")
        for run in view["runs"]:
            lines.append(f"  {run['task_id']} | {run['mode'] or '-'} | {run['run_dir'] or '-'}")
    return "\n".join([*lines, *_errors_text(view)])
