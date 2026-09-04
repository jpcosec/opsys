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

        if args.atoms_command == "create":
            try:
                result = operations.create_atom_from_source(
                    args.doc_id,
                    five_wh_one_plus=args.five_wh_one_plus,
                    title=getattr(args, "title", None),
                    tags=list(args.tag or []),
                    from_pill=getattr(args, "from_pill", None),
                    from_graph=getattr(args, "from_graph", None),
                    from_diagram=getattr(args, "from_diagram", None),
                    graph_path=getattr(args, "graph", None),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Created atom {result.doc_id}")
            print(f"Path: {result.path}")
            print(f"Source kind: {result.source_kind}")
            print(f"Source selector: {result.source_selector}")
            print(f"Source provenance: {result.provenance}")
            return 0

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

        if args.atoms_command == "split":
            try:
                result = operations.split_atom(
                    args.doc_id,
                    into_ids=list(args.into or []),
                    section_flags=list(args.section or []),
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Split atom {result.original_id}")
            print(f"Original path: {result.original_path}")
            for record in result.created:
                print(f"Created atom {record.doc_id} at {record.path}")
            print(f"Original kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            if result.inbound_references:
                print("Inbound references acknowledged:")
                for item in result.inbound_references:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "merge":
            try:
                result = operations.merge_atom(
                    args.doc_id,
                    into_selector=args.into,
                    force=bool(getattr(args, "force", False)),
                )
            except (FileNotFoundError, ValueError, FileExistsError, RuntimeError) as exc:
                print(f"Error: {exc}")
                return 1
            print(f"Merged atom {result.source_id} into {result.target_id}")
            print(f"Source path: {result.source_path}")
            print(f"Target path: {result.target_path}")
            print(f"Source kept as redirect stub: {'yes' if result.redirect_kept else 'no'}")
            print(f"Inbound references rewritten: {len(result.rewritten_references)}")
            if result.rewritten_references:
                for item in result.rewritten_references:
                    print(f"- {item}")
            if result.ambiguities:
                print("Merge ambiguities acknowledged:")
                for item in result.ambiguities:
                    print(f"- {item}")
            return 0

        if args.atoms_command == "reorganize":
            try:
                report = operations.reorganize_atoms(dry_run=bool(getattr(args, "dry_run", False)))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            verb = "Would move" if report["dry_run"] else "Moved"
            print(f"Folder axis: {report['axis']}")
            if not report["moves"]:
                print("No atoms need to move.")
            for move in report["moves"]:
                print(f"{verb} {move['id']}: {move['from']} -> {move['to']}")
            for error in report["errors"]:
                print(f"Skipped: {error}")
            return 1 if report["errors"] else 0

        if args.atoms_command == "list":
            try:
                axis, payloads = operations.list_atoms(getattr(args, "axis_value", None))
            except (FileNotFoundError, ValueError) as exc:
                print(f"Error: {exc}")
                return 1
            if getattr(args, "format", "text") == "json":
                import json
                print(json.dumps({"axis": axis, "atoms": payloads}, indent=2, default=str))
                return 0
            for payload in payloads:
                label = payload.get("title") or payload["id"]
                if axis:
                    values = ",".join(payload.get("axis_values") or []) or "-"
                    print(f"{payload['id']} | {label} | {axis}:{values}")
                else:
                    print(f"{payload['id']} | {label}")
            return 0

        if args.atoms_command == "show":
            args.command = "show"
            args.subject = "atom"
            from deskops.cli.commands.operations import OperationsCLI
            return OperationsCLI().run(args)

        return 1
