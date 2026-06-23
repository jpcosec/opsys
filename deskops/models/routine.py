from pydantic import Field

from .base import PrimitiveDoc


class RoutineDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "routine"], "workspace": ["desk", "routines"]}
    __template__ = """---
# routine-xxx
id: ⸢rev•id⸥
# active | archived
status: ⸢rev•status⸥
# Initial node identifier
entrypoint: ⸢rev•entrypoint⸥
# Ordered or grouped primitive identifiers
decomposition: ⸢rev•decomposition⸥
# Edge identifiers composing the graph
edges: ⸢rev•edges⸥
# Terminal node identifiers
terminal_nodes: ⸢rev•terminal_nodes⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this routine does and how its nodes fit together._

⸢rev•summary⸥
""".strip()

    entrypoint: str = Field(description="Initial node identifier for the routine.")
    decomposition: list[str] = Field(
        default_factory=list,
        description="Ordered or grouped primitive identifiers participating in the routine.",
    )
    edges: list[str] = Field(default_factory=list, description="Edge identifiers composing the routine graph.")
    terminal_nodes: list[str] = Field(
        default_factory=list,
        description="Node identifiers considered terminal for the routine.",
    )
