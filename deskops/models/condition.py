from pydantic import Field

from .base import PrimitiveDoc


class ConditionDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "condition"], "workspace": ["desk", "primitives"]}
    __template__ = """---
# condition-xxx
id: ⸢rev•id⸥
# active | archived
status: ⸢rev•status⸥
# Payload path the condition reads
subject: ⸢rev•subject⸥
# Predicate applied to the value (e.g., eq, contains)
predicate: ⸢rev•predicate⸥
# Expected value used by the predicate
expected: ⸢rev•expected⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize the predicate this condition checks._

⸢rev•summary⸥
""".strip()

    subject: str = Field(description="Payload path the condition reads.")
    predicate: str = Field(description="Predicate applied to the subject value.")
    expected: str = Field(default="", description="Expected value used by the predicate when needed.")
