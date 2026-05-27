from __future__ import annotations

from pathlib import Path
from typing import Any

from .repo import RepoCLI


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

        desk_dir = target_path / "desk"
        subdirs = ["tasks", "pills", "inbox", "registry"]
        
        print(f"Scaffolding desk at {desk_dir}...")
        desk_dir.mkdir(exist_ok=True)
        for sub in subdirs:
            (desk_dir / sub).mkdir(exist_ok=True)

        # Write Board.md
        board_path = desk_dir / "tasks" / "Board.md"
        if not board_path.exists():
            board_path.write_text(self._board_template(target_path.name), encoding="utf-8")
            print(f"Wrote {board_path}")

        # Write STANDARDS.md
        standards_path = desk_dir / "STANDARDS.md"
        if not standards_path.exists():
            standards_path.write_text(self._standards_template(target_path.name), encoding="utf-8")
            print(f"Wrote {standards_path}")

        # Auto-register the repo in the ecosystem registry
        print("Registering repository in ecosystem...")
        repo_args = type('Args', (), {
            'name': args.name or target_path.name,
            'path': str(target_path.relative_to(self._ecosystem_root())),
            'id': args.id,
            'description': f"Workflow surface for {target_path.name}.",
            'tags': "type:tool,layer:distributed",
            'store': args.store,
            'pythonpath': args.pythonpath,
            'repo_command': 'register'
        })
        
        repo_cli = RepoCLI()
        return repo_cli.register(repo_args)

    def _ecosystem_root(self) -> Path:
        # Assuming ecosystem root is the parent of the root store
        from sldb.store.resolver import find_local_store
        from sldb.store.layout import project_root
        
        local_store = find_local_store()
        if local_store:
            return project_root(local_store)
        return Path.cwd()

    def _board_template(self, name: str) -> str:
        return f"""# {name} Board

## Current State Summary

Bootstrap complete. Execution surface ready.

## Active

- none

## Recently Closed

- none

## Working Rules

1. Every task ends in a closing commit.
2. Decisions belong in pills.
3. Inbox is for incoming noise/suggestions.
"""

    def _standards_template(self, name: str) -> str:
        return f"""# {name} Desk Standards

## Purpose

Maintain operational health for {name}.

## Rituals

- **Initialization**: Review Board.md and triage Inbox.
- **Execution**: Small atomic commits.
- **Testing**: Run local test suite.
- **Closeout**: Update Board.md and move to next task.
"""
