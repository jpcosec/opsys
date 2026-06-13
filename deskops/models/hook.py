from pydantic import Field

from .base import PrimitiveDoc


class HookDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "hook"], "workspace": ["desk", "primitives"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
event: ⸢rev•event⸥
target: ⸢rev•target⸥
condition_ref: ⸢rev•condition_ref⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    event: str = Field(description="Event name that can trigger the hook.")
    target: str = Field(description="Operator or routine identifier the hook targets.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the hook.")
