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
        if args.command == "atoms":
            from desk.cli.commands.atoms import AtomsCLI

            return AtomsCLI().run(args)
        if args.command == "graph":
            return self._graph(args)
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

    def _graph(self, args: Any) -> int:
        if args.graph_command == "build":
            return self._graph_build(args)
        if args.graph_command == "neighbors":
            return self._graph_neighbors(args)
        if args.graph_command == "missing":
            return self._graph_missing(args)

        print(f"Unknown graph command: {args.graph_command}")
        return 2

    def _graph_build(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        try:
            from deskops.graph.snapshot import GraphSnapshotCapabilityError
            from deskops.graph.snapshot import write_graph_snapshot

            output_path = write_graph_snapshot(root)
        except GraphSnapshotCapabilityError as exc:
            print(f"Error: {exc}")
            return 1

        print(f"Graph snapshot written: {output_path}")
        return 0

    def _graph_neighbors(self, args: Any) -> int:
        root = Path(args.root).resolve()
        from deskops.graph.snapshot import DEFAULT_SNAPSHOT_PATH

        graph_path = Path(args.graph).resolve() if args.graph else root / DEFAULT_SNAPSHOT_PATH

        try:
            from deskops.graph.snapshot import GraphSnapshotReadError
            from deskops.graph.snapshot import read_graph_neighbors

            neighbors = read_graph_neighbors(graph_path, args.id)
        except GraphSnapshotReadError as exc:
            print(f"Error: {exc}")
            return 1

        self._print_graph_neighbors(args.id, neighbors)
        return 0

    def _graph_missing(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        graph_path = Path(args.graph).resolve() if args.graph else None
        try:
            from deskops.graph.checks import GraphMissingCheckError
            from deskops.graph.checks import find_missing_graph_references

            findings = find_missing_graph_references(root, graph_path)
        except GraphMissingCheckError as exc:
            print(f"Error: {exc}")
            return 1

        if not findings:
            print("No missing graph references found.")
            return 0

        print("Missing graph references:")
        for finding in findings:
            print(f"- {finding.kind}: {finding.source_id} -> {finding.target_id}")
            if finding.role:
                print(f"  role: {finding.role}")
            if finding.provenance_path:
                locator = f":{finding.provenance_locator}" if finding.provenance_locator else ""
                print(f"  provenance: {finding.provenance_path}{locator}")
            print(f"  reason: {finding.reason}")
        return 1

    def _print_graph_neighbors(self, node_id: str, neighbors: dict[str, Any]) -> None:
        nodes = neighbors["nodes"]
        node = neighbors["node"]
        print(f"Node: {node_id} ({_graph_node_label(node)})")
        print("Outgoing:")
        if neighbors["outgoing"]:
            for edge in neighbors["outgoing"]:
                target = nodes.get(edge["target"], {"id": edge["target"]})
                print(f"- {edge['role']} -> {edge['target']} ({_graph_node_label(target)})")
        else:
            print("- none")

        print("Incoming:")
        if neighbors["incoming"]:
            for edge in neighbors["incoming"]:
                source = nodes.get(edge["source"], {"id": edge["source"]})
                print(f"- {edge['source']} ({_graph_node_label(source)}) -> {edge['role']}")
        else:
            print("- none")

    def _apply_default_pythonpath(self, args: Any, bootstrap: SLDBBootstrap) -> None:
        if not hasattr(args, "pythonpath"):
            return
        if getattr(args, "pythonpath"):
            return
        args.pythonpath = bootstrap.default_pythonpath()


def _graph_node_label(node: dict[str, Any]) -> str:
    return str(node.get("label") or node.get("title") or node.get("id"))


def main(argv: Any = None) -> int:
    try:
        return CLI().run(argv)
    except SystemExit:
        raise
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(f"Missing required field: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"Invalid value: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        if exc.__class__.__name__ == "ValidationError":
            print(f"Validation error:\n{exc}", file=sys.stderr)
            return 1
        if exc.__class__.__name__ == "SLDBStoreError":
            print(f"Store error: {exc}", file=sys.stderr)
            return 1
        raise SystemExit(f"Unexpected: {exc}")


if __name__ == "__main__":
    sys.exit(main())
