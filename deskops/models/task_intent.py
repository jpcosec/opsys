"""TaskIntentDoc: the 'how' of a task — implementation path, touched files,
and the explicit frontier of what is out of scope."""

from pydantic import Field

from .base import PrimitiveDoc


class TaskIntentDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "task_intent"], "workspace": ["desk"]}
    __containment__ = {}
    __template__ = """---
# task-intent-xxx
id: ⸢rev•id⸥
# draft | active | complete | archived
status: ⸢rev•status⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what this task intends to change and why it is scoped this way._

⸢rev•summary⸥

## Implementation Path

_Describe the expected implementation route for this task._

⸢rev•implementation_path⸥

## Files

_List the files or paths this task is expected to change._

- ⸢rev,list•files⸥

## Out of Scope

_State what this task explicitly does not cover._

⸢rev•out_of_scope⸥
""".strip()

    implementation_path: str = Field(
        description="Suggested implementation path for completing the task."
    )
    files: list[str] = Field(
        default_factory=list,
        description="Files or paths expected to change during the task.",
    )
    out_of_scope: str = Field(
        default="",
        description="What the task explicitly leaves out of scope.",
    )