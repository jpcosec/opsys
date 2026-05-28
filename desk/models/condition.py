from pydantic import Field

from .base import PrimitiveDoc


class ConditionDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "condition"], "workspace": ["desk", "primitives"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Subject

⸢rev•subject⸥

## Predicate

⸢rev•predicate⸥

## Expected

⸢rev•expected⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    subject: str = Field(description="Payload path the condition reads.")
    predicate: str = Field(description="Predicate applied to the subject value.")
    expected: str = Field(default="", description="Expected value used by the predicate when needed.")
