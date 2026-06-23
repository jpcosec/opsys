from pydantic import Field

from .base import PrimitiveDoc


class EdgeDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "edge"], "workspace": ["desk", "primitives"]}
    __template__ = """---
# edge-xxx
id: ⸢rev•id⸥
# active | archived
status: ⸢rev•status⸥
# Source node identifier
source: ⸢rev•source⸥
# Target node identifier
target: ⸢rev•target⸥
# Optional condition identifier guarding the transition
condition_ref: ⸢rev•condition_ref⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize the transition this edge represents._

⸢rev•summary⸥
""".strip()

    source: str = Field(description="Source node identifier.")
    target: str = Field(description="Target node identifier.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the transition.")
