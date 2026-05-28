from pydantic import Field

from .base import PrimitiveDoc


class EdgeDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "edge"], "workspace": ["desk", "primitives"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Source

⸢rev•source⸥

## Target

⸢rev•target⸥

## Condition

⸢rev•condition_ref⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    source: str = Field(description="Source node identifier.")
    target: str = Field(description="Target node identifier.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the transition.")
