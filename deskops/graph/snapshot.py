from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.graph.extract_coverage import EXTRACTOR_NAME as COVERAGE_EXTRACTOR
from deskops.graph.extract_coverage import CoverageGraphEdge
from deskops.graph.extract_coverage import extract_coverage_graph
from deskops.graph.extract_docs import EXTRACTOR_NAME as DOC_NODE_EXTRACTOR
from deskops.graph.extract_docs import extract_doc_nodes
from deskops.graph.extract_edges import EXTRACTOR_NAME as DECLARED_EDGE_EXTRACTOR
from deskops.graph.extract_edges import DeclaredGraphEdge
from deskops.graph.extract_edges import extract_declared_edges
from deskops.graph.extract_sources import EXTRACTOR_NAME as SOURCE_FILE_NODE_EXTRACTOR
from deskops.graph.extract_sources import extract_source_file_nodes


SNAPSHOT_SCHEMA = "deskops_kgdb_graph_snapshot_v1"
SNAPSHOT_EXTRACTOR = "deskops_kgdb_snapshot_v1"
DEFAULT_SNAPSHOT_PATH = Path(".sldb/runtime/knowledge_graph.kg.json")


class GraphSnapshotCapabilityError(RuntimeError):
    """Raised when KGDB snapshot validation support is unavailable."""


class GraphSnapshotReadError(RuntimeError):
    """Raised when an existing graph snapshot cannot satisfy a read query."""


def read_graph_neighbors(snapshot_path: Path, node_id: str) -> dict[str, Any]:
    """Return incoming and outgoing neighbors for one node from a graph snapshot."""
    if not snapshot_path.exists() or not snapshot_path.is_file():
        raise GraphSnapshotReadError(f"graph snapshot not found: {snapshot_path}")

    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    nodes = _snapshot_nodes_by_id(snapshot)
    if node_id not in nodes:
        raise GraphSnapshotReadError(f"graph node not found: {node_id}")

    edges = _snapshot_edges(snapshot)
    return {
        "node": nodes[node_id],
        "incoming": [edge for edge in edges if edge["target"] == node_id],
        "outgoing": [edge for edge in edges if edge["source"] == node_id],
        "nodes": nodes,
    }


def build_graph_snapshot(root: Path) -> dict[str, Any]:
    """Build a KGDB GraphSnapshot-compatible payload from deskops extractors."""
    project_root = root.resolve()
    doc_nodes = [node.to_dict() for node in extract_doc_nodes(project_root)]
    source_nodes = [node.to_dict() for node in extract_source_file_nodes(project_root)]
    edge_result = extract_declared_edges(project_root)
    coverage_result = extract_coverage_graph(project_root)

    nodes_by_id = _merge_nodes([*doc_nodes, *source_nodes, *[node.to_dict() for node in coverage_result.nodes]])
    all_edges = [*edge_result.edges, *coverage_result.edges]
    edges_by_source = _edges_by_source(all_edges)
    snapshot_nodes = [
        _kgdb_node(node, edges_by_source.get(node_id, []))
        for node_id, node in sorted(nodes_by_id.items())
    ]

    return {
        "version": "1.0",
        "nodes": snapshot_nodes,
        "metadata": {
            "schema": SNAPSHOT_SCHEMA,
            "extractor": SNAPSHOT_EXTRACTOR,
            "runtime_output_path": DEFAULT_SNAPSHOT_PATH.as_posix(),
            "source_extractors": [
                DOC_NODE_EXTRACTOR,
                SOURCE_FILE_NODE_EXTRACTOR,
                DECLARED_EDGE_EXTRACTOR,
                COVERAGE_EXTRACTOR,
            ],
            "node_count": len(snapshot_nodes),
            "edge_count": len(all_edges),
        },
    }


def write_graph_snapshot(
    root: Path,
    output_path: Path | None = None,
) -> Path:
    """Write the generated graph snapshot to the ignored runtime output path."""
    destination = output_path or root / DEFAULT_SNAPSHOT_PATH
    snapshot = build_graph_snapshot(root)
    _validate_graph_snapshot(snapshot)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def _validate_graph_snapshot(snapshot: dict[str, Any]) -> None:
    try:
        from kgdb.contracts.io import GraphSnapshot
    except ImportError as exc:
        raise GraphSnapshotCapabilityError(
            "KGDB graph snapshot validation is unavailable; install kgdb before running `deskops graph build`."
        ) from exc

    GraphSnapshot.model_validate(snapshot)


def _snapshot_nodes_by_id(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    for node in snapshot.get("nodes", []):
        if "id" in node:
            nodes[node["id"]] = node
            continue

        identity = node.get("identity", {})
        node_id = identity.get("node_id")
        if node_id:
            semantics = node.get("semantics", {})
            nodes[node_id] = {
                "id": node_id,
                "kind": identity.get("node_type"),
                "label": semantics.get("title") or semantics.get("label") or node_id,
                **semantics,
            }
    return nodes


def _snapshot_edges(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    if "edges" in snapshot:
        return [
            {
                "source": edge["source"],
                "target": edge["target"],
                "role": edge.get("role") or edge.get("relation_type") or "related",
            }
            for edge in snapshot.get("edges", [])
        ]

    edges: list[dict[str, Any]] = []
    for node in snapshot.get("nodes", []):
        identity = node.get("identity", {})
        source_id = identity.get("node_id")
        if not source_id:
            continue

        for edge in node.get("edges", []):
            edges.append(
                {
                    "source": source_id,
                    "target": edge["target_id"],
                    "role": edge.get("relation_type") or "related",
                }
            )
    return edges


def _merge_nodes(nodes: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for node in nodes:
        node_id = node["id"]
        if node_id not in merged:
            merged[node_id] = {**node, "provenance": [node["provenance"]]}
            continue

        current = merged[node_id]
        current["provenance"].append(node["provenance"])
        for key, value in node.items():
            if key == "provenance" or value is None:
                continue
            current.setdefault(key, value)
    return merged


def _edges_by_source(edges: list[DeclaredGraphEdge | CoverageGraphEdge]) -> dict[str, list[DeclaredGraphEdge | CoverageGraphEdge]]:
    grouped: dict[str, list[DeclaredGraphEdge | CoverageGraphEdge]] = {}
    for edge in edges:
        grouped.setdefault(edge.source_id, []).append(edge)
    return grouped


def _kgdb_node(node: dict[str, Any], edges: list[DeclaredGraphEdge | CoverageGraphEdge]) -> dict[str, Any]:
    node_id = node["id"]
    node_kind = node["kind"]
    return {
        "identity": {
            "node_id": node_id,
            "node_type": node_kind,
        },
        "edges": [_kgdb_edge(edge) for edge in edges],
        "semantics": {
            key: value
            for key, value in node.items()
            if key not in {"id", "kind", "provenance"} and value is not None
        },
        "source": {
            "extractor": SNAPSHOT_EXTRACTOR,
            "provenance": node["provenance"],
        },
    }


def _kgdb_edge(edge: DeclaredGraphEdge | CoverageGraphEdge) -> dict[str, Any]:
    metadata = {
        "role": edge.role,
        "source_kind": edge.source_kind,
        "confidence": edge.confidence,
        "provenance_path": edge.provenance_path,
        "provenance_locator": edge.provenance_locator,
        "extractor": edge.extractor,
    }
    for key in ("atom_id", "facet", "score", "match_basis", "evidence", "source_field"):
        value = getattr(edge, key, None)
        if value is not None:
            metadata[key] = value
    return {
        "target_id": edge.target_id,
        "relation_type": edge.role,
        "metadata": metadata,
    }
