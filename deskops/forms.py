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

from deskops.derived_conditions import UnknownTaskError
from deskops.derived_conditions import split_ref
from deskops.derived_status import derive_status
from deskops.world import DocId
from deskops.world import World
from deskops.world import ensure_store_root
from deskops.world import extract_model_data
from deskops.world import get_world
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
    from deskops.bootstrap import bootstrap_world

    root_path = ensure_store_root(root)
    if root_path not in _READY_ROOTS:
        bootstrap_world(root_path)
        _READY_ROOTS.add(root_path)
    return get_world(root_path)


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
    """The task as the store holds it, with its derived status."""
    world = world_for(root)
    ref = task_id if ":" in task_id else f"TaskDoc:{task_id}"
    name = split_ref(ref)[1]
    doc = world.store.doc(DocId.of("TaskDoc", name))
    if doc is None:
        raise UnknownTaskError(task_id)
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
    """Every tracked task with its derived status, in store order."""
    world = world_for(root)
    views: list[TaskView] = []
    for doc in world.store.docs_of("TaskDoc"):
        try:
            views.append(read_task(root, f"TaskDoc:{doc.name}"))
        except UnknownTaskError:  # pragma: no cover - defensive
            continue
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
    doc = world.store.doc(DocId.of("TaskDoc", name))
    if doc is None:
        # An authored task the store does not track yet: adopt it, then edit.
        authored = find_task_file(root, name)
        if authored is None:
            raise FileNotFoundError(f"No task found for {task_id}")
        document = authored
        world.store.track(DocId.of("TaskDoc", name), document.relative_to(Path(root).resolve()))
    else:
        document = doc_file(root, doc)
    model = world.store.model_type("TaskDoc")
    payload = extract_model_data(model, document.read_text(encoding="utf-8"))
    payload[field] = parse_field_value(field, raw_value)
    document.write_text(render_model_markdown(model, payload), encoding="utf-8")
    missing = _missing_targets(world, payload)
    if missing:
        raise FormsError(f"Edit left unresolvable references: {', '.join(missing)}")
    return show_task(root, name)


def _missing_targets(world: World, payload: dict[str, Any]) -> list[str]:
    """Refs the edited document names that the store does not track."""
    missing: list[str] = []
    for field in ("depends_on", "pills", "references", "atoms", "plan", "acceptance"):
        value = payload.get(field) or []
        items = [value] if isinstance(value, str) else value
        for ref in items:
            text = str(ref).strip()
            if not text or ":" not in text:
                continue
            model, name = split_ref(text)
            if world.store.doc(DocId.of(model, name)) is None:
                missing.append(text)
    return missing
