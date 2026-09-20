"""AcceptanceDoc: the closure contract of a task — validation checks,
observable done-when rules, and the evidence that supports closeout."""

from pydantic import Field

from .base import PrimitiveDoc


class AcceptanceDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "acceptance"], "workspace": ["desk"]}
    __containment__ = {}
    __template__ = """---
# acceptance-xxx
id: ⸢rev•id⸥
# draft | active | complete | archived
status: ⸢rev•status⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize what closing this task requires._

⸢rev•summary⸥

## Validation

_List the tests, checks, or commands required before closure._

- ⸢rev,list•validation⸥

## Done When

_List the observable completion rules for this task._

- ⸢rev,list•done_when⸥

## Evidence

_List the evidence produced that supports closeout._

- ⸢rev,list•evidence⸥
""".strip()

    validation: list[str] = Field(
        default_factory=list,
        description="Tests, checks, or commands required before closure.",
    )
    done_when: list[str] = Field(
        default_factory=list,
        description="Observable completion rules for the task.",
    )
    evidence: list[str] = Field(
        default_factory=list,
        description="Evidence produced or expected that supports closeout.",
    )