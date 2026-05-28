from pydantic import Field

from .base import PrimitiveDoc


class ChecklistDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "checklist"], "workspace": ["desk", "primitives"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Items

- ⸢rev,list•items⸥

## Conditions

- ⸢rev,list•condition_refs⸥

## Mode

⸢rev•mode⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    items: list[str] = Field(default_factory=list, description="Human-readable checklist items.")
    condition_refs: list[str] = Field(
        default_factory=list,
        description="Condition identifiers that determine completion.",
    )
    mode: str = Field(default="all", description="Checklist completion mode, such as all or any.")
