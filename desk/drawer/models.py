from pydantic import Field

from sldb import StructuredNLDoc


class FeatureDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "feature"], "workspace": ["drawer"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Goal

⸢rev•goal⸥

## Why

⸢rev•why⸥

## Scope

⸢rev•scope⸥

## Proposed Shape

⸢rev•proposed_shape⸥

## Adoption Path

⸢rev•adoption_path⸥

## Validation

- ⸢rev,list•validation⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Short future-facing feature title.")
    id: str = Field(description="Stable deferred feature identifier.")
    status: str = Field(
        description="Deferred feature status, such as proposed or incubating."
    )
    goal: str = Field(description="Intended outcome of the future feature.")
    why: str = Field(description="Why the feature matters and what gap it closes.")
    scope: str = Field(description="What belongs to the feature and what does not.")
    proposed_shape: str = Field(
        description="Proposed structure, architecture, or contract for the feature."
    )
    adoption_path: str = Field(
        description="How the feature would move from drawer into active execution."
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Signals or checks that would show the feature is ready for active execution.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb' or 'workspace:drawer'.",
    )
