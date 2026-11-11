from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import seed_desk


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

        result = seed_desk(target_path)
        if result.wrote_anything:
            print(f"Scaffolded desk at {target_path / 'desk'}.")
            for path in result.created_paths:
                print(f"Wrote {path}")
            for path in result.rewritten_paths:
                print(f"Rewrote {path}")
        else:
            print(f"Desk already exists at {target_path / 'desk'}.")
        from deskops.lifecycle import write_lifecycle_graph

        for change in write_lifecycle_graph(target_path):
            print(f"Lifecycle graph: {change}")
        # The store declares the namespaces of the seeded desk/atoms/tag-namespaces.yaml for
        # sldb's tag family (CC35d resto); a declaration already equal is left alone.
        from deskops.atom_tags import sync_tag_declaration

        if sync_tag_declaration(target_path):
            print("Declared the tag namespaces of desk/atoms/tag-namespaces.yaml in .sldb/store.yaml.")
        print("Initialization complete.")
        return 0
