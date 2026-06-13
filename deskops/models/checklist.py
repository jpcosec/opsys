from pydantic import Field

from .base import PrimitiveDoc


class ChecklistDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "checklist"], "workspace": ["desk", "primitives"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
condition_refs: ⸢rev•condition_refs⸥
mode: ⸢rev•mode⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥

## Items

- ⸢rev,list•items⸥

""".strip()

    items: list[str] = Field(default_factory=list, description="Human-readable checklist items.")
    condition_refs: list[str] = Field(
        default_factory=list,
        description="Condition identifiers that determine completion.",
    )
    mode: str = Field(default="all", description="Checklist completion mode, such as all or any.")
