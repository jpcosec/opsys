from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.errors import UsageError


class GraphCLI:
    def run(self, args: Any) -> int:
        if args.graph_command == "build":
            return self._build(args)
        if args.graph_command == "neighbors":
            return self._neighbors(args)
        if args.graph_command == "missing":
            return self._missing(args)
        if args.graph_command == "reflect":
            return self._reflect(args)
        raise UsageError(f"Unknown graph command: {args.graph_command}")

    def _build(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        from deskops.graph.snapshot import GraphSnapshotCapabilityError
        from deskops.graph.snapshot import networkx_path_for_snapshot
        from deskops.graph.snapshot import write_graph_snapshot

        try:
            requested_output = Path(args.output) if args.output else None
            if requested_output is not None and not requested_output.is_absolute():
                requested_output = root / requested_output
            output_path = (
                write_graph_snapshot(root, requested_output)
                if requested_output is not None
                else write_graph_snapshot(root)
            )

            from sldb.api.graph.snapshot import snapshot_load
            from sldb.store.graph.graph_io import save_graph

            save_graph(snapshot_load(output_path), networkx_path_for_snapshot(output_path))

        except GraphSnapshotCapabilityError as exc:
            print(f"Error: {exc}")
            return 1

        print(f"Graph snapshot written: {output_path}")
        return 0

    def _neighbors(self, args: Any) -> int:
        root = Path(args.root).resolve()
        from deskops.graph.snapshot import GraphSnapshotReadError
        from deskops.graph.snapshot import default_snapshot_read_path
        from deskops.graph.snapshot import read_graph_neighbors

        graph_path = Path(args.graph).resolve() if args.graph else default_snapshot_read_path(root)

        try:
            neighbors = read_graph_neighbors(graph_path, args.id)
        except GraphSnapshotReadError as exc:
            print(f"Error: {exc}")
            return 1

        self._print_neighbors(args.id, neighbors)
        return 0

    def _missing(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        # Imported outside the try: a failing import must surface as itself,
        # not as an unbound name in the except clause.
        from deskops.graph.checks import GraphMissingCheckError
        from deskops.graph.checks import find_missing_graph_references

        graph_path = Path(args.graph).resolve() if args.graph else None
        try:
            findings = find_missing_graph_references(root, graph_path)
        except GraphMissingCheckError as exc:
            print(f"Error: {exc}")
            return 1

        if not findings:
            print("No missing graph references found.")
            return 0

        failing = [finding for finding in findings if not finding.record]
        informational = [finding for finding in findings if finding.record]

        if failing:
            print("Missing graph references:")
            for finding in failing:
                self._print_missing_finding(finding)
        if informational:
            print("Informational (archived records):")
            for finding in informational:
                self._print_missing_finding(finding)

        print(f"{len(failing)} missing, {len(informational)} informational")
        return 1 if failing else 0

    def _print_missing_finding(self, finding: Any) -> None:
        print(f"- {finding.kind}: {finding.source_id} -> {finding.target_id}")
        if finding.role:
            print(f"  role: {finding.role}")
        if finding.provenance_path:
            locator = f":{finding.provenance_locator}" if finding.provenance_locator else ""
            print(f"  provenance: {finding.provenance_path}{locator}")
        print(f"  reason: {finding.reason}")

    def _reflect(self, args: Any) -> int:
        root = Path(args.root).resolve()
        if not root.exists() or not root.is_dir():
            print(f"Error: graph root is not a directory: {root}")
            return 1

        from deskops.graph.snapshot import GraphSnapshotReadError
        from deskops.graph.snapshot import default_snapshot_read_path
        from deskops.graph.snapshot import read_graph_snapshot

        graph_path = Path(args.graph).resolve() if args.graph else default_snapshot_read_path(root)
        from deskops.graph.checks import GraphMissingCheckError
        from deskops.graph.self_reflection import build_self_reflection_report
        from deskops.graph.self_reflection import write_self_reflection_report

        try:
            snapshot = read_graph_snapshot(graph_path)
            report = build_self_reflection_report(snapshot)
            output_path = write_self_reflection_report(root, report)
        except (GraphSnapshotReadError, GraphMissingCheckError) as exc:
            print(f"Error: {exc}")
            return 1

        summary = report["summary"]
        print(f"Self-reflection report written: {output_path}")
        print(f"Findings: {summary['finding_count']}")
        print(f"Suppressed duplicates: {summary['suppressed_duplicate_count']}")
        return 0

    def _print_neighbors(self, node_id: str, neighbors: dict[str, Any]) -> None:
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


def _graph_node_label(node: dict[str, Any]) -> str:
    return str(node.get("label") or node.get("title") or node.get("id"))
