from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import scaffold_desk


class AboutCLI:
    def run(self, args: Any) -> int:
        # Resolved through the CLI module so a patched entrypoint stays visible.
        from deskops.cli import main as main_module

        return main_module.print_about()


class BootstrapCLI:
    def run(self, args: Any) -> int:
        return SLDBBootstrap().ensure_machine_ready()


class InitCLI:
    def run(self, args: Any) -> int:
        target_path = Path(args.path).resolve()
        ok, error = ensure_target_directory(target_path)
        if not ok:
            print(error)
            return 1

        bootstrap = SLDBBootstrap()
        ready = bootstrap.ensure_machine_ready()
        if ready != 0:
            return ready

        local_store = bootstrap.init_local_store(target_path)
        if local_store != 0:
            return local_store

        result = scaffold_desk(target_path)
        if result.wrote_anything:
            print(f"Scaffolded desk at {target_path / 'desk'}.")
            for path in result.created_paths:
                print(f"Wrote {path}")
        else:
            print(f"Desk already exists at {target_path / 'desk'}.")
        from deskops.lifecycle import ensure_lifecycle_graph

        for change in ensure_lifecycle_graph(target_path):
            print(f"Lifecycle graph: {change}")
        print("Initialization complete.")
        return 0
