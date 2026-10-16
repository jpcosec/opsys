from pydantic import Field

from sldb import StructuredNLDoc


class PrimitiveDoc(StructuredNLDoc):
    __template__ = """---
# primitive-xxx
id: ⸢rev•id⸥
# draft | active | archived
status: ⸢rev•status⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Summary

⸢rev•summary⸥
""".strip()

    title: str = Field(description="Short primitive title.")
    id: str = Field(description="Stable primitive identifier.")
    status: str = Field(default="", description="Primitive lifecycle status.")
    summary: str = Field(
        default="",
        description="Short semantic summary for the primitive.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end using namespaced forms.",
    )


class OperationalArtifactDoc(PrimitiveDoc):
    current_node: str = Field(
        default="",
        description="Current node of the artifact in its lifecycle graph (a ritual id, or 'complete').",
    )
    history: list[str] = Field(
        default_factory=list,
        description="Lifecycle transitions the artifact went through, by relation type.",
    )
