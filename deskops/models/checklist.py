from pydantic import Field

from .base import PrimitiveDoc


class ChecklistDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "checklist"], "workspace": ["desk", "primitives"]}
    __template__ = """---
# checklist-xxx
id: ⸢rev•id⸥
# draft | active | complete | archived
status: ⸢rev•status⸥
# List of condition-xxx paths
condition_refs: ⸢rev•condition_refs⸥
# all | any
mode: ⸢rev•mode⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this checklist proves._

⸢rev•summary⸥

## Items

_List the human-readable checks in this checklist._

- ⸢rev,list•items⸥

""".strip()

    items: list[str] = Field(default_factory=list, description="Human-readable checklist items.")
    condition_refs: list[str] = Field(
        default_factory=list,
        description="Condition identifiers that determine completion.",
    )
    mode: str = Field(default="all", description="Checklist completion mode, such as all or any.")
