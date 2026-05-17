from pydantic import Field

from sldb import StructuredNLDoc


class AtomDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["workflow", "atom"],
        "workspace": ["drawer", "atoms"],
    }
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥
Category: ⸢rev•category⸥

## What

⸢rev•what⸥

## Why

⸢rev•why⸥

## How

⸢rev•how⸥

## When

⸢rev•when⸥

## Where

⸢rev•where⸥

## For Whom

⸢rev•for_whom⸥

## Related Atoms

- ⸢rev,list•related_atoms⸥

## Materializes Into

- ⸢rev,list•materializes_into⸥

## Stabilized In

- ⸢rev,list•stabilized_in⸥

## Distinct From

⸢rev•distinct_from_pills⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Short durable concept title.")
    id: str = Field(description="Stable atom identifier.")
    status: str = Field(
        description="Atom lifecycle state, such as stable or incubating."
    )
    category: str = Field(description="Concept category used to group related atoms.")
    what: str = Field(description="Stable statement of what the concept is.")
    why: str = Field(
        description="Why the concept matters and what it protects or enables."
    )
    how: str = Field(description="How the concept should be applied or interpreted.")
    when: str = Field(description="When the concept becomes relevant in the workflow.")
    where: str = Field(
        description="Where the concept applies in code, docs, or operations."
    )
    for_whom: str = Field(description="Who should use or care about this concept.")
    related_atoms: list[str] = Field(
        default_factory=list,
        description="Related atom identifiers or references.",
    )
    materializes_into: list[str] = Field(
        default_factory=list,
        description="Derived artifact references such as docs, features, tasks, or pills.",
    )
    stabilized_in: list[str] = Field(
        default_factory=list,
        description="Durable artifacts where the atom has been stabilized or explained.",
    )
    distinct_from_pills: str = Field(
        description="How this durable concept differs from temporary execution-time pills."
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'topic:atoms' or 'system:sldb'.",
    )
