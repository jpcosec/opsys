from pydantic import Field

from .base import PrimitiveDoc


class FieldInstanceDoc(PrimitiveDoc):
    __semantics__ = {"type": ["workflow", "field"], "workspace": ["desk", "fields"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Summary

⸢rev•summary⸥

## Field Key

⸢rev•field_key⸥

## Value Type

⸢rev•value_type⸥

## Owner Artifact

⸢rev•owner_artifact⸥

## Value

⸢rev,markdown•serialized_value⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    field_key: str = Field(description="Logical field key represented by this instance.")
    value_type: str = Field(description="Declared value type for this field instance.")
    owner_artifact: str = Field(description="Artifact identifier that owns this field instance.")
    serialized_value: str = Field(description="Serialized field value for markdown persistence.")
