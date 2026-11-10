"""``deskops graph build``: sldb's project graph of the desk written as a KGDB GraphSnapshot file.

The graph is sldb's (``desk_graph``); this module only lays its nodes and edges out in the
KGDB node-link shape (``sldb.api.graph.snapshot.GraphSnapshot`` validates it) at the ignored
runtime path, for tools that read a graph file. The graph commands do not read it back.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from deskops.graph.desk_graph import DECLARED_EDGE_EXTRACTOR
from deskops.graph.desk_graph import DOC_NODE_EXTRACTOR
from deskops.graph.desk_graph import SOURCE_FILE_NODE_EXTRACTOR
from deskops.graph.desk_graph import desk_graph


SNAPSHOT_SCHEMA = "deskops_kgdb_graph_snapshot_v1"
SNAPSHOT_EXTRACTOR = "deskops_kgdb_snapshot_v1"
DEFAULT_SNAPSHOT_PATH = Path(".sldb/runtime/graphs/deskops.kg.json")


class GraphSnapshotCapabilityError(RuntimeError):
    """Raised when sldb graph snapshot validation support is unavailable."""


def networkx_path_for_snapshot(snapshot_path: Path) -> Path:
    """Return the sibling NetworkX path for a GraphSnapshot destination."""
    without_json = snapshot_path.with_suffix("")
    if without_json.suffix == ".kg":
        return without_json.with_suffix(".nx.json")
    return snapshot_path.with_suffix(".nx.json")


def build_graph_snapshot(root: Path) -> dict[str, Any]:
    """The desk's project graph as a KGDB GraphSnapshot payload: one node per id, its edges nested."""
    graph = desk_graph(root.resolve())
    nodes: dict[str, dict[str, Any]] = {}
    for node in (*graph.nodes.documents, *graph.nodes.files):
        item = node.to_dict()
        merged = nodes.setdefault(item["id"], {**item, "provenance": []})
        merged["provenance"].append(item["provenance"])
        for key, value in item.items():
            if key != "provenance" and value is not None:
                merged.setdefault(key, value)
    edges = graph.extraction().edges
    by_source: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        by_source.setdefault(edge.source_id, []).append(
            {
                "target_id": edge.target_id,
                "relation_type": edge.role,
                "metadata": {
                    "role": edge.role, "source_kind": edge.source_kind, "confidence": edge.confidence,
                    "provenance_path": edge.provenance_path, "provenance_locator": edge.provenance_locator,
                    "extractor": edge.extractor,
                },
            }
        )
    snapshot_nodes = [
        {
            "identity": {"node_id": node_id, "node_type": node["kind"]},
            "edges": by_source.get(node_id, []),
            "semantics": {key: value for key, value in node.items() if key not in {"id", "kind", "provenance"} and value is not None},
            "source": {"extractor": SNAPSHOT_EXTRACTOR, "provenance": node["provenance"]},
        }
        for node_id, node in sorted(nodes.items())
    ]
    return {
        "version": "1.0",
        "nodes": snapshot_nodes,
        "metadata": {
            "schema": SNAPSHOT_SCHEMA,
            "extractor": SNAPSHOT_EXTRACTOR,
            "runtime_output_path": DEFAULT_SNAPSHOT_PATH.as_posix(),
            "source_extractors": [DOC_NODE_EXTRACTOR, SOURCE_FILE_NODE_EXTRACTOR, DECLARED_EDGE_EXTRACTOR],
            "node_count": len(snapshot_nodes),
            "edge_count": len(edges),
        },
    }


def write_graph_snapshot(root: Path, output_path: Path | None = None) -> Path:
    """Write the graph snapshot to the ignored runtime output path (or ``output_path``)."""
    destination = output_path or root / DEFAULT_SNAPSHOT_PATH
    snapshot = build_graph_snapshot(root)
    try:
        from sldb.api.graph.snapshot import GraphSnapshot
    except ImportError as exc:
        raise GraphSnapshotCapabilityError(
            "sldb graph API unavailable (sldb.api.graph.snapshot); upgrade structuredLanguageDB before running `deskops graph build`."
        ) from exc
    GraphSnapshot.model_validate(snapshot)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination
