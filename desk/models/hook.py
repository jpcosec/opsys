from pydantic import Field

from .base import PrimitiveDoc


class HookDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "hook"], "workspace": ["desk", "primitives"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Event

⸢rev•event⸥

## Target

⸢rev•target⸥

## Condition

⸢rev•condition_ref⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    event: str = Field(description="Event name that can trigger the hook.")
    target: str = Field(description="Operator or routine identifier the hook targets.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the hook.")
