from pydantic import Field

from sldb import StructuredNLDoc


class PrimitiveDoc(StructuredNLDoc):
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
    routine: str = Field(
        default="",
        description="Primary routine identifier that makes the artifact actionable.",
    )
    current_node: str = Field(
        default="",
        description="Current node in the operational routine or state machine.",
    )
    history: list[str] = Field(
        default_factory=list,
        description="Operational transition history for the artifact.",
    )
