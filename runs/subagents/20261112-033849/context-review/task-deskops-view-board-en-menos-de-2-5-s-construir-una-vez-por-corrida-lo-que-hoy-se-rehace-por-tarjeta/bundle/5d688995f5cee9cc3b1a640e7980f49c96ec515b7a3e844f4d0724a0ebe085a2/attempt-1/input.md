FILE:desk/tasks/task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta.md
---
sldb:
  by: agent
  at: '2026-11-12T03:37:46Z'
  authority: generated
  via: create_document
id: task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/cli/commands/view.py
- deskops/services/tasks.py
- deskops/services/closeout_gates.py
- deskops/lifecycle.py
- deskops/graph/desk_graph.py
- deskops/operations.py
- tests/
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops view board en menos de 2,5 s: construir una vez por corrida lo que hoy se rehace por tarjeta (transiciones, closeout, grafo del desk) y abrir el store menos veces

## Rationale

_Explain why this task exists or the business driver behind it._

Resto de la meta de CC52. Con la tarea H11 de sldb integrada, sldb views run board baja a 1,6 s, pero deskops view board sigue en 4,9 s (mediana de 3, store construido, proceso nuevo): el trabajo propio de deskops es unos 3,3 s. Lo midió el worker de H11: show_task de cada tarjeta (las transiciones con transition_findings, el closeout con build_closeout_graph_context y desk_graph, que arma un ProjectGraph de unos 2 s) se repite por tarjeta, y 31 open_store hacen cada uno migrate_store_layout y _already_canonical (unos 1,3 s bajo perfil, 16 000 Path.resolve).

## Goal

_Describe the concrete result this task must produce._

deskops view board, con el store construido y en un proceso nuevo, tarda 2,5 s o menos (mediana de 3, layout del benchmark de H11) y su salida es idéntica a la de hoy; lo que se construye una vez por corrida se comparte entre las tarjetas.

## Scope

_State what is in scope and what is out of scope._

En alcance: view board de deskops (la construcción de las tarjetas en deskops/cli/commands/view.py y lo que llaman show_task, el closeout de solo lectura y las transiciones), compartir entre tarjetas el grafo del desk, el contexto de closeout y el snapshot de lectura, reducir las llamadas de deskops que abren el store, tests, docs y CHANGELOG. Fuera: sldb (memoizar open_store o migrate_store_layout es una hipótesis para sldb, no se escribe aquí), cambiar lo que muestra el board o el contrato de la vista, y deskops view task salvo que comparta el mismo código.

## Implementation Path

_Outline the expected implementation route or affected surface._

Origen: informe del worker de H11 (hipótesis para deskops) y decisión del coordinador de proyecto. Precondición: la tarea H11 de sldb está integrada en sldb main; esta tarea corre contra ese sldb. Si no lo está, el worker para y avisa.

REPRODUCCIÓN: la del worker de H11 sobre su layout (deskops 4904ddfe, sldb con H11, spec2viz b16c021, scion 4ead6d0bf; runs/subagents/20261112-repro-boardperf/repro.log), con caché frío y caliente: deskops view board caliente 4,94 s, y 1,59 s de sldb views run board en el mismo layout. Primera corrida tras el build, 11,3 s (compone y guarda la caché de composición).

ESTADO ACTUAL (de las lecturas del código; el worker lo confirma con un perfil): la tarjeta de cada tarea llama a show_task, que pasa por _lifecycle_gates y transition_findings, y al closeout de solo lectura; el closeout arma build_closeout_graph_context (que usa desk_graph) y desk_graph construye un ProjectGraph propio. Nada de eso se comparte entre tarjetas más allá del snapshot de lectura que ya existe.

CAMBIO (p1-p5), el worker mide cada paso antes y después:
p1: línea base propia y perfil con cProfile de deskops view board en el layout, commiteados, que cuentan las llamadas a open_store, a desk_graph y a build_closeout_graph_context por corrida.
p2: el grafo del desk y el contexto de closeout se construyen una vez por corrida de view board y se pasan a las tarjetas, por el snapshot de lectura que ya existe o por un parámetro explícito; sin estado global que sobreviva a la corrida.
p3: las llamadas de deskops que abren el store por tarjeta se reducen a las necesarias, con el mismo manejo de errores; el costo propio de open_store en sldb queda como hipótesis para sldb en el informe.
p4: la salida de view board y de view task es byte a byte la de antes sobre el mismo desk (un test la compara contra una corrida con el camino viejo, o con los goldens existentes si cubren el caso). Si un golden cambia, el worker para y muestra el diff antes de actualizarlo.
p5: docs y CHANGELOG. Si la meta de 2,5 s no se alcanza, el informe dice cuánto falta y qué lo explica, con la medición, y qué parte es de sldb.

VALIDACIÓN: el worker corre de a uno los tests que toca; antes de entregar, la suite completa de deskops de a un archivo desde /dev/shm, ci-knowledge-check y graph missing. Los 4 pasos del CI de deskops los corre el coordinador. Las mediciones van con caché frío y caliente.

## Validation

_List the checks required before this task can close._

- Benchmark: deskops view board, store construido, proceso nuevo, mediana de 3, 2,5 s o menos en el layout de H11; medidas antes y después en el informe
- Test: la salida de view board y de view task es idéntica a la de antes sobre el mismo desk
- Perfil antes y después que cuenta las llamadas a open_store, desk_graph y build_closeout_graph_context por corrida
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

## Done When

_Name the observable condition that makes the task complete._

p1-p5 hechos con las mediciones, salida idéntica, tests y suite completa en verde, y la meta de 2,5 s alcanzada o explicada con la medición; docs y CHANGELOG actualizados.

FILE:deskops/cli/commands/view.py
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

FILE:deskops/services/tasks.py
"""Task lifecycle service: create, list, show, advance, next, and the task type registry.

TaskDoc reads go only through sldb's ``extract_model_data``; this service never
overlays a regex parse on top of the model. Document storage (read/write/track,
selector resolution, the task payload with its inherited context) is
``deskops.doc_access``; the lifecycle graph is ``deskops.lifecycle``.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops import lifecycle
from deskops.lifecycle import TransitionResult
from deskops.models import BoardDoc
from deskops.models import PillDoc
from deskops.models import TaskDoc
from deskops.models.validation import validated
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.models.task_types import canonical_task_type_name
from deskops.runtime import Task
from deskops.specs import compile_task_spec
from deskops.workflow.next_actions import match_workflow_state
from deskops.workflow.next_actions import render_workflow_mermaid

if TYPE_CHECKING:
    from deskops.operations import DeskopsOperations


@dataclass(slots=True)
class TaskBundle:
    task_id: str
    task_path: Path


def registered_task_types(root: Path) -> dict[str, type[Any]]:
    """task_type name -> model class: the factory types plus desk-local types in the store.

    A desk adds its own types as ``desk/models/*.py`` subclasses; ``desk update --apply``
    registers them with ``pythonpath`` = the desk root. Factory types are importable directly
    and are merged in first, so local modules never shadow them.
    """
    registry: dict[str, type[Any]] = dict(TASK_TYPE_MODELS)
    store_dir = root / ".sldb"
    if store_dir.exists():
        try:
            from sldb.api.model_registry.model_reference import resolve_model_ref

            from deskops.bootstrap import SLDBBootstrap

            entries = SLDBBootstrap()._registered_model_entries(store_dir)
            pythonpath = str(doc_access.desk_root(root))
            for name, entry in entries.items():
                if name in registry:
                    continue
                model_ref = getattr(entry, "model_ref", "") or ""
                if not model_ref:
                    continue
                try:
                    cls = resolve_model_ref(model_ref, pythonpath=pythonpath)
                except Exception:
                    continue
                if not isinstance(cls, type) or not issubclass(cls, TaskDoc):
                    continue
                field = cls.model_fields.get("task_type")
                default = getattr(field, "default", None)
                if default not in (None, ""):
                    registry[str(default)] = cls
        except Exception:
            pass
    return registry


class TasksService:
    def __init__(self, root: Path, operations: "DeskopsOperations") -> None:
        self._ops = operations
        self.root = operations.root
        self.desk_root = operations.desk_root
        self.logger = operations.logger
        self._task_type_registry: dict[str, type[Any]] | None = None

    def registered_task_types(self) -> dict[str, type[Any]]:
        """The task type registry of this desk, read once per service instance."""
        if self._task_type_registry is None:
            self._task_type_registry = registered_task_types(self.root)
        return self._task_type_registry

    # ---------------------------------------------------------------- create
    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        """Write one task and route it on the Board. Its lifecycle is the desk's graph
        (deskops/lifecycle.py), so nothing else is written per task."""
        doc_access.ensure_workspace(self.root)
        # A task's closeout evidence is declared by its type, not written into the task. The
        # task is stored under its type's model so `model <= TaskCodeDoc` finds it.
        raw_task_type = str(raw_payload.get("task_type") or "").strip()
        registry = self.registered_task_types()
        task_type = raw_task_type if raw_task_type in registry else canonical_task_type_name(raw_task_type)
        type_model = registry.get(task_type) or registry.get("task.code") or TaskDoc
        spec = lifecycle.load_lifecycle_spec()
        compiled = compile_task_spec({**raw_payload, "task_type": task_type}, entry_node=spec.entry_node)
        validated(type_model, compiled.task_payload)
        task_id = compiled.task_payload["id"]
        task_path = self._task_path(task_id)

        with doc_access.desk_transaction(self.root):
            doc_access.create_doc(self.root, task_path, type_model, compiled.task_payload, task_id)
            self._append_task_to_board(task_id)
        return TaskBundle(task_id=task_id, task_path=task_path)

    def _append_task_to_board(self, task_id: str) -> None:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_ref = f"desk/tasks/{task_id}.md"
        tasks = list(board_payload.get("tasks") or [])
        if task_ref not in tasks:
            tasks.append(task_ref)
            board_payload["tasks"] = tasks
            doc_access.write_doc(self.root, board_path, BoardDoc, board_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[doc_access.DocumentRecord, str, bool]:
        doc_access.ensure_workspace(self.root)
        task_path = doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        pill_path = doc_access.resolve_artifact_selector(self.root, "artifact.pill", self.desk_root / "contexts", pill_selector)
        task_payload = doc_access.read_doc(task_path, TaskDoc)
        doc_access.read_doc(pill_path, PillDoc)
        pill_ref = str(pill_path.relative_to(self.root))
        pills = list(task_payload.get("pills") or [])
        record = doc_access.DocumentRecord(kind="task", doc_id=str(task_payload.get("id", task_path.stem)), path=task_path)
        if pill_ref in pills:
            return record, pill_ref, False
        task_payload["pills"] = [*pills, pill_ref]
        doc_access.write_doc(self.root, task_path, TaskDoc, task_payload)
        return record, pill_ref, True

    # ---------------------------------------------------------------- read
    def list_tasks(self) -> list[Task]:
        task_dir = self.desk_root / "tasks"
        if not task_dir.exists():
            if not self.desk_root.exists():
                raise FileNotFoundError(f"Desk root not found at {self.desk_root}. Run 'deskops init' to initialize.")
            return []
        tasks: list[Task] = []
        for path in sorted(task_dir.glob("task-*.md")):
            try:
                tasks.append(doc_access.load_task(self.root, path.stem))
            except Exception as e:
                print(f"Warning: Failed to load task {path}: {e}", file=sys.stderr)
        return tasks

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        """The task and the lifecycle transitions leaving its current node, each with
        whether its condition holds now (empty when the graph is missing or the task is
        complete)."""
        try:
            task = doc_access.load_task(self.root, task_id)
        except FileNotFoundError:
            return None, []
        return task, self._lifecycle_gates(task)

    def _lifecycle_gates(self, task: Task) -> list[dict[str, Any]]:
        if not task.current_node or task.current_node == lifecycle.COMPLETE:
            return []
        try:
            transitions = lifecycle.transitions_from(self.root, task.current_node, snapshot=self._ops.snapshot)
        except Exception:
            return []
        task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task.id)
        payload = doc_access.read_doc(task_path, TaskDoc)
        findings = self._transition_findings(task_path, payload)
        return [
            {
                "relation_type": t.relation_type,
                "target": lifecycle.COMPLETE if t.terminal else t.target,
                "condition": t.condition,
                "holds": lifecycle.condition_holds(t.condition, payload),
                **({"findings": findings} if findings else {}),
            }
            for t in transitions
        ]

    def _transition_findings(self, task_path: Path, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """The findings of the task's ``on_transition`` rules (sldb GO08): what blocks the gate
        leaving its node, as ``show`` and ``next`` print them; empty for an untracked task."""
        document = lifecycle.task_document(self.root, task_path)
        if document is None:
            return []
        try:
            return lifecycle.transition_findings(self.root, document, payload, snapshot=self._ops.snapshot)
        except Exception:
            return []

    def render_next_action_diagram(self) -> str:
        spec = lifecycle.load_lifecycle_spec()
        return render_workflow_mermaid(spec, lifecycle.lifecycle_transitions(self.root, spec))

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        board_path = self.desk_root / "tasks" / "Board.md"
        board_ref = str(board_path.relative_to(self.root))
        if not task_selector:
            task_refs = list(doc_access.read_doc(board_path, BoardDoc).get("tasks") or [])
            if not task_refs:
                return {
                    "kind": "no_board_task",
                    "board": board_ref,
                    "suggested_commands": [
                        "deskops list tasks --root .",
                        "deskops promote inbox-to-drawer-task <selector> --root .",
                        'deskops add task --root . --title "..." ...',
                    ],
                }
            if len(task_refs) > 1:
                tasks = []
                for task_ref in task_refs:
                    path = self.root / str(task_ref)
                    payload = doc_access.read_doc(path, TaskDoc)
                    tasks.append(
                        {
                            "id": str(payload.get("id") or path.stem),
                            "status": str(payload.get("status") or ""),
                            "title": str(payload.get("title") or ""),
                        }
                    )
                return {
                    "kind": "multiple_board_tasks",
                    "board": board_ref,
                    "tasks": tasks,
                    "suggested_commands": [
                        "deskops next <task-id> --root .",
                        "deskops list tasks --root .",
                    ],
                }
        task_path = self._next_task_path(task_selector, board_path)
        payload = doc_access.resolve_task_payload(self.root, task_path.stem)
        spec = lifecycle.load_lifecycle_spec()
        state = match_workflow_state(spec, str(payload.get("current_node") or ""))
        findings = self._transition_findings(task_path, dict(payload)) if payload.get("current_node") else []
        pills = list(dict.fromkeys([*self._board_pills(board_path), *list(payload.get("effective_pills") or payload.get("pills") or [])]))
        sources = {
            "task": str(task_path.relative_to(self.root)),
            "board": str(board_path.relative_to(self.root)),
            "workflow": "deskops/spec/workflows/task_lifecycle.yaml",
        }
        why = [
            "task selected by explicit selector"
            if task_selector
            else "task selected from the single board route",
            f"current_node {payload.get('current_node', '')} matched workflow state {state['id']} in {sources['workflow']}",
            "pills merged from desk/tasks/Board.md and the task",
            f"source task: {sources['task']}",
            f"source board: {sources['board']}",
            f"source workflow: {sources['workflow']}",
        ]
        return {
            "task": {
                "id": payload["id"],
                "title": payload["title"],
                "status": payload["status"],
                "current_node": payload.get("current_node", ""),
                "task_type": payload.get("task_type", ""),
                "inherits_from": list(payload.get("inherits_from") or []),
            },
            "phase": state["phase"],
            "ritual": state.get("ritual", ""),
            "pills": pills,
            "next_actions": list(state.get("next_actions") or []),
            "advance_when": list(state.get("advance_when") or []),
            "findings": findings,
            "why": why,
            "sources": sources,
        }

    # ---------------------------------------------------------------- advance
    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        try:
            task_path = doc_access.resolve_glob(self.root, self.desk_root / "tasks", task_id)
        except FileNotFoundError:
            return None, None
        payload = doc_access.read_doc(task_path, TaskDoc)

        current_node = str(payload.get("current_node") or "")
        current_status = str(payload.get("status") or "")
        # The edge's effects validate against the task type's model. A task whose task_type is
        # not a registered type (empty or legacy, what `desk update --apply` migrates) validates
        # against TaskDoc, the model it was read with: a typed model's `task_type` literal could
        # not accept it (d4, instead of k5's TaskCodeDoc).
        model = self.registered_task_types().get(str(payload.get("task_type") or "")) or TaskDoc
        result = lifecycle.advance(self.root, payload, model, document=lifecycle.task_document(self.root, task_path))
        if result.progressed and payload.get("current_node") == lifecycle.COMPLETE:
            # The lifecycle graph would close the task. Do not persist it; the
            # only closing entry point is `deskops closeout commit`.
            self.logger.info(f"Task {task_id} reached the closure gate; deferring to closeout commit.")
            restored = {**payload, "current_node": current_node, "status": current_status}
            return doc_access.hydrate_task(restored), self._closure_required(task_id, restored)
        advanced_task = doc_access.hydrate_task(payload)
        if result.progressed:
            doc_access.write_doc(self.root, task_path, TaskDoc, payload)
        self.logger.info(f"Advanced task {task_id} to node {payload.get('current_node')}")
        return advanced_task, result

    @staticmethod
    def _closure_required(task_id: str, payload: dict[str, Any]) -> TransitionResult:
        node = str(payload.get("current_node") or "")
        status = str(payload.get("status") or "")
        message = (
            f"Task {task_id} closes with 'deskops closeout commit --task {task_id} "
            f"--run-dir <runs/subagents/dir>' or 'deskops closeout commit --task {task_id} "
            f"--no-run --reason <why>'."
        )
        return TransitionResult(node, status, False, True, message)

    # ---------------------------------------------------------------- paths
    def _task_path(self, task_id: str) -> Path:
        return self.desk_root / "tasks" / f"{task_id}.md"

    def _next_task_path(self, task_selector: str | None, board_path: Path) -> Path:
        if task_selector:
            return doc_access.resolve_artifact_selector(self.root, "artifact.task", self.desk_root / "tasks", task_selector)
        board_payload = doc_access.read_doc(board_path, BoardDoc)
        task_refs = list(board_payload.get("tasks") or [])
        if not task_refs:
            raise FileNotFoundError("No active tasks routed by desk/tasks/Board.md")
        if len(task_refs) > 1:
            raise ValueError("Multiple active tasks are routed; pass a task selector")
        return self.root / str(task_refs[0])

    def _board_pills(self, board_path: Path) -> list[str]:
        try:
            board_payload = doc_access.read_doc(board_path, BoardDoc)
        except Exception:
            return []
        return [str(pill) for pill in board_payload.get("pills") or []]

FILE:deskops/services/closeout_gates.py
"""Closeout evidence gates.

Closeout verification accepts only real evidence: a lowercase commit id naming
a commit in HEAD's history, and a Python test file inside the repository's
``tests/`` directory. A front-matter string that merely looks like evidence is
not evidence.
"""

from __future__ import annotations

from pathlib import Path
import re
import subprocess
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from deskops.identity import RegisteredRepository


COMMIT_ID_PATTERN = re.compile(r"[0-9a-f]{7,40}")
URL_PATTERN = re.compile(r"https?://\S+")

# Closed vocabulary for a task's declared closeout evidence. `atom` and
# `materialization` are alternatives of one gate: either link satisfies it.
CLOSEOUT_EVIDENCE_VOCABULARY = ("tests", "commit", "atom", "materialization", "document", "external")

CODE_EVIDENCE = ("tests", "commit", "atom", "materialization")
DOCUMENT_EVIDENCE = ("commit", "document")
EXTERNAL_EVIDENCE = ("external",)

DOCUMENT_SUFFIXES = frozenset({".md", ".rst", ".txt", ".adoc", ".yaml", ".yml"})


class CloseoutEvidenceError(ValueError):
    """The declared closeout evidence is invalid or missing."""


def normalize_declared_evidence(value: Any) -> list[str]:
    """Validate a declared evidence list against the closed vocabulary, keeping order."""
    if value in (None, ""):
        return []
    items = value if isinstance(value, (list, tuple)) else [value]
    declared: list[str] = []
    for item in items:
        kind = str(item).strip().lower()
        if not kind:
            continue
        if kind not in CLOSEOUT_EVIDENCE_VOCABULARY:
            raise CloseoutEvidenceError(
                f"Unknown closeout evidence '{item}'. Allowed: {', '.join(CLOSEOUT_EVIDENCE_VOCABULARY)}."
            )
        if kind not in declared:
            declared.append(kind)
    return declared


def order_evidence_kinds(kinds: list[str]) -> list[str]:
    """Deduplicate a declared evidence list in the vocabulary order, keeping the kinds that
    are declared on a type but not in the CLI vocabulary (``children``, ``goldens``) last.
    """
    seen: list[str] = []
    for kind in [*CLOSEOUT_EVIDENCE_VOCABULARY, *kinds]:
        if kind in kinds and kind not in seen:
            seen.append(kind)
    return seen


def collapse_link_kinds(kinds: list[str]) -> list[str]:
    """Show atom and materialization as the one alternative gate they are."""
    if "atom" in kinds and "materialization" in kinds:
        out: list[str] = []
        for kind in kinds:
            label = "atom|materialization" if kind in {"atom", "materialization"} else kind
            if label not in out:
                out.append(label)
        return out
    return list(kinds)


def gate_summary(declared: list[str], found: list[str]) -> str:
    declared_text = ", ".join(collapse_link_kinds(declared)) or "nada"
    found_text = ", ".join(found) or "nada"
    return f"esta tarea declaró {declared_text}; encontré {found_text}"


class CloseoutGatesService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()

    def closeout_reference_evidence(
        self,
        payload: dict[str, Any],
        *,
        points_to_atom: Callable[[str], bool],
        points_to_routed_follow_up: Callable[[str], bool],
    ) -> dict[str, list[str]]:
        evidence = {"tests": [], "atom": [], "commit": [], "follow_up": [], "document": [], "external": []}
        references = payload.get("references") or []
        if not isinstance(references, list):
            references = [references]
        files = payload.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for reference in references:
            ref = str(reference).strip()
            if not ref:
                continue
            if self.reference_points_to_test(ref, files=files):
                evidence["tests"].append(ref)
            if points_to_atom(ref):
                evidence["atom"].append(ref)
            if self.reference_points_to_commit(ref):
                evidence["commit"].append(ref)
            if points_to_routed_follow_up(ref):
                evidence["follow_up"].append(ref)
            if self.reference_points_to_url(ref):
                evidence["external"].append(ref)
        for candidate in [*references, *files]:
            ref = str(candidate).strip()
            if ref and self.reference_points_to_document(ref) and ref not in evidence["document"]:
                evidence["document"].append(ref)
        return evidence

    @staticmethod
    def reference_points_to_url(reference: str) -> bool:
        """True for an http(s) URL: the record of work done outside this repository."""
        return bool(URL_PATTERN.fullmatch(reference.strip()))

    def reference_points_to_document(self, reference: str) -> bool:
        """True only for an existing document file inside the repository.

        Documents are prose or spec files (``DOCUMENT_SUFFIXES``). Test sources and
        the task bundle itself, which closure removes, are not documents.
        """
        path = Path(reference.split("::", 1)[0].strip())
        if not str(path) or path.is_absolute():
            return False
        resolved = (self.root / path).resolve()
        if resolved.suffix.lower() not in DOCUMENT_SUFFIXES or not resolved.is_file():
            return False
        if not resolved.is_relative_to(self.root):
            return False
        excluded = ((self.root / "tests").resolve(), (self.root / "desk" / "tasks").resolve())
        return not any(resolved.is_relative_to(parent) for parent in excluded)

    def reference_points_to_test(self, reference: str, files: list[Any] | None = None) -> bool:
        """True only for an existing .py file inside the repository that is a test location.

        After dropping an optional ``::node`` suffix (the node is not validated) and the
        ``pytest <path>`` form, the reference must name an existing file, relative to the
        root, whose suffix is exactly ``.py`` and which resolves inside the root. It counts
        when one of its directories (relative to the root) is named ``tests`` (``tests/``,
        ``runtime/foo/tests/``, ``ops/tests/sub/``) or when its path is declared in
        ``files``, the evaluated TaskDoc's ``files``: they widen where tests may live but
        are not evidence by themselves. Absolute paths, paths that leave the root through
        ``..`` or a symlink, and files under a directory starting with ``.`` or named
        ``site-packages`` or ``node_modules`` (third-party code) are not evidence. Each
        reference is checked on its own; the disk is not walked.
        """
        for candidate in self._test_path_candidates(reference):
            path_text = candidate.split("::", 1)[0]
            path = Path(path_text)
            if not path_text or path.is_absolute():
                continue
            resolved = (self.root / path).resolve()
            if resolved.suffix != ".py" or not resolved.is_file():
                continue
            if not resolved.is_relative_to(self.root):
                continue
            directories = resolved.relative_to(self.root).parts[:-1]
            if any(part.startswith(".") or part in {"site-packages", "node_modules"} for part in directories):
                continue
            if "tests" in directories:
                return True
            for entry in files or []:
                declared = str(entry).strip()
                if declared and not Path(declared).is_absolute() and (self.root / declared).resolve() == resolved:
                    return True
        return False

    def full_commit_sha(self, reference: str) -> str:
        """The full id of a commit reference that passes ``reference_points_to_commit``, else ''."""
        if not self.reference_points_to_commit(reference):
            return ""
        resolved = subprocess.run(
            ["git", "rev-parse", "--verify", f"{reference.strip()}^{{commit}}"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        return resolved.stdout.strip() if resolved.returncode == 0 else ""

    def reference_points_to_commit(self, reference: str) -> bool:
        """True only for a lowercase hex id resolving to HEAD or an ancestor.

        The pattern rejects symbolic names such as ``HEAD`` or ``main``; an
        ambiguous abbreviation fails ``rev-parse --verify``; an unrelated or
        descendant commit fails the ancestor check.
        """
        candidate = reference.strip()
        if not COMMIT_ID_PATTERN.fullmatch(candidate):
            return False
        try:
            resolved = subprocess.run(
                ["git", "rev-parse", "--verify", f"{candidate}^{{commit}}"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
            if resolved.returncode != 0:
                return False
            full_sha = resolved.stdout.strip()
            if not full_sha:
                return False
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", full_sha, "HEAD"],
                cwd=self.root,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            return False
        return ancestor.returncode == 0

    def build_closeout_graph_context(self) -> "CloseoutGraph":
        """The declared-edge graph the closeout link gate reads, built lazily.

        Nodes come from one pass over the repository's document surfaces and file tree,
        tracked documents and schema edges from one read of the sldb index; the declared
        edges of a document are read only when the gate asks about it.
        """
        from deskops.graph.desk_graph import desk_graph

        return CloseoutGraph(desk_graph(self.root))

    def _test_path_candidates(self, reference: str) -> list[str]:
        candidates: list[str] = []
        stripped = reference.strip()
        if stripped.startswith("pytest "):
            for token in stripped.split()[1:]:
                token = token.strip("\"'")
                if token.startswith("-"):
                    continue
                if ".py" in token:
                    candidates.append(token)
        elif ".py" in stripped:
            candidates.append(stripped)
        return candidates


class RepositoryReferences:
    """Split closeout references qualified by a registered repository: ``<repo-id>:<value>``.

    The reference is cut at its first ``:``. When what comes before it is the id of a
    repository in the desk's own registry (``desk/registry/repo-*.md``), the rest is the
    value (a commit id or a test path, which may carry a pytest ``::node``) and it is
    checked in that repository's root. Otherwise the whole reference is what it was
    before: a local commit, a local test path or an http(s) URL. A prefix naming the desk
    itself (its ``project_identity`` or a registered repository whose root is the desk's
    root) is local: the value is checked as an unqualified reference.
    """

    def __init__(
        self,
        root: Path,
        entries: "list[RegisteredRepository]",
        *,
        own_identity: str | None = None,
    ) -> None:
        self.root = root.resolve()
        self.entries = {entry.id: entry for entry in entries}
        self.own_identity = (own_identity or "").strip() or None
        self._gates: dict[Path, CloseoutGatesService] = {}

    def split(self, reference: str) -> "tuple[RegisteredRepository | None, str]":
        """(the other repository, the value) for a qualified reference, else (None, the local reference)."""
        text = reference.strip()
        if CloseoutGatesService.reference_points_to_url(text) or ":" not in text:
            return None, text
        prefix, value = text.split(":", 1)
        if self.own_identity is not None and prefix == self.own_identity:
            return None, value.strip()
        entry = self.entries.get(prefix)
        if entry is None:
            return None, text
        if entry.repo_root is not None and entry.repo_root.resolve() == self.root:
            return None, value.strip()
        return entry, value.strip()

    @staticmethod
    def missing_root_message(entry: "RegisteredRepository") -> str | None:
        """The refusal for a registered repository whose root is not on this machine, else None."""
        if entry.repo_root is not None and entry.repo_root.is_dir():
            return None
        location = entry.repo_root if entry.repo_root is not None else entry.relative_path or "(no path)"
        return f"Registered repository {entry.id} is not at {location} on this machine."

    def gates(self, entry: "RegisteredRepository") -> CloseoutGatesService:
        """The evidence gates of a registered repository, rooted at its registered root."""
        assert entry.repo_root is not None
        root = entry.repo_root.resolve()
        if root not in self._gates:
            self._gates[root] = CloseoutGatesService(root)
        return self._gates[root]


class CloseoutGraph:
    """What the closeout link gate asks of the declared-edge graph.

    The gate needs, for a changed file, the edges leaving its node and the edges a
    materialization points at it, plus the edges that link test files to atoms or
    materializations. Only the materialization documents and the documents the gate asks
    about are read; ``edges_around`` and ``test_link_edges`` return supersets of what the
    gate keeps, in the order a full scan of the sorted edge list would visit them, so the
    gate's own conditions produce the same evidence in the same order.
    """

    def __init__(self, graph: Any) -> None:
        self.graph = graph
        lookup = graph.nodes.lookup
        self.node_ids_by_path = {path: node.id for path, node in lookup.by_path.items()}
        materializations = sorted(
            node_id for node_id in lookup.existing_ids | graph.node_ids() if node_id.startswith("materialization:")
        )
        self.invalid_materializations = {node_id for node_id in materializations if graph.missing_from(node_id)}
        self._materialization_edges_to: dict[str, list[Any]] = {}
        for node_id in materializations:
            for edge in graph.edges_from(node_id):
                self._materialization_edges_to.setdefault(edge.target_id, []).append(edge)

    def node_id(self, relative_path: str) -> str | None:
        return self.node_ids_by_path.get(relative_path)

    def edges_around(self, node_id: str) -> list[Any]:
        """Edges leaving ``node_id`` and materialization edges into it, sorted and unique."""
        return _sorted_unique([*self.graph.edges_from(node_id), *self._materialization_edges_to.get(node_id, [])])

    def test_link_edges(self) -> list[Any]:
        """Edges leaving a test file, and materialization edges into a test file."""
        edges = [
            edge
            for node_id in sorted(self.graph.node_ids())
            if node_id.startswith("test_file:")
            for edge in self.graph.edges_from(node_id)
        ]
        edges += [
            edge
            for target_id, into in self._materialization_edges_to.items()
            if target_id.startswith("test_file:")
            for edge in into
        ]
        return _sorted_unique(edges)


def _sorted_unique(edges: list[Any]) -> list[Any]:
    unique = {(edge.source_id, edge.target_id, edge.role, edge.provenance_locator): edge for edge in edges}
    return [unique[key] for key in sorted(unique)]

FILE:deskops/lifecycle.py
"""The task lifecycle as a graph in the desk's sldb store.

States are the desk's tracked rituals (``RitualDoc:ritual-execution`` and its siblings).
Transitions are sldb ``RelationDoc`` edges between those rituals, typed by a
``RelationTypeDoc`` whose name is the verb (``task_activates``), with a ``condition``
written as an sldb ``--where`` predicate over the task and the transition's effects in
``attributes``: ``sets`` (the task fields the transition writes, ``status`` today) and
``terminal`` (the task closes), the convention sldb reads (GO09). The six documents are
managed seeds of the package (``deskops/data/desk_declaration.yaml``, templates in
``deskops/data/lifecycle/``): ``deskops init`` and ``deskops desk update --apply`` write
them under ``desk/lifecycle/`` and rewrite a desk's copy that differs.

The activation gate of each factory task type is a ``RuleDoc`` (sldb GO06/GO08), also a
managed seed (``deskops/data/rules/``, written to ``desk/lifecycle/rule-activation-<type>.md``):
``on_transition`` over ``ritual-execution``, with subject ``model <= <TypeDoc>`` so a desk's
subtype inherits it without code, requiring the review receipts the type asks for
(``any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")``) and
the task's dependencies closed (``all(depends_on: status = "closed")``). sldb evaluates those
rules when ``edges_holding`` receives the task as ``document``; an ``error`` finding blocks
every edge and ``edges_blocked`` returns them with the findings ``deskops advance``, ``next``
and ``show`` print.

deskops keeps three things: the states ``deskops next`` describes
(``deskops/spec/workflows/task_lifecycle.yaml``), the call to sldb for the edges whose
condition holds (``sldb.api.edges_holding``) and their effects (``sldb.api.apply_effects``),
and the task's ``history``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from deskops.paths import data_path
from deskops.paths import package_pythonpath

SPEC_PATH = data_path("spec", "workflows", "task_lifecycle.yaml")
LIFECYCLE_DIR = Path("desk") / "lifecycle"
COMPLETE = "complete"
RELATION_TYPE_MODEL = "RelationTypeDoc"
RELATION_MODEL = "RelationDoc"
RITUAL_MODEL = "RitualDoc"
RULE_MODEL = "RuleDoc"
RULE_MODEL_REF = "sldb.models.rule_doc:RuleDoc"


class LifecycleGraphMissing(RuntimeError):
    """The desk's store has no lifecycle graph, or it does not cover a task's state."""


class LifecycleSeedOutOfDate(LifecycleGraphMissing):
    """The edge ``deskops advance`` would take does not carry the package's effect (a desk's
    lifecycle seed older than CC31, ``attributes: {}``): applying it would write a state the
    ``TaskDoc`` validator rejects. Raised before any effect is applied; the fix is
    ``deskops desk update --apply``, which restores the managed seed."""


@dataclass(frozen=True, slots=True)
class Transition:
    """One edge of the lifecycle graph leaving ``source``, with its effects as the edge declares them."""

    relation_type: str
    source: str
    target: str
    condition: str
    sets: dict[str, Any] = field(default_factory=dict)
    terminal: bool = False
    #: The name of the ``RelationDoc`` that authors the edge (its file is ``desk/lifecycle/<name>.md``).
    relation_doc: str = ""
    #: The findings of the task's ``on_transition`` rules (sldb GO08), as ``finding_dict`` gives
    #: them: every finding on a blocked edge, only alerts on a holding one, none without a document.
    findings: tuple[dict[str, Any], ...] = ()

    @property
    def effects(self) -> dict[str, Any]:
        return {"sets": dict(self.sets), "terminal": self.terminal}


@dataclass(frozen=True, slots=True)
class LifecycleSpec:
    """The states of ``task_lifecycle.yaml``: what ``deskops next`` says at each node."""

    entry_node: str
    states: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def rituals(self) -> list[str]:
        return [node for node in (str(state.get("current_node") or "") for state in self.states) if node and node != COMPLETE]


@dataclass(slots=True)
class ReadSnapshot:
    """Task-independent graph reads shared by every task read of one read-only pass.

    ``DeskopsOperations.read_snapshot`` opens one; ``transitions_from`` keeps the transitions
    leaving each node in it, ``transition_findings`` the store's rule graph (sldb loads the
    whole index for it, ~3 s on a small desk) and the closure service the closeout graph context.
    """

    transitions: dict[str, list["Transition"]] = field(default_factory=dict)
    graph_context: Any = None
    rule_graph: Any = None
    has_rules: bool | None = None


@dataclass(slots=True)
class TransitionResult:
    current_node: str
    status: str
    progressed: bool
    blocked: bool
    message: str


def load_lifecycle_spec(path: Path = SPEC_PATH) -> LifecycleSpec:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    states = tuple(state for state in payload.get("states") or [] if isinstance(state, dict))
    if not states:
        raise ValueError(f"Lifecycle spec declares no states: {path}")
    return LifecycleSpec(entry_node=str(payload.get("entry_node") or states[0].get("current_node") or ""), states=states)


# ---------------------------------------------------------------- conditions
def condition_holds(condition: str, payload: dict[str, Any]) -> bool:
    """Whether an sldb ``--where`` condition (predicates joined by `` and ``) holds on a task payload."""
    from sldb.api import where_matches

    return where_matches(condition, payload)


# ---------------------------------------------------------------- the graph
def _store(root: Path) -> Path:
    return root / ".sldb"


def ritual_export_id(ritual_id: str) -> str:
    return f"{RITUAL_MODEL}:{ritual_id}"


def finding_dict(finding: Any) -> dict[str, Any]:
    """An sldb ``Finding`` as the plain mapping ``show --format json`` prints."""
    return {"level": finding.level, "code": finding.code, "subject": finding.subject, "what": finding.what}


def finding_line(finding: dict[str, Any]) -> str:
    """One finding as sldb prints it: ``<level>: [<code>] <node>: <message> | <clause> (seen: ...)``."""
    return f"{finding['level']}: [{finding['code']}] {finding['subject']}: {finding['what']}"


def _transition(node: str, edge: Any) -> Transition:
    """The edge as a transition; ``effects`` (filled by ``edges_holding``) else the declared attributes."""
    attributes = edge.metadata.get("attributes") or {}
    effects = edge.effects or {"sets": attributes.get("sets") or {}, "terminal": attributes.get("terminal")}
    return Transition(
        relation_type=edge.relation,
        source=node,
        target=edge.target.rsplit(":", 1)[-1],
        condition=str(edge.metadata.get("condition") or ""),
        sets=dict(effects.get("sets") or {}),
        terminal=bool(effects.get("terminal")),
        relation_doc=str(edge.metadata.get("relation_doc") or ""),
        findings=tuple(finding_dict(f) for f in (getattr(edge, "findings", None) or ())),
    )


def _is_lifecycle_edge(edge: Any) -> bool:
    """An authored edge (a RelationDoc) whose target is a ritual (`sldb://document/RitualDoc:<id>`)."""
    return edge.metadata.get("origin") == "relation_doc" and edge.target.rsplit("/", 1)[-1].startswith(f"{RITUAL_MODEL}:")


def _lifecycle_edges(node: str, edges: list[Any]) -> list[Transition]:
    """The authored edges between rituals, in the order sldb returns them."""
    return [_transition(node, e) for e in edges if _is_lifecycle_edge(e)]


def transitions_from(root: Path, node: str, *, snapshot: ReadSnapshot | None = None) -> list[Transition]:
    """The lifecycle transitions leaving ``node``, as the desk's graph declares them.

    Topology, conditions and effects all come from the graph. The lifecycle graph lives in the
    desk's own store, so only that store's edge index is read (sldb keeps it composed while
    its shards do not move), not the index composed with every linked store.

    With a ``snapshot``, the transitions leaving a node are read once and reused.
    """
    if snapshot is not None:
        if node not in snapshot.transitions:
            snapshot.transitions[node] = transitions_from(root, node)
        return snapshot.transitions[node]
    from sldb.api import edges_from

    return _lifecycle_edges(node, edges_from(_store(root), ritual_export_id(node), include_linked=False))


def transitions_holding(root: Path, node: str, payload: dict[str, Any], document: str | None = None) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` (``sldb.api.edges_holding``),
    each with its effects resolved for that payload. With ``document`` (the task's ``Model:name``
    in the store) the task's ``on_transition`` rules run too: an error finding holds every edge back."""
    from sldb.api import edges_holding

    return _lifecycle_edges(node, edges_holding(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transitions_blocked(root: Path, node: str, payload: dict[str, Any], document: str) -> list[Transition]:
    """The transitions leaving ``node`` whose condition holds on ``payload`` but that an error
    finding of the task's ``on_transition`` rules blocks (``sldb.api.edges_blocked``), each
    carrying every finding."""
    from sldb.api import edges_blocked

    return _lifecycle_edges(node, edges_blocked(_store(root), ritual_export_id(node), payload, include_linked=False, document=document))


def transition_findings(root: Path, document: str, payload: dict[str, Any], *, snapshot: ReadSnapshot | None = None) -> list[dict[str, Any]]:
    """The findings of the task's ``on_transition`` rules read as ``payload`` (``sldb.api.transition_findings``).

    With a ``snapshot``, the store's rule graph is loaded once and shared by every task read of
    the pass (what ``sldb.api.transition_findings`` does on each call); a store without
    ``RuleDoc`` has no findings and loads nothing."""
    if snapshot is None:
        from sldb.api import transition_findings as sldb_transition_findings

        return [finding_dict(f) for f in sldb_transition_findings(_store(root), document, payload)]
    from sldb.api.rules.rule_graph import rule_graph
    from sldb.api.rules.rule_subjects import resolve_subject
    from sldb.api.rules.rules_on_transition import has_rules
    from sldb.api.rules.rules_on_transition import payload_findings

    if snapshot.has_rules is None:
        snapshot.has_rules = has_rules(_store(root))
    if not snapshot.has_rules:
        return []
    if snapshot.rule_graph is None:
        snapshot.rule_graph = rule_graph(_store(root))
    graph = snapshot.rule_graph
    return [finding_dict(f) for f in payload_findings(graph, "on_transition", resolve_subject(graph, document), payload)]


def task_document(root: Path, task_path: Path) -> str | None:
    """The ``Model:name`` the desk's store tracks ``task_path`` under (the subject of its rules);
    None for an untracked task or a desk without a store, where no rule runs."""
    from sldb.api.stores.doc_status import doc_status

    if not (_store(root) / "core").exists():
        return None
    try:
        status = doc_status(_store(root), task_path.resolve().relative_to(root.resolve()).as_posix())
    except Exception:
        return None
    if not status.model or not status.name:
        return None
    return f"{status.model}:{status.name}"


def lifecycle_transitions(root: Path, spec: LifecycleSpec | None = None) -> list[Transition]:
    """Every transition of the desk's lifecycle graph, ritual by ritual; empty without a store."""
    if not (_store(root) / "core").exists():
        return []
    spec = spec or load_lifecycle_spec()
    return [t for node in spec.rituals for t in transitions_from(root, node)]


def advance(root: Path, payload: dict[str, Any], model: type[Any], spec: LifecycleSpec | None = None, document: str | None = None) -> TransitionResult:
    """Take the first transition out of the task's current node whose condition holds.

    The edge's effects are applied with ``sldb.api.apply_effects`` (``sets`` replaces the
    payload's top-level keys; the result validates against ``model``, the task type's model)
    and, when the edge is ``terminal``, ``current_node`` becomes ``complete``; the relation type
    is appended to ``history``. Mutates ``payload`` and reports what happened; one call takes
    at most one transition. The graph has one edge leaving each ritual, so the order sldb
    returns the holding edges in decides nothing (k4).

    With ``document`` (``task_document``) the task's ``on_transition`` rules run: when an error
    finding holds the edges back, the message lists each finding (rule, clause, node and value
    seen) instead of the edges' conditions.
    """
    from sldb.api import apply_effects

    spec = spec or load_lifecycle_spec()
    node = str(payload.get("current_node") or spec.entry_node)
    status = str(payload.get("status") or "")
    if node == COMPLETE:
        return TransitionResult(COMPLETE, status, False, False, "Task already complete.")
    if not (_store(root) / "core").exists():
        raise LifecycleGraphMissing(
            f"No sldb store at {_store(root)}: run 'deskops init' (or 'deskops desk update --apply' on an "
            "existing store) to create the lifecycle graph that 'deskops advance' reads."
        )
    transitions = transitions_from(root, node)
    if not transitions:
        raise LifecycleGraphMissing(
            f"No lifecycle transition leaves '{node}' in the graph of {_store(root)}. "
            "Run 'deskops desk update --apply' to write the lifecycle graph."
        )
    holding = transitions_holding(root, node, payload, document)
    if not holding:
        payload["current_node"] = node
        blocked = transitions_blocked(root, node, payload, document) if document else []
        findings = [f for t in blocked for f in t.findings if f["level"] == "error"]
        if findings:
            lines = "; ".join(finding_line(f) for f in findings)
            return TransitionResult(node, status, False, True, f"Gate {node} is blocked by its rules: {lines}")
        gates = "; ".join(f"{t.relation_type}: {t.condition}" for t in transitions)
        return TransitionResult(node, status, False, True, f"Gate {node} is not complete ({gates}).")
    transition = holding[0]
    target = COMPLETE if transition.terminal else transition.target
    _check_against_package(payload, transition, target)
    # The model validates the whole new state (TaskDoc's lifecycle coherence): the edge's
    # ``sets``, the history it appends to and the node it leads to are applied together.
    history = [str(item) for item in payload.get("history") or []]
    sets = {**transition.sets, "history": [*history, transition.relation_type], "current_node": target}
    payload.update(apply_effects(payload, {**transition.effects, "sets": sets}, model))
    verb = "Completed" if transition.terminal else "Advanced to"
    return TransitionResult(target, str(payload.get("status") or ""), True, False, f"{verb} {target} via {transition.relation_type}.")


UPDATE_SEEDS = "deskops desk update --apply"


def _check_against_package(payload: dict[str, Any], transition: Transition, target: str) -> None:
    """Refuse an edge whose effect differs from the package's lifecycle table (b6).

    The ``TaskDoc`` validator checks the new state against ``lifecycle_table()``, the package's
    edges; the desk's edge is what ``advance`` applies. When the two differ (a desk seed older
    than CC31 has no ``attributes.sets``), the write would fail inside pydantic without naming
    the edge, so the edge is compared first: same ``relation_type``, same target, same
    ``sets.status``. The table is cached; no file is read here.
    """
    from deskops.models.task_lifecycle import lifecycle_table

    task_id = str(payload.get("id") or "")
    edge_file = f"{LIFECYCLE_DIR.as_posix()}/{transition.relation_doc or transition.relation_type}.md"
    head = f"Cannot advance {task_id} via {transition.relation_type}: the edge {edge_file}"
    tail = f" The desk's lifecycle seeds are out of date: run '{UPDATE_SEEDS}'."
    expected = lifecycle_table().edges.get(transition.relation_type)
    if expected is None:
        raise LifecycleSeedOutOfDate(f"{head} is not a transition of the deskops package lifecycle.{tail}")
    seen = transition.sets.get("status")
    if str(seen or "") != expected.status:
        shown = "missing" if seen in (None, "") else str(seen)
        raise LifecycleSeedOutOfDate(
            f"{head} does not set status {expected.status} (attributes.sets.status is {shown}).{tail}"
        )
    if target != expected.target:
        raise LifecycleSeedOutOfDate(f"{head} does not lead to {expected.target} (it leads to {target}).{tail}")


# ---------------------------------------------------------------- writing the graph
def seed_changes(root: Path, result: Any) -> list[str]:
    """What a desk scaffold did to the lifecycle graph: ``wrote <path>`` and ``rewrote <path>`` lines."""
    root = root.resolve()
    prefix = LIFECYCLE_DIR.as_posix() + "/"
    created = [path.resolve().relative_to(root).as_posix() for path in result.created_paths]
    rewritten = [path.resolve().relative_to(root).as_posix() for path in result.rewritten_paths]
    return [f"wrote {rel}" for rel in created if rel.startswith(prefix)] + [f"rewrote {rel}" for rel in rewritten]


def _ritual_paths(spec: LifecycleSpec) -> dict[str, str]:
    return {f"desk/rituals/{node.removeprefix('ritual-')}.md": node for node in spec.rituals}


def tracked_line(model: str, path: str, spec: LifecycleSpec | None = None) -> str | None:
    """The change line for a lifecycle document the declared includes tracked; None for any other."""
    if path.startswith(LIFECYCLE_DIR.as_posix() + "/"):
        return f"tracked {path}"
    ritual = _ritual_paths(spec or load_lifecycle_spec()).get(path)
    if model == RITUAL_MODEL and ritual:
        return f"tracked {path} as {ritual_export_id(ritual)}"
    return None


def ensure_rule_model(root: Path) -> bool:
    """Register sldb's ``RuleDoc`` in the desk's store when it lacks it (``sldb.api.add_model``);
    True when it was registered now. Tracking an activation rule needs the model, and each
    ``model <= <TypeDoc>`` of a rule's subject needs the type registered, which the deskops
    models always are."""
    from sldb.api import add_model
    from sldb.api import is_model_registered

    if is_model_registered(_store(root), RULE_MODEL):
        return False
    add_model(_store(root), RULE_MODEL_REF, pythonpath=package_pythonpath())
    return True


def write_lifecycle_graph(root: Path) -> list[str]:
    """Make the desk's store carry the lifecycle graph; return what was written or tracked.

    Idempotent: writes the managed lifecycle seeds (the graph and the activation rules) and
    restores one the desk changed (``workspace.seed_desk``), registers sldb's relation models
    and ``RuleDoc`` when the store lacks them and tracks the declared desk documents
    (``workspace.apply_desk_includes``): the lifecycle documents and the lifecycle rituals by
    their ids. Any other declared document pending is tracked too and reported in the same way.
    """
    from sldb.api import init_relations
    from sldb.api import is_model_registered

    from deskops.workspace import apply_desk_includes
    from deskops.workspace import pending_desk_includes
    from deskops.workspace import seed_desk

    root = root.resolve()
    changes = seed_changes(root, seed_desk(root, restore_managed=True))
    if not all(is_model_registered(_store(root), name) for name in (RELATION_MODEL, RELATION_TYPE_MODEL)):
        init_relations(_store(root), pythonpath=package_pythonpath())
    ensure_rule_model(root)
    spec = load_lifecycle_spec()
    pending = {path: model for model, path in pending_desk_includes(root)}
    for path in apply_desk_includes(root):
        model = pending.get(path, "")
        changes.append(tracked_line(model, path, spec) or f"tracked {path} as {model}")
    return changes


# Alias de compatibilidad hacia atrás
ensure_lifecycle_graph = write_lifecycle_graph

FILE:deskops/graph/desk_graph.py
"""The desk's graph as configuration over sldb's project graph.

sldb (``sldb.api.edges.project_graph``) reads the nodes, the store's edge index and the
declarations; this module only says what a desk is made of: where its documents live, which
files are nodes, which fields and sections declare references, and which documents are history.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from sldb.api.edges.project_graph import DeclaredFileTargets
from sldb.api.edges.project_graph import DocumentNode
from sldb.api.edges.project_graph import DocumentSurface
from sldb.api.edges.project_graph import FileExclusions
from sldb.api.edges.project_graph import FileNode
from sldb.api.edges.project_graph import FileRule
from sldb.api.edges.project_graph import LineMentions
from sldb.api.edges.project_graph import MentionPattern
from sldb.api.edges.project_graph import MissingTargetKind
from sldb.api.edges.project_graph import ProjectGraph
from sldb.api.edges.project_graph import ProjectGraphConfig
from sldb.api.edges.project_graph import ProjectGraphExtraction
from sldb.api.edges.project_graph import ReferenceField
from sldb.api.edges.project_graph import SectionMentions
from sldb.api.edges.project_graph import extract_document_nodes
from sldb.api.edges.project_graph import extract_file_nodes

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD


DOC_NODE_EXTRACTOR = "desk_doc_nodes_v1"
SOURCE_FILE_NODE_EXTRACTOR = "desk_source_file_nodes_v1"
DECLARED_EDGE_EXTRACTOR = "desk_declared_edges_v1"

# Declared fields that record where a document came from. They link to the source while it
# exists; once it is deleted the provenance stays recorded as text and is not a reference.
PROVENANCE_FIELDS = ("from_drawer",)

_MD = (".md",)
SURFACES = (
    DocumentSurface(kind="atom", directory="desk/atoms", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="materialization", directory="desk/materializations", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="role", directory="desk/roles", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="runtime_profile", directory="desk/runtimes", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="run", directory="desk/runs", pattern="**/*.md", identity="document_id"),
    DocumentSurface(kind="pill", directory="desk/contexts", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="task", directory="desk/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="issue", directory="desk/drawer/issues", pattern="*.md", identity="document_id_or_slug"),
    DocumentSurface(kind="question", directory="desk/drawer/questions", pattern="*.md"),
    DocumentSurface(kind="task", directory="desk/drawer/tasks", pattern="*.md", excluded_names=("Board.md",), identity="document_id"),
    DocumentSurface(kind="feature", directory="desk/drawer/features", pattern="*.md"),
    DocumentSurface(kind="use_case", directory="desk/drawer/use-cases", pattern="*.md"),
    DocumentSurface(kind="stress_test", directory="desk/drawer/stress-tests", pattern="**/*.md"),
    DocumentSurface(kind="diagram", directory="docs/diagrams", pattern="**/*", suffixes=(".md", ".mmd")),
    DocumentSurface(kind="doc", directory="docs", pattern="**/*.md", excluded_parts=("diagrams",)),
    DocumentSurface(kind="doc", directory="", pattern="README.md"),
    DocumentSurface(kind="doc", directory="deskops/data", pattern="**/*.md"),
    DocumentSurface(kind="spec", directory="spec", pattern="**/*", suffixes=(".md", ".yaml", ".yml")),
    DocumentSurface(kind="board", directory="desk/tasks", pattern="Board.md", identity="document_id"),
    DocumentSurface(kind="drawer_board", directory="desk/drawer/tasks", pattern="Board.md"),
    DocumentSurface(kind="ritual", directory="desk/rituals", pattern="*.md", identity="document_id"),
    DocumentSurface(kind="step", directory="desk/steps", pattern="*.md", identity="document_id"),
)

_SPEC = (".md", ".yaml", ".yml")
_DATA = (".json", ".yaml", ".yml")
FILE_RULES = (
    FileRule(kind="spec", file_kind="spec", path_prefixes=("spec", "docs/architecture/spec2viz"), suffixes=_SPEC),
    FileRule(kind="test_file", file_kind="test", path_prefixes=("tests",), suffixes=(".py",)),
    FileRule(kind="config_file", file_kind="config", suffixes=(".cfg", ".ini", ".toml")),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, hidden_name=True),
    FileRule(kind="config_file", file_kind="config", suffixes=_DATA, stem_keywords=("config", "namespace", "registry")),
    FileRule(kind="source_file", file_kind="source", path_prefixes=("desk", "deskops"), suffixes=(".py",)),
)

EXCLUSIONS = FileExclusions(
    directories=(".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", ".tmp", ".venv", "__pycache__", "build", "dist", "node_modules", "tools", "venv"),
    path_prefixes=(".sldb/runtime", ".sldb/core/documents", ".sldb_cache", "tests/fixtures"),
    suffixes=(".pyc", ".pyo"),
    path_endings=(".graph.json", ".kgdb.json", ".snapshot.json"),
)

MATERIALIZATION_TARGETS = DeclaredFileTargets(
    directory="desk/materializations", field="target_identity", kind="source_file", file_kind="source",
    source_kind="declared_materialization_target",
)


def _atom_field(*path: str, index_owned: bool = False) -> ReferenceField:
    return ReferenceField(path=path, target_prefix="atom:", default_role=DEFAULT_ROLE, allowed_roles=ALLOWED_ROLES, index_owned=index_owned)


def _target_field(*path: str) -> ReferenceField:
    return ReferenceField(path=path, default_role=DEFAULT_ROLE, scalar_only=True)


REFERENCE_FIELDS = (
    *(_atom_field(field, index_owned=True) for field in (CANONICAL_FIELD, MATERIALIZATION_FIELD, *LEGACY_FIELDS)),
    _atom_field("materialization", "source_atoms"),
    _target_field("materialization", "target_identity"),
    _target_field("target_identity"),
)

# A slug like `atom-pills-carry-transitional-task-knowledge` contains `task-knowledge`, which is
# part of an atom name, not a task reference; a real reference starts at a non-word, non-hyphen.
TASK_OR_ISSUE = MentionPattern(regex=r"(?<![\w-])(?P<kind>task|issue)-[a-z0-9][a-z0-9-]*\b", target="{kind}:{0}")
ATOM = MentionPattern(regex=r"\batom-[a-z0-9][a-z0-9-]*\b", target="atom:{0}")
# The same atom named with its kind, `atom:atom-<slug>`, as a whole token: `xatom:atom-a`,
# `atom:atom-a.b` and `atom:atom-a/b` name nothing (the token is longer than the atom id).
ATOM_ID = MentionPattern(regex=r"(?<![\w:./-])atom:atom-[a-z0-9][a-z0-9-]*(?![\w:/-]|\.\w)", target="{0}")
# A bullet of the drawer Board names one drawer entry: `- `tasks/<id>.md``, `- `<id>``.
DRAWER_BULLET = MentionPattern(
    regex=r"(?<=^- `)(?:tasks/|issues/)?(?P<id>(?P<kind>task|issue)-[^`\s/]+?)(?:\.md)?(?=`)", target="{kind}:{id}",
)
SOURCE_PATH = MentionPattern(
    regex=r"(?<![\w/.-])(?P<path>(?:deskops|desk|tests|spec|docs)/[A-Za-z0-9_./-]+\.(?:py|yaml|yml|md|toml|json|mmd))(?![\w/.-])",
    target="{path}",
)
SECTION_MENTIONS = (
    SectionMentions(
        headings=("related atoms", "source atoms", "related tasks", "related issues", "related task", "related issue"),
        patterns=(ATOM_ID, ATOM, TASK_OR_ISSUE), role=DEFAULT_ROLE,
    ),
    SectionMentions(headings=("source", "sources", "diagram source", "diagram sources"), patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, kinds=("diagram",)),
)
# Drawer tasks keep the extraction they had as `drawer_task` nodes: their lines are not scanned.
LINE_MENTIONS = (
    LineMentions(
        kinds=("task", "issue"), excluded_path_prefixes=("desk/drawer/tasks",), skipped_frontmatter_fields=PROVENANCE_FIELDS,
        patterns=(SOURCE_PATH,), role=DEFAULT_ROLE, locator="source-file-reference",
    ),
    # `atom:atom-<slug>` anywhere in a task or issue: what `atoms merge` rewrites in prose.
    LineMentions(
        kinds=("task", "issue"), excluded_path_prefixes=("desk/drawer/tasks",), skipped_frontmatter_fields=PROVENANCE_FIELDS,
        patterns=(ATOM_ID,), role=DEFAULT_ROLE, locator="atom-mention",
    ),
    LineMentions(kinds=("drawer_board",), patterns=(DRAWER_BULLET,), role=DEFAULT_ROLE, locator="drawer-bullet"),
)
MISSING_TARGET_KINDS = (
    MissingTargetKind(parts=("docs", "diagrams"), kind="diagram"),
    MissingTargetKind(parts=("docs",), kind="doc"),
    MissingTargetKind(parts=("tests",), kind="test_file"),
    MissingTargetKind(parts=("spec",), kind="spec"),
    MissingTargetKind(parts=(), one_of_first=("desk", "deskops"), ending=".py", kind="source_file"),
)


def _closed_issue(kind: str, text: str) -> bool:
    """A closed issue is history, like a ``record: true`` document."""
    if kind != "issue":
        return False
    from deskops.services.issues import issue_status

    return issue_status(text) == "closed"


def _model_classes() -> dict[str, Any]:
    from deskops import models

    return {name: value for name, value in vars(models).items() if isinstance(value, type)}


def _declared_fields(model: Any) -> tuple[str, ...]:
    return (*getattr(model, "__containment__", {}).keys(), *getattr(model, "__references__", []))


def _model_kind(model: Any) -> str | None:
    types = (getattr(model, "__semantics__", None) or {}).get("type") or []
    return types[-1] if types else None


def _fields_by_kind() -> dict[str, tuple[str, ...]]:
    """Model-declared reference fields per surface kind: the first model (in ``models.__all__``) of that type."""
    from deskops import models

    fields: dict[str, tuple[str, ...]] = {}
    for kind in {surface.kind for surface in SURFACES}:
        normalized = kind.removeprefix("drawer_")
        model = next((getattr(models, name) for name in models.__all__ if _model_kind(getattr(models, name)) == normalized), None)
        if model is not None:
            fields[kind] = _declared_fields(model)
    return fields


@lru_cache(maxsize=1)
def desk_graph_config() -> ProjectGraphConfig:
    """What a desk's graph is made of."""
    classes = _model_classes()
    kinds = {name: _model_kind(model) for name, model in classes.items()}
    return ProjectGraphConfig(
        document_extractor=DOC_NODE_EXTRACTOR, file_extractor=SOURCE_FILE_NODE_EXTRACTOR, edge_extractor=DECLARED_EDGE_EXTRACTOR,
        surfaces=SURFACES, file_rules=FILE_RULES, exclusions=EXCLUSIONS, declared_file_targets=(MATERIALIZATION_TARGETS,),
        reference_fields=REFERENCE_FIELDS, fields_by_kind=_fields_by_kind(),
        fields_by_model={name: _declared_fields(model) for name, model in classes.items()},
        kind_by_model={name: "materialization" if kind == "materialization_contract" else kind for name, kind in kinds.items() if kind},
        provenance_fields=PROVENANCE_FIELDS, section_mentions=SECTION_MENTIONS, line_mentions=LINE_MENTIONS,
        missing_target_kinds=MISSING_TARGET_KINDS, closed_document=_closed_issue,
    )


def desk_graph(root: Path) -> ProjectGraph:
    """The desk's declared-edge graph, read source by source."""
    return ProjectGraph(root, desk_graph_config())


def extract_doc_nodes(root: Path) -> list[DocumentNode]:
    """Every desk document as a node."""
    return extract_document_nodes(root, desk_graph_config())


def extract_source_file_nodes(root: Path) -> list[FileNode]:
    """Every source, test, config and spec file (and declared materialization target) as a node."""
    return extract_file_nodes(root, desk_graph_config())


def extract_declared_edges(root: Path) -> ProjectGraphExtraction:
    """Every declared edge of the desk and every declared target that does not resolve."""
    return desk_graph(root).extraction()

FILE:deskops/operations.py
"""The facade of one desk: every operation the CLI and the UIs call, as one call each.

``DeskopsOperations`` builds the arguments and delegates to the service that owns the
operation (tasks, atoms, closure, drawer, closeout gates), to ``deskops.doc_access`` for
plain document reads and writes, or to ``deskops.lifecycle``. No logic lives here.
"""

from __future__ import annotations

from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Any
from typing import Iterator
from typing import TYPE_CHECKING

from deskops import doc_access
from deskops.doc_access import ARTIFACT_MODELS
from deskops.doc_access import ARTIFACT_PATHS
from deskops.doc_access import ARTIFACT_SUBJECTS
from deskops.doc_access import DocumentRecord
from deskops.doc_access import RepoTaskRoute
from deskops.doc_access import slugify
from deskops.lifecycle import ReadSnapshot
from deskops.lifecycle import TransitionResult
from deskops.paths import data_path
from deskops.runtime import Task
from deskops.services.atoms import AtomCreateResult
from deskops.services.atoms import AtomMergeResult
from deskops.services.atoms import AtomSplitResult
from deskops.services.atoms import AtomValidationRecord
from deskops.services.closure import CloseoutGateReport
from deskops.services.tasks import TaskBundle

if TYPE_CHECKING:
    from deskops.services.atoms import AtomsService
    from deskops.services.closure import ClosureService
    from deskops.services.closeout_gates import CloseoutGatesService
    from deskops.services.drawer import DrawerService
    from deskops.services.tasks import TasksService

__all__ = [
    "ARTIFACT_MODELS",
    "ARTIFACT_PATHS",
    "ARTIFACT_SUBJECTS",
    "AtomCreateResult",
    "AtomMergeResult",
    "AtomSplitResult",
    "AtomValidationRecord",
    "CloseoutGateReport",
    "DeskopsOperations",
    "DocumentRecord",
    "RepoTaskRoute",
    "TaskBundle",
    "slugify",
]


class DeskopsOperations:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"
        self.spec_root = data_path("spec")
        self.snapshot: ReadSnapshot | None = None
        self._drawer: DrawerService | None = None
        self._tasks: TasksService | None = None
        self._closeout_gates: CloseoutGatesService | None = None
        self._closure: ClosureService | None = None
        self._atoms: AtomsService | None = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_file = self.root / ".deskops.log"
        self.logger = logging.getLogger("deskops")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

    @contextmanager
    def read_snapshot(self) -> Iterator[None]:
        """Reuse task-independent graph reads for the duration of one read-only pass.

        Inside the block, the closeout graph context and the lifecycle transitions
        leaving each node are computed once and shared by every task read. The caller
        promises not to write the desk inside the block; nesting reuses the outer one.
        """
        if self.snapshot is not None:
            yield
            return
        self.snapshot = ReadSnapshot()
        try:
            yield
        finally:
            self.snapshot = None

    # ---------------------------------------------------------------- services
    @property
    def closeout_gates(self) -> "CloseoutGatesService":
        if self._closeout_gates is None:
            from deskops.services.closeout_gates import CloseoutGatesService

            self._closeout_gates = CloseoutGatesService(self.root)
        return self._closeout_gates

    @property
    def closure(self) -> "ClosureService":
        if self._closure is None:
            from deskops.services.closure import ClosureService

            self._closure = ClosureService(self.root, self)
        return self._closure

    @property
    def drawer(self) -> "DrawerService":
        if self._drawer is None:
            from deskops.services.drawer import DrawerService

            self._drawer = DrawerService(self.root)
        return self._drawer

    @property
    def tasks(self) -> "TasksService":
        if self._tasks is None:
            from deskops.services.tasks import TasksService

            self._tasks = TasksService(self.root, self)
        return self._tasks

    @property
    def atoms(self) -> "AtomsService":
        if self._atoms is None:
            from deskops.services.atoms import AtomsService

            self._atoms = AtomsService(self.root, self)
        return self._atoms

    # ---------------------------------------------------------------- documents
    def ensure_workspace(self) -> None:
        doc_access.ensure_workspace(self.root)

    def create_artifact(self, artifact_id: str, raw_payload: dict[str, Any]) -> DocumentRecord:
        return doc_access.create_artifact(self.root, artifact_id, raw_payload)

    def edit_artifact_field(self, subject: str, selector: str, field: str, raw_value: str) -> DocumentRecord:
        return doc_access.edit_artifact_field(self.root, subject, selector, field, raw_value)

    def list_artifacts(self, artifact_id: str) -> list[dict[str, Any]]:
        return doc_access.list_artifacts(self.root, artifact_id)

    def show_artifact(self, artifact_id: str, doc_id: str) -> dict[str, Any]:
        return doc_access.show_artifact(self.root, artifact_id, doc_id)

    def list_repo_task_routes(self) -> list[RepoTaskRoute]:
        return doc_access.list_repo_task_routes(self.root)

    # ---------------------------------------------------------------- tasks
    def registered_task_types(self) -> dict[str, type[Any]]:
        return self.tasks.registered_task_types()

    def create_task_bundle(self, raw_payload: dict[str, Any]) -> TaskBundle:
        return self.tasks.create_task_bundle(raw_payload)

    def bind_pill_to_task(self, task_selector: str, pill_selector: str) -> tuple[DocumentRecord, str, bool]:
        return self.tasks.bind_pill_to_task(task_selector, pill_selector)

    def list_tasks(self) -> list[Task]:
        return self.tasks.list_tasks()

    def show_task(self, task_id: str) -> tuple[Task | None, list[dict[str, Any]]]:
        return self.tasks.show_task(task_id)

    def advance_task(self, task_id: str) -> tuple[Task | None, TransitionResult | None]:
        return self.tasks.advance_task(task_id)

    def next_action_report(self, task_selector: str | None = None) -> dict[str, Any]:
        return self.tasks.next_action_report(task_selector)

    def render_next_action_diagram(self) -> str:
        return self.tasks.render_next_action_diagram()

    # ---------------------------------------------------------------- closeout
    def verify_task_closeout(self, task_selector: str) -> dict[str, Any]:
        return self.closure.verify_task_closeout(task_selector)

    # ---------------------------------------------------------------- drawer
    def resolve_drawer_source(self, selector: str) -> Path:
        return self.drawer.resolve_drawer_source(selector)

    def attach_drawer_source(self, payload: dict[str, Any], drawer_file: Path) -> dict[str, Any]:
        return self.drawer.attach_drawer_source(payload, drawer_file)

    # ---------------------------------------------------------------- atoms
    def atom_folder_axis(self) -> str | None:
        return self.atoms.atom_folder_axis()

    def list_atoms(self, axis_value: str | None = None) -> tuple[str | None, list[dict[str, Any]]]:
        return self.atoms.list_atoms(axis_value)

    def reorganize_atoms(self, *, dry_run: bool = False) -> dict[str, Any]:
        return self.atoms.reorganize_atoms(dry_run=dry_run)

    def validate_atoms(self, selector: str | None = None) -> list[dict[str, Any]]:
        return self.atoms.validate_atoms(selector)

    def delete_atom(self, selector: str, *, force: bool = False) -> DocumentRecord:
        return self.atoms.delete_atom(selector, force=force)

    def create_atom_from_source(
        self,
        atom_id: str,
        *,
        five_wh_one_plus: str,
        title: str | None = None,
        tags: list[str] | None = None,
        from_pill: str | None = None,
        from_graph: str | None = None,
        from_diagram: str | None = None,
        graph_path: str | None = None,
    ) -> AtomCreateResult:
        return self.atoms.create_atom_from_source(
            atom_id,
            five_wh_one_plus=five_wh_one_plus,
            title=title,
            tags=tags,
            from_pill=from_pill,
            from_graph=from_graph,
            from_diagram=from_diagram,
            graph_path=graph_path,
        )

    def split_atom(
        self,
        selector: str,
        *,
        into_ids: list[str],
        section_flags: list[str] | None = None,
        force: bool = False,
    ) -> AtomSplitResult:
        return self.atoms.split_atom(
            selector,
            into_ids=into_ids,
            section_flags=section_flags,
            force=force,
        )

    def merge_atom(
        self,
        selector: str,
        *,
        into_selector: str,
        force: bool = False,
    ) -> AtomMergeResult:
        return self.atoms.merge_atom(selector, into_selector=into_selector, force=force)

    # ---------------------------------------------------------------- private helpers
    def _atom_doc_path(self, atom_id: str, tags: list[str]) -> Path:
        return doc_access.atom_doc_path(self.root, atom_id, tags)

FILE:docs/operator-manual.md
# deskops Operator Manual

This manual is the end-to-end operational playbook for `deskops`.

It is written for two audiences:

- people who operate a desk by hand
- agents that follow documented commands instead of reconstructing behavior from source

The examples are executable. Every fenced block marked `bash runnable` is
extracted, in document order, by `tests/test_operator_manual.py`. The test runs
the blocks in a throwaway git repository under `pytest`'s `tmp_path`, with an
isolated `HOME`, so the manual cannot drift from the real CLI.

Blocks marked `bash` are illustrative only. They show expected failures,
destructive alternatives, cross-repo targeting, or commands that need an
external runtime such as Herdr.

For the first, shortest walkthrough, read `docs/quickstart.md`. For the CLI's
first-use question index, run `deskops faq`. This manual does not re-document
SLDB; it only covers the deskops workflow surface built on top of SLDB.

## Runnables convention

The runnable walkthrough assumes:

- the current directory is an empty git repository with at least one commit
- `deskops` resolves to this checkout (`tests/test_operator_manual.py` supplies
  a shim so the examples stay spelled `deskops ...`)
- no real `~/.sldb` or user desk is touched

Run one block at a time, or let the test run all blocks in order. State created
by one block is visible to later blocks.

## Machine and repository setup

### Help and bootstrap

`deskops bootstrap` is the machine-level repair path. It verifies that SLDB is
importable, installs it from the sibling checkout only when needed, creates the
global `~/.sldb` store, and registers the deskops model set there.

```bash runnable
deskops --help
deskops bootstrap
```

### Initialize the repository

`deskops init` runs the bootstrap preflight, creates a local `.sldb/` store,
scaffolds `desk/`, and writes the lifecycle graph under `desk/lifecycle/`.

```bash runnable
deskops init .
```

### Orient yourself

```bash runnable
deskops about
deskops faq
deskops faq 1
```

`deskops faq` with no argument lists the available questions. Pass a question
index, slug, or text fragment to print one answer.

### Check desk health

`deskops doctor` reports desk shape, store registration, tracking, and model
validity. `deskops status` is a deprecated alias for the same command.

```bash runnable
deskops doctor --root .
deskops status --root .
```

The report has two parts. **Errors** mean the desk is broken: missing structure,
a tracked document that is gone, a document its model cannot read, an unregistered
model, a store that cannot be read. They make `doctor` exit 1. **Alerts** mean the
store moved under an expected change: a document edited, moved or added by hand, a
model contract that changed. Nothing is broken; register them with
`deskops desk update --apply`. Alerts alone exit 0, and they are always printed.

A task its model rejects (its `status`, `current_node` and `history` are not a state
the lifecycle can produce) is an error of its own, one line per task with the file and
the validator's text, read from the task's frontmatter: `sldb stores check` stops at the
first such document, so doctor names every one and still runs the other checks
(structure, store, models). A task the legacy migration decides says
`Migrate it with deskops desk update --apply`; any other one says what its owner can
do (`decide its state: deskops closeout supersede --task <id> --reason ... --ref ...`).

`doctor` also compares the desk's managed seeds (the lifecycle graph and its rules
under `desk/lifecycle/`) with the ones the installed deskops ships, by the same
comparison `deskops desk update --apply` makes before rewriting them. Each copy
that differs is one finding, naming the top-level frontmatter fields that differ
(`body` when only the text below the frontmatter does; the `sldb:` write
provenance is named only when nothing else differs):

```text
lifecycle seed out of date: desk/lifecycle/execution-task_activates.md differs from the deskops package (attributes). Fix: deskops desk update --apply
```

It is an **error** when a lifecycle edge's transition fields differ (`source_id`,
`target_id`, `relation_type`, `condition`, `attributes`): `deskops advance` refuses
that edge. Any other difference (a rule, the body or notes of a seed) is an
**alert**. A desk seeded before CC31 has `attributes: {}` on its edges and shows
up here; `deskops desk update --apply` restores the managed seeds.

`--repair` acts on errors only (it scaffolds structure and registers models). Use it
when you understand the reported errors:

```bash
deskops doctor --root . --repair
```

### Inspect the lifecycle graph

On a fresh desk, `next --diagram` renders the state machine as Mermaid from the
source spec. The states are ritual docs and the transitions are sldb relation
docs.

```bash runnable
deskops next --diagram --root .
```

The rendered edges include their conditions:

- `task_activates` moves a draft task into execution.
- `task_hands_to_closeout` requires a non-empty `validation` field.
- `task_completes` requires `status = 'ready_for_testing'` and verified
  closeout evidence.

## Repository identity and the ecosystem registry

`deskops repo whoami` prints the repository's configured project identity.
`deskops repo register` writes a canonical `RepositoryDoc` into the registry and
tracks it in SLDB.

Register the current repository before sending messages. Message delivery
requires the current repository to resolve through the registry when any
registry entries exist.

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo register "$identity" . --store .sldb --pythonpath .
deskops repo whoami --root .
```

`deskops repo remove <id>` takes a registration out of the registry so the
repository can be registered again, for example after a rename:

```bash runnable
identity="$(deskops repo whoami --root .)"
deskops repo remove "$identity" --root . --store .sldb
deskops repo register "$identity" . --store .sldb --pythonpath .
```

`deskops add repository` is different: it creates a local repository artifact
under `desk/registry/` for discovery or routing. It is not the canonical
ecosystem registration path. The runnable walkthrough creates one later for a
sibling desk.

Cross-repo targeting uses the registered repository id:

```bash
deskops message send "Need a follow-up" --to sibling-desk --title "Follow-up"
deskops list tasks --include-repos
```

## Desk scaffold, migration, and repair

`deskops desk install` scaffolds only the desk folders and starter docs. It does
not create a store, register a repository, or write the lifecycle graph.

```bash runnable
mkdir -p ../sibling
deskops desk install ../sibling
deskops desk migrate --root ../sibling
deskops desk update --root ../sibling --apply
```

- `desk install <path>` creates `tasks/`, `contexts/`, `rituals/`, `atoms/`,
  `roles/`, `inbox/`, `drawer/`, the starter boards/pills/rituals, and
  `desk/config.json`.
- `desk migrate` adopts a legacy or partial desk non-destructively. It reports
  what it adopted, preserved, or left for manual conversion.
- `desk update` is a dry run by default. Add `--apply` to create a missing
  store, register missing models, and write the lifecycle graph.
- `desk update` also migrates the tasks a desk migrated before CC31 left in a
  state no transition produces: an empty history with a terminal or drawer
  status at a node. The dry run lists them as `Legacy task states to migrate`;
  `--apply` writes them first, one line per changed field
  (`desk/tasks/<task>.md: history [] -> [superseded]`). The table:
  `superseded` gets `history [superseded]` (its node stays); `closed`,
  `resolved`, `done`, `complete` and `cancelled` (pre-lifecycle resolved), and
  `deferred` and `candidate` (drawer), get `current_node ''`, outside the
  lifecycle. A non-terminal status with an empty history (any status that is
  not `draft` nor one of those above, nor a closeout status: `active`,
  `ready_for_testing`, `blocked`...) is backed by no transition, so it gets
  `status draft` at the entry node `ritual-execution` (an empty
  `current_node` stays empty), reported as
  `desk/tasks/<task>.md: status active -> draft` plus
  `current_node <node> -> ritual-execution` when the node moves, and its
  `summary` gets one line in front, `Migrada a draft por deskops desk update:
  estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).`, followed by the
  previous summary. A non-empty history with an incoherent status is not
  migrated. Any other task the model rejects is listed under
  `Invalid task documents (not written)` with the validator's text and what its
  owner can do; it is never written. The write goes to the frontmatter, not
  through sldb (sldb rebuilds every task of the store on each write and stops at
  the invalid one), and the new text is validated with `TaskDoc`; a task it
  still rejects is restored. While `sldb stores check` cannot read the store,
  `--apply` reports it and skips every other repair (structure, lifecycle
  graph, models, tracking, task types, indexes) instead of leaving the store
  half written. `--apply` exits 0
  when nothing is left and 1 while a task waits for its owner; a second run
  migrates nothing.

A dry run exits `1` when it finds divergence:

```bash
deskops desk update --root ../sibling
# Desk divergence report:
# - Missing store: .sldb
# - Unregistered models: ...
# Run with --apply to repair these issues.
```

## Artifact commands

The `add`, `edit`, `list`, and `show` families are generated from the artifact
registry. The same grammar applies to every artifact subject.

### Add artifacts

```bash runnable
deskops add atom --root . \
  --title "Operator manual evidence" \
  --five-wh-one-plus what \
  --answer "The operator manual examples run against the real CLI." \
  --tags system:manual topic:docs

deskops add pill --root . \
  --title "Pattern: Manual examples stay runnable" \
  --summary "Executable documentation." \
  --what "What." --why "Why." --when "When." --where "Where." \
  --how "How." --how-not "How not." \
  --tags topic:docs

deskops add ritual --root . \
  --title "Manual ritual" \
  --purpose "Purpose." --trigger "Trigger." --completion "Completion."

deskops add board --root . \
  --title "Manual board" --scope "Scope." --purpose "Purpose."

deskops add materialization --root . \
  --title "Manual materialization" \
  --source-atoms atom-operator-manual-evidence \
  --target-kind board \
  --target-identity desk/tasks/Board.md \
  --intent "Document the CLI." \
  --validation pytest

deskops add repository --root . \
  --name "Sibling desk" --path ../sibling --description "Sibling sandbox."

deskops add faq-doc --root . --title "Manual FAQ" --body "FAQ body."

deskops add step --root . \
  --title "Manual step" --action "Action." --outcome "Outcome."

deskops add inbox-note --root . \
  --kind suggestion \
  --created-at "2026-01-01T00:00:00" \
  --status open \
  --title "Manual inbox note" \
  --body "Promote this note."
```

Required and commonly used flags per subject:

| Subject | Required flags | Common extras |
|---|---|---|
| `task` | `--title` | `--why`, `--goal`, `--scope`, `--task-type` (default `task.code`), `--implementation-path`, `--done-when`, `--validation`, `--from-drawer`, `--depends-on`, `--evidence` (adds kinds only), `--inherits-from`, `--atom`, `--inherit-acceptance-context` |
| `pill` | `--what`, `--why`, `--when`, `--where`, `--how`, `--how-not` | `--summary`, `--tags` |
| `ritual` | `--purpose`, `--trigger`, `--completion` | `--preconditions`, `--steps`, `--validation`, `--failure-modes`, `--tags` |
| `board` | `--scope`, `--purpose` | `--tasks`, `--pills`, `--rituals`, `--notes`, `--tags` |
| `atom` | `--five-wh-one-plus`, `--answer` | `--title`, `--tags`, `--provenance` |
| `materialization` | `--target-kind`, `--target-identity`, `--intent` | `--source-atoms`, `--validation`, `--tags`, `--provenance` |
| `repository` | `--name`, `--description` | `--path`, `--status`, `--tags` |
| `inbox-note` | `--kind`, `--created-at`, `--status`, `--body` | `--sender-project`, `--target-project`, `--title`, `--acknowledged-by`, `--acknowledged-at` |
| `faq-doc` | `--body` | `--title` |
| `step` | `--action`, `--outcome` | `--title`, `--tags` |

`--validation`, `--depends-on`, `--atom`, and similar list flags accept repeated
or space-separated values. Put them last in a command when mixing with another
multi-value flag, because argparse consumes following tokens until the next
flag.

`--from-yaml <file>` loads the payload from YAML for every `add` subject.

`--evidence <kind>...` adds closeout evidence kinds to the type's (`tests`,
`commit`, `atom`, `materialization`, `document`, `external`); it cannot remove
one the type requires. Without `--task-type` the type is `task.code`. See Closeout.

### List artifacts

Plural subjects list all documents of a type. `--format json` is available on
every list command. `list tasks --include-repos` also follows task boards
registered as sibling repositories.

```bash runnable
deskops list atoms --root .
deskops list pills --root .
deskops list rituals --root .
deskops list boards --root .
deskops list materializations --root .
deskops list repositories --root .
deskops list faq-docs --root .
deskops list steps --root .
deskops list inbox-notes --root .
```

### Show artifacts

Singular subjects show one document by exact id, filename, stem, or a unique
slug fragment. `--format json` is available.

```bash runnable
deskops show atom atom-operator-manual-evidence --root .
deskops show pill pill-pattern-manual-examples-stay-runnable --root .
deskops show ritual ritual-manual-ritual --root .
deskops show board board-manual-board --root .
deskops show materialization materialization-manual-materialization --root .
deskops show repository repo-sibling-desk --root .
deskops show faq-doc faq-manual-faq --root .
deskops show step step-manual-step --root .
deskops show inbox-note inbox-note-manual-inbox-note --root .
```

### Edit artifacts

The edit grammar is:

```text
deskops edit <subject> <selector> <field> <value> [--root .]
```

Field names accept hyphens in place of underscores. Values are parsed like SLDB
field values, so JSON lists and quoted strings work. The document is re-rendered
through its model.

A section field of text whose template carries an italic placeholder paragraph
(`_Outline the expected implementation route or affected surface._` in a task,
`_Describe the incoming message with enough evidence to triage._` in an inbox
note) gets it from the template on every render, so `edit` drops from the value
any paragraph that is exactly that field's placeholder. Passing the raw section
text back with a new paragraph leaves one placeholder, the same value twice leaves
the same file, and a value that is only the placeholder empties the field. The
phrase inside a longer paragraph, a quote, a list or a code block is content and
stays. The placeholders are read from the model's template, never from a list.

```bash runnable
deskops edit atom atom-operator-manual-evidence title "Operator manual evidence (edited)" --root .
deskops edit pill pill-pattern-manual-examples-stay-runnable summary "Edited summary." --root .
deskops edit ritual ritual-manual-ritual summary "Edited summary." --root .
deskops edit board board-manual-board notes "Edited notes." --root .
deskops edit materialization materialization-manual-materialization intent "Edited intent." --root .
deskops edit repository repo-sibling-desk status maintenance --root .
deskops edit faq-doc faq-manual-faq body "Edited FAQ body." --root .
deskops edit step step-manual-step outcome "Edited outcome." --root .
deskops edit inbox-note inbox-note-manual-inbox-note body "Edited inbox body." --root .
```

The same subjects exist for `add`, `edit`, `list`, and `show`; `list` uses
plural names and `show` uses singular names.

## Inbox, messages, and drawer

### Send, list, read, and acknowledge messages

`deskops message` is the canonical cross-desk surface. Files are written to the
target desk's `desk/inbox/` as timestamped Markdown notes. Acknowledging closes
the note but keeps the file as the trace.

```bash runnable
deskops message send "Please clarify the manual example." \
  --kind unclear --title "Manual message" --root .
deskops message list --root .
deskops message read manual-message --root .
deskops message ack manual-message --root .
```

`deskops inbox` is a deprecated alias for the same storage. Its flag grammar
(`--list`, `--show`, `--ack`) still works:

```bash runnable
deskops inbox --list --root .
```

`--to <repo>` targets another registered repository. `--from <project>` overrides
the resolved sender identity (`--sender` is the deprecated `inbox` spelling).
`--desk-root` targets an explicit desk directory. `--format json|yaml` prints
the result for machines.

### Promote an inbox note to a drawer candidate

Inbox notes are intake. Promotion turns one note into a loose deferred candidate
under `desk/drawer/tasks/`, removes the inbox file, and records the new
candidate on the drawer board. The candidate is not yet an active task.

```bash runnable
deskops promote inbox-to-drawer-task manual-inbox-note --root .
```

`--title <text>` overrides the candidate title.

### Remove a drawer entry

`deskops drawer remove` removes the file, its tracking, and its drawer-board
bullets. It refuses when an active task records the entry in `from_drawer`
unless `--force` is passed. Any other reference to the entry is left as it is.
Each file that holds one is reported on stderr as
`alert: <entry> still referenced by <file>`, and the exit code does not change.
These references are what `sldb.api.referrers` finds over the desk graph: a
drawer-board bullet in another form, such as `` `tasks/<id>.md` ``, or a task
that names the entry. `deskops closeout` reports the files that still name the
closed task in the same way.

```bash runnable
deskops message send "Remove this candidate." \
  --kind suggestion --title "Removable candidate" --root .
deskops promote inbox-to-drawer-task removable-candidate --root .
deskops drawer remove task-removable-candidate --root .
```

### Retire any other desk document

`deskops retire` removes one obsolete file under `desk/` that has no dedicated
verb (pills, inbox notes, steps, roles, runtimes, FAQ docs, materializations,
leftovers), with a reason and a `--ref` that resolves to an ancestor commit or
an existing path. The declared fields that name the document lose that entry
in the transaction that deletes it. For a pill, these are the `pills` of the
Board and of every task. A mention in prose, such as a path in a task body, is
never rewritten, so retire refuses while one remains unless `--force` is passed.
Both kinds of reference are what `sldb.api.referrers` finds: the store's field
index, and the mention patterns of the desk graph. Tasks, drawer entries, atoms, and registry
entries keep their own verbs: `closeout`, `drawer remove`, `atoms delete`,
`repo remove`.

```bash runnable
deskops retire desk/steps/step-manual-step.md --root . \
  --reason "The manual step was only an example" \
  --ref "$(git rev-parse HEAD)"
```

## Tasks

### Author a task from a drawer candidate

There is no direct drawer-to-active promotion. A person or agent authors the
active task explicitly and records the drawer file with `--from-drawer`. The
drawer file is kept for manual cleanup. Like every task, its type declares its
closeout evidence: `--task-type task.docs` declares `commit` and `document`.

```bash runnable
deskops add task --root . \
  --title "Close a manual task" \
  --task-type task.docs \
  --why "Why." \
  --goal "Goal." \
  --scope "Scope." \
  --implementation-path "Path." \
  --done-when "Done." \
  --from-drawer task-manual-inbox-note \
  --validation "pytest tests/test_manual_smoke.py"
```

### Bind reusable context pills

Pills are reusable atomic context, not one-to-one task artifacts. Bind the ones
whose `when`, `where`, and `how_not` match the task.

```bash runnable
deskops bind pill task-close-a-manual-task \
  pill-pattern-manual-examples-stay-runnable --root .
```

### Inspect, edit, and advance a task

`next <task>` explains the next valid workflow action without mutating the
task; `next <task> --why` adds why this task and these actions were selected. `show task` prints the lifecycle gates and whether each holds.

```bash runnable
deskops list tasks --root .
deskops show task task-close-a-manual-task --root .
deskops next task-close-a-manual-task --root .
deskops edit task task-close-a-manual-task scope "Edited scope." --root .
deskops review record task-close-a-manual-task --kind preflight --operator "Manual operator" \
  --evidence desk/tasks/task-close-a-manual-task.md --reason "Contract read; nothing ambiguous" --root .
deskops review dispose review-task-close-a-manual-task-preflight-1 --verdict accepted --reason "Contract reviewed by the operator" --root .
deskops advance task task-close-a-manual-task --root .
deskops advance task task-close-a-manual-task --root .
```

A task leaves `ritual-execution` only with the review receipts its type asks for
(here `task.docs`: an accepted `preflight` on the task's current contract, so it
is recorded after the last edit). This sandbox has no reviewer model, so the
operator records a human receipt (`engine: human`, `no model available`; see
[Cold context reviews](#cold-context-reviews)); a desk where the model runs uses
`deskops review preflight`. The two advances move the task from `draft` to `active` and then
`ready_for_testing`. `advance` stops at `ritual-closeout`; it never closes a
task. When no outgoing transition condition holds, it exits non-zero and names
the blocked gate.

Before applying an edge, `advance` checks it against the lifecycle the installed
deskops ships: same `relation_type`, same target ritual and same
`attributes.sets.status`. An edge that differs (a desk seeded before CC31 has
`attributes: {}`) would write a state the task model rejects, so `advance` stops
first, exits 1 and leaves the task unchanged:

```text
Error: Cannot advance task-x via task_activates: the edge desk/lifecycle/execution-task_activates.md does not set status active (attributes.sets.status is missing). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.
```

`deskops doctor` reports the same seed; `deskops desk update --apply` restores it.

There is no manual override: a transition fires only when its condition
holds, and a blocked task stays where it is while `advance` names the gate.
Closing is `deskops closeout commit` for work that was done, `closeout
resolved-by` for work that already entered the history (for example through a
PR) before the closeout, `closeout supersede` when the task's subject no longer
exists, and `closeout retire` for a task resolved before the ritual lifecycle.

## Closeout

A task's type declares the evidence that closes it (`task.code`: tests + commit + atom|materialization; `task.docs` and `task.decision`: commit + document; `task.external`: external; `task.aggregate`: children + commit; `task.refactor`: task.code's evidence plus goldens). `--evidence` only adds kinds to the type's, never removes one. `deskops closeout verify`
checks exactly that set for a board-routed task, nothing more and nothing less,
and prints `esta tarea declaró X; encontré Y` (declared X; found Y):

| Evidence | What counts |
|---|---|
| `tests` | an existing `.py` file under `tests/`, optionally with `::node`, or a `pytest <path>` reference |
| `atom` / `materialization` | one gate: an atom reference, or graph/materialization coverage or a routed follow-up reference for every path in `files`; exempt in a desk without local atom documents |
| `commit` | a lowercase 7-40 character commit id resolving to `HEAD` or an ancestor |
| `document` | an existing `.md`, `.rst`, `.txt`, `.adoc`, or `.yaml` file in `references` or `files`, outside `tests/` and `desk/tasks/` |
| `external` | an `http(s)` URL in `references`, for work tracked outside the repository |

Changed `.py` files in a task that did not declare `tests` print a visible alert
without blocking. A task created before the field existed is gated as code and
alerted to declare its evidence with
`deskops edit task <id> closeout_evidence '["commit", "document"]'`.

Verify before adding evidence. It exits `1` and prints the missing gates:

```bash
deskops closeout verify --root . --task task-close-a-manual-task
```

The manual task was authored with `--task-type task.docs`, so its type declares
`commit` and `document`: the gate asks for no test file. The example still writes
`tests/test_manual_smoke.py` because the task's `--validation` names it, and
the `pytest ...` reference is extra context the gate does not read. The atom
file is the document evidence. The commit reference must already exist, so use
an earlier commit such as the repository seed or the authoring commit. The
closing commit does not exist yet.

```bash runnable
mkdir -p tests
cat > tests/test_manual_smoke.py <<'EOF'
def test_manual_smoke():
    assert True
EOF

commit="$(git rev-parse HEAD)"
deskops edit task task-close-a-manual-task references \
  "[\"desk/atoms/atom-operator-manual-evidence.md\", \"pytest tests/test_manual_smoke.py::test_manual_smoke\", \"$commit\"]" \
  --root .
deskops edit task task-close-a-manual-task files \
  '["desk/atoms/atom-operator-manual-evidence.md"]' --root .
deskops closeout verify --root . --task task-close-a-manual-task
```

`deskops closeout commit` creates the closing commit itself. It offers two
routes:

- `--run-dir runs/subagents/<dir>` links the commit to subagent run evidence
  and adds `Task-Id`, `Run-Dir`, `Run-Id`, and `Session-Sha256` trailers.
- `--no-run --reason "<why>"` closes manually and adds `Task-Id`,
  `Closeout-Mode: manual`, and `Closeout-Reason` trailers.

Either route removes the task bundle from `desk/tasks/`, removes it from
`desk/tasks/Board.md`, records the commit in `runs/subagents/index.jsonl`, and
commits only the paths it staged. Unrelated staged work stays staged. `--paths`
accepts files and directories.

```bash runnable
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --no-run --reason "Operator manual runnable example" \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

A subagent-run closeout instead looks like:

```bash
deskops closeout commit --root . \
  --task task-close-a-manual-task \
  --run-dir runs/subagents/20260101-120000-task-close-a-manual-task \
  --run-id 6046eaef \
  --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \
  --paths desk/atoms/atom-operator-manual-evidence.md tests/test_manual_smoke.py
```

### Supersede or retire a task

Two closes skip the evidence gates because no work is being proven.
`closeout supersede` closes a task whose subject no longer exists. `closeout
retire` removes a task whose status is already `resolved`, `closed`, `done`,
`complete` or `cancelled`, as pre-lifecycle tasks are, or `superseded`,
`deferred` or `candidate` with an empty history (what a desk migrated before
CC31 left; a `superseded` task with only its `superseded` record, what
`desk update --apply` makes of it, too). Retire reads the task's frontmatter, so it also removes a task its
model rejects; in a desk with a store it waits until no other task is invalid
(`deskops desk update --apply` first). `closeout supersede` also closes a task
its model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads and writes the frontmatter, with the same
commit and trailers, and waits the same way while another task is invalid. Both need `--reason` and at least one
`--ref` (an ancestor commit; supersede also accepts an existing path), make
exactly one closing commit with `Closeout-Mode: superseded` or
`Closeout-Mode: legacy-resolved` trailers, and take the task off the Board.

```bash runnable
deskops add task --root . \
  --title "Superseded manual task" \
  --task-type task.docs \
  --goal "Goal." --scope "Scope." --validation "pytest"
deskops closeout supersede --root . \
  --task task-superseded-manual-task \
  --reason "The feature this task targeted was removed before any work started" \
  --ref "$(git rev-parse HEAD)"
```

```bash
deskops closeout retire --root . \
  --task task-already-resolved \
  --reason "Resolved before the ritual lifecycle existed" \
  --ref 3900ad4
```

### Close a task whose work already entered the history

`closeout resolved-by` closes a task whose work was already committed, for
example merged through a PR, before anyone ran its closeout. It does not ask for
an atom per changed file. Its evidence is a `--reason`, at least one `--ref`
that is a commit at HEAD or an ancestor (further refs may be ancestor commits or
http(s) URLs, such as the PR), and at least one `--test` that the tests gate
accepts for the task's `files`. A ref or test that does not resolve is refused
and nothing is written. It makes exactly one closing commit with
`Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and
one `Closeout-Test` per test; the task is marked `resolved` (history
`resolved-by`) and leaves the Board. `--paths` adds paths to the closing commit
and `--message` replaces its subject. Like supersede, it also closes a task its
model rejects (a lifecycle no migration decides, such as a `draft` after
`task_hands_to_closeout`): it reads the task's `files` and history from the
frontmatter, applies the same ref and test gates, writes `status: resolved` and
the `resolved-by` record into the frontmatter (validated with `TaskDoc`, restored
if it fails) and makes the same closing commit with the same trailers. In a desk
with a store, supersede, retire and resolved-by refuse before writing anything
while another task is invalid: sldb re-extracts the whole model on every write
(sldb H2, note 3895e9f7). Migrate the others with `deskops desk update --apply`,
decide them by hand, or close each with `closeout supersede` or `closeout retire`
once it is the only invalid task, then run the close again.

```bash
deskops closeout resolved-by --root . \
  --task task-fix-thing \
  --reason "The fix entered main through PR #42 before the closeout" \
  --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \
  --test tests/test_fix_thing.py
```

When the task's code entered another repository (a task.code of a coordinating
desk whose code lives in a sibling repo), qualify the ref and the test with that
repository's id: `--ref <repo-id>:<sha>` and `--test <repo-id>:<test path>`.
The id is looked up in the desk's own registry, `desk/registry/repo-*.md`,
written by `deskops repo register`. The reference is cut at its first `:`: when
what comes before it is a registered id, the rest is checked in that
repository's registered root, with the same rules as a local reference (a
lowercase commit id that is its HEAD or an ancestor; an existing `.py` file
under one of its `tests/` directories, optionally with a pytest `::node`). The
task's `files` do not widen where another repository's tests live. A prefix
that is not a registered id (or a reference without `:`) is checked locally as
before, and a prefix naming the desk itself (its `project_identity`, or a
registered repository whose root is the desk's root) is local. A registered
repository whose root is missing on this machine refuses the close with
`Registered repository <id> is not at <path> on this machine.` and writes
nothing. The closing commit is the same, made in the desk's repository, and its
`Closeout-Ref` and `Closeout-Test` trailers keep each reference as written
(`Closeout-Ref: infra:87671716`). `closeout verify`, `closeout commit` and
`closeout supersede` still accept only local evidence.

```bash
deskops repo register infra --path /srv/infra --id infra --store .sldb
deskops closeout resolved-by --root . \
  --task task-wire-infra \
  --reason "The code entered infra through PR #7" \
  --ref infra:87671716 --ref https://example.com/org/infra/pull/7 \
  --test infra:tests/test_wire.py
```

## Issues

Issues are plain Markdown files under `desk/issues/` or
`desk/drawer/issues/`. They are intentionally not modeled documents.
`deskops issue list` filters by `open`, `closed`, or `all`. `deskops issue close`
rewrites the status and appends a `## Resolution` section; it never deletes the
file.

```bash runnable
mkdir -p desk/issues
cat > desk/issues/issue-manual-example.md <<'EOF'
# Manual example issue

## Status

open

## Problem

The manual needs an issue example.
EOF

deskops issue list --root .
deskops issue close issue-manual-example --reason "Manual example" --ref . --root .
deskops issue list --status closed --root .
```

### Replace text in an unmodeled desk file

`deskops desk replace` edits a file under `desk/` that no `deskops edit`
subject reaches (issue bodies, drawer notes, role prompts, the tag namespace
file). `--old` must occur exactly `--count` times (default 1); a modeled
document is refused and pointed at its `edit` verb. The write is sldb's
`replace_text` inside the desk transaction: a store-tracked file (a role prompt)
must still validate under its model after the replacement, or nothing is written
and the command exits 1 with `Refusing to replace in <path>: ...`.

```bash runnable
deskops desk replace desk/issues/issue-manual-example.md --root . \
  --old "The manual needs an issue example." \
  --new "The manual has an issue example."
```

## Atoms

Atoms are the durable knowledge layer. The `atoms` commands cover namespaces,
protoatoms, typed atoms, crossroads, domain trees, provenance-preserving
creation, splitting, merging, deletion, and validation.

### Namespaces, crossroads, and the domain tree

A domain tag such as `domain:manual.docs` needs a written crossroad for every
parent path, created top-down. Crossroads describe what hangs below a path.
sldb checks it (and that every atom or protoatom namespace is declared) as its
tag family, from the declaration `deskops init` and `deskops desk update --apply`
write in `.sldb/store.yaml`; a desk without a store checks neither. See
`docs/atoms.md` ("Who checks the namespaces and the domain parents").

```bash runnable
deskops atoms add-namespace manual \
  --meaning "Manual-only tags" \
  --use-when "Operator manual examples" \
  --do-not-use-when "Durable knowledge" \
  --example manual:example --root .

deskops atoms crossroad manual \
  --title "Manual domain" --content "Root of manual examples." --root .
deskops atoms crossroad manual.docs \
  --title "Manual docs" --content "Documentation children." --root .

deskops atoms proto proto-manual \
  --title "Manual proto" --content "Free text." \
  --tag domain:manual.docs --root .

deskops atoms tree --root .
```

### Type a protoatom

`atoms type` converts a protoatom into a tracked model document and keeps the
protoatom as a redirect stub. For `AtomDoc`, pass `--content-field answer`
because `AtomDoc` has no `content` field.

```bash runnable
deskops atoms type proto-manual \
  --model AtomDoc \
  --id atom-typed-manual \
  --content-field answer \
  --data '{"title":"Typed manual atom","five_wh_one_plus":"what"}' \
  --root .
```

### Create an atom from a source

`atoms create` preserves exact provenance from a pill field, a missing graph
finding, or a diagram source.

```bash runnable
deskops atoms create atom-from-manual-pill \
  --five-wh-one-plus what \
  --from-pill pill-pattern-manual-examples-stay-runnable \
  --root .
```

Other source routes:

```bash
deskops atoms create atom-from-graph \
  --five-wh-one-plus what \
  --from-graph source-id->target-id \
  --graph .deskops/graph.json --root .

deskops atoms create atom-from-diagram \
  --five-wh-one-plus what \
  --from-diagram docs/diagrams/example/source.mmd --root .
```

### Merge, delete, and validate

Merge rewrites every reference to the source atom so that it names the target,
in the same transaction as the merge. It covers fields such as a task's
`atoms`, `atom:atom-<source>` anywhere in a task or issue, and a bare
`atom-<source>` under a Related Atoms heading. The source stays as a redirect
stub. `atoms delete` and `atoms split` find the same references. `atoms split` is not shown here: since CC35a sldb
refuses headings inside a field, so a sectioned atom cannot be written through
the CLI (see the drawer entry
task-atoms-split-no-se-puede-alimentar-por-el-cli-desde-cc35a-sldb-rechaza-encabezados-en-el-field).

```bash runnable
deskops add atom --root . \
  --title "Merge source manual atom" \
  --five-wh-one-plus what \
  --answer "One."
deskops add atom --root . \
  --title "Merge target manual atom" \
  --five-wh-one-plus what \
  --answer "Two."
deskops atoms merge atom-merge-source-manual-atom \
  --into atom-merge-target-manual-atom --root .

deskops add atom --root . \
  --title "Delete manual atom" \
  --five-wh-one-plus what \
  --answer "Temporary."
deskops atoms delete atom-delete-manual-atom --root .

deskops atoms validate --all --root .
deskops list atoms --root .
deskops show atom atom-typed-manual --root .
```

`list atoms` and `show atom` are the current spellings; `atoms list` and
`atoms show` are deprecated aliases. `atoms delete` refuses to delete an atom with inbound references
unless `--force` is passed.

### Reorganize atoms by tag namespace

`atoms reorganize` moves atoms into folders derived from the
`atom_folder_axis` configured in `desk/config.json`. Without that config it
exits non-zero:

```bash
deskops atoms reorganize --dry-run --root .
# Error: No 'atom_folder_axis' configured in desk/config.json; nothing to reorganize.
```

Configure one namespace, then run it:

```json
{ "atom_folder_axis": "object" }
```

```bash
deskops atoms reorganize --dry-run --root .
deskops atoms reorganize --root .
```

## Graph

The graph surface builds a KGDB snapshot, shows one node's neighbors, reports
missing declared targets, and writes review-only self-reflection findings.

```bash runnable
deskops graph build --root . --output .deskops/graph.json
deskops graph neighbors atom:atom-from-manual-pill --root . --graph .deskops/graph.json
deskops graph missing --root . --graph .deskops/graph.json
deskops graph reflect --root . --graph .deskops/graph.json
```

`graph missing` exits `1` when a declared target does not resolve. For example,
a materialization whose `--target-identity` names a file that does not exist as
a graph node is reported as `missing_declared_target`.

`graph reflect` writes `.sldb/runtime/self_reflection_findings.json` and only
reports findings; it does not edit desk documents.

## Roles, materialization, and drift

Role docs under `desk/roles/` are materialized into pi-agent files.
`deskops materialize` writes them to `~/.pi/agent/agents/` by default; `--out`
overrides the directory. `deskops drift check` compares rendered output with
the installed files and also checks runtime-profile bindings.

A role with `kind: pi` needs a matching `RuntimeProfileDoc` under
`desk/runtimes/`. Without it, drift reports a missing runtime profile.

```bash runnable
cat > desk/roles/manual-role.md <<'EOF'
---
id: role-manual-example
name: manual-example
description: Example role for the operator manual.
kind: pi
model: example-model
fallback_models: []
tools: []
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Manual example role

Act as the example role.
EOF

mkdir -p desk/runtimes
cat > desk/runtimes/runtime-pi.md <<'EOF'
---
id: runtime-pi
status: active
kind: pi
binary: pi
model_flag: --model
fallback_models_flag: ''
fallback_models_join: comma
tools_flag: --tools
tools_join: comma
system_prompt_flag: --append-system-prompt
system_prompt_delivery: file
session_flag: --session
extra_args: []
unsupported_role_fields:
- fallback_models
tags:
- system:manual
---

# Pi runtime

## Summary

Pi agent runtime profile.

## Notes

Example profile.
EOF

deskops materialize --root . --out .pi-agent
deskops drift check --root . --out .pi-agent
```

`drift check` exits `1` on any finding. A mismatch names the installed file and
the role doc it was rendered from.

## Runtime and Herdr

The `runtime` commands manage a live Herdr Space. They need a `herdr`
executable and are not part of the runnable walkthrough.

```bash
# Initialize or reuse this desk's Herdr Space.
deskops runtime init --root .
deskops runtime init --root . --agents

# Inspect, focus, and close the Space.
deskops runtime status --root .
deskops runtime attach --root .
deskops runtime stop --root .

# List live agents machine-wide.
deskops runtime workers
deskops runtime workers --format json

# Block on one agent's lifecycle and report blocked/done settles.
deskops runtime supervise deskops-executor --root .
deskops runtime supervise deskops-executor --max-iterations 1 --timeout-ms 30000

# Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template
# (.scion/templates/<role-name>/: scion-agent.yaml, system-prompt.md, agents.md).
deskops runtime template deskops-executor --root .
deskops runtime template deskops-executor --root . --harness claude \
  --mode executor --task task-fix-thing --agent deskops-e-0123456789ab

# A tester is its own role and mode, with separate scope and completion rules.
deskops runtime template deskops-tester --root . --harness claude \
  --mode tester --task task-fix-thing --agent deskops-t-0123456789ab \
  --task-root . --run-dir runs/subagents/20261110-120000-task-fix-thing-testing
```

`runtime template` needs no live Herdr Space: it writes the template files from
the role and runtime-profile docs. `--mode executor` writes the agents.md for one
bounded task, `--mode tester` writes the independent verification instructions,
and `--mode coordinator` writes it for an agent that owns a desk. An explicit
mode always wins; otherwise only the selected role's own name/id is inspected
(a name or id ending in `-tester` chooses tester; a selected name or id naming a
supervisor/coordinator chooses coordinator; anything else executor). With
`--task` and `--agent` it also records the in_progress RunDoc launch intent under
`runs/subagents/`; its summary says it is intent, not proof of start.
`--task-root` names the repository whose desk owns the task (default `--root`)
and `--run-dir` points at the evidence directory. An existing RunDoc is reused
for reconciliation but never overwritten: a retry gets a new run_dir, and
attempts and their evidence are immutable.

`--context-file` accepts JSON with exactly `project`, `workspace_root`,
`desk_root`, `source_root` and `sldb_root`. `project` is a non-empty Scion slug
or UUID, never a filesystem path; the other four are absolute directories inside
`workspace_root`, where `desk_root` contains `desk/`, `source_root` contains the
`deskops` package and `sldb_root` is sldb's `src` directory. Missing, unknown,
relative, out-of-workspace or invalid values are refused before any template is
written. A valid context emits `DESKOPS_DESK_ROOT`, `DESKOPS_SOURCE_ROOT`,
`DESKOPS_SLDB_SOURCE_ROOT`, `DESKOPS_WORKSPACE_ROOT`, `DESKOPS_SCION_PROJECT`
and `PYTHONPATH=source_root:sldb_root`, plus a volume whose source and target are
`workspace_root`. It carries no secrets. Omitting the flag preserves CLI, path
and environment compatibility; the corrected prompt text is intentionally not
byte-identical to the faulty earlier wording.

The coordinator derives a stable child identity from the task contract:
`deskops-e-<12hex>` for an executor or `deskops-t-<12hex>` for a tester, where
the hex is SHA-256 of `task_id + NUL + contract_sha256 + NUL + role`.
`contract_sha256` is the SLDB `TaskDoc.__contract__` digest. Attempt 1 uses the
base name, attempt 2 appends `-a2`, and there is no attempt 3; labels are
`deskops.task_id`, `deskops.contract_sha256`, `deskops.role` and
`deskops.attempt`. The runtime helper `scion_child_identity(task_path, role,
attempt)` returns that name and label set, and `scion_start_argv` builds the
explicit native start argv. These helpers only derive identity/argv; native
Scion orchestration remains Scion, not a DeskOps scheduler.

Native labels must be printable ASCII and at most 63 characters. The helper
preserves the full canonical task id and 64-hex contract hash in its returned
identity and name derivation; `deskops.contract_sha256` carries the 63-hex prefix.
A long or non-ASCII task-id label uses a bounded hash descriptor while TaskDoc
and RunDoc retain the full id. Copy the helper label map exactly rather than
pasting a full 64-hex digest into `--label`.

The generated coordinator reconciles its own existing executor/tester lanes and
completed handoffs before selecting new work; a restart or successful child
completion must not skip its own task or duplicate a child. It reads Scion
activity first and phase only as fallback, because the native bridge can report
`activity=completed` while `phase=running`. A dependency-ready task missing its
preflight/bundle receipt is routine work: run the cheap context review and
adjudicate factual findings before dispatch. Implementation and validation run
from the configured `desk_root`, with template artifacts and evidence under the
assigned desk `runs/` path rather than `/tmp`. Closeout runs
`deskops closeout verify`, reviews the diff, and commits only scoped
implementation/evidence/review paths with `closeout commit --paths` (never
`git add -A`). The coordinator signals `task_completed` only after all authorized
work is closed, declared evidence verified and required phase integration/commit
done; an external blocker is recorded and signalled as blocked, and only an
actual owner decision uses `ask_user`.

`runtime supervise` never answers a blocked agent's prompt and never advances a
task on a done settle. A human or supervisor decides what happens next.

## Cold context reviews

`deskops review` runs the cheap isolated reviewer from
`desk/rituals/context-review.md` and writes the receipts (`ReviewDoc`) under
`desk/reviews/`. The default engine is the `runtime-pi-deepseek-flash` profile
seeded under `desk/runtimes/` by `deskops init` and `deskops desk update --apply`;
`--engine` picks any other `RuntimeProfileDoc` under `desk/runtimes/`. Every run
also writes ritual evidence under
`runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/`.

The reviewer is an external model process, so these examples are illustrative
only; they are not part of the runnable walkthrough.

```bash
deskops review preflight task-fix-thing --root .
deskops review bundle task-fix-thing --root .
deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
deskops review status task-fix-thing --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

An unchanged input is not reviewed again; a second run does not call the model.
`review status` compares the SHA-256 of the exact current builder input bytes
with all receipts for the key. No receipts means `missing`; receipts with no
matching input mean `stale`, regardless of their old verdict. Among matching
receipts, priority is `accepted`, `rejected`, `pending` (reported as `reviewed`),
then `incomplete` (reported as `technical_failure`). A current accepted
receipt therefore survives later rejected or failed attempts. Task subjects
use the same task id whether plain or pinned with a SHA-256 anchor. Status
preserves receipts and run evidence and does not change lifecycle gates.
See [the source atom](../desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md).

`--max-attempts` (default 2) caps the good
attempts per key; `--force --reason` is the only way to re-review a key whose
input already has a good attempt. A transport failure (non-zero exit, timeout,
or output without `REFORMULACION`) is recorded with `technical_ok: false` and a
`verdict: incomplete` / `reason: technical` receipt, kept separate from
comprehension findings.

Reproduction, goldens and owner receipts are not produced by a model: whoever
operates the desk records them with the evidence they checked, and disposes of
them like any other receipt.

```bash
deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
```

`record` writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor`
from the desk identity, and the evidence paths in `summary`. Each `--evidence` is
an existing file inside the root; anything else fails with
`Error: evidence not found: <path>` (exit 1) and writes nothing. `reproduction`
and `goldens` need at least one `--evidence`; `owner` may carry only `--reason`.
`input_sha256` is the SHA-256 of `<path>\n<content>\n` for each evidence file,
paths relative to the root, sorted and without repeats (empty without evidence).
`--kind` accepts `reproduction`, `goldens`, `owner`, `preflight` and `bundle`;
`node` comes from its own command. `deskops review dispose <review-id>` writes
the verdict.

A desk with no model to run the reviewer (the CI scenarios, the quickstart) can
still activate a task: whoever operates it records the `preflight` and `bundle`
receipts by hand. `--operator <name>` is required for those two kinds; without
it the command fails and writes nothing. The receipt keeps `engine: human`,
names the operator as its `actor`, and says `no model available` in its title
and `summary`, so nobody mistakes it for a model review. It is not a stand-in
for `deskops review preflight|bundle` on a desk where the model runs.

```bash
deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .
deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
```

## Verb coverage

This table maps every CLI verb to the section that documents it.

| Verb | Section |
|---|---|
| `about` | Orient yourself |
| `doctor`, `status` | Check desk health |
| `faq` | Orient yourself |
| `bootstrap` | Help and bootstrap |
| `init` | Initialize the repository |
| `inbox` | Inbox, messages, and drawer |
| `message send/list/read/ack` | Send, list, read, and acknowledge messages |
| `promote inbox-to-drawer-task` | Promote an inbox note to a drawer candidate |
| `drawer remove` | Remove a drawer entry |
| `retire` | Retire any other desk document |
| `issue close/list` | Issues |
| `add task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Add artifacts |
| `edit ...` | Edit artifacts |
| `bind pill` | Bind reusable context pills |
| `next`, `next --why`, `next --diagram` | Inspect the lifecycle graph; Inspect, edit, and advance a task |
| `list tasks/pills/rituals/boards/atoms/materializations/repositories/inbox-notes/faq-docs/steps` | List artifacts |
| `show task/pill/ritual/board/atom/materialization/repository/inbox-note/faq-doc/step` | Show artifacts |
| `advance task` | Inspect, edit, and advance a task |
| `repo register/whoami/remove` | Repository identity and the ecosystem registry |
| `desk install/migrate/update` | Desk scaffold, migration, and repair |
| `desk replace` | Replace text in an unmodeled desk file |
| `atoms add-namespace/list/reorganize/show/validate/create/delete/split/merge/crossroad/proto/type/tree` | Atoms |
| `graph build/neighbors/missing/reflect` | Graph |
| `materialize` | Roles, materialization, and drift |
| `drift check` | Roles, materialization, and drift |
| `closeout verify/commit` | Closeout |
| `closeout supersede/retire` | Supersede or retire a task |
| `closeout resolved-by` | Close a task whose work already entered the history |
| `runtime init/status/attach/stop/workers/supervise/template` | Runtime and Herdr |
| `review node/preflight/bundle/status/dispose/record` | Cold context reviews |

FILE:CHANGELOG.md
# Changelog

All notable changes to deskops are recorded here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Entries cover the unreleased changes since tag `v-stable-2026.08.29`.

## [Unreleased]

### Added

- Closeout rules (CC33b): the closeout gate of each factory task type is a `RuleDoc` seed, `deskops/data/rules/rule-closeout-task-<type>.md`, written as a managed seed to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`, glob `rule-closeout-*.md`; a second `--apply` changes nothing). Each is `on_transition`, `severity: error`, `where current_node = "ritual-closeout"` (the source of `task_completes`), subject `model <= <TypeDoc>`, and asks for the evidence receipts of CC33a, accepted and intact: `any(^subject: kind = "evidence" and fact = "<kind>" and anchor_state = "intact" and verdict = "accepted")` per kind, `atom|materialization` as an `or` of two. `task.refactor` adds the `goldens` review receipt (`deskops review record --kind goldens`) to the `task.code` rule its family gets; `task.aggregate` asks only for `commit` (no `children` field yet). The kinds per type are data, `deskops/data/rules/closeout-evidence.yaml`, which `deskops closeout verify` and `deskops add task` read (a desk subtype reads its nearest factory ancestor's entry); `tests/test_closeout_rules.py` checks the rules against it. Two `on_write` alert rules cover task fields: `rule-closeout-alert-implicit-code` and `rule-closeout-alert-pill-graduation`.
- Evidence receipts (CC33a): `deskops closeout verify` runs the closeout fact producers it already ran and writes, for each kind the task declares (its `closeout_evidence`, or its type's `__closeout_evidence__`), one `ReviewDoc` kind `evidence` under `desk/reviews/<task>/evidence-<fact>-<n>.md` (`review-<task>-evidence-<fact>-<n>`, engine `deskops-closeout`). `ReviewDoc` gains `kind: evidence` and two optional fields, `fact` (`tests`, `commit`, `atom`, `materialization`, `document`, `external`) and `value`; the model requires `fact` on kind `evidence` and refuses `fact`/`value` on every other kind, and receipts written before keep reading with both empty. The verdict is `accepted` (reason `verified: <fact> <value>`) when the kind's producer found evidence (`reference_points_to_test`, `reference_points_to_commit`, the link gate, `reference_points_to_document`, `reference_points_to_url`) and `rejected` with the gate's finding message otherwise. `value` is what passed, sorted, paths POSIX-relative to the root, joined by newlines: the test references, the full commit ids, the linking atom or materialization ids (an `atom` receipt for atom links and a `materialization` receipt for materialization links), the document paths, the URLs. `input_sha256` is the SHA-256 of `<fact>\n<value>\n` followed by `<path>\n<sha256 of its bytes>\n` per file of `value`. Each receipt is created and saved again unchanged in the same transaction, so its `subject` is pinned (`doc:<Model>:<task>@sha256:...`). A repeated verify writes nothing while a receipt of the same fact has the same `input_sha256` and an intact anchor; after the task's contract changes (the receipt is `changed`) it writes a new one (`n+1`) and leaves the old one. The JSON and text verify print are unchanged; a desk without a store gets no receipts, and the board view and `closeout commit` (which run the same verification) write none. The closing gate does not read the receipts yet (CC33b) (`tests/test_closeout_evidence_receipts.py`).
- Scion autonomy contract (task-scion-autonomy-coordinator-contract): runtime templates add independent `--mode tester`, strict `--context-file` and separate task-data `--task-root`. Coordinators reconcile their own children and Scion activity before selecting work, prepare missing reviews, require independent passing tests, and verify scoped closeout before continuing through phases. Child identities use the full canonical SLDB contract; native label descriptors fit Scion ASCII/63-character limits. RunDocs record immutable launch intent, and the supervisor may mutate modeled workflow through CLIs while implementation stays with executors.
- `deskops review record --kind preflight|bundle --operator <name>` (main en verde, decisión B del coordinador de proyecto con las condiciones del overlord): a desk without a model (CI scenarios, the quickstart) records those receipts by hand. `--operator` is required for both kinds (without it nothing is written); the receipt keeps `engine: human`, names the operator as `actor` and says `no model available` in its title and summary. Real desk tasks still get them from `deskops review preflight|bundle`.
- The activation gate of each factory task type is a `RuleDoc` seed of the desk (CC32, sldb GO06/GO08): `deskops/data/rules/rule-activation-<type>.md`, one per type (`task.code`, `task.docs`, `task.debug`, `task.refactor`, `task.decision`, `task.aggregate`, `task.external`), written as managed seeds to `desk/lifecycle/` and tracked as `RuleDoc` by `deskops init` and `deskops desk update --apply` (declared in `deskops/data/desk_declaration.yaml`; `lifecycle.ensure_rule_model` registers sldb's `RuleDoc` in the store; a second `--apply` changes nothing). Each rule is `on_transition` over `ritual-execution` with subject `model <= <TypeDoc>`, so a desk subtype inherits it and a desk `RuleDoc` can add a clause; it requires the receipts the type asks for (`any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "<kind>")`) and `all(depends_on: status = "closed")`; `task.refactor` only adds `goldens` to the `task.code` rule its family already gets, `task.aggregate` only needs its dependencies closed. `deskops advance` passes the task as the `document` of `sldb.api.edges_holding`; when an error finding holds the edge back, the message lists the findings of `sldb.api.edges_blocked` (`error: [rules/<rule>] <Model>:<task>: <message> | <clause> (seen: ...) (witness: ...)`) instead of the edge conditions (exit 1 as before; a gate held back by its own condition keeps `Gate <node> is not complete (...)`). `deskops show task` prints them under each lifecycle gate (`blocked by:`, `findings` in JSON) and `deskops next` under `Blocked by:`. `docs/workflow-policy-reference.md` carries the table of rules per type.
- Task types as models with a hierarchy (`deskops/models/task_types.py`): `TaskCodeDoc` (`task.code`), `TaskDocsDoc` (`task.docs`), `TaskDebugDoc` (`task.debug`), `TaskRefactorDoc` (`task.refactor`, extends `TaskCodeDoc`), `TaskDecisionDoc` (`task.decision`), `TaskAggregateDoc` (`task.aggregate`) and `TaskExternalDoc` (`task.external`). Each fixes `task_type` with a `Literal` default and declares `__closeout_evidence__` and `__activation_receipts__`; `TaskDoc` declares `__contract__`.
- `deskops add task --task-type` accepts only registered types (and lists them on an unknown name); without `--task-type` the type defaults to `task.code` with an envelope note. Tasks are stored under their type model, so `model <= TaskCodeDoc` names the family.
- A desk can add its own subtypes in `desk/models/*.py` (DC7); `deskops desk update --apply` registers them and migrates legacy `task_type` strings onto their canonical type (idempotent, with a per-task report).
- `ReviewDoc` (`deskops/models/review.py`): a review receipt for preflight, bundle, reproduction, goldens, or owner checks. `kind` and `verdict` are closed vocabularies; `subject` holds a `doc:<Model>:<id>` anchor (or `subject_ref` names a plan node), and `verdict: accepted|rejected` requires a reason and `disposed_by`. The model declares `subject` in `__doc_anchors__` and leaves `__references__` alone until sldb GO07 (`G_SLDB_ANCHORS`).
- `deskops init` and `deskops desk update` create `desk/reviews/`. The `review` subject is registered for `deskops edit review`, which refuses `verdict`, `reason`, `disposed_at`, and `disposed_by`: the verdict is written by `deskops review dispose` (GC03), and a new review is a new document.
- `deskops review` replaces the two governed `context_review.py` scripts with a CLI command (`node`, `preflight`, `bundle`, `status`, `dispose`). Each run writes the ritual evidence under `runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/` and a `ReviewDoc` receipt; the default engine is the `runtime-pi-deepseek-flash` profile seeded idempotently under `desk/runtimes/` (`RuntimeProfileDoc` gains an optional `system_prompt`). `--max-attempts` (default 2) caps good attempts per key, `--force --reason` re-reviews an unchanged input, and transport failures leave `technical_ok: false` with `verdict: incomplete` / `reason: technical`.
- `deskops review record <task> --kind {reproduction,goldens,owner} --evidence <path>... --reason "..."` records the receipts a model does not produce (follow-up of CC32). It writes a `ReviewDoc` with `verdict: pending`, `engine: human`, `actor` from the desk identity, the task anchor as `subject` (pinned on write like the other receipts), and the evidence paths in `summary`; `input_sha256` is the SHA-256 of `<path>\n<content>\n` over the evidence files, paths relative to the root, sorted and without repeats. Evidence that does not exist or leaves the root fails with `Error: evidence not found: <path>` (exit 1) and writes nothing; `reproduction` and `goldens` require at least one `--evidence`, `owner` may have none, and `--kind` refuses `preflight`, `bundle` and `node`. `deskops review dispose` writes the verdict, as for the other receipts (`tests/test_review_record.py`).
- `deskops closeout resolved-by --task <id> --reason "..." --ref <commit> [--ref <commit|URL>...] --test <test> [--test ...] [--paths ...] [--message ...]` closes a task whose work already entered the history (for example through a PR) before its closeout (`ClosureService.close_resolved_by`). It does not ask for an atom per changed file: at least one `--ref` must be a commit that is HEAD or an ancestor of the `--root` repository, the other refs may be ancestor commits or http(s) URLs, and at least one `--test` is required, each one accepted by the tests gate for the task's `files`. Any ref or test that does not resolve, or a blank reason, is refused with exit 1 and writes nothing. It makes one closing commit with `Task-Id`, `Closeout-Mode: resolved-by`, `Closeout-Reason`, one `Closeout-Ref` per ref and one `Closeout-Test` per test, marks the task `resolved` with `resolved-by` in its history, takes it off the Board and records the index entry with `mode: resolved-by` (`tests/test_closeout_resolved_by.py`).
- `deskops closeout resolved-by` accepts references qualified by a registered repository (inbox a79fe2d6, AntonIA): `--ref <repo-id>:<sha>` and `--test <repo-id>:<test path>` close a task whose code entered another repository. The reference is cut at its first `:`; when the prefix is the id of a repository in the desk's own registry (`desk/registry/repo-*.md`, `deskops repo register`), the value is checked in that repository's registered root with the local rules (a lowercase commit id that is its HEAD or an ancestor; an existing `.py` under one of its `tests/` directories, `::node` allowed), and the task's `files` do not widen the other repository's tests (`RepositoryReferences` in `deskops/services/closeout_gates.py`). A prefix that is not registered keeps the whole reference local, as before; a prefix naming the desk itself (its `project_identity` or a registered root equal to the desk's root) is local; a URL stays a URL. A registered root missing on this machine refuses with `Registered repository <id> is not at <path> on this machine.` (exit 1, nothing written), and a registry that cannot be read refuses with `Could not read the repository registry: ...`; the registry is read only when a reference has a `:` and is not a URL. The closing commit and its trailers are the same; `Closeout-Ref` and `Closeout-Test` keep each reference as written. `closeout verify`, `commit` and `supersede` are unchanged (`tests/test_closeout_resolved_by_xrepo.py`).

### Changed

- Tag namespaces and the domain tree are checked by sldb (CC35d resto, sldb GD27 for deskops): the desk's store declares the namespaces of `desk/atoms/tag-namespaces.yaml` in `.sldb/store.yaml` (`tag_namespaces`, `domain` with `anchored_by: {model: CrossroadDoc, field: path, value: bare}`, `tag_models: [AtomDoc, ProtoAtomDoc]`), written by `deskops init`, `deskops desk update --apply` (new divergence line `- Tag namespace declaration: .sldb/store.yaml differs from desk/atoms/tag-namespaces.yaml` and apply line `Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.`) and `deskops atoms add-namespace`; the file wins and a second run changes nothing (`deskops.atom_tags.sync_tag_declaration`). `require_domain_parents`, `_domain_errors`, `missing_parents` and `validate_atom_tag_namespaces` are gone: `deskops atoms validate` prints sldb's `tag_check` findings with the same texts (only for documents the store tracks), and creating an atom, protoatom or crossroad keeps refusing a missing parent (`Write the parent first: ...`) or an undeclared namespace with the same message and exit 1, from sldb's data (`tag_namespaces`, `tag_tree`, `TagNamespace.required`) as a bridge until sldb H4 (`create_document`/`track` evaluating `on_write`). A desk without a store, or whose store declares no namespaces, checks neither. The atom folder is sldb's `tag_folder`, and the atom model refuses a tag value with an empty segment (`a..b`, `a.`, `.a`) in its validator, so the model contract is unchanged (`tests/test_domain_tree.py`, `tests/test_atom_tags.py`).
- `deskops view board|task` from sldb ViewDocs (CC34): the views are the seed ViewDocs `deskops/data/views/board.md` and `task.md` (only in the package, DA4), tracked as `ViewDoc` in the deskops repo's own store (`.sldb/store.yaml`, written with `sldb stores declare --write`), evaluated by `sldb.api.run_view` and projected to the unchanged contract of `docs/deskops-ui.md` by `deskops.cli.commands.view.project`, a public function graph_ui calls in process on what `GET /views/<view>` of `sldb serve` returns. The task view's `revision` is now the ETag of the view (GD25): it moves whenever the task, the Board, a pill or an atom the view read changes; the key and its optimistic guard are the same. What the ViewDoc model does not express yet is added by the CLI from the read operations that already existed (gates from `show_task`, closeout from a read-only `verify_task_closeout`, `next` and the columns' phase from the lifecycle spec, inherited fields from `resolve_task_payload`; sldb hypotheses H1-H8), and drawer and inbox still read the desk's files (H10: those folders are not tracked in a desk's store). The agents view moved to `deskops/runtime/desk_agents.py`. `deskops/services/desk_view.py` (`DeskView`, `task_revision`, `note_revision`) and the private aliases `_read_doc`, `_resolve_glob`, `_registered_repositories` and `_repository_root` of `DeskopsOperations` are gone; an error that stops a view is the envelope type `ViewError` (was `DeskViewError`). Until sldb resolves a ViewDoc of a linked store (H9), `deskops view board|task` works only on a desk whose own store tracks the ViewDocs (the deskops repo); elsewhere it exits 1 with `Unknown view: <view>`. JSON goldens of the four views are in `tests/fixtures/golden/output/view_*.json` (`tests/test_view_goldens.py`, `tests/test_view.py`).
- Incoming references (CC35c, sldb GD22): `deskops atoms delete`, `split` and `merge`, `deskops retire`, `deskops drawer remove` and the closeouts that delete a task now find references to a document with sldb. They use `resolve_target` and `find_hits` of `sldb.api.edges.referrers` with the desk graph built in process (`deskops/services/references.py`, DO8). Fields come from the store's edge index, and prose mentions from the graph's `MentionPattern` rules. Merge rewrites through `rewrite_references` (fields), and through `rewritten_line` plus `replace_text` (mentions), inside the merge's `desk_transaction`. Retire removes the retired document from the declared fields that name it, such as the Board's `pills` and every task's `pills`, inside the transaction that deletes it, so a failure leaves every file as it was. A mention in prose still refuses retire unless `--force` is given. `drawer remove` and closeout do not rewrite: each file that still names the deleted document is reported on stderr as `alert: <document> still referenced by <file>`, and the exit code does not change. The desk graph gains two patterns. `ATOM_ID` (`atom:atom-<slug>` as a whole token) is read in Related Atoms sections and on every line of tasks and issues. `DRAWER_BULLET` (`` - `tasks/<id>.md` `` or `` - `<id>` ``) is read on the drawer Board. The old searches are gone: `_find_inbound_atom_references`, `_rewrite_inbound_atom_references` and retire's `_inbound_references`. Files that are neither tracked documents nor desk graph nodes have no referrers, so retire no longer refuses a file such as a `desk/logbook/` note because a doc names its path. A desk without a store has no field references, so retire leaves its Board untouched (`tests/test_atoms_merge.py`, `tests/test_retire_cli.py`, `tests/test_inbox_promote_cli_gaps.py`).
- `deskops desk replace` writes through `sldb.api.replace_text` (CC35d a4, GD27) inside the desk transaction (`doc_access.desk_transaction`), instead of writing the bytes and untracking and re-tracking the document itself. deskops keeps which files the verb reaches (modeled subjects are still pointed at `deskops edit`) and the count guard with its message (`Refusing to replace in <path>: found N occurrence(s) of --old, expected M. The file is unchanged.`), checked before sldb is called. A plain file (a drawer note, an issue body, `tag-namespaces.yaml`) is rewritten as before. A store-tracked file (a role prompt) is now validated under its model and the store's `on_write` rules before it is rewritten and tracked again, and a replacement that breaks it is refused with `Refusing to replace in <path>: <sldb error> The file is unchanged.` (exit 1), the transaction rolled back. A desk without a store still writes the file directly. (`tests/test_desk_replace.py`).
- `deskops closeout commit` writes no receipt and no longer gates on verify's result: it evaluates the task type's closeout rule on the receipts `deskops closeout verify` wrote (task read at `ritual-closeout`). A blocked commit prints `Closeout gate blocked <task>; the closing commit was not made.`, the declared/found line and alerts of a read-only verify, one `- error: [rules/rule-closeout-<type>] ...` line per finding and `Run 'deskops closeout verify --task <task>' ...`; a task the store does not track cannot be evaluated and is blocked with that reason. The `task_completes` edge condition is `status = "ready_for_testing"` (the `has(closeout_evidence_verified)` fact is gone), so `deskops show task`, `next` and `advance` show the rule's findings on that gate. Editing a contract field after verify leaves the receipts `changed` and blocks again.
- `deskops closeout verify`: the task's `closeout_evidence` only adds kinds to its type's (DA5): an added kind is verified and gets its receipt, and a failure is the alert `added_closeout_evidence_not_verified` instead of a blocking finding; an added kind outside the vocabulary is the alert `unknown_closeout_evidence`. `goldens` is read by the rule from the review receipt, not produced by verify, and `children` is no longer declared, so `closeout_evidence_not_verifiable` is gone. When the atom|materialization gate passes without a linking document (exempt desk, follow-up only, skill guard test) verify writes an accepted `atom` receipt with `value: exempt: <why>` (b3). The `closeout_evidence_not_declared` alert moved to the `rule-closeout-alert-implicit-code` rule.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. Es una decisión revisable hasta que CC33c pase `graph` a `sldb graph project` (GD21). Tests en `tests/test_graph_missing_existing_files.py`.
- `deskops graph neighbors|missing|reflect` and `deskops drift check` read sldb's project graph of the desk (CC33c, GD21: `sldb.api.edges.project_graph.ProjectGraph` with the configuration of `deskops/graph/desk_graph.py`) instead of a snapshot deskops built and read back. Without `--graph`, `graph neighbors` and `graph reflect` no longer need a prior `graph build` and no longer read `.sldb/runtime/graphs/deskops.kg.json` or the legacy `.sldb/runtime/knowledge_graph.kg.json`; `drift check` reads the graph's edges and its dangling edge targets whether or not a snapshot was built. `--graph <path>` still reads that graph file (`deskops/graph/view.py`, `read_graph_file`). `deskops graph build` still writes the KGDB GraphSnapshot and its NetworkX sibling, unchanged, from the same graph (`deskops/graph/export.py`). `deskops/graph/snapshot.py` is gone (its runtime-path fallback and `read_graph_neighbors` with it), and the atom-reference check of `drift check` reads the frontmatter of the project graph's documents under `desk/` and `docs/` instead of an `rglob` (`grep rglob deskops/graph/` is empty). `graph neighbors` and `graph missing` were compared with the frozen v1 extractors over a copy of the real desk (619 nodes, 296 edges, the same `(source, target, role)` sets and the same missing findings), and `tests/graph_oracle_v1/` was then removed; `tests/closeout_graph_oracle.py` keeps only the lifecycle-transitions oracle.
- `deskops graph missing` no reporta un target declarado que existe como archivo dentro del repo aunque el grafo de proyecto no tenga nodo para él (un `.yaml` del drawer, un fixture `.json`). Un target inexistente, un átomo o una ruta que sale del root siguen siendo missing. CC33c lo decidió (a4): el grafo de proyecto de sldb sigue sin nodo para `desk/drawer/plans/deskops-como-config/dag.yaml` ni para `tests/fixtures/model_contract_hashes.json`, así que la excepción queda. Tests en `tests/test_graph_missing_existing_files.py`.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or `deferred`, what a drawer task holds, when `current_node` is empty); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- A task's lifecycle is a validator of `TaskDoc` (CC37, DK6/DA6), so no write leaves it outside the rules: `status`, `current_node` and `history` must form a state the lifecycle can produce, or the model refuses the payload with `Task <id> lifecycle is inconsistent: <field>: '<value>' ...; expected '<value>'`. Coherent states (`deskops/models/task_lifecycle.py`): the entry state (empty `history`, `current_node` the entry node `ritual-execution` or empty, `status` in `ENTRY_STATUSES` = `{draft}`, or, when `current_node` is empty (a task outside the lifecycle), `deferred` (a drawer task) or `resolved`/`closed`/`done`/`complete` (a task resolved before the lifecycle, what `closeout retire` removes)); the state after a transition (the last `history` item is the `relation_type` of an edge, and `current_node`/`status` are that edge's target and `sets.status`, read from the package's `RelationDoc` seeds in `deskops/data/lifecycle/`, a `terminal` edge leading to `complete`); and the closeout records `CLOSEOUT_STATES` (`closed` after `task_completes` at `complete`, `superseded` after `superseded`, `resolved` after `resolved-by`, the last two from any node). `task_type` keeps matching the model through each typed model's `Literal`; `TaskDoc` itself still accepts any `task_type`. Because sldb builds the model on every write, `sldb fields update`, `sldb docs update` and `sldb serve`'s `/save` reject an inconsistent task with that message (`tests/test_task_lifecycle_validator.py`); a coherent state written without a transition is still accepted (no "transition only" field). `deskops advance` applies the edge's `sets`, the appended `history` and the new `current_node` in one `apply_effects` call, so the model validates the whole new state. `deskops desk update` reports a task whose lifecycle is inconsistent (`- Inconsistent task lifecycles (not written): N task(s)` and one `inconsistent task lifecycle in <path>, not written: <errors>` line each) and `--apply` leaves it as it is instead of migrating its `task_type`. `deskops add task` with a JSON payload carrying a non-entry `status` is now refused by the model.
- Selectors of tracked desk documents resolve through `sldb.api.select_documents` (CC35b, GD23). `doc_access.resolve_document` asks the store twice, in order: by name (`prefix`, where an exact name wins over the one prefix match) under the directory's pattern, then, only if that found nothing, by file name (`path_glob` of `<selector>*.md`), so a ritual tracked as `ritual-execution` in `desk/rituals/execution.md` resolves as `ritual-execution` and as `execution`; an ambiguous query stops there. `resolve_glob`, `resolve_artifact_selector[_multi]`, `resolve_ritual_selector`, `registered_repositories` and the task and pill lookups of `deskops review` use it; the messages are the same (`No <what> file found for selector '<s>'`, `Ambiguous <what> selector '<s>': <paths relative to desk/>`), the ambiguity candidates being the rows sldb names. Gone: `_tracked_task_paths` (which read `.sldb/core/documents/` directly) and the frontmatter-id fallbacks of reviews and rituals (`frontmatter_id`): a legacy task resolves by the `TaskDoc` model family, a review and a ritual by the name the store tracks them by. A file on a tracked surface that the store does not track no longer resolves. The drawer and `desk/issues`, which the store does not track, and a desk without a store keep the disk rule of `desk_paths.resolve_selector` (marked `CC35b-a3`); the `operations.py` aliases graph_ui calls are marked `CC34`. `resolve_artifact_selector_multi` tries its directories in order (an active pill before a drawer pill of the same selector) instead of one candidate set across them. The desk declaration's `include` now names the seeded Board (`desk/tasks/Board.md` as `BoardDoc:Board`) and phase ritual (`desk/rituals/phase.md` as `RitualDoc:ritual-phase`), so `deskops init` and `deskops desk update --apply` track them and a new desk's `deskops edit board Board` resolves (CC35b d1); the Board seed keeps `track: false`.
- The closeout tests gate (`CloseoutGatesService.reference_points_to_test`) accepts a referenced `.py` file under any directory named `tests` in the repository (`tests/`, `runtime/foo/tests/`, `ops/tests/sub/`), or declared in the evaluated TaskDoc's `files`, not only under `<root>/tests/`. The evidence still comes from `references` (`files` only widens where tests may live). Still rejected: absolute paths, paths that leave the root through `..` or a symlink, missing files, suffixes other than exactly `.py`, files under a directory starting with `.` or named `site-packages` or `node_modules`, and strings that only look like evidence. Each reference is checked on its own, without walking the disk (`tests/test_closeout_test_paths.py`).
- Every write of deskops goes through `sldb.api.transaction` and `deskops/doc_io.py` is gone (CC35a, GD24). `doc_access.desk_transaction(root)` opens the desk store's transaction with the deskops package path (nested blocks join; a root without a store runs the block without one), and the services, `cli/commands/message.py`, `repo.py`, `runtime/scion.py` and `doc_access` write with `create`, `update`, `delete`, `track`, `untrack`, `write_file` and `record` of that transaction; `bootstrap.py`, `workspace.py`, `lifecycle.py` and `cli/commands/desk.py` call `add_model`, `link_store`, `inherit_model`, `init_relations`, `init_store`, `update_store_indexes`, `remove_model`, `track_document_file` and `untrack_document` directly. An update of a tracked document carries `expected_source_hash`: `read_doc` keeps the source hash the store had indexed for the document (`doc_access.index_entries`, from `store_fingerprint` and `tracked_documents`, indexes only), `update_tracked_doc` passes it, and a document the store rewrote in between is refused with `Error: <path> changed since deskops read it; nothing was written. Re-run the command.` (exit 1, no traceback), the whole transaction rolled back; a document edited by hand and not reindexed keeps its indexed hash and still takes `deskops edit`. A failure in the middle of `atoms merge` or `atoms split` (referrers rewritten, target written, source failing) leaves `desk/` and `.sldb/core/` as they were. `message send` writes the note and tracks it in the target store's transaction (a tracking failure still leaves the note delivered, with the same warning) and `message ack` is a guarded update of the tracked note; the manual restore of the note is gone. Tracked documents deskops creates or updates now carry sldb's provenance block (`sldb:` in the frontmatter), as every document sldb writes does; sldb's structural-noise refusal applies to documents deskops creates (an atom whose answer carries undeclared headings is refused on `add atom` under the store's default policy; `desk update --apply` still tracks such a file). `tests/test_transaction.py` replaces `test_doc_io.py` and `test_atoms_transactions.py`.
- `__activation_receipts__` and `task_type_activation_receipts` are gone from `deskops/models/task_types.py`: the receipts a type requires live only in its activation `RuleDoc` (CC32). `ReviewDoc`'s docstring says what sldb does with `subject` now that GO07 is in (pins it on save, computes `anchor_state` on read); the model is unchanged. The tests that activate a task write its receipts first with `tests/activation_receipts.py` (accepted and pinned through `sldb.api.transaction`).
- The desk a repository gets is data the sldb scaffold writes (CC36, DP3): the templates `deskops init` used to carry as strings in `workspace.py` (`config.json`, `pills.md`, the four lifecycle rituals, `drawer/README.md`, `atoms/tag-namespaces.yaml`) live in `deskops/data/templates/`, and `deskops/data/desk_declaration.yaml` declares the desk's `folders` (the artifact directories `ensure_workspace` created among them), its `if_missing` seeds (the Board and the `runtime-pi-deepseek-flash` profile as `document` seeds rendered by their model) and `include` rules `{model, glob}` per desk folder. `workspace.seed_desk` renders the seeds for the desk's name (`{desk_name}`, the only placeholder) and passes them in process to `sldb.api.scaffold_store`; `scaffold_desk`, `_write_if_missing`, the `*_template` functions and `guess_model_for_path` are gone, `_write_or_patch_config` only patches an existing file, and `desk update --apply` tracks desk documents through the declared includes (`sldb.api.stores.apply_declaration.apply_includes`) instead of guessing a model by path. What `init` and `desk update --apply` write is byte for byte what they wrote before (`tests/fixtures/golden/scaffold/`, `tests/test_scaffold_golden.py`); `init` now also creates `desk/materializations/`, `desk/steps/`, `desk/registry/` and `desk/faq/`.
- Document invariants are validators of their model (DK6), so sldb applies them on every write (`deskops`, `sldb fields update`, `sldb docs update`): `AtomDoc` and `ProtoAtomDoc` check the slug convention of their id, the `namespace:value` form of each tag and the domain path of each `domain:` tag, `ProtoAtomDoc` takes one `domain:` tag, `CrossroadDoc` checks its path and that its id names it, and `TaskDoc` refuses a blank title. The same checks are gone from `domain_tree.py`, `atom_tags.py`, `services/atoms.py` and `specs/compiler.py`; what needs another document or the file tree (written parents, file names, the tag namespace registry, `typed_as` targets, provenance) stays where it was. Services report the validator's own line (`deskops.models.validation`), and `atoms validate` lists it next to the other findings of the document. `atoms crossroad`, `proto` and `type` write through `doc_access` again (they called facade names CC30 removed) (CC38).
- `deskops/operations.py` is a facade: each method delegates one call to a service, to the new `deskops/doc_access.py` (document reads, writes and selector resolution, as module functions over `root`) or to `deskops.lifecycle`. Task logic lives in `services/tasks.py`, closeout verification in `services/closure.py`, and no service constructs `DeskopsOperations`. The per-artifact YAML specs (`spec/artifacts/`, `spec/fields/`, `SpecRegistry`, `specs/mermaid.py`) are gone: each model declares `__artifact__` (`id_pattern`, `status_default`, `tags`), `compile_task_spec` is the one task normalization, and `task_lifecycle.yaml` is loaded only by `lifecycle.load_lifecycle_spec`. CLI grammar and output are unchanged (CC30).
- The desk graph is configuration over sldb: `deskops/graph/desk_graph.py` declares the desk's document surfaces, file rules, reference fields, section and line mentions, and which documents are history; sldb's `ProjectGraph` (`sldb.api.edges.project_graph`, branch `wt/closeout-graph-sldb`) reads the nodes, the store's cached edge index and the declarations. `deskops/graph/extract_docs.py`, `extract_edges.py` and `extract_sources.py` are removed; `graph build`, `graph missing`, atom traces and the closeout gate read the same graph (node, edge and finding output unchanged).
- `build_closeout_graph_context` returns a `CloseoutGraph` over `ProjectGraph`: tracked documents and schema edges come from one read of the store index, and only the materializations and the documents the gate asks about are read.
- `lifecycle.transitions_from` reads the desk's own store (`include_linked=False`), not the index composed with every linked store.
- The task lifecycle is a graph with effects, declared in the desk (CC31, GO09): each `RelationDoc` under `desk/lifecycle/` carries `attributes: {sets: {status: <value>}, terminal: <bool>}` (`active`, `ready_for_testing`, `closed`; `terminal: true` on `task_completes`), and `deskops advance` takes the edge `sldb.api.edges_holding` says holds, applies its effects with `sldb.api.apply_effects` (validated against the task type's model, `TaskDoc` when the task's type is not a registered one), sets `current_node: complete` when the edge is terminal and appends the relation type to `history`; the terminal transition is still not persisted from `advance` (the closing gate is `closeout commit`). The six lifecycle documents (three `RelationTypeDoc`, three `RelationDoc`) are `managed` seeds of `deskops/data/desk_declaration.yaml` with templates in `deskops/data/lifecycle/` (`file:` seeds are now relative to `deskops/data/`): `deskops init` and `deskops desk update --apply` write them, rewrite a desk's copy that differs (`desk update` lists it as `Lifecycle documents to rewrite`, `--apply` reports `Lifecycle graph: rewrote ...`) and track them through the declared includes, together with the three lifecycle rituals by their ids; any other scaffold only creates what is missing. Gone: `Transition.sets_status`/`terminal` from the YAML, `LifecycleSpec.effect`, the `transitions` key of `task_lifecycle.yaml` (only `entry_node` and `states` remain, read by `deskops next`), `ensure_lifecycle_graph` (now `write_lifecycle_graph`), the legacy ritual migration and `deskops/lifecycle_migration.py` (no desk needs them). `deskops next --diagram` draws the desk's graph.
- `DeskopsOperations._read_doc` parses a document once per text for the whole process, so a reader that builds a new `DeskView` per request (graph_ui's `serve.py`) does not re-parse unchanged documents.
- `deskops view board` on the deskops desk: ~30 s cold / ~11 s warm before, ~1.7 s cold / ~0.4 s warm after (new `DeskView` per call). `tests/test_closeout_gates.py` compares the new path with the old extractors, frozen in `tests/graph_oracle_v1/`.
- `deskops advance task --to` is removed (breaking): a task moves only through a lifecycle transition whose condition holds, and a blocked task stays where it is with the gate named. Close with `deskops closeout commit` (or `closeout supersede`/`closeout retire`), never by forcing a node.
- `edit task` refuses `status`, `current_node`, `history`, `task_type` and `closeout_evidence` with exit 1 and names the command that writes each field. Ordinary fields such as `goal` stay editable. `force`-style flags that skip a gate are not offered (D2).
- Closeout evidence is read from the task's type, not written into the task (`TASK_TYPE_EVIDENCE` and `evidence_for_task_type` are gone). `--evidence` is a floor: it can only add kinds to the type's, never remove one. A task's own non-empty `closeout_evidence` still overrides the type.
- `closeout verify` names `children` and `goldens` (declared by `task.aggregate` and `task.refactor`) as not yet verifiable.
- `tests/fixtures/model_contract_hashes.json` records the new `RelationDoc` contract from sldb GO09 (`attributes.sets`/`terminal`; sldb 33b3c7a0, closeout d39bf915); the deskops store was migrated with `sldb stores update` in 09b5075c. The other desks are migrated by their own repos.
- `docs/operator-manual.md`: the merge/delete/validate example no longer shows `atoms split`, because sldb refuses headings inside a field since CC35a; the split question is in the drawer (revisable decision).

### Fixed

- `deskops edit <subject> <selector> <field> <value>` no longer stores the template's placeholder paragraph as content (task.debug, drawer 8d9c8f8c). A value that carried it, such as the raw text of the section plus a new paragraph, was rendered after the template's own anchor and read back as content, one more copy per edit (CC33c, 4305c7d9: from one to three). `doc_access.edit_artifact_field` now passes text fields through `strip_template_placeholders`, which drops top-level paragraphs that are exactly the field's placeholder; `template_placeholders(model)` reads them from the model's template (the literal italic paragraph that sldb's extract anchors on before the field), for every subject of `edit`. A value that is only the placeholder empties the field; the phrase inside a longer paragraph, a quote, a list or a code block stays, and list fields are not touched. `promote inbox-to-drawer-task` reads the TaskDoc placeholders from the same source instead of its own list (`_TASK_SECTION_PLACEHOLDERS`, which matched the template) (`tests/test_edit_template_placeholder.py`).

- `deskops closeout resolved-by` closes a task its model rejects (for example a `draft` after `task_activates, task_hands_to_closeout`, as the two drafts of shared_llm-gateway), which used to exit 1 with `Validation error: ... lifecycle is inconsistent`. Like `closeout supersede`, it reads the task from its frontmatter when the model rejects it, applies the same `--ref` and `--test` gates (the tests gate uses the frontmatter's `files`), writes `status: resolved` and appends `resolved-by` to the history with `workspace.rewrite_task_fields` (validated with `TaskDoc`, restored if it fails), and makes the same closing commit with the same trailers as for a valid task. Supersede and resolved-by share that path (`ClosureService._read_closing_task` and `_record_closing_status`). With a store, it refuses before writing anything while another task is invalid, as supersede and retire do; the refusal of the three now names sldb H2 (note 3895e9f7: sldb re-extracts the whole model on every write) and the manual route (decide the other task by hand, or close it with supersede or retire once it is the only invalid one) (`tests/test_closeout_resolved_by.py`, `tests/test_legacy_task_states.py`).
- `deskops desk update --apply` migrates a task with a non-terminal status and an empty history (`active`, `ready_for_testing`, `blocked`..., left by desks migrated before CC31) instead of listing it as not migratable and skipping every other repair (task.debug of non-terminal tasks, decision of the overlord, 2026-11-11). `legacy_state_migration` had no row for it and returned `None`. It now gives `status draft` and, when `current_node` is set and is not the entry node, the entry node `ritual-execution` (an empty node stays empty); a status is terminal when it is `superseded`, a `CLOSEOUT_STATES` key, a `LEGACY_RESOLVED_STATUSES` or a `DRAWER_STATUSES` status. The task's `summary` gets the line `Migrada a draft por deskops desk update: estado heredado '<status>' sin history (<YYYY-MM-DD UTC>).` in front of its previous text, on one line. The report prints `<file>: status <before> -> draft` and `<file>: current_node <before> -> ritual-execution` when the node moves; a second run changes nothing, and doctor points the task to `deskops desk update --apply`. A non-empty history with an incoherent status still waits for its owner (`tests/test_legacy_task_states.py`, golden `desk_update_nonterminal_migration.text`).

- Tasks left by desks migrated before CC31 with a terminal or drawer status, an empty history and `current_node: ritual-execution` (shared_llm-gateway, the Chatbot_Infra kit, Governance, labchile) no longer break the desk (task.debug of legacy states). `deskops desk update` migrates them by a table (`superseded`: `history [superseded]`; `closed`, `resolved`, `done`, `complete`, `cancelled`, `deferred`, `candidate`: `current_node ''`), dry-run by default and written with `--apply` before the models are registered, one `<file>: <field> <before> -> <after>` line per field; the write goes to the frontmatter and is validated with `TaskDoc`, and a second run changes nothing. Any other task the model rejects is reported with the validator's text and a fixed suggestion, never written, and `--apply` exits 1 while one remains. `desk update` no longer raises when `sldb stores check` cannot read the store because of an invalid task (sldb stops at the first invalid document): it reports it and skips every repair but the migration (the scaffold re-tracks the lifecycle graph too); a store check without JSON and without an invalid task is still an environment error (exit 3). `deskops doctor` reports each invalid task as an error (file, validator text, fix) and runs every other check. `cancelled` joins `LEGACY_RESOLVED_STATUSES`. `deskops closeout retire` reads the task's frontmatter instead of the model and also retires `cancelled`, and `superseded`, `deferred` or `candidate` with an empty history (and `superseded` with only `history [superseded]`, what the migration leaves); with a store, it refuses while another task is invalid (sldb rebuilds every task when one is untracked). `deskops closeout supersede` closes a task its model rejects (for example a `draft` after `task_hands_to_closeout`) by reading and writing its frontmatter, with the same commit and trailers and the same wait. The suggestion for an undecided task uses the real grammar (`deskops closeout supersede --task <id> --reason ... --ref ...`, `deskops closeout resolved-by --task <id> --reason ... --ref <commit> --test <file>`). Its help changes only in that list of statuses (`tests/test_legacy_task_states.py`, `tests/test_closeout.py`, `tests/test_task_lifecycle_validator.py`).
- A desk whose lifecycle seeds predate CC31 (edges with `attributes: {}`, as the Chatbot_Infra kit has) is reported and no longer fails with a pydantic error (task.debug, nota de inbox 5106e3f8). `deskops doctor` compares the desk's managed seeds with the package by the comparison `deskops desk update --apply` makes (`seed_desk(apply=False, restore_managed=True)`) and reports each copy that differs: `lifecycle seed out of date: desk/lifecycle/<file> differs from the deskops package (<top-level frontmatter keys, without the `sldb:` write provenance>). Fix: deskops desk update --apply`, an error when a lifecycle edge's transition fields differ (`source_id`, `target_id`, `relation_type`, `condition`, `attributes`), an alert otherwise (rules, body or notes). `deskops advance` compares the edge it is about to apply with the package's lifecycle table (`lifecycle_table()`, cached): an edge with another `relation_type`, target or `attributes.sets.status` fails before any effect is applied with `Error: Cannot advance <task> via <relation_type>: the edge desk/lifecycle/<file> does not set status <expected> (attributes.sets.status is <seen|missing>). The desk's lifecycle seeds are out of date: run 'deskops desk update --apply'.` (exit 1, the task unchanged) instead of `Validation error: ... lifecycle is inconsistent` (`tests/test_lifecycle_seed_drift.py`).
- `deskops review status` preserves current accepted/rejected dispositions, selects matching exact-input receipts before applying verdict priority, and groups pinned task subjects by task id. Older receipts no longer mask a current acceptance or turn a changed input into a technical failure.

- `deskops review preflight|bundle|record|status <selector>` key and anchor the receipt on the task's full id (its frontmatter `id`), not on the selector as typed: `review preflight task-cc37` wrote `review-task-cc37-preflight-1` with subject `doc:TaskCodeDoc:task-cc37`, which no activation rule matches (main en verde).
- `deskops add ritual|board|repository|faq-doc|step|inbox-note` tracks the new document in the desk's store, as `add atom|pill|materialization` already did. Since CC35b `show`/`edit` resolve those surfaces through the store only, so a document `add` left untracked could not be shown or edited until `desk update --apply` (main en verde, fallo 4: `test_operator_manual` bloque 11).
- The wheel ships the activation rule templates (`data/rules/**/*` in the package data): CC32 added `deskops/data/rules/` to the desk declaration but not to `pyproject.toml`, so an installed deskops could not seed them (main en verde, fallo 6).
- `tests/test_cli_grammar.py` classifies the `review` noun (GC03) once, under `operational`, and fixes its `mutates` guards as the registry declares them (`review` and `review dispose` mutate, `review status` does not); the grammar test passes again.
- `tests/test_gitignore_policy.py` asserts the current `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are tracked, `.sldb_cache/` is ignored, and nothing under `.sldb/runtime/` is tracked.

### Removed

- `__closeout_evidence__` on the task type classes, the `closeout_evidence_verified` and `pill_graduation_verified` facts, `TasksService.add_closeout_facts`, `ClosureService.has_verified_task_closeout_evidence` and `has_verified_task_pill_graduation`, `task_type_closeout_evidence` and `NOT_YET_VERIFIABLE_EVIDENCE` (CC33b).

## [0.2.0] - Unreleased

### Added (rewrite plan F1–F6)

- Model contract snapshot (`tests/fixtures/model_contract_hashes.json`), CLI contract tests, and golden files for help, output, and graph.
- One selector resolution module (`deskops/desk_paths.py`) for every desk artifact lookup.
- Typed errors with fixed exit codes (1 domain, 2 usage, 3 unexpected) and `--debug` for tracebacks.
- Transactional document I/O (`deskops/doc_io.py`): a command writes all its documents and store records, or none.
- Services for drawer routing, closeout gates, tasks, atoms, and closure.
- `deskops drawer remove`, which refuses while an active task names the entry in `from_drawer` (`--force` skips the check).
- Command registry, one output renderer with a JSON error envelope, and `--root`/`--store` agreement checks.
- `scripts/migrate_desk_stores.py` to migrate every store that tracks deskops models (dry-run by default).
- CI running `pytest tests` on Python 3.13, and this changelog.

### Changed (rewrite plan F1–F6)

- `deskops closeout commit` is the only way to close a task; `advance` stops at closeout and points to it (breaking). The closure runs the full `closeout verify` gate.
- `init` links deskops models from the deskops store (federated) instead of copying them; bootstrap registers every deskops model.
- The graph reads sldb's edge index (`__reference_models__`, structuredLanguageDB >= 0.1.12) and one snapshot reader.
- TaskDoc declares its frontmatter explicitly; `pills`, `current_node`, and `atoms` are references, not containment.
- `inbox`, `status`, `atoms list`, and `atoms show` remain as deprecated aliases with a warning.
- The package runs outside an editable install: specs live in `deskops/spec/`, the FAQ ships as `deskops/data/faq.md`.
- `desk update --apply` writes the lifecycle graph.

### Removed (rewrite plan F1–F6)

- `deskops/graph/extract_coverage.py` (recovery issue points at c378d15).

### Fixed (rewrite plan F1–F6)

- Tasks written before the explicit TaskDoc frontmatter (no `tags:` key) validate again.
- Task selectors resolve tracked tasks whose file name predates `task-*`.
- Rewrites (`edit`, `advance`, `bind`) refuse instead of silently erasing headings or frontmatter keys the model does not declare.
- `edit` keeps text field values literal: multi-line text and values starting with `**` survive.
- The test suite no longer writes to the real `~/.sldb`.

### Added (desk-to-zero, 2026-10-18)

- `deskops issue close|list` closes an issue in any of the three status formats with a Resolution section (reason, refs) and keeps the file.
- `deskops closeout supersede` closes a task whose subject no longer exists (reason plus a resolvable ref); `deskops closeout retire` removes a task resolved before the ritual lifecycle (`Closeout-Mode: legacy-resolved`).
- `deskops repo remove` takes a repository out of the registry so it can be registered again under the right id.
- `deskops next --why`, and guidance from `deskops next` when the Board routes no task or several.
- `docs/operator-manual.md`, whose runnable examples the suite executes.
- Drift findings for invalid atom-reference roles, the legacy `related_atoms` field, and global policy restated inside tasks.

### Changed (desk-to-zero, 2026-10-18)

- Requires Python >=3.12 (Python 3.10 reaches end of life in October 2026; the whole suite moves to 3.12). CI runs the suite on 3.12 and 3.13. The test that kept the package importable on 3.10 and 3.11 is removed.
- Requires structuredLanguageDB>=0.1.13 (link replacement, broken-link detection, and the extraction fixes in sldb main).
- `closeout commit` folds the run index line into the closing commit; the tree stays clean.
- deskops' FAQ model is `DeskFAQDoc`; ritual steps are prose, not StepDoc references.
- `desk update --apply` archives legacy rituals RitualDoc cannot carry to `desk/drawer/rituals/legacy-*.md` and re-signs moved deskops model contracts.

### Fixed (desk-to-zero, 2026-10-18)

- `promote inbox-to-drawer-task` writes a TaskDoc; `closeout commit` accepts a directory in `--paths`; `edit` reaches drawer tasks and finds rituals by id; message delivery and ack work with desks that do not register the sender or themselves.

### Added

- Task lifecycle in the SLDB graph: rituals are states and gated relations are transitions.
- `deskops message send|list|read|ack` for cross-desk transport.
- `deskops closeout verify` with a strict all-of evidence gate.
- `deskops closeout commit --no-run --reason` to close without a subagent run.
- `deskops desk update` to reconcile a desk and its store.
- `deskops desk migrate` and `deskops doctor` findings for absent, empty, and legacy desks.
- `deskops repo whoami` and one canonical cross-repo identity resolution path.
- Verifiable cross-desk inbox delivery with a delivery result and `--ack`.
- Live Herdr agent inventory in `deskops runtime`, grouped by Herdr space.
- Supervised execution over Herdr.
- RoleDoc model, `desk/roles/` sources, and materialize/drift-check commands.
- MaterializationContractDoc model, spec, CLI surface, and reference-resolution validation.
- Atom validate and delete commands, plus split with provenance-safe rerouting and merge with reference reconciliation.
- Protoatoms, domain crossroads, and protoatom typing.
- Configurable atom folder axis by tag namespace.
- Declared graph edges derived from model containment and references.
- Per-project desk config and version contract with deterministic deep merge.
- Drift-check review loop and knowledge-surface findings.
- Graph snapshot and graph CLI commands.

### Changed

- Agent-facing inbox transport is renamed to the `message` command family (breaking).
- A drawer item becomes an active task only through `deskops add task --from-drawer`.
- Bootstrap and init drive SLDB in process instead of one subprocess per model.
- The store uses SLDB's per-document layout.
- Doctor excludes unmodeled desk surfaces from untracked findings and clarifies broken-tracking wording.
- Promotion and TaskDoc reads flatten structured source sections into task fields.

### Removed

- Direct drawer-to-active-task promotion command (breaking).
- The old `inbox` transport subcommands (breaking).
- The kgdb dependency: `graph build` validates and writes through `sldb.api.graph`; requires structuredLanguageDB >= 0.1.11.

### Fixed

- F0: the closeout commit `advance` makes contains only the closing task's paths; unrelated staged changes stay staged.
- F0: merge retargets whole tokens instead of substrings.
- F0: pytest collects only `tests/`.
- F0: ambiguous selectors are rejected instead of guessed.
- F0: the payload and flag drawer paths resolve the same way.
- F0: the graph ignores vendored trees.
- F0: closing a task amends HEAD only when HEAD's `Task-Id` trailer is that task.
- F0: doctor no longer crashes on desk-less roots.
- `graph missing` reports findings from archived records (`record: true`) as informational and exits 0 when only those remain.
- `desk update --apply` re-renders lifecycle rituals RitualDoc cannot read before tracking them.
- `closeout verify` no longer aborts on a multi-document YAML block in docs.
- `message` tracks a delivered note in the target repo's store with a relative path, and `--ack` re-signs it.
- Empty and whitespace-only selectors are rejected before any lookup.
- Graph commands import on Python 3.10/3.11 and report the real error.
- `from_drawer` is treated as provenance, not as a reference that must resolve.
- Edit keeps literal text fields and only guards deletion when the document is unreadable.
- Unreadable documents are no longer rewritten.
- Closeout commits the closure before deleting the task bundle.
- `init` scaffolds `desk/rituals/phase.md`, which the doctor requires.
- Tracked documents are written through the store, not under it.
- Repo registry supports `repo register --path`, tolerates model-entry shadowing, and reports actionable errors.
- Cross-repo identity resolution and inbox targeting precedence are unified.
- Doctor detects unregistered models and proposes a `desk update` repair.
- Optional-field and untrack paths are realigned with current SLDB.

FILE:instruccion
Cold-bundle de la tarea task-deskops-view-board-en-menos-de-2-5-s-construir-una-vez-por-corrida-lo-que-hoy-se-rehace-por-tarjeta: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- Benchmark: deskops view board, store construido, proceso nuevo, mediana de 3, 2,5 s o menos en el layout de H11; medidas antes y después en el informe
- Test: la salida de view board y de view task es idéntica a la de antes sobre el mismo desk
- Perfil antes y después que cuenta las llamadas a open_store, desk_graph y build_closeout_graph_context por corrida
- suite completa de deskops de a un archivo desde /dev/shm en verde
- 4 pasos del CI de deskops en clon limpio

