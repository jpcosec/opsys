"""Test oracle: the lifecycle transitions as deskops read them before they were read from
the desk's own store (deskops 9ced34e5, wt/board-perf): the edge index composed with the
linked stores. Tests compare the live path against it; nothing in ``deskops`` imports it.

The closeout graph part of this oracle (the frozen full scan of ``tests/graph_oracle_v1``)
was compared with sldb's project graph over the real desk and removed by CC33c.
"""

from __future__ import annotations

from pathlib import Path

from deskops import lifecycle

__all__ = ["transitions_from_v1"]


# ------------------------------------------------------------------ lifecycle
def transitions_from_v1(root: Path, node: str) -> list[lifecycle.Transition]:
    """``lifecycle.transitions_from`` as it was: the index composed with the linked stores."""
    from sldb.api import edges_from

    found: list[lifecycle.Transition] = []
    for edge in edges_from(root / ".sldb", lifecycle.ritual_export_id(node)):
        if edge.metadata.get("origin") != "relation_doc" or not edge.target.rsplit("/", 1)[-1].startswith("RitualDoc:"):
            continue
        attributes = edge.metadata.get("attributes") or {}
        found.append(
            lifecycle.Transition(
                relation_type=edge.relation,
                source=node,
                target=edge.target.rsplit(":", 1)[-1],
                condition=str(edge.metadata.get("condition") or ""),
                sets=dict(attributes.get("sets") or {}),
                terminal=bool(attributes.get("terminal")),
                relation_doc=str(edge.metadata.get("relation_doc") or ""),
            )
        )
    return found
