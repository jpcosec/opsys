from pydantic import Field

from .base import PrimitiveDoc


class OperatorDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "operator"], "workspace": ["desk", "primitives"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Action

⸢rev•action⸥

## Target

⸢rev•target⸥

## Value

⸢rev•value⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    action: str = Field(description="Atomic runtime action, such as set_field or append_list.")
    target: str = Field(description="Payload path modified by the operator.")
    value: str = Field(default="", description="Value used by the operator action.")
