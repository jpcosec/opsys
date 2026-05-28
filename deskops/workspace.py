from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class DeskScaffoldResult:
    created_paths: list[Path]

    @property
    def wrote_anything(self) -> bool:
        return bool(self.created_paths)


def ensure_target_directory(path: Path) -> tuple[bool, str | None]:
    if not path.exists():
        return False, f"Error: Path {path} does not exist."
    if not path.is_dir():
        return False, f"Error: Path {path} is not a directory."
    return True, None


def scaffold_desk(target_path: Path) -> DeskScaffoldResult:
    desk_dir = target_path / "desk"
    created_paths: list[Path] = []
    subdirs = [
        "tasks",
        "contexts",
        "rituals",
        "inbox",
        "drawer",
        "drawer/atoms",
        "fields",
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

    return DeskScaffoldResult(created_paths=created_paths)


def _write_if_missing(path: Path, content: str, created_paths: list[Path]) -> None:
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")
    created_paths.append(path)


def _board_template(name: str) -> str:
    return f"""# {name} Board

ID: board-001
Scope: desk

## Purpose

Route the active execution set for {name}.

## Tasks

- none

## Pills

- desk/contexts/pills.md

## Rituals

- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md

## Notes

Bootstrap complete. Add active task docs under `desk/tasks/` and route them here.

## Tags

- workspace:desk
"""


def _pills_template(name: str) -> str:
    return f"""# Pills

Pills are reusable context documents for the {name} desk routine.

## Notes

- Keep active task-to-pill binding in task docs.
- Add temporary context here only when it affects execution safety or scope.
"""


def _execution_template(name: str) -> str:
    return f"""# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for {name}.
"""


def _testing_template(name: str) -> str:
    return f"""# Testing ritual

Run the smallest relevant validation first, then broaden coverage when {name} changes shared behavior.
"""


def _closeout_template(name: str) -> str:
    return f"""# Closeout ritual

Close a {name} task only after validation passes, the board is updated, and the final change is ready to commit.
"""


def _drawer_template(name: str) -> str:
    return f"""# Drawer

Deferred desk work for {name} lives here until it is promoted into active execution.
"""
