from pydantic import Field

from .base import PrimitiveDoc


class OperatorDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "operator"], "workspace": ["desk", "primitives"]}
    __template__ = """---
# operator-xxx
id: ⸢rev•id⸥
# active | archived
status: ⸢rev•status⸥
# Atomic runtime action, e.g., set_field, append_list
action: ⸢rev•action⸥
# Payload path modified by the operator
target: ⸢rev•target⸥
# Value used by the operator action
value: ⸢rev•value⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

_Summarize the state transition this operator performs._

⸢rev•summary⸥
""".strip()

    action: str = Field(description="Atomic runtime action, such as set_field or append_list.")
    target: str = Field(description="Payload path modified by the operator.")
    value: str = Field(default="", description="Value used by the operator action.")
