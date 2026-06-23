from pydantic import Field

from .base import PrimitiveDoc


class HookDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "hook"], "workspace": ["desk", "primitives"]}
    __template__ = """---
# hook-xxx
id: ⸢rev•id⸥
# active | archived
status: ⸢rev•status⸥
# Event name that can trigger the hook
event: ⸢rev•event⸥
# Operator or routine identifier the hook targets
target: ⸢rev•target⸥
# Optional condition identifier guarding the hook
condition_ref: ⸢rev•condition_ref⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize when this hook fires and what it invokes._

⸢rev•summary⸥
""".strip()

    event: str = Field(description="Event name that can trigger the hook.")
    target: str = Field(description="Operator or routine identifier the hook targets.")
    condition_ref: str = Field(default="", description="Optional condition identifier guarding the hook.")
