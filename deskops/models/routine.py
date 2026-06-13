from pydantic import Field

from .base import PrimitiveDoc


class RoutineDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "routine"], "workspace": ["desk", "routines"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
entrypoint: ⸢rev•entrypoint⸥
decomposition: ⸢rev•decomposition⸥
edges: ⸢rev•edges⸥
terminal_nodes: ⸢rev•terminal_nodes⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

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
