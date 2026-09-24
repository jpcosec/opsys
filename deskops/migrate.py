"""Migrate an authored desk into the world (F7 T7.1).

Every desk surface has a model: the migration walks the folders, reads each
authored file with its model, and tracks it in the store where it lives. Files
are never rewritten by default: a document that does not validate is reported
with its reason instead of being guessed into shape.

The absorbed models (conditions, operators, checklists, edges, hooks, routines)
are still migrated when they are on disk, because the store is the record of
what the desk had; nothing new is written in those shapes.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

from deskops.world import DocId
from deskops.world import extract_model_data
from deskops.world import World

# Desk folder (relative to the repo root) -> the model of the files it holds.
FOLDER_MODELS: tuple[tuple[str, str], ...] = (
    ("desk/tasks", "TaskDoc"),
    ("desk/drawer/tasks", "TaskDoc"),
    ("desk/contexts", "PillDoc"),
    ("desk/rituals", "RitualDoc"),
    ("desk/steps", "StepDoc"),
    ("desk/roles", "RoleDoc"),
    ("desk/faq", "FAQDoc"),
    ("desk/inbox", "InboxNoteDoc"),
    ("desk/registry", "RepositoryDoc"),
    ("desk/routines", "RoutineDoc"),
    ("desk/relation_types", "RelationTypeDoc"),
    ("desk/primitives/conditions", "ConditionDoc"),
    ("desk/primitives/operators", "OperatorDoc"),
    ("desk/primitives/checklists", "ChecklistDoc"),
    ("desk/primitives/edges", "EdgeDoc"),
    ("desk/primitives/hooks", "HookDoc"),
)

# Files with a model of their own inside a folder of another model.
FILENAME_MODELS: tuple[tuple[str, str], ...] = (
    ("desk/tasks/Board.md", "BoardDoc"),
    ("desk/drawer/tasks/Board.md", "BoardDoc"),
)

# Folders that carry no model yet: reported, never tracked silently.
UNMODELED_FOLDERS = (
    "desk/features",
    "desk/logbook",
    "desk/materializations",
)

ATOM_FOLDER = "desk/atoms"


@dataclass(frozen=True)
class MigrateFailure:
    """One document the migration refused to guess."""

    path: str
    model: str
    reason: str


@dataclass
class MigrateReport:
    """What one migration run found and did."""

    tracked: list[str] = field(default_factory=list)
    already: list[str] = field(default_factory=list)
    failures: list[MigrateFailure] = field(default_factory=list)
    unmodeled: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """One line per outcome, for the CLI to print."""
        return (
            f"tracked {len(self.tracked)} · already {len(self.already)} · "
            f"failed {len(self.failures)} · unmodeled {len(self.unmodeled)}"
        )


def model_for(relative: str) -> str | None:
    """The model of one desk file path, or None when the desk has no model for it."""
    if relative in dict(FILENAME_MODELS):
        return dict(FILENAME_MODELS)[relative]
    if relative.startswith(ATOM_FOLDER + "/") and relative.endswith(".md"):
        return "AtomDoc"
    for folder, model in FOLDER_MODELS:
        if relative.startswith(folder + "/") and relative.endswith(".md"):
            return model
    return None


def desk_files(root: str | Path) -> list[str]:
    """Every markdown file of the desk, repository-relative and sorted."""
    root_path = Path(root).resolve()
    desk = root_path / "desk"
    return sorted(
        str(path.relative_to(root_path))
        for path in desk.rglob("*.md")
        if path.is_file()
    )


# Prose documents: "# Title", an "ID:" line and "## Section" bodies. The old
# desk wrote pills and boards this way before the models existed.
PROSE_SECTIONS: dict[str, dict[str, str]] = {
    "PillDoc": {
        "what": "what",
        "why": "why",
        "when": "when",
        "where": "where",
        "how": "how",
        "how not": "how_not",
    },
    "BoardDoc": {"purpose": "purpose"},
    "TaskDoc": {
        "goal": "goal",
        "scope": "scope",
        "implementation path": "implementation_path",
        "done when": "done_when",
    },
}


def prose_payload(text: str, model_name: str, *, name: str) -> dict[str, Any] | None:
    """The payload of a prose document written before the models existed.

    Returns None when the file does not look like one (no title or no `ID:`
    line): those are index pages and placeholders, not documents to adopt.
    """
    sections = PROSE_SECTIONS.get(model_name)
    if sections is None:
        return None
    title = ""
    identifier = ""
    bodies: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            continue
        if stripped.startswith("## "):
            current = stripped[3:].strip().lower()
            bodies.setdefault(current, [])
            continue
        if stripped.startswith("ID:"):
            identifier = stripped[3:].strip()
            continue
        if current is not None:
            bodies[current].append(line)
    if not title or not identifier:
        return None
    payload: dict[str, Any] = {
        "id": identifier or name,
        "title": title,
        "status": "",
        "summary": "",
        "tags": ["workspace:desk"],
    }
    for heading, field in sections.items():
        lines = [
            line.strip()
            for line in bodies.get(heading, [])
            if line.strip() and not (line.strip().startswith("_") and line.strip().endswith("_"))
        ]
        payload[field] = "\n".join(lines)
    if model_name == "BoardDoc":
        payload.setdefault("scope", "desk")
        payload.setdefault("tasks", [])
        payload.setdefault("pills", [])
        payload.setdefault("rituals", [])
        payload["notes"] = payload.pop("purpose", "")
    return payload


def migrate_desk(
    root: str | Path,
    *,
    world: World | None = None,
    dry_run: bool = False,
    adopt_prose: bool = False,
) -> MigrateReport:
    """Track every authored desk document with its model, idempotent.

    A document already tracked at the same path is left alone; a document that
    does not validate with its model is reported, not rewritten.
    """
    from deskops.bootstrap import ensure_world

    root_path = Path(root).resolve()
    world = world or ensure_world(root_path)
    report = MigrateReport()
    for relative in desk_files(root_path):
        model_name = model_for(relative)
        if model_name is None:
            if any(relative.startswith(folder) for folder in UNMODELED_FOLDERS):
                report.unmodeled.append(relative)
            continue
        if model_name not in world.store.model_names():
            report.failures.append(MigrateFailure(relative, model_name, "model not registered"))
            continue
        model = world.store.model_type(model_name)
        name = Path(relative).stem
        doc_id = DocId.of(model_name, name)
        existing = world.store.doc(doc_id)
        if existing is not None and str(existing.path) == relative:
            report.already.append(relative)
            continue
        text = (root_path / relative).read_text(encoding="utf-8")
        payload: dict[str, Any] | None = None
        try:
            extract_model_data(model, text)
        except Exception as exc:  # noqa: BLE001 - the point is to report it
            payload = prose_payload(text, model_name, name=name) if adopt_prose else None
            if payload is None:
                report.failures.append(MigrateFailure(relative, model_name, str(exc).splitlines()[0]))
                continue
        if payload is not None and not dry_run:
            from deskops.world import render_model_markdown

            (root_path / relative).write_text(
                render_model_markdown(model, payload), encoding="utf-8"
            )
        if dry_run:
            report.tracked.append(relative)
            continue
        if existing is not None:
            world.store.untrack(doc_id)
        world.store.track(doc_id, Path(relative))
        report.tracked.append(relative)
    return report


def store_contents(world: World) -> dict[str, int]:
    """How many documents of each model the store holds, by model name."""
    counts: dict[str, int] = {}
    for model_name in sorted(world.store.model_names()):
        try:
            counts[model_name] = len(world.store.docs_of(model_name))
        except Exception:  # noqa: BLE001 - a model with no documents is simply absent
            counts[model_name] = 0
    return {name: count for name, count in counts.items() if count}


def desk_gaps(root: str | Path) -> dict[str, Any]:
    """What the migration could not place: the honest state of a desk."""
    report = migrate_desk(root, dry_run=True)
    return {
        "summary": report.summary(),
        "failures": [failure.__dict__ for failure in report.failures],
        "unmodeled": report.unmodeled,
    }
