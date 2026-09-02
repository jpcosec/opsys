from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
from typing import Literal

from deskops.constants import CURRENT_DESK_FORMAT

DeskClassification = Literal["absent", "empty", "legacy", "current"]

_MODELED_DESK_TOP_LEVEL_DIRS = {
    "tasks",
    "contexts",
    "rituals",
    "atoms",
    "registry",
    "steps",
    "faq",
    "routines",
    "primitives",
}


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths)


@dataclass
class DeskInspection:
    classification: DeskClassification
    surface_docs: list[Path]
    missing_surfaces: list[str]
    malformed_surfaces: list[str]
    tracked_surface_docs: set[Path]
    invalid_surface_docs: list[str]
    store_check_message: str | None = None


@dataclass
class DeskMigrationResult:
    adopted: list[str]
    preserved: list[str]
    still_manual: list[str]

    @property
    def changed(self) -> bool:
        return bool(self.adopted)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def classify_desk(root: Path) -> DeskClassification:
    return inspect_desk(root).classification


def inspect_desk(root: Path) -> DeskInspection:
    desk_dir = root / "desk"
    if not desk_dir.exists():
        return DeskInspection(
            classification="absent",
            surface_docs=[],
            missing_surfaces=["desk/"],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    surface_docs = _surface_docs(desk_dir)
    if not surface_docs:
        return DeskInspection(
            classification="empty",
            surface_docs=[],
            missing_surfaces=[],
            malformed_surfaces=[],
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    missing_surfaces: list[str] = []
    malformed_surfaces: list[str] = []

    config_path = desk_dir / "config.json"
    if not config_path.exists():
        missing_surfaces.append("desk/config.json")
        return DeskInspection(
            classification="legacy",
            surface_docs=surface_docs,
            missing_surfaces=missing_surfaces,
            malformed_surfaces=malformed_surfaces,
            tracked_surface_docs=set(),
            invalid_surface_docs=[],
        )

    desk_format = _read_declared_desk_format(config_path)
    if desk_format != CURRENT_DESK_FORMAT:
        malformed_surfaces.append(
            f"desk/config.json (versions.desk_format={desk_format!r}; expected {CURRENT_DESK_FORMAT!r})"
        )

    tracked_surface_docs, invalid_surface_docs, store_check_message = _inspect_surface_store_health(root, surface_docs)
    malformed_surfaces.extend(invalid_surface_docs)
    if store_check_message:
        malformed_surfaces.append(store_check_message)

    classification: DeskClassification = "legacy" if malformed_surfaces else "current"
    return DeskInspection(
        classification=classification,
        surface_docs=surface_docs,
        missing_surfaces=missing_surfaces,
        malformed_surfaces=malformed_surfaces,
        tracked_surface_docs=tracked_surface_docs,
        invalid_surface_docs=invalid_surface_docs,
        store_check_message=store_check_message,
    )


def migrate_desk(root: Path) -> DeskMigrationResult:
    before = inspect_desk(root)
    adopted: list[str] = []
    preserved = [str(path.relative_to(root)) for path in before.surface_docs]
    still_manual: list[str] = []

    desk_dir = root / "desk"
    result = scaffold_desk(root)
    adopted.extend(str(path.relative_to(root)) for path in result.created_paths)

    config_status = _write_or_patch_config(root)
    if config_status == "created" and "desk/config.json" not in adopted:
        adopted.append("desk/config.json")
    elif config_status == "updated":
        adopted.append("desk/config.json (patched desk_format)")

    after = inspect_desk(root)
    tracked_after = after.tracked_surface_docs if after.classification in {"legacy", "current"} else set()
    for path in after.surface_docs:
        rel = str(path.relative_to(root))
        if path not in tracked_after:
            still_manual.append(f"{rel} (preserved; manual model conversion or sldb docs track required)")

    for invalid in after.invalid_surface_docs:
        still_manual.append(f"{invalid} (manual SLDB/model repair required)")

    if after.store_check_message:
        still_manual.append(f"{after.store_check_message} (manual SLDB health follow-up)")

    return DeskMigrationResult(
        adopted=_dedupe(adopted),
        preserved=_dedupe(preserved),
        still_manual=_dedupe(still_manual),
    )


def scaffold_desk(target_path: Path) -> DeskScaffoldResult:
    desk_dir = target_path / "desk"
    created_paths: list[Path] = []
    subdirs = [
        "tasks",
        "contexts",
        "rituals",
        "atoms",
        "inbox",
        "drawer",
        "routines",
        "primitives/conditions",
        "primitives/operators",
        "primitives/checklists",
        "primitives/hooks",
        "primitives/edges",
    ]

    desk_dir.mkdir(parents=True, exist_ok=True)
    for sub in subdirs:
        subdir = desk_dir / sub
        if not subdir.exists():
            subdir.mkdir(parents=True, exist_ok=True)
            created_paths.append(subdir)

    _write_if_missing(
        desk_dir / "config.json",
        _config_template(target_path.name),
        created_paths,
    )

    _write_if_missing(
        desk_dir / "tasks" / "Board.md",
        _board_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "contexts" / "pills.md",
        _pills_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "execution.md",
        _execution_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "testing.md",
        _testing_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "rituals" / "closeout.md",
        _closeout_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "drawer" / "README.md",
        _drawer_template(target_path.name),
        created_paths,
    )
    _write_if_missing(
        desk_dir / "atoms" / "tag-namespaces.yaml",
        _atom_tag_namespaces_template(),
        created_paths,
    )

    return DeskScaffoldResult(created_paths=created_paths)


def _config_template(name: str) -> str:
    data = {
        "project_identity": name,
        "versions": {
            "desk_format": CURRENT_DESK_FORMAT,
            "model_version": "1.0.0",
        },
        "sandbox": {
            "enabled": False,
            "sandbox_root": ".tmp/deskops-sandbox",
        },
    }
    return json.dumps(data, indent=2) + "\n"


def _write_if_missing(path: Path, content: str, created_paths: list[Path]) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")
    created_paths.append(path)


def _write_or_patch_config(root: Path) -> str | None:
    desk_dir = root / "desk"
    config_path = desk_dir / "config.json"
    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(_config_template(root.name), encoding="utf-8")
        return "created"

    data: dict[str, object]
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        payload = {}

    if not isinstance(payload, dict):
        payload = {}

    data = dict(payload)
    versions = data.get("versions")
    if not isinstance(versions, dict):
        versions = {}
    versions = dict(versions)
    changed = versions.get("desk_format") != CURRENT_DESK_FORMAT
    versions["desk_format"] = CURRENT_DESK_FORMAT
    data["versions"] = versions
    data.setdefault("project_identity", root.name)

    rendered = json.dumps(data, indent=2) + "\n"
    if config_path.read_text(encoding="utf-8") != rendered:
        config_path.write_text(rendered, encoding="utf-8")
        return "updated"
    return None


def _board_template(name: str) -> str:
    return f"""---
id: board-001
scope: desk
tasks: []
pills:
- desk/contexts/pills.md
rituals:
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
tags:
- workspace:desk
---

# {name} Board

## Purpose

Route the active execution set for {name}.

## Notes

Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.
"""


def _pills_template(name: str) -> str:
    return f"""---
id: contexts-pills
tags:
- workspace:desk
---

# Pills

Pills are reusable context documents for the {name} desk routine.

## Notes

- Keep active task-to-pill binding in task docs.
- Add temporary context here only when it affects execution safety or scope.
"""


def _execution_template(name: str) -> str:
    return f"""---
id: ritual-execution
steps: []
tags:
- workspace:desk
---

# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for {name}.
"""


def _testing_template(name: str) -> str:
    return f"""---
id: ritual-testing
steps: []
tags:
- workspace:desk
---

# Testing ritual

Run the smallest relevant validation first, then broaden coverage when {name} changes shared behavior.
"""


def _closeout_template(name: str) -> str:
    return f"""---
id: ritual-closeout
steps: []
tags:
- workspace:desk
---

# Closeout ritual

Close a {name} task only after validation passes, any durable knowledge from bound pills is linked to an atom when needed, the board is updated, and the final change is ready to commit.
"""


def _drawer_template(name: str) -> str:
    return f"""# Drawer

Deferred desk work for {name} lives here until it is promoted into active execution.
"""


def _atom_tag_namespaces_template() -> str:
    return """namespaces:
  domain:
    do_not_use_when: A more specific system, topic, layer, or pattern tag applies.
    examples:
    - domain:knowledge-management
    - domain:task-execution
    meaning: Problem domain or durable area of concern.
    use_when: The atom belongs to a reusable problem domain.
  layer:
    do_not_use_when: The tag names only a broad topic or system.
    examples:
    - layer:document-model
    - layer:runtime
    - layer:cli
    meaning: Architectural layer where the atom applies.
    use_when: The atom is scoped to a layer of the system.
  system:
    do_not_use_when: The tag is only a general topic.
    examples:
    - system:deskops
    meaning: System, project, or tool the atom belongs to.
    use_when: The atom is about a specific system.
  topic:
    do_not_use_when: The atom describes a reusable implementation shape.
    examples:
    - topic:atoms
    - topic:composition
    meaning: Subject area discussed by the atom.
    use_when: The atom is about a conceptual topic.
"""


def desk_markdown_docs(desk_dir: Path) -> list[Path]:
    return sorted(path for path in desk_dir.rglob("*.md") if path.is_file())


def desk_doc_is_modeled_by_sldb(root: Path, doc_path: Path) -> bool:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return False

    parts = relative.parts
    if not parts:
        return False

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return False

    return top_level in _MODELED_DESK_TOP_LEVEL_DIRS


def desk_doc_unmodeled_reason(root: Path, doc_path: Path) -> str | None:
    try:
        relative = doc_path.resolve().relative_to((root / "desk").resolve())
    except ValueError:
        return None

    parts = relative.parts
    if not parts:
        return None

    top_level = parts[0]
    if len(parts) == 1 and relative.suffix == ".md":
        return f"desk/{relative.name} is a top-level desk note intentionally not SLDB-modeled"
    if top_level not in _MODELED_DESK_TOP_LEVEL_DIRS:
        return f"desk/{top_level}/** is intentionally not SLDB-modeled"
    return None


def modeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if desk_doc_is_modeled_by_sldb(root, path)]


def unmodeled_desk_markdown_docs(root: Path, desk_dir: Path) -> list[Path]:
    return [path for path in desk_markdown_docs(desk_dir) if not desk_doc_is_modeled_by_sldb(root, path)]


def _surface_docs(desk_dir: Path) -> list[Path]:
    docs: list[Path] = []
    board = desk_dir / "tasks" / "Board.md"
    if board.exists():
        docs.append(board)

    tasks_dir = desk_dir / "tasks"
    if tasks_dir.exists():
        docs.extend(sorted(path for path in tasks_dir.glob("*.md") if path.name != "Board.md"))

    contexts_dir = desk_dir / "contexts"
    if contexts_dir.exists():
        docs.extend(sorted(path for path in contexts_dir.glob("*.md")))
    return docs


def _read_declared_desk_format(config_path: Path) -> str | None:
    try:
        payload = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    versions = payload.get("versions")
    if not isinstance(versions, dict):
        return None
    desk_format = versions.get("desk_format")
    return desk_format if isinstance(desk_format, str) else None


def _inspect_surface_store_health(root: Path, surface_docs: list[Path]) -> tuple[set[Path], list[str], str | None]:
    store_path = root / ".sldb"
    if not store_path.exists():
        return set(), [], None

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "sldb",
            "stores",
            "check",
            "--store",
            str(store_path),
            "--format",
            "json",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    tracked: set[Path] = set()
    invalid: list[str] = []
    tracked_surface_set = {path.resolve() for path in surface_docs}

    payload: dict[str, object] | None = None
    if result.stdout.strip():
        try:
            loaded = json.loads(result.stdout)
        except json.JSONDecodeError:
            return tracked, invalid, "sldb stores check returned unreadable JSON"
        if isinstance(loaded, dict):
            payload = loaded

    if payload is not None:
        for model in payload.get("models", []):
            if not isinstance(model, dict):
                continue
            for doc in model.get("documents", []):
                if not isinstance(doc, dict):
                    continue
                doc_path = doc.get("path")
                if not isinstance(doc_path, str):
                    continue
                absolute = (root / doc_path).resolve()
                if absolute not in tracked_surface_set:
                    continue
                tracked.add(absolute)
                note = doc.get("note")
                if note not in ("ok", "benign_mutation"):
                    invalid.append(f"{doc_path} ({note})")

    if result.returncode != 0 and not invalid:
        stderr = result.stderr.strip().splitlines()
        if stderr:
            return tracked, invalid, f"sldb stores check failed: {stderr[0]}"
        return tracked, invalid, "sldb stores check failed"

    return tracked, invalid, None


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered
