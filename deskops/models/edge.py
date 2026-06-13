from pydantic import Field

from .base import PrimitiveDoc


class EdgeDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "edge"], "workspace": ["desk", "primitives"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
source: ⸢rev•source⸥
target: ⸢rev•target⸥
condition_ref: ⸢rev•condition_ref⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    source: str = Field(description="Source node identifier.")
    target: str = Field(description="Target node identifier.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the transition.")
