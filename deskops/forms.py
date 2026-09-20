"""The forms layer: workflow moves expressed over the pron World.

F4. The replacement for the `operations.py` CRUD: a task move is a write of one
document, reads come from `World.store` / `World.graph`, and the status a task
shows is the derived one (`deskops.derived_status`), never a field the caller
sets.

Scope of this module today: task creation, field edits and the read surfaces.
`advance`, `closeout` and the artifact/atom subjects still live in
`deskops.operations` and are repointed one subject at a time.

Materialization decision (F4, spec §TaskDoc): the task file carries its whole
task — core, intent and acceptance — inline, because one task is one file in
`desk/tasks/`. `TaskIntentDoc`/`AcceptanceDoc` stay for the separate-materialization
case.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import re
import sys

from deskops.derived_conditions import UnknownTaskError
from deskops.derived_conditions import split_ref
from deskops.derived_status import closeout_evidence_present
from deskops.derived_status import derive_status
from deskops.derived_status import is_routed
from deskops.derived_conditions import task_slice
from deskops.world import DocId
from deskops.world import World
from deskops.world import extract_model_data
from deskops.world import render_model_markdown

# Task fields the CLI may write, mapped to the model that declares them.
TASK_FIELDS = (
    "title",
    "why",
    "goal",
    "scope",
    "task_type",
    "status",
    "implementation_path",
    "validation",
    "done_when",
    "references",
    "depends_on",
    "pills",
    "files",
    "atoms",
)

# Fields a move may never rewrite: they name the document.
IMMUTABLE_FIELDS = frozenset({"id"})

LIST_FIELDS = frozenset({"validation", "references", "depends_on", "pills", "files", "atoms"})

SLUG_RE = re.compile(r"[^a-z0-9]+")

# Roots whose store was already built in this process: `bootstrap_world` costs
# seconds, and a CLI run touches the same root many times.
_READY_ROOTS: set[Path] = set()


class FormsError(RuntimeError):
    """A move that the world refuses: unknown task, unknown field, bad value."""


@dataclass(frozen=True)
class TaskView:
    """One task as read from the store: id, path, payload and derived status."""

    id: str
    path: Path
    status: str
    payload: dict[str, Any]


def slugify(text: str) -> str:
    """The id fragment a title becomes: lowercase, single dashes, no edges."""
    return SLUG_RE.sub("-", text.strip().lower()).strip("-")


def world_for(root: str | Path = ".") -> World:
    """The pron World at `root`, built from the spec the first time this process asks.

    A repo whose `.sldb` store is missing or was never bootstrapped gets the
    world F3 T3.4 declares (`bootstrap_world`), so a first `add task` on a fresh
    desk works without a separate init step.
    """
    from deskops.bootstrap import ensure_world

    return ensure_world(root)


def doc_file(root: str | Path, doc) -> Path:
    """The absolute file of a tracked document (`doc.path` is store-relative)."""
    return Path(root).resolve() / str(doc.path)


def task_path(root: str | Path, task_id: str) -> Path:
    """Where a task document lives: the drawer while no board routes it."""
    root_path = Path(root)
    routed = root_path / "desk" / "tasks" / f"{task_id}.md"
    if routed.exists():
        return routed
    return root_path / "desk" / "drawer" / "tasks" / f"{task_id}.md"


def create_task(
    root: str | Path,
    *,
    title: str,
    goal: str,
    scope: str,
    why: str = "",
    implementation_path: str = "",
    validation: list[str] | None = None,
    done_when: str = "",
    task_type: str = "",
    drawer: bool = True,
) -> TaskView:
    """Write one task document and return it as read back from the store.

    `drawer=True` (the default) is the repo rule for new unrouted work: the
    task lands in `desk/drawer/tasks/` and its derived status is `drawer` until
    a board routes it.
    """
    root_path = Path(root)
    world = world_for(root_path)
    task_id = f"task-{slugify(title)}"
    payload: dict[str, Any] = {
        "id": task_id,
        "title": title.strip(),
        "status": "draft" if drawer else "active",
        "why": why or "Not provided.",
        "goal": goal,
        "scope": scope,
        "task_type": task_type,
        "implementation_path": implementation_path,
        "validation": list(validation or []),
        "done_when": done_when or "",
        "tags": ["workspace:desk", "artifact:task"],
    }
    folder = "desk/drawer/tasks" if drawer else "desk/tasks"
    relative = Path(folder) / f"{task_id}.md"
    path = root_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    world.store.create(DocId.of("TaskDoc", task_id), payload, relative)
    return show_task(root_path, task_id)


def read_task(root: str | Path, task_id: str) -> TaskView:
    """The task as the store holds it, with its derived status.

    An authored task file the store does not track yet is adopted first: the
    desk still holds files written before the world existed, and a read must
    work on them (`deskops doctor`/F7 migrate report the rest).
    """
    world = world_for(root)
    ref = task_id if ":" in task_id else f"TaskDoc:{task_id}"
    name = split_ref(ref)[1]
    authored = find_task_file(root, name)
    if authored is None:
        raise UnknownTaskError(task_id)
    if world.store.doc(DocId.of("TaskDoc", name)) is None:
        world, name, doc = ensure_tracked(root, name)
    else:
        doc = world.store.doc(DocId.of("TaskDoc", name))
    if doc is None:  # pragma: no cover - ensure_tracked already raised
        raise UnknownTaskError(task_id)
    ref = f"TaskDoc:{name}"
    derivation = derive_status(world, ref)
    return TaskView(
        id=name,
        path=doc_file(root, doc),
        status=derivation.status,
        payload=dict(doc.payload),
    )


def show_task(root: str | Path, task_id: str) -> TaskView:
    """Alias kept for the read surface naming: one task, as the store holds it."""
    return read_task(root, task_id)


def list_tasks(root: str | Path) -> list[TaskView]:
    """Every task of the desk with its derived status.

    The desk's task files come first (a file written before the world existed
    is adopted when it is readable) and any tracked document the scan did not
    see follows. A task that cannot be read is a warning on stderr, never a
    silent omission.
    """
    world = world_for(root)
    root_path = Path(root).resolve()
    names: list[str] = []
    for folder in ("desk/tasks", "desk/drawer/tasks"):
        for path in sorted((root_path / folder).glob("task-*.md")):
            if path.stem not in names:
                names.append(path.stem)
    for doc in world.store.docs_of("TaskDoc"):
        if doc.name not in names:
            names.append(doc.name)
    views: list[TaskView] = []
    for name in names:
        try:
            views.append(read_task(root_path, name))
        except Exception as exc:  # noqa: BLE001 - one bad file must not hide the rest
            located = find_task_file(root_path, name) or name
            print(f"Warning: Failed to load task {located}: {exc}", file=sys.stderr)
    return views


def resolve_task_id(root: str | Path, selector: str) -> str:
    """The task id a CLI selector names: exact id, filename, stem or unique slug fragment.

    Raises FormsError when the fragment matches more than one task, which is
    the ambiguity the caller must fix by naming the id.
    """
    names: list[str] = []
    root_path = Path(root)
    for folder in ("desk/tasks", "desk/drawer/tasks"):
        for path in sorted((root_path / folder).glob("task-*.md")):
            if path.stem not in names:
                names.append(path.stem)
    if selector in names:
        return selector
    matches = [name for name in names if selector in name]
    if not matches:
        raise FileNotFoundError(f"No task found for {selector}")
    if len(matches) > 1:
        raise FormsError(f"Ambiguous artifact.task selector '{selector}'")
    return matches[0]


def find_task_file(root: str | Path, task_id: str) -> Path | None:
    """The authored task file, tracked or not: drawers hold the unrouted ones."""
    root_path = Path(root)
    for folder in ("desk/tasks", "desk/drawer/tasks"):
        candidate = root_path / folder / f"{task_id}.md"
        if candidate.exists():
            return candidate
    return None


# The section headings the pre-world task files used, mapped to model fields.
LEGACY_TASK_SECTIONS = {
    "rationale": "why",
    "goal": "goal",
    "scope": "scope",
    "implementation path": "implementation_path",
    "validation": "validation",
    "done when": "done_when",
}


def payload_from_legacy_task(text: str, name: str) -> dict[str, Any]:
    """Read a pre-world task file (no frontmatter, no markers) into a payload.

    Every task file written before the world existed looks like this: a title,
    `ID:`/`Status:` lines and `## Section` bodies with an italic placeholder the
    author was meant to replace. Sections that only carry the placeholder are
    left empty, list sections read their bullets.
    """
    payload: dict[str, Any] = {
        "id": name,
        "title": name,
        "status": "deferred",
        "why": "",
        "goal": "",
        "scope": "",
        "implementation_path": "",
        "validation": [],
        "done_when": "",
        "tags": ["workspace:desk", "artifact:task"],
    }
    current: str | None = None
    body: dict[str, list[str]] = {}
    for line in text.splitlines():
        if line.startswith("# ") and payload["title"] == name:
            payload["title"] = line[2:].strip() or name
            continue
        if line.startswith("## "):
            current = line[3:].strip().lower()
            body.setdefault(current, [])
            continue
        if line.startswith("ID:") and not payload.get("id"):
            payload["id"] = line[3:].strip() or name
        if current is not None:
            body[current].append(line)
    for heading, field in LEGACY_TASK_SECTIONS.items():
        lines = [line.strip() for line in body.get(heading, [])]
        if field == "validation":
            payload[field] = [line.lstrip("- ").strip() for line in lines if line.startswith("- ")]
            continue
        values = [
            line
            for line in lines
            if line and not (line.startswith("_") and line.endswith("_"))
        ]
        payload[field] = values[0] if values else ""
    return payload


def _merge_unique(*groups: Any) -> list[str]:
    """The values of every group, in order, without repeats."""
    merged: list[str] = []
    for group in groups:
        items = [group] if isinstance(group, str) else list(group or [])
        for item in items:
            text = str(item)
            if text and text not in merged:
                merged.append(text)
    return merged


def effective_payload(root: str | Path, task_id: str, stack: tuple[str, ...] = ()) -> dict[str, Any]:
    """The task payload plus the `effective_*` fields `inherits_from` resolves.

    Parents contribute first, then the task itself; `inherit_acceptance_context`
    decides whether validation and done_when follow the same rule. A cycle is an
    error, not a silent truncation.
    """
    view = read_task(root, task_id)
    name = view.id
    if name in stack:
        raise FormsError(f"Task inheritance cycle detected: {' -> '.join([*stack, name])}")
    payload = dict(view.payload)
    parents = [
        effective_payload(root, split_ref(parent)[1] or str(parent), (*stack, name))
        for parent in (payload.get("inherits_from") or [])
    ]
    payload["effective_references"] = _merge_unique(
        *[parent.get("effective_references", parent.get("references", [])) for parent in parents],
        payload.get("references", []),
    )
    payload["effective_pills"] = _merge_unique(
        *[parent.get("effective_pills", parent.get("pills", [])) for parent in parents],
        payload.get("pills", []),
    )
    payload["effective_tags"] = _merge_unique(
        *[parent.get("effective_tags", parent.get("tags", [])) for parent in parents],
        payload.get("tags", []),
    )
    payload["effective_atoms"] = _merge_unique(
        *[parent.get("effective_atoms", parent.get("atoms", [])) for parent in parents],
        payload.get("atoms", []),
    )
    if payload.get("inherit_acceptance_context"):
        payload["effective_validation"] = _merge_unique(
            *[parent.get("effective_validation", parent.get("validation", [])) for parent in parents],
            payload.get("validation", []),
        )
        parent_done_when = next(
            (
                str(parent.get("effective_done_when") or parent.get("done_when") or "")
                for parent in parents
                if str(parent.get("effective_done_when") or parent.get("done_when") or "")
            ),
            "",
        )
        payload["effective_done_when"] = str(payload.get("done_when") or parent_done_when)
    else:
        payload["effective_validation"] = list(payload.get("validation") or [])
        payload["effective_done_when"] = str(payload.get("done_when") or "")
    payload["status"] = view.status
    return payload


def ensure_tracked(root: str | Path, task_id: str):
    """The tracked TaskDoc for `task_id`, adopting an authored file if needed."""
    world = world_for(root)
    name = split_ref(task_id if ":" in task_id else f"TaskDoc:{task_id}")[1]
    doc = world.store.doc(DocId.of("TaskDoc", name))
    if doc is not None:
        return world, name, doc
    authored = find_task_file(root, name)
    if authored is None:
        raise FileNotFoundError(f"No task found for {task_id}")
    text = authored.read_text(encoding="utf-8")
    model = world.store.model_type("TaskDoc")
    try:
        extract_model_data(model, text)
    except Exception:  # noqa: BLE001 - a pre-world file: normalize it first
        if text.lstrip().startswith("---"):
            # Broken frontmatter is corruption, not a pre-world file: guessing
            # here would hide it. The reader reports it instead.
            raise
        authored.write_text(
            render_model_markdown(model, payload_from_legacy_task(text, name)), encoding="utf-8"
        )
    world.store.track(DocId.of("TaskDoc", name), authored.relative_to(Path(root).resolve()))
    doc = world.store.doc(DocId.of("TaskDoc", name))
    if doc is None:
        raise FileNotFoundError(f"No task found for {task_id}")
    return world, name, doc


@dataclass(frozen=True)
class Gate:
    """The condition the next rung of the ladder needs, and whether it holds."""

    satisfied: bool
    message: str


def next_gate(root: str | Path, task_id: str) -> Gate:
    """What the task needs to reach the next derived status, evaluated now.

    This is what `deskops advance` answers: the ladder is derived, so there is
    no state to move. Either the next rung's condition already holds (the task
    advanced) or this is the gate that blocks it.
    """
    world = world_for(root)
    _, name, _ = ensure_tracked(root, task_id)
    ref = f"TaskDoc:{name}"
    derivation = derive_status(world, ref)
    status = derivation.status
    slice_ = task_slice(world, ref)

    if status == "drawer":
        routed = is_routed(world, ref)
        return Gate(routed, "Task is not routed by a board (promote it first).")
    if status == "active":
        declared = int(derivation.value_of("contracts_declared") or 0)
        if slice_.targets or declared:
            return Gate(True, "Plan targets are declared; the planning gate is met.")
        return Gate(False, "No plan targets are declared for this task.")
    if status == "planning":
        gaps = int(derivation.value_of("plan_targets_without_contract") or 0)
        open_targets = [
            entry["target"]
            for entry in derivation.conditions["plan_targets_without_contract"].detail["open_targets"]
        ]
        return Gate(
            gaps == 0,
            f"{gaps} plan target(s) with change_kind add|modify lack a complete contract: "
            f"{', '.join(open_targets)}",
        )
    if status == "execution":
        declared = int(derivation.value_of("contracts_declared") or 0)
        implemented = int(derivation.value_of("contracts_implemented") or 0)
        pending = [str(entry["contract"]) for entry in derivation.conditions["contracts_implemented"].detail["pending"]]
        return Gate(
            implemented >= declared,
            f"{declared - implemented} of {declared} contracts are not implemented: {', '.join(pending)}",
        )
    if status == "testing":
        proven = bool(derivation.value_of("tests_from_contracts_passing"))
        uncovered = [
            str(ref_)
            for ref_ in derivation.conditions["tests_from_contracts_passing"].detail["uncovered_contracts"]
        ]
        if proven:
            return Gate(True, "Contract tests are proven by a successful run.")
        return Gate(
            False,
            "Contract tests are not proven: no TestCoverageDoc plus successful RunDoc for "
            f"{', '.join(uncovered) or 'the declared contracts'}.",
        )
    if status == "closeout":
        has_evidence = closeout_evidence_present(world, slice_)
        return Gate(
            has_evidence,
            "Closeout evidence is missing: record evidence together with the done_when rules.",
        )
    return Gate(True, "Task is closed.")


def promote_task(root: str | Path, task_id: str, **fields: Any) -> TaskView:
    """Route a task and mark it active: the move out of the drawer.

    Two writes on purpose: the task document becomes active where the desk
    keeps routed work (and the store tracks it there), and the active BoardDoc
    gains the entry that makes the task routed, which is what takes it out of
    `drawer`. Field overrides land in the same write as the status.
    """
    root_path = Path(root).resolve()
    world, name, doc = ensure_tracked(root_path, task_id)
    payload = dict(doc.payload)
    payload.update({key: value for key, value in fields.items() if value is not None})
    payload["status"] = "active"
    world.store.replace(DocId.of("TaskDoc", name), payload)

    source = root_path / "desk" / "drawer" / "tasks" / f"{name}.md"
    target = root_path / "desk" / "tasks" / f"{name}.md"
    if source.exists() and not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        source.replace(target)
        try:
            world.store.untrack(DocId.of("TaskDoc", name))
        except Exception:  # noqa: BLE001 - already untracked
            pass
        world.store.track(DocId.of("TaskDoc", name), target.relative_to(root_path))
    _route_on_board(world, root_path, name)
    return read_task(root_path, name)


def _route_on_board(world: World, root: Path, task_name: str) -> None:
    """Add the task path to the active board's `tasks` list, once."""
    root = root.resolve()
    board_path = root / "desk" / "tasks" / "Board.md"
    if not board_path.exists():
        # Routing needs a board: a desk without one gets the minimal board the
        # scaffold would have written.
        board_path.parent.mkdir(parents=True, exist_ok=True)
        board_path.write_text(
            render_model_markdown(
                world.store.model_type("BoardDoc"),
                {
                    "id": "board-001",
                    "title": "Desk Board",
                    "scope": "desk",
                    "purpose": "Route the active work.",
                    "tasks": [],
                    "pills": [],
                    "rituals": [],
                    "notes": "",
                    "tags": ["workspace:desk"],
                },
            ),
            encoding="utf-8",
        )
    model = world.store.model_type("BoardDoc")
    payload = extract_model_data(model, board_path.read_text(encoding="utf-8"))
    entry = f"desk/tasks/{task_name}.md"
    tasks = [str(item) for item in payload.get("tasks") or []]
    payload.setdefault("id", "board-001")
    payload.setdefault("title", "Desk Board")
    if entry not in tasks and f"TaskDoc:{task_name}" not in tasks:
        tasks.append(entry)
        payload["tasks"] = tasks
        board_path.write_text(render_model_markdown(model, payload), encoding="utf-8")
    # The board must be a tracked document: routing is read from the store, and
    # a board file nobody tracks routes nothing.
    if world.store.doc(DocId.of("BoardDoc", str(payload["id"]))) is None:
        world.store.track(DocId.of("BoardDoc", str(payload["id"])), board_path.relative_to(root.resolve()))


def advance_task(root: str | Path, task_id: str) -> tuple[TaskView, Gate]:
    """Read the task, evaluate the next gate and return both."""
    view = read_task(root, task_id)
    return view, next_gate(root, task_id)


def parse_field_value(field: str, raw: str) -> Any:
    """The value a CLI argument carries: a JSON list for list fields, else the text."""
    if field in LIST_FIELDS:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise FormsError(f"Field '{field}' takes a JSON list: {exc}") from exc
        if not isinstance(value, list):
            raise FormsError(f"Field '{field}' takes a JSON list, got {type(value).__name__}.")
        return [str(item) for item in value]
    return raw


def edit_task_field(root: str | Path, task_id: str, field: str, raw_value: str) -> TaskView:
    """Set one modeled task field in place, preserving the rest of the document.

    The document is read, the payload patched and re-rendered with the model's
    reversible template, so unrelated sections and fields survive the edit.
    """
    if field in IMMUTABLE_FIELDS:
        raise FormsError(f"Cannot edit immutable field '{field}'")
    if field not in TASK_FIELDS:
        raise FormsError(f"Unknown field '{field}' for task")
    world = world_for(root)
    name = split_ref(task_id if ":" in task_id else f"TaskDoc:{task_id}")[1]
    if world.store.doc(DocId.of("TaskDoc", name)) is None:
        name = resolve_task_id(root, name)
    world, name, doc = ensure_tracked(root, name)
    document = doc_file(root, doc)
    model = world.store.model_type("TaskDoc")
    payload = extract_model_data(model, document.read_text(encoding="utf-8"))
    payload[field] = parse_field_value(field, raw_value)
    document.write_text(render_model_markdown(model, payload), encoding="utf-8")
    return show_task(root, name)
