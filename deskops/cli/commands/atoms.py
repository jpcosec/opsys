from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.atom_tags import add_namespace
from deskops.atom_tags import default_registry_path
from deskops.atom_tags import ensure_default_namespaces
from deskops.operations import DeskopsOperations


class AtomsCLI:
    def run(self, args: Any) -> int:
        root = Path(getattr(args, "root", ".")).resolve()
        registry_path = default_registry_path(root)
        operations = DeskopsOperations(root)

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

        if args.atoms_command == "validate":
            try:
                results = operations.validate_atoms(args.doc_id if not getattr(args, "all", False) else None)
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            invalid = False
            for record in results:
                print(f"Atom: {record['id']}")
                print(f"Path: {record['path']}")
                if record["errors"]:
                    invalid = True
                    for error in record["errors"]:
                        print(f"- {error}")
                else:
                    print("- valid")
            return 1 if invalid else 0

        if args.atoms_command == "delete":
            try:
                record = operations.delete_atom(args.doc_id, force=bool(getattr(args, "force", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Deleted atom {record.doc_id}")
            print(f"Path: {record.path}")
            print(f"Store untracked: {'yes' if record.kind == 'atom-untracked' else 'no'}")
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

        return 1
