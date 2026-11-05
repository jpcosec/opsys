"""Test oracle: the closeout graph and the lifecycle transitions as deskops read them
before they were read from sldb (deskops 9ced34e5, wt/board-perf).

The extraction is the frozen full scan in ``tests/graph_oracle_v1`` (every document and
source file of the repository extracted, ``doc_status`` asked once per document, the
declared edges of every document read); the transitions are read from the edge index
composed with the linked stores. Tests compare the live path against it; nothing in
``deskops`` imports it.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops import lifecycle
from tests.graph_oracle_v1.extract_docs import extract_doc_nodes as extract_doc_nodes_v1
from tests.graph_oracle_v1.extract_edges import DeclaredGraphEdge
from tests.graph_oracle_v1.extract_edges import extract_declared_edges as extract_declared_edges_v1
from tests.graph_oracle_v1.extract_sources import extract_source_file_nodes as extract_source_file_nodes_v1

__all__ = [
    "FullScanCloseoutGraph",
    "closeout_graph_context_v1",
    "extract_declared_edges_v1",
    "extract_doc_nodes_v1",
    "extract_source_file_nodes_v1",
    "transitions_from_v1",
]


# ------------------------------------------------------------------ closeout graph
def closeout_graph_context_v1(root: Path) -> dict[str, Any]:
    """``CloseoutGatesService.build_closeout_graph_context`` as it was."""
    root = root.resolve()
    doc_nodes = extract_doc_nodes_v1(root)
    source_nodes = extract_source_file_nodes_v1(root)
    by_path = {node.path: node.id for node in [*doc_nodes, *source_nodes]}
    extraction = extract_declared_edges_v1(root)
    invalid_materializations = {
        missing.source_id
        for missing in extraction.missing_targets
        if missing.source_id.startswith("materialization:")
    }
    return {
        "node_ids_by_path": by_path,
        "edges": extraction.edges,
        "invalid_materializations": invalid_materializations,
    }


class FullScanCloseoutGraph:
    """The old context dict behind the reader interface the closeout gate uses.

    Every query hands back the whole edge list, in the order the old gate scanned it;
    the gate's own conditions pick the edges, exactly as they did over the dict.
    """

    def __init__(self, context: dict[str, Any]) -> None:
        self.context = context
        self.invalid_materializations = context["invalid_materializations"]

    def node_id(self, relative_path: str) -> str | None:
        return self.context["node_ids_by_path"].get(relative_path)

    def edges_around(self, node_id: str) -> list[DeclaredGraphEdge]:
        return list(self.context["edges"])

    def test_link_edges(self) -> list[DeclaredGraphEdge]:
        return list(self.context["edges"])


# ------------------------------------------------------------------ lifecycle
def transitions_from_v1(root: Path, node: str) -> list[lifecycle.Transition]:
    """``lifecycle.transitions_from`` as it was: the index composed with the linked stores."""
    from sldb.api import edges_from

    spec = lifecycle.load_lifecycle_spec()
    known = {t.relation_type for t in spec.transitions}
    found: list[lifecycle.Transition] = []
    for edge in edges_from(root / ".sldb", lifecycle.ritual_export_id(node)):
        if edge.relation not in known or edge.metadata.get("origin") != "relation_doc":
            continue
        effect = spec.effect(edge.relation)
        found.append(
            lifecycle.Transition(
                relation_type=edge.relation,
                title=effect.title,
                description=effect.description,
                source=node,
                target=edge.target.rsplit(":", 1)[-1],
                condition=str(edge.metadata.get("condition") or ""),
                sets_status=effect.sets_status,
                terminal=effect.terminal,
            )
        )
    return sorted(found, key=lambda t: [x.relation_type for x in spec.transitions].index(t.relation_type))
