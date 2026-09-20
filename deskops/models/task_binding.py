"""TaskBindingDoc: why a task exists and why it is bound the way it is."""

from pydantic import Field

from .base import PrimitiveDoc


class TaskBindingDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "task_binding"], "workspace": ["desk"]}
    __containment__ = {}
    __template__ = """---
# task-binding-xxx
id: ⸢rev•id⸥
# draft | active | complete | archived
status: ⸢rev•status⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this task is bound to and why._

⸢rev•summary⸥

## Rationale

_Explain why this task exists or is bound to its context._

⸢rev•rationale⸥
""".strip()

    rationale: str = Field(
        description="Why this task exists or why it is bound to its context."
    )