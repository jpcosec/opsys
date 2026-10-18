from __future__ import annotations

import importlib
import os
from pathlib import Path
import sys
import traceback
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
if str(PACKAGE_ROOT) in sys.path:
    sys.path.remove(str(PACKAGE_ROOT))
sys.path.insert(0, str(PACKAGE_ROOT))

from deskops.cli.parser import build_parser
from deskops.cli.registry import command_for_path

from deskops.about import print_about
from deskops.bootstrap import SLDBBootstrap
from deskops.errors import DeskopsError
from deskops.errors import UsageError


_SLDB_BEFORE_DISPATCH = frozenset(
    {
        "add",
        "edit",
        "bind",
        "next",
        "list",
        "show",
        "advance",
        "materialize",
        "drift",
        "message",
        "inbox",
        "repo",
    }
)
_DEFAULT_PYTHONPATH_COMMANDS = frozenset({"message", "inbox", "repo"})


def _load_handler(reference: str) -> type:
    module_name, _, attribute = reference.partition(":")
    module = importlib.import_module(module_name)
    return getattr(module, attribute)


def _validate_selectors(args: Any) -> None:
    cmd_parts = ["deskops", args.command]
    subject = getattr(args, "subject", None)
    if subject:
        cmd_parts.append(subject)
    elif getattr(args, "atoms_command", None):
        cmd_parts.append(getattr(args, "atoms_command"))
    elif getattr(args, "promote_command", None):
        cmd_parts.append(getattr(args, "promote_command"))

    cmd_str = " ".join(cmd_parts)

    selector_fields = {
        "selector": "selector",
        "doc_id": "selector",
        "task_id": "task selector",
        "pill": "pill selector",
        "task": "task selector",
    }
    
    for field, label in selector_fields.items():
        if hasattr(args, field):
            val = getattr(args, field)
            if val is not None and isinstance(val, str):
                if not val.strip():
                    raise ValueError(f"{cmd_str}: {label} cannot be empty or whitespace-only")

class CLI:
    """Main CLI dispatcher for deskops."""

    debug = False

    def run(self, argv: Any = None) -> int:
        bootstrap = SLDBBootstrap()
        parser = build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            if isinstance(exc.code, int):
                return exc.code
            return 0 if exc.code is None else 1

        self.debug = bool(getattr(args, "debug", False))

        _validate_selectors(args)

        self._apply_test_root_override(args)

        # An optional --root (message/inbox) leaves the attribute present but
        # None; only validate it when a value was actually supplied.
        if getattr(args, "root", None) is not None:
            root_path = Path(args.root).resolve()
            if not root_path.exists() or not root_path.is_dir():
                import sys
                print(f"Error: Provided --root is not a valid directory: {args.root}", file=sys.stderr)
                return 1

        command_path = getattr(args, "_deskops_command_path", None)
        if command_path is None:
            raise UsageError(f"Unknown command: {args.command}")
        try:
            command = command_for_path(command_path)
        except KeyError:
            raise UsageError(f"Unknown command: {' '.join(command_path)}")

        if command.path[0] in _SLDB_BEFORE_DISPATCH:
            ready = bootstrap.ensure_sldb_available()
            if ready != 0:
                return ready

        if command.path[0] in _DEFAULT_PYTHONPATH_COMMANDS:
            self._apply_default_pythonpath(args, bootstrap)

        return _load_handler(command.handler)().run(args)

    def _apply_test_root_override(self, args: Any) -> None:
        if not hasattr(args, "root"):
            return
        if getattr(args, "root", None) != ".":
            return
        if args.command not in {"add", "edit", "bind", "list", "show", "advance", "next", "promote", "message", "inbox", "repo", "graph", "materialize", "drift"}:
            return
            
        from deskops.config import DeskConfig
        from pathlib import Path
        import os

        # Authoritative precedence for test-root selection:
        # explicit CLI flag > DESKOPS_TEST_ROOT env > config.local.json > config.json > defaults.
        # This helper only applies when the CLI root is still the default ".".
        original_root = Path(".").resolve()
        desk_root = original_root / "desk"

        test_root = os.environ.get("DESKOPS_TEST_ROOT", "").strip()

        config = DeskConfig.load(desk_root)

        if test_root:
            target_root = test_root
        elif config.sandbox.enabled and config.sandbox.sandbox_root:
            target_root = config.sandbox.sandbox_root
        else:
            return

        root_path = Path(target_root).resolve()
        root_path.mkdir(parents=True, exist_ok=True)
        args.root = str(root_path)

    def _apply_default_pythonpath(self, args: Any, bootstrap: SLDBBootstrap) -> None:
        if not hasattr(args, "pythonpath"):
            return
        if getattr(args, "pythonpath"):
            return
        args.pythonpath = bootstrap.default_pythonpath()


def main(argv: Any = None) -> int:
    cli = CLI()
    try:
        return cli.run(argv)
    except SystemExit:
        raise
    except DeskopsError as exc:
        stream = sys.stdout if isinstance(exc, UsageError) else sys.stderr
        print(str(exc), file=stream)
        return exc.exit_code
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"Missing required field: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        from pydantic import ValidationError

        if isinstance(exc, ValidationError):
            print(f"Validation error:\n{exc}", file=sys.stderr)
            return 1
        print(f"Invalid value: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        from sldb.core.exceptions import SLDBStoreError

        if isinstance(exc, SLDBStoreError):
            print(f"Store error: {exc}", file=sys.stderr)
            return 1
        if getattr(cli, "debug", False):
            traceback.print_exc()
        print(
            f"Unexpected error: {type(exc).__name__}: {exc} "
            "(rerun with --debug for the traceback)",
            file=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    sys.exit(main())
