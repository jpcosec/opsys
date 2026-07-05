from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.atom_tags import add_namespace
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces


class AtomsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        registry_path = default_registry_path(root)

        if args.atoms_command == "add-namespace":
            ensure_default_namespaces(registry_path)
            try:
                add_namespace(
                    registry_path,
                    args.namespace,
                    meaning=args.meaning,
                    use_when=args.use_when,
                    do_not_use_when=args.do_not_use_when,
                    examples=list(args.example or []),
                )
            except ValueError as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Added atom tag namespace {args.namespace}")
            print(f"Path: {registry_path}")
            return 0

        # Proxy these to the main operation CLI or mark as not implemented
        if args.atoms_command == "list":
            args.command = "list"
            args.subject = "atoms"
            from deskops.cli.commands.operations import OperationsCLI
            return OperationsCLI().run(args)

        if args.atoms_command == "show":
            args.command = "show"
            args.subject = "atom"
            from deskops.cli.commands.operations import OperationsCLI
            return OperationsCLI().run(args)

        if args.atoms_command in ("new", "validate"):
            print(f"atoms {args.atoms_command} grammar added; implementation deferred.")
            return 0

        return 1
