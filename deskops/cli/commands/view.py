"""`deskops view`: the read-only views the deskops UI draws (contract: docs/deskops-ui.md).

`board` and `task` are sldb ViewDocs (`deskops/data/views/`) evaluated by
`sldb.api.run_view`; `project` turns that result into the contract. What the ViewDoc model
cannot express yet is added by the CLI from deskops' existing read operations, each named by
its pending sldb hypothesis (CC34 H1-H8):

- H1-H3 `gates`: `DeskopsOperations.show_task` (the transitions leaving the node, whether
  their condition holds, and the task's `on_transition` findings);
- H4 `closeout`: `verify_task_closeout` without writing receipts;
- H5 the lifecycle nodes' `phase`/`purpose` and `next`: the lifecycle spec and
  `next_action_report`;
- H6 the effective (inherited) pills, atoms, validation, done_when and references:
  `doc_access.resolve_task_payload`.

`drawer` and `inbox` read the desk's files (H7, H8, H10: those folders are not tracked in a
desk's store yet), and `agents` is what is not a document (`deskops.runtime.desk_agents`).
graph_ui reads `GET /views/<view>` from `sldb serve` and calls `project` in process.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import shlex
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error

CONTRACT_VERSION = 1
BOARD_REF = Path("desk") / "tasks" / "Board.md"
EXCERPT_LINES = 3
SLDB_VIEWS = ("board", "task")
_TEMPLATE_HINT = re.compile(r"^_.*_$")
_NOTE_STAMP = re.compile(r"^(\d{4})(\d{2})(\d{2})-(\d{2})(\d{2})(\d{2})-")


class ViewError(RuntimeError):
    """The view cannot be produced at all (no desk, unknown task)."""


# ---------------------------------------------------------------- sldb
def run_view(root: Path, name: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    """`sldb.api.run_view` of the ViewDoc `name` on the desk's store."""
    from sldb.api import run_view as sldb_run_view

    return sldb_run_view(Path(root) / ".sldb", name, params or {})


def _require_board(root: Path) -> Path:
    board = root / BOARD_REF
    if not board.is_file():
        raise ViewError(f"No desk board at {board}; run 'deskops init' first.")
    return board


def task_params(root: Path, selector: str) -> dict[str, str]:
    """The `task` ViewDoc's params for a task selector (id, unique prefix or file name)."""
    from deskops import doc_access

    root = Path(root).resolve()
    _require_board(root)
    try:
        path = doc_access.resolve_artifact_selector(root, "artifact.task", root / "desk" / "tasks", selector)
    except (FileNotFoundError, ValueError) as exc:
        raise ViewError(f"Task '{selector}' does not resolve: {exc}") from exc
    return {"id": str(doc_access.resolve_task_payload(root, path.stem).get("id") or path.stem)}


def board_view(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    _require_board(root)
    return project("board", run_view(root, "board"), root)


def task_view(root: Path, selector: str) -> dict[str, Any]:
    root = Path(root).resolve()
    return project("task", run_view(root, "task", task_params(root, selector)), root)


# ---------------------------------------------------------------- projection
def project(view: str, result: dict[str, Any], root: Path) -> dict[str, Any]:
    """The contract payload of `view` (`board` or `task`) from its `run_view` result, plus the
    CLI aggregates H1-H6 read from the desk at `root`."""
    if view not in SLDB_VIEWS:
        raise ViewError(f"Unknown view: {view}")
    from deskops.operations import DeskopsOperations

    root = Path(root).resolve()
    projection = _Projection(root, result, DeskopsOperations(root))
    with projection.ops.read_snapshot():
        return projection.board() if view == "board" else projection.task()


def _rows(result: dict[str, Any], key: str) -> list[dict[str, Any]]:
    section = (result.get("sections") or {}).get(key) or {}
    if "groups" in section:
        return [row for group in section["groups"] for row in group["rows"]]
    return list(section.get("rows") or [])


def _error(errors: list[dict[str, str]], reference: str, cause: str, task: str | None = None) -> None:
    item = {"reference": reference, "cause": cause}
    if task:
        item["task"] = task
    if item not in errors:
        errors.append(item)


class _Projection:
    def __init__(self, root: Path, result: dict[str, Any], ops: Any) -> None:
        self.root = root
        self.result = result
        self.ops = ops
        boards = _rows(result, "board")
        if not boards:
            raise ViewError(f"No desk board at {root / BOARD_REF}; run 'deskops init' first.")
        self.board_row = boards[0]
        self.pill_rows = _rows(result, "pills")
        self.atom_rows = _rows(result, "atoms")

    # ------------------------------------------------ lookups over the rows
    @staticmethod
    def _find(rows: list[dict[str, Any]], ref: str) -> dict[str, Any] | None:
        for row in rows:
            if ref in (row["name"], row["path"], str(row["fields"].get("id") or "")):
                return row
        return None

    def _board_pills(self) -> list[str]:
        return [str(p) for p in self.board_row["fields"].get("pills") or []]

    def _board_task_rows(self, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
        """The rows of the tasks the Board lists, in the Board's order (the Board is the truth)."""
        tasks_dir = (self.root / "desk" / "tasks").resolve()
        by_path = {(self.root / row["path"]).resolve(): row for row in _rows(self.result, "tasks")}
        chosen: list[dict[str, Any]] = []
        for ref in self.board_row["fields"].get("tasks") or []:
            path = (self.root / str(ref)).resolve()
            if not path.is_relative_to(tasks_dir) or path.suffix != ".md" or path.name == "Board.md":
                _error(errors, str(ref), "Board reference is outside desk/tasks/ or is not a task file.")
                continue
            row = by_path.get(path)
            if row is None:
                _error(errors, str(ref), "Board reference points to a missing task file.")
                continue
            if any(row is seen for seen in chosen):
                _error(errors, str(ref), "Task listed twice in the Board.")
                continue
            chosen.append(row)
        return chosen

    def _pills(self, refs: list[tuple[str, str]], errors: list[dict[str, str]], *, detail: bool, task: str | None = None) -> list[dict[str, Any]]:
        pills = []
        for pill_id, source in refs:
            row = self._find(self.pill_rows, pill_id)
            if row is None:
                _error(errors, pill_id, f"Pill referenced by the {source} does not resolve to a PillDoc.", task if source == "task" else None)
                continue
            doc = row["fields"]
            item = {"id": pill_id, "title": str(doc.get("title") or ""), "source": source}
            if detail:
                item.update({key: str(doc.get(key) or "") for key in ("what", "when", "how_not")})
            pills.append(item)
        return pills

    def _atoms(self, ids: list[str], errors: list[dict[str, str]], *, detail: bool, task: str | None = None) -> list[dict[str, Any]]:
        atoms = []
        for atom_id in ids:
            row = self._find(self.atom_rows, atom_id)
            if row is None:
                _error(errors, atom_id, "Atom referenced by the task does not resolve to an AtomDoc.", task)
                continue
            doc = row["fields"]
            item = {"id": atom_id, "title": str(doc.get("title") or "")}
            if detail:
                item["question"] = str(doc.get("five_wh_one_plus") or "")
                item["answer"] = str(doc.get("answer") or "")
            atoms.append(item)
        return atoms

    # ------------------------------------------------ CLI aggregates (H1-H6)
    def _effective(self, stem: str) -> dict[str, Any]:
        """H6: the task's payload with its inherited fields (`resolve_task_payload`)."""
        from deskops import doc_access

        return doc_access.resolve_task_payload(self.root, stem)

    @staticmethod
    def _atom_ids(payload: dict[str, Any]) -> list[str]:
        ids = [str(item) for item in payload.get("effective_atoms") or payload.get("atoms") or []]
        ids += [str(ref) for ref in payload.get("effective_references") or payload.get("references") or [] if str(ref).startswith("atom-")]
        return list(dict.fromkeys(ids))

    def _gates(self, stem: str, task_id: str, node: str, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
        """H1-H3: `show_task`'s gates; no gate out of a non-final node is an error with its cause."""
        from deskops import lifecycle

        task, gates = self.ops.show_task(stem)
        if task is not None and not gates and node and node != lifecycle.COMPLETE:
            try:
                lifecycle.transitions_from(self.root, node, snapshot=self.ops.snapshot)
                cause = f"The desk lifecycle graph declares no transition leaving {node}."
            except Exception as exc:
                cause = f"Lifecycle gates unavailable: {exc}"
            _error(errors, task_id, cause)
        return [dict(gate) for gate in gates]

    def _closeout(self, stem: str, node: str, errors: list[dict[str, str]]) -> dict[str, Any] | None:
        """H4: `verify_task_closeout` (read only), one evidence entry per gate."""
        try:
            report = self.ops.verify_task_closeout(stem)
        except Exception as exc:
            _error(errors, stem, f"verify_task_closeout failed: {exc}")
            return None
        at_closeout = node == "ritual-closeout"
        evidence = []
        for name, gate in report.get("gates", {}).items():
            state = "holds" if gate.get("ok") else ("failing" if at_closeout else "pending")
            evidence.append({"gate": name, "state": state, "evidence": list(gate.get("evidence") or []), "findings": list(gate.get("findings") or [])})
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

    @staticmethod
    def _lifecycle_nodes() -> list[dict[str, Any]]:
        """H5: the lifecycle nodes with their phase and purpose, in the spec's order."""
        from deskops import lifecycle

        spec = lifecycle.load_lifecycle_spec()
        nodes = []
        for state in spec.states:
            node = str(state.get("current_node") or "")
            if not node or node == lifecycle.COMPLETE:
                continue
            nodes.append({"node": node, "phase": str(state.get("phase") or ""), "purpose": str(state.get("purpose") or "")})
        known = {item["node"] for item in nodes}
        nodes += [{"node": node, "phase": "", "purpose": ""} for node in spec.rituals if node not in known]
        return nodes

    # ------------------------------------------------ the card
    def _card(self, row: dict[str, Any], errors: list[dict[str, str]], *, detail: bool = False) -> tuple[dict[str, Any], dict[str, Any]]:
        fields = row["fields"]
        stem = Path(row["path"]).stem
        payload = self._effective(stem)
        task_id = str(fields.get("id") or stem)
        node = str(fields.get("current_node") or "")
        gates = self._gates(stem, task_id, node, errors)
        pill_refs = [(str(p), "task") for p in payload.get("effective_pills") or payload.get("pills") or []]
        pill_refs += [(p, "board") for p in self._board_pills() if p not in {ref for ref, _ in pill_refs}]
        card = {
            "id": task_id,
            "title": str(fields.get("title") or ""),
            "status": str(fields.get("status") or ""),
            "current_node": node,
            "task_type": str(fields.get("task_type") or ""),
            "path": row["path"],
            "gates": gates,
            "gates_holding": sum(1 for gate in gates if gate.get("holds")),
            "gates_total": len(gates),
            "closeout": self._closeout(stem, node, errors),
            "pills": self._pills(pill_refs, errors, detail=detail, task=task_id),
            "atoms": self._atoms(self._atom_ids(payload), errors, detail=detail, task=task_id),
        }
        return card, payload

    # ------------------------------------------------ views
    def board(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        columns = {item["node"]: {**item, "in_lifecycle": True, "count": 0, "tasks": []} for item in self._lifecycle_nodes()}
        for row in self._board_task_rows(errors):
            try:
                card, _ = self._card(row, errors)
            except Exception as exc:
                _error(errors, row["path"], f"Task does not load: {exc}")
                continue
            node = card["current_node"]
            if node not in columns:
                _error(errors, card["id"], f"current_node '{node}' is not a node of the task lifecycle.")
                columns[node] = {"node": node, "phase": "", "purpose": "", "in_lifecycle": False, "count": 0, "tasks": []}
            columns[node]["tasks"].append(card)
            columns[node]["count"] += 1
        cards = [card for column in columns.values() for card in column["tasks"]]
        return {
            "view": "board",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "board": {"path": self.board_row["path"], "pills": self._pills([(p, "board") for p in self._board_pills()], errors, detail=False)},
            "columns": list(columns.values()),
            "counts": {
                "tasks": len(cards),
                "by_node": {node: column["count"] for node, column in columns.items()},
                "gates_holding": sum(card["gates_holding"] for card in cards),
                "gates_total": sum(card["gates_total"] for card in cards),
            },
            "errors": errors,
        }

    def task(self) -> dict[str, Any]:
        errors: list[dict[str, str]] = []
        rows = _rows(self.result, "task")
        if not rows:
            task_id = (self.result.get("params") or {}).get("id")
            raise ViewError(f"Task '{task_id}' does not resolve: it is not tracked in the desk's store.")
        row = rows[0]
        card, payload = self._card(row, errors, detail=True)
        fields = row["fields"]
        try:
            report = self.ops.next_action_report(Path(row["path"]).stem)
            next_info = {
                "phase": report.get("phase", ""),
                "ritual": report.get("ritual", ""),
                "next_actions": list(report.get("next_actions") or []),
                "advance_when": list(report.get("advance_when") or []),
            }
        except Exception as exc:
            next_info = None
            _error(errors, card["id"], f"next_action_report failed: {exc}")
        return {
            "view": "task",
            "contract": CONTRACT_VERSION,
            "root": str(self.root),
            "task": {
                **card,
                "on_board": row["export_id"] in (self.board_row.get("tasks") or []),
                "why": str(fields.get("why") or ""),
                "goal": str(fields.get("goal") or ""),
                "scope": str(fields.get("scope") or ""),
                "implementation_path": str(fields.get("implementation_path") or ""),
                "validation": [str(v) for v in payload.get("effective_validation") or payload.get("validation") or []],
                "done_when": str(payload.get("effective_done_when") or payload.get("done_when") or ""),
                "references": [str(r) for r in payload.get("effective_references") or payload.get("references") or []],
                "files": [str(f) for f in fields.get("files") or []],
                "depends_on": [str(d) for d in fields.get("depends_on") or []],
                "inherits_from": [str(i) for i in fields.get("inherits_from") or []],
                "from_drawer": str(fields.get("from_drawer") or ""),
                "history": [str(h) for h in fields.get("history") or []],
            },
            "next": next_info,
            # The ETag of the ViewDoc's result (GD25): the advance guard of graph_ui.
            "revision": self.result["revision"],
            "errors": errors,
        }


# ---------------------------------------------------------------- drawer and inbox (H10: read from disk)
def _rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError:
        return str(path)


def drawer_view(root: Path) -> dict[str, Any]:
    from deskops import doc_access
    from deskops.models import TaskDoc
    from deskops.operations import DeskopsOperations

    root = Path(root).resolve()
    _require_board(root)
    ops = DeskopsOperations(root)
    errors: list[dict[str, str]] = []
    drawer_dir = root / "desk" / "drawer" / "tasks"
    index_files = ops.drawer.DRAWER_INDEX_FILES
    entries = []
    files = sorted(p for p in drawer_dir.glob("*.md") if p.name not in index_files) if drawer_dir.is_dir() else []
    for path in files:
        rel = _rel(root, path)
        try:
            text = ops.drawer._read_markdown(path)
        except Exception as exc:
            _error(errors, rel, f"Drawer file does not parse: {exc}")
            continue
        try:
            doc = doc_access.read_doc(path, TaskDoc)
        except Exception as exc:
            doc = {}
            _error(errors, rel, f"Drawer file is not a valid TaskDoc: {exc}")
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
                "command": "deskops add task --root . --from-drawer " + shlex.quote(rel) + " --title " + shlex.quote(text["title"]),
            }
        )
    return {"view": "drawer", "contract": CONTRACT_VERSION, "root": str(root), "tasks": entries, "count": len(entries), "errors": errors}


def inbox_view(root: Path) -> dict[str, Any]:
    from deskops import doc_access
    from deskops.cli.commands.message import MessageCLI
    from deskops.models import InboxNoteDoc

    root = Path(root).resolve()
    _require_board(root)
    errors: list[dict[str, str]] = []
    reader = MessageCLI()
    notes = []
    for path in reader._iter_notes(root / "desk"):
        rel = _rel(root, path)
        try:
            detail = reader._note_detail(path)
        except Exception as exc:
            _error(errors, rel, f"Inbox note does not parse: {exc}")
            continue
        try:
            body = str(doc_access.read_doc(path, InboxNoteDoc).get("body") or "")
        except Exception as exc:
            body = str(detail.get("body") or "")
            _error(errors, rel, f"Inbox note is not a valid InboxNoteDoc; body shown raw: {exc}")
        match = _NOTE_STAMP.match(path.name)
        date = "{}-{}-{}T{}:{}:{}".format(*match.groups()) if match else None
        if date is None:
            _error(errors, rel, "Inbox note filename carries no YYYYMMDD-HHMMSS stamp.")
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
                # The guard of the inbox actions: sha256 of the note's bytes (H8).
                "revision": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    return {
        "view": "inbox",
        "contract": CONTRACT_VERSION,
        "root": str(root),
        "notes": notes,
        "count": len(notes),
        "open": sum(1 for note in notes if not note["acknowledged"]),
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


class ViewCLI:
    """Read-only views of a desk for the deskops UI (contract: docs/deskops-ui.md)."""

    def run(self, args: Any) -> int:
        from sldb.core.exceptions import SLDBError

        fmt = getattr(args, "format", "text")
        root = Path(args.root).resolve()
        try:
            command = args.view_command
            if command == "board":
                payload = board_view(root)
            elif command == "task":
                payload = task_view(root, args.task_id)
            elif command == "drawer":
                payload = drawer_view(root)
            elif command == "inbox":
                payload = inbox_view(root)
            elif command == "agents":
                from deskops.runtime.desk_agents import agents_view

                payload = agents_view(root, runs_limit=getattr(args, "runs", 20), herdr=getattr(args, "herdr", "herdr"))
            else:
                return render_error(f"Unknown view: {command}", fmt, type_name="DomainError")
        except (ViewError, SLDBError, FileNotFoundError, ValueError) as exc:
            return render_error(str(exc), fmt, type_name=type(exc).__name__, text=f"Error: {exc}")
        return render(payload, fmt, render_text)
