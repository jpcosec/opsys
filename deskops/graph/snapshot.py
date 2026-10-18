from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from deskops.graph.extract_docs import EXTRACTOR_NAME as DOC_NODE_EXTRACTOR
from deskops.graph.extract_docs import extract_doc_nodes
from deskops.graph.extract_edges import EXTRACTOR_NAME as DECLARED_EDGE_EXTRACTOR
from deskops.graph.extract_edges import DeclaredGraphEdge
from deskops.graph.extract_edges import extract_declared_edges
from deskops.graph.extract_sources import EXTRACTOR_NAME as SOURCE_FILE_NODE_EXTRACTOR
from deskops.graph.extract_sources import extract_source_file_nodes


SNAPSHOT_SCHEMA = "deskops_kgdb_graph_snapshot_v1"
SNAPSHOT_EXTRACTOR = "deskops_kgdb_snapshot_v1"
DEFAULT_SNAPSHOT_PATH = Path(".sldb/runtime/graphs/deskops.kg.json")
LEGACY_SNAPSHOT_PATH = Path(".sldb/runtime/knowledge_graph.kg.json")


class GraphSnapshotCapabilityError(RuntimeError):
    """Raised when sldb graph snapshot validation support is unavailable."""


class GraphSnapshotReadError(RuntimeError):
    """Raised when an existing graph snapshot cannot satisfy a read query."""


@dataclass(frozen=True)
class Node:
    id: str
    kind: str | None = None
    path: str | None = None
    identity: dict[str, Any] | str | None = None
    label: str | None = None


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    role: str = "related"
    provenance_path: str | None = None
    provenance_locator: str | None = None
    extractor: str | None = None


@dataclass(frozen=True)
class GraphSnapshot:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)


def networkx_path_for_snapshot(snapshot_path: Path) -> Path:
    """Return the sibling NetworkX path for a GraphSnapshot destination."""
    without_json = snapshot_path.with_suffix("")
    if without_json.suffix == ".kg":
        return without_json.with_suffix(".nx.json")
    return snapshot_path.with_suffix(".nx.json")


def default_snapshot_read_path(root: Path) -> Path:
    """Prefer the DeskOps projection and fall back to the read-only legacy path."""
    preferred = root / DEFAULT_SNAPSHOT_PATH
    if preferred.exists():
        return preferred
    legacy = root / LEGACY_SNAPSHOT_PATH
    return legacy if legacy.exists() else preferred


def read_graph_snapshot(path: Path) -> GraphSnapshot:
    """Read a graph snapshot from disk into nodes and flat edges."""
    if not path.exists() or not path.is_file():
        raise GraphSnapshotReadError(f"graph snapshot not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GraphSnapshotReadError(f"graph snapshot is not valid JSON: {path}") from exc

    if not isinstance(payload, dict):
        raise GraphSnapshotReadError(f"graph snapshot must be a JSON object: {path}")

    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, list):
        raise GraphSnapshotReadError(f"graph snapshot is missing the nodes list: {path}")

    nodes: list[Node] = []
    nested_edges: list[Edge] = []
    for raw_node in raw_nodes:
        if not isinstance(raw_node, dict):
            raise GraphSnapshotReadError(f"graph snapshot contains a non-object node: {path}")
        node = _read_node(raw_node, path)
        nodes.append(node)
        nested_edges.extend(_read_nested_edges(raw_node, node.id, path))

    if "edges" in payload:
        raw_edges = payload["edges"]
        if not isinstance(raw_edges, list):
            raise GraphSnapshotReadError(f"graph snapshot edges must be a list: {path}")
        edges = [_read_top_level_edge(raw_edge, path) for raw_edge in raw_edges]
    else:
        edges = nested_edges

    return GraphSnapshot(nodes=nodes, edges=edges)


def read_graph_neighbors(snapshot_path: Path, node_id: str) -> dict[str, Any]:
    """Return incoming and outgoing neighbors for one node from a graph snapshot."""
    snapshot = read_graph_snapshot(snapshot_path)
    nodes = _neighbor_nodes(snapshot.nodes)
    if node_id not in nodes:
        raise GraphSnapshotReadError(f"graph node not found: {node_id}")

    edges = [
        {"source": edge.source, "target": edge.target, "role": edge.role}
        for edge in snapshot.edges
    ]
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

    nodes_by_id = _merge_nodes([*doc_nodes, *source_nodes])
    all_edges = edge_result.edges
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
            ],
            "node_count": len(snapshot_nodes),
            "edge_count": len(all_edges),
        },
    }


def _read_node(raw_node: dict[str, Any], path: Path) -> Node:
    identity = raw_node.get("identity")
    semantics = raw_node.get("semantics")
    if not isinstance(semantics, dict):
        semantics = {}

    node_id = raw_node.get("id")
    if not isinstance(node_id, str) and isinstance(identity, dict):
        node_id = identity.get("node_id")
    if not isinstance(node_id, str) or not node_id:
        raise GraphSnapshotReadError(f"graph snapshot node is missing its id: {path}")

    kind = raw_node.get("kind")
    if not isinstance(kind, str) and isinstance(identity, dict):
        kind = identity.get("node_type")

    node_path = raw_node.get("path")
    if not isinstance(node_path, str):
        node_path = semantics.get("path") if isinstance(semantics.get("path"), str) else None

    label = (
        semantics.get("title")
        or raw_node.get("label")
        or semantics.get("label")
        or node_id
    )
    return Node(
        id=node_id,
        kind=kind if isinstance(kind, str) else None,
        path=node_path,
        identity=identity if isinstance(identity, (dict, str)) else None,
        label=str(label),
    )


def _read_nested_edges(raw_node: dict[str, Any], source_id: str, path: Path) -> list[Edge]:
    raw_edges = raw_node.get("edges")
    if raw_edges is None:
        return []
    if not isinstance(raw_edges, list):
        raise GraphSnapshotReadError(f"graph snapshot node edges must be a list: {path}")

    edges: list[Edge] = []
    for raw_edge in raw_edges:
        if not isinstance(raw_edge, dict):
            raise GraphSnapshotReadError(f"graph snapshot contains a non-object edge: {path}")
        metadata = raw_edge.get("metadata")
        metadata = metadata if isinstance(metadata, dict) else {}
        target = raw_edge.get("target")
        if not isinstance(target, str):
            target = raw_edge.get("target_id")
        if not isinstance(target, str) or not target:
            raise GraphSnapshotReadError(f"graph snapshot edge is missing its target: {path}")
        role = raw_edge.get("relation_type") or metadata.get("role") or "related"
        edges.append(
            Edge(
                source=source_id,
                target=target,
                role=str(role),
                **_edge_provenance(raw_edge, metadata, metadata_wins=False),
            )
        )
    return edges


def _read_top_level_edge(raw_edge: Any, path: Path) -> Edge:
    if not isinstance(raw_edge, dict):
        raise GraphSnapshotReadError(f"graph snapshot contains a non-object edge: {path}")
    metadata = raw_edge.get("metadata")
    metadata = metadata if isinstance(metadata, dict) else {}

    source = raw_edge.get("source")
    if not isinstance(source, str):
        source = raw_edge.get("source_id")
    if not isinstance(source, str) or not source:
        raise GraphSnapshotReadError(f"graph snapshot edge is missing its source: {path}")

    target = raw_edge.get("target")
    if not isinstance(target, str):
        target = raw_edge.get("target_id")
    if not isinstance(target, str) or not target:
        raise GraphSnapshotReadError(f"graph snapshot edge is missing its target: {path}")

    role = raw_edge.get("role") or raw_edge.get("relation_type") or metadata.get("role") or "related"
    return Edge(
        source=source,
        target=target,
        role=str(role),
        **_edge_provenance(raw_edge, metadata, metadata_wins=True),
    )


def _edge_provenance(
    raw_edge: dict[str, Any],
    metadata: dict[str, Any],
    *,
    metadata_wins: bool,
) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for key in ("provenance_path", "provenance_locator", "extractor"):
        direct = raw_edge.get(key)
        meta = metadata.get(key)
        direct = direct if isinstance(direct, str) else None
        meta = meta if isinstance(meta, str) else None
        values[key] = (meta if meta is not None else direct) if metadata_wins else (direct if direct is not None else meta)
    return values


def _neighbor_nodes(nodes: list[Node]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        item: dict[str, Any] = {"id": node.id, "kind": node.kind, "label": node.label}
        if node.identity is not None:
            item["identity"] = node.identity
        if node.path is not None:
            item["path"] = node.path
        by_id[node.id] = item
    return by_id


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
        from sldb.api.graph.snapshot import GraphSnapshot
    except ImportError as exc:
        raise GraphSnapshotCapabilityError(
            "sldb graph API unavailable (sldb.api.graph.snapshot); upgrade structuredLanguageDB before running `deskops graph build`."
        ) from exc

    GraphSnapshot.model_validate(snapshot)


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


def _edges_by_source(edges: list[DeclaredGraphEdge]) -> dict[str, list[DeclaredGraphEdge]]:
    grouped: dict[str, list[DeclaredGraphEdge]] = {}
    for edge in edges:
        grouped.setdefault(edge.source_id, []).append(edge)
    return grouped


def _kgdb_node(node: dict[str, Any], edges: list[DeclaredGraphEdge]) -> dict[str, Any]:
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


def _kgdb_edge(edge: DeclaredGraphEdge) -> dict[str, Any]:
    metadata = {
        "role": edge.role,
        "source_kind": edge.source_kind,
        "confidence": edge.confidence,
        "provenance_path": edge.provenance_path,
        "provenance_locator": edge.provenance_locator,
        "extractor": edge.extractor,
    }
    return {
        "target_id": edge.target_id,
        "relation_type": edge.role,
        "metadata": metadata,
    }
