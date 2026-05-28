from pydantic import Field

from .base import PrimitiveDoc


class RoutineDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "routine"], "workspace": ["desk", "routines"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Entrypoint

⸢rev•entrypoint⸥

## Decomposition

- ⸢rev,list•decomposition⸥

## Edges

- ⸢rev,list•edges⸥

## Terminal Nodes

- ⸢rev,list•terminal_nodes⸥

## Tags

- ⸢rev,list•tags⸥
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
