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
from deskops.cli.registry import resolve_context
from deskops.cli.render import render_deprecation
from deskops.cli.render import render_error
from deskops.cli.render import requested_format
from deskops.identity import find_context_root

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


def _root_option_given(argv: list[str]) -> bool:
    """Whether ``--root`` was supplied, distinguishing it from the default."""
    return any(token == "--root" or token.startswith("--root=") for token in argv)


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
        raw_argv = list(sys.argv[1:] if argv is None else argv)
        root_explicit = _root_option_given(raw_argv)
        parser = build_parser()
        try:
            args = parser.parse_args(argv)
        except SystemExit as exc:
            if isinstance(exc.code, int):
                return exc.code
            return 0 if exc.code is None else 1

        self.debug = bool(getattr(args, "debug", False))

        _validate_selectors(args)

        setattr(args, "_deskops_root_explicit", root_explicit)

        command_path = getattr(args, "_deskops_command_path", None)
        if command_path is None:
            raise UsageError(f"Unknown command: {args.command}")
        try:
            command = command_for_path(command_path)
        except KeyError:
            raise UsageError(f"Unknown command: {' '.join(command_path)}")

        if command.deprecated_for is not None:
            render_deprecation(command.deprecated_for)

        self._apply_test_root_override(
            args,
            mutates=command.mutates,
            root_explicit=root_explicit,
        )

        resolved_root, resolved_store = resolve_context(args)
        if hasattr(args, "root"):
            args.root = str(resolved_root)
        if hasattr(args, "store") and resolved_store is not None and not getattr(args, "store", None):
            args.store = str(resolved_store)

        # An optional --root (message/inbox) leaves the attribute present but
        # None; only validate it when a value was actually supplied.
        if getattr(args, "root", None) is not None:
            root_path = Path(args.root).resolve()
            if not root_path.exists() or not root_path.is_dir():
                message = f"Provided --root is not a valid directory: {args.root}"
                if requested_format(raw_argv) == "json":
                    return render_error(message, "json", type_name="DomainError")
                print(f"Error: {message}", file=sys.stderr)
                return 1

        if command.path[0] in _SLDB_BEFORE_DISPATCH:
            ready = bootstrap.ensure_sldb_available()
            if ready != 0:
                return ready

        if command.path[0] in _DEFAULT_PYTHONPATH_COMMANDS:
            self._apply_default_pythonpath(args, bootstrap)

        return _load_handler(command.handler)().run(args)

    def _apply_test_root_override(self, args: Any, *, mutates: bool, root_explicit: bool) -> None:
        """Redirect a mutating command to the configured sandbox root.

        Only applies when the registry marks the command ``mutates`` and the
        caller did not pass ``--root`` explicitly. It rewrites the root; it
        never refuses the invocation.
        """
        if root_explicit or not mutates:
            return
        if not hasattr(args, "root"):
            return

        from deskops.config import DeskConfig

        # Authoritative precedence for test-root selection:
        # explicit CLI flag > DESKOPS_TEST_ROOT env > config.local.json > config.json > defaults.
        original_root = find_context_root()
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
        setattr(args, "_deskops_root_override", True)

    def _apply_default_pythonpath(self, args: Any, bootstrap: SLDBBootstrap) -> None:
        if not hasattr(args, "pythonpath"):
            return
        if getattr(args, "pythonpath"):
            return
        args.pythonpath = bootstrap.default_pythonpath()


def _error_parts(exc: BaseException) -> tuple[int, str, str, str, Any]:
    """One (code, type, message, display text, stream) tuple for every failure."""

    from pydantic import ValidationError
    from sldb.core.exceptions import SLDBStoreError

    if isinstance(exc, DeskopsError):
        stream = sys.stdout if isinstance(exc, UsageError) else sys.stderr
        return exc.exit_code, type(exc).__name__, str(exc), str(exc), stream
    if isinstance(exc, FileNotFoundError):
        return 1, type(exc).__name__, str(exc), f"File not found: {exc}", sys.stderr
    if isinstance(exc, KeyError):
        return 1, type(exc).__name__, str(exc), f"Missing required field: {exc}", sys.stderr
    if isinstance(exc, ValidationError):
        return 1, type(exc).__name__, str(exc), f"Validation error:\n{exc}", sys.stderr
    if isinstance(exc, ValueError):
        return 1, type(exc).__name__, str(exc), f"Invalid value: {exc}", sys.stderr
    if isinstance(exc, SLDBStoreError):
        return 1, type(exc).__name__, str(exc), f"Store error: {exc}", sys.stderr
    display = (
        f"Unexpected error: {type(exc).__name__}: {exc} "
        "(rerun with --debug for the traceback)"
    )
    return 3, type(exc).__name__, str(exc), display, sys.stderr


def main(argv: Any = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    fmt = requested_format(raw_argv)
    cli = CLI()
    try:
        return cli.run(argv)
    except SystemExit:
        raise
    except BaseException as exc:
        code, type_name, message, display, stream = _error_parts(exc)
        if fmt == "json":
            return render_error(message, "json", code=code, type_name=type_name)
        if code == 3 and getattr(cli, "debug", False):
            traceback.print_exc()
        print(display, file=stream)
        return code


if __name__ == "__main__":
    sys.exit(main())
