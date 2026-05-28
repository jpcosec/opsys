from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
if str(PACKAGE_ROOT) in sys.path:
    sys.path.remove(str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT))

from desk.cli.parser import build_parser

from deskops.about import print_about
from deskops.bootstrap import SLDBBootstrap
from deskops.workspace import ensure_target_directory
from deskops.workspace import scaffold_desk


class CLI:
    """Main CLI dispatcher for deskops."""

    def run(self, argv: Any = None) -> int:
        bootstrap = SLDBBootstrap()
        parser = build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            if isinstance(exc.code, int):
                return exc.code
            return 0 if exc.code is None else 1

        if args.command == "faq":
            from desk.cli.commands.faq import FAQCLI

            return FAQCLI().run(args)
        if args.command == "about":
            return print_about()
        if args.command == "desk":
            from desk.cli.commands.desk import DeskCLI

            return DeskCLI().run(args)
        if args.command in {"add", "list", "show", "advance"}:
            ready = bootstrap.ensure_sldb_available()
            if ready != 0:
                return ready

            from desk.cli.commands.operations import OperationsCLI

            return OperationsCLI().run(args)
        if args.command == "bootstrap":
            return self._bootstrap()
        if args.command == "init":
            return self._init(args)

        ready = bootstrap.ensure_sldb_available()
        if ready != 0:
            return ready

        self._apply_default_pythonpath(args, bootstrap)

        if args.command == "inbox":
            from desk.cli.commands.inbox import InboxCLI

            return InboxCLI().run(args)
        if args.command == "repo":
            from desk.cli.commands.repo import RepoCLI

            return RepoCLI().run(args)

        print(f"Unknown command: {args.command}")
        return 2

    def _bootstrap(self) -> int:
        return SLDBBootstrap().ensure_machine_ready()

    def _init(self, args: Any) -> int:
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
        print("Initialization complete.")
        return 0

    def _apply_default_pythonpath(self, args: Any, bootstrap: SLDBBootstrap) -> None:
        if not hasattr(args, "pythonpath"):
            return
        if getattr(args, "pythonpath"):
            return
        args.pythonpath = bootstrap.default_pythonpath()


def main(argv: Any = None) -> int:
    try:
        return CLI().run(argv)
    except SystemExit:
        raise
    except Exception as exc:
        raise SystemExit(f"Unexpected: {exc}")


if __name__ == "__main__":
    sys.exit(main())
