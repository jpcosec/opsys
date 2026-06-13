from pydantic import Field

from .base import PrimitiveDoc


class OperatorDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "operator"], "workspace": ["desk", "primitives"]}
    __template__ = """---
id: ⸢rev•id⸥
status: ⸢rev•status⸥
action: ⸢rev•action⸥
target: ⸢rev•target⸥
value: ⸢rev•value⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    action: str = Field(description="Atomic runtime action, such as set_field or append_list.")
    target: str = Field(description="Payload path modified by the operator.")
    value: str = Field(default="", description="Value used by the operator action.")
