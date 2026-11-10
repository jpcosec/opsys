"""The desk graph as the graph commands read it: nodes and flat edges.

By default the view is sldb's project graph (GD21) with the desk configuration of
``desk_graph.py``: ``graph neighbors``, ``graph missing``, ``graph reflect`` and ``drift check``
read it directly, with no snapshot built first. A ``--graph`` path names a graph file the
caller already has (a hand-written fixture, a KGDB snapshot some other tool wrote); it is read
as given.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from deskops.graph.desk_graph import desk_graph


class GraphReadError(RuntimeError):
    """Raised when a graph file cannot satisfy a read query."""


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
class GraphView:
    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)


def project_graph_view(root: Path) -> GraphView:
    """The desk's project graph (sldb, GD21): every node, and every declared edge leaving a node."""
    graph = desk_graph(Path(root).resolve())
    nodes: dict[str, Node] = {}
    for node in (*graph.nodes.documents, *graph.nodes.files):
        nodes.setdefault(node.id, Node(id=node.id, kind=node.kind, path=node.path, identity=node.identity, label=getattr(node, "label", None) or node.id))
    edges = [
        Edge(edge.source_id, edge.target_id, edge.role, edge.provenance_path, edge.provenance_locator, edge.extractor)
        for edge in graph.extraction().edges
        if edge.source_id in nodes
    ]
    return GraphView(nodes=[nodes[node_id] for node_id in sorted(nodes)], edges=sorted(edges, key=lambda edge: edge.source))


def graph_view(root: Path, graph_path: Path | None) -> GraphView:
    """The graph file at ``graph_path`` when one is given, else the desk's project graph."""
    return read_graph_file(graph_path) if graph_path is not None else project_graph_view(root)


def graph_neighbors(view: GraphView, node_id: str) -> dict[str, Any]:
    """Incoming and outgoing neighbors of one node."""
    nodes = _neighbor_nodes(view.nodes)
    if node_id not in nodes:
        raise GraphReadError(f"graph node not found: {node_id}")
    edges = [{"source": edge.source, "target": edge.target, "role": edge.role} for edge in view.edges]
    return {
        "node": nodes[node_id],
        "incoming": [edge for edge in edges if edge["target"] == node_id],
        "outgoing": [edge for edge in edges if edge["source"] == node_id],
        "nodes": nodes,
    }


def read_graph_file(path: Path) -> GraphView:
    """Read a graph file (simple ``nodes``/``edges`` JSON or a KGDB snapshot) into nodes and flat edges."""
    if not path.exists() or not path.is_file():
        raise GraphReadError(f"graph snapshot not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise GraphReadError(f"graph snapshot is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise GraphReadError(f"graph snapshot must be a JSON object: {path}")
    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, list):
        raise GraphReadError(f"graph snapshot is missing the nodes list: {path}")

    nodes: list[Node] = []
    nested_edges: list[Edge] = []
    for raw_node in raw_nodes:
        if not isinstance(raw_node, dict):
            raise GraphReadError(f"graph snapshot contains a non-object node: {path}")
        node = _read_node(raw_node, path)
        nodes.append(node)
        nested_edges.extend(_read_edges(raw_node.get("edges"), path, source=node.id))
    if "edges" in payload:
        if not isinstance(payload["edges"], list):
            raise GraphReadError(f"graph snapshot edges must be a list: {path}")
        return GraphView(nodes=nodes, edges=_read_edges(payload["edges"], path))
    return GraphView(nodes=nodes, edges=nested_edges)


def _read_node(raw_node: dict[str, Any], path: Path) -> Node:
    identity = raw_node.get("identity")
    semantics = raw_node.get("semantics") if isinstance(raw_node.get("semantics"), dict) else {}
    node_id = raw_node.get("id")
    if not isinstance(node_id, str) and isinstance(identity, dict):
        node_id = identity.get("node_id")
    if not isinstance(node_id, str) or not node_id:
        raise GraphReadError(f"graph snapshot node is missing its id: {path}")
    kind = raw_node.get("kind")
    if not isinstance(kind, str) and isinstance(identity, dict):
        kind = identity.get("node_type")
    node_path = raw_node.get("path")
    if not isinstance(node_path, str):
        node_path = semantics.get("path") if isinstance(semantics.get("path"), str) else None
    label = semantics.get("title") or raw_node.get("label") or semantics.get("label") or node_id
    return Node(
        id=node_id,
        kind=kind if isinstance(kind, str) else None,
        path=node_path,
        identity=identity if isinstance(identity, (dict, str)) else None,
        label=str(label),
    )


def _read_edges(raw_edges: Any, path: Path, source: str | None = None) -> list[Edge]:
    """Edges nested under ``source`` (direct fields win) or listed at the top level (metadata wins)."""
    if raw_edges is None and source is not None:
        return []
    if not isinstance(raw_edges, list):
        raise GraphReadError(f"graph snapshot node edges must be a list: {path}")
    edges: list[Edge] = []
    for raw_edge in raw_edges:
        if not isinstance(raw_edge, dict):
            raise GraphReadError(f"graph snapshot contains a non-object edge: {path}")
        metadata = raw_edge.get("metadata") if isinstance(raw_edge.get("metadata"), dict) else {}
        edge_source = source if source is not None else _end(raw_edge, "source")
        if not edge_source:
            raise GraphReadError(f"graph snapshot edge is missing its source: {path}")
        target = _end(raw_edge, "target")
        if not target:
            raise GraphReadError(f"graph snapshot edge is missing its target: {path}")
        direct_role = raw_edge.get("relation_type") if source is not None else raw_edge.get("role") or raw_edge.get("relation_type")
        role = direct_role or metadata.get("role") or "related"
        edges.append(Edge(edge_source, target, str(role), **_provenance(raw_edge, metadata, metadata_wins=source is None)))
    return edges


def _end(raw_edge: dict[str, Any], end: str) -> str | None:
    value = raw_edge.get(end)
    if not isinstance(value, str):
        value = raw_edge.get(f"{end}_id")
    return value if isinstance(value, str) and value else None


def _provenance(raw_edge: dict[str, Any], metadata: dict[str, Any], *, metadata_wins: bool) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for key in ("provenance_path", "provenance_locator", "extractor"):
        direct = raw_edge.get(key) if isinstance(raw_edge.get(key), str) else None
        meta = metadata.get(key) if isinstance(metadata.get(key), str) else None
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
