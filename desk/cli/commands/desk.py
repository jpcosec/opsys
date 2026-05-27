from __future__ import annotations

from pathlib import Path
from typing import Any


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        return 1

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        if not target_path.exists():
            print(f"Error: Path {target_path} does not exist.")
            return 1
        if not target_path.is_dir():
            print(f"Error: Path {target_path} is not a directory.")
            return 1

        desk_dir = target_path / "desk"
        subdirs = [
            "tasks",
            "contexts",
            "rituals",
            "inbox",
            "drawer",
            "drawer/atoms",
        ]

        print(f"Scaffolding local desk at {desk_dir}...")
        desk_dir.mkdir(parents=True, exist_ok=True)
        for sub in subdirs:
            (desk_dir / sub).mkdir(parents=True, exist_ok=True)

        self._write_if_missing(
            desk_dir / "tasks" / "Board.md",
            self._board_template(target_path.name),
        )
        self._write_if_missing(
            desk_dir / "contexts" / "pills.md",
            self._pills_template(target_path.name),
        )
        self._write_if_missing(
            desk_dir / "rituals" / "execution.md",
            self._execution_template(target_path.name),
        )
        self._write_if_missing(
            desk_dir / "rituals" / "testing.md",
            self._testing_template(target_path.name),
        )
        self._write_if_missing(
            desk_dir / "rituals" / "closeout.md",
            self._closeout_template(target_path.name),
        )
        self._write_if_missing(
            desk_dir / "drawer" / "README.md",
            self._drawer_template(target_path.name),
        )

        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def _write_if_missing(self, path: Path, content: str) -> None:
        if path.exists():
            return
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")

    def _board_template(self, name: str) -> str:
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

    def _pills_template(self, name: str) -> str:
        return f"""# Pills

Pills are reusable context documents for the {name} desk routine.

## Notes

- Keep active task-to-pill binding in task docs.
- Add temporary context here only when it affects execution safety or scope.
"""

    def _execution_template(self, name: str) -> str:
        return f"""# Execution ritual

Review the board, bind the relevant pills, keep scope tight, and implement only the active task for {name}.
"""

    def _testing_template(self, name: str) -> str:
        return f"""# Testing ritual

Run the smallest relevant validation first, then broaden coverage when {name} changes shared behavior.
"""

    def _closeout_template(self, name: str) -> str:
        return f"""# Closeout ritual

Close a {name} task only after validation passes, the board is updated, and the final change is ready to commit.
"""

    def _drawer_template(self, name: str) -> str:
        return f"""# Drawer

Deferred desk work for {name} lives here until it is promoted into active execution.
"""
