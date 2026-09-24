from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.workspace import ensure_target_directory
from deskops.workspace import scaffold_desk


class DeskCLI:
    """Handle desk workspace scaffolding and rituals."""

    def run(self, args: Any) -> int:
        if args.desk_command == "install":
            return self.install(args)
        if args.desk_command == "migrate":
            return self.migrate(args)
        return 1

    def install(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        desk_dir = target_path / "desk"
        print(f"Scaffolding local desk at {desk_dir}...")
        result = scaffold_desk(target_path)
        for path in result.created_paths:
            print(f"Wrote {path}")

        print("Scaffold complete.")
        print("Register the repo separately with 'deskops repo register ...' when you are ready.")
        return 0

    def migrate(self, args: Any) -> int:
        target_path = Path(args.root).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        # F7 T7.1: the migration adopts every authored desk document into the
        # world; the workspace scaffolder's report stays for the file layout.
        from deskops.migrate import migrate_desk as migrate_world
        from deskops.workspace import migrate_desk as migrate_workspace

        workspace = migrate_workspace(target_path)
        print(f"Desk migration report for {target_path}:")
        print("Adopted:")
        for item in workspace.adopted or ["none"]:
            print(f"- {item}")
        print("Preserved:")
        for item in workspace.preserved or ["none"]:
            print(f"- {item}")
        print("Still manual:")
        for item in workspace.still_manual or ["none"]:
            print(f"- {item}")

        report = migrate_world(target_path)
        print(f"World: {report.summary()}")
        for item in report.tracked[:20]:
            print(f"- tracked {item}")
        if len(report.tracked) > 20:
            print(f"- ... and {len(report.tracked) - 20} more")
        for failure in report.failures:
            print(f"- refused {failure.path} ({failure.model}): {failure.reason}")
        for item in report.unmodeled:
            print(f"- unmodeled {item}")
        return 0
