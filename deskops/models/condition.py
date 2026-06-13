from pydantic import Field

from .base import PrimitiveDoc


class ConditionDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "condition"], "workspace": ["desk", "primitives"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
subject: ⸢rev•subject⸥
predicate: ⸢rev•predicate⸥
expected: ⸢rev•expected⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    subject: str = Field(description="Payload path the condition reads.")
    predicate: str = Field(description="Predicate applied to the subject value.")
    expected: str = Field(default="", description="Expected value used by the predicate when needed.")
