from enum import StrEnum
from typing import Annotated

from pydantic import Field

from sldb import StructuredNLDoc


class AtomQuestion(StrEnum):
    WHAT = "what"
    WHY = "why"
    HOW = "how"
    HOW_NOT = "how_not"
    WHEN = "when"
    WHERE = "where"
    FOR_WHOM = "for_whom"


AtomTag = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$",
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


class AtomDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["knowledge", "atom"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
five_wh_one_plus: ⸢rev•five_wh_one_plus⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Answer

⸢rev•answer⸥
""".strip()

    id: str = Field(
        description="Stable, unique atom identifier, conventionally 'atom-<slug>'."
    )
    title: str = Field(
        description="Short, descriptive title for the atomic knowledge unit."
    )
    five_wh_one_plus: AtomQuestion = Field(
        description=(
            "The single 5WH1+ question this atom answers: one of "
            "what, why, how, how_not, when, where, for_whom."
        )
    )
    answer: str = Field(
        description=(
            "The curated raw answer to the selected 5WH1+ question, written as "
            "one stable knowledge unit."
        )
    )
    tags: list[AtomTag] = Field(
        default_factory=list,
        description=(
            "Namespaced semantic tags used for retrieval and grouping, each in the "
            "form namespace:value (e.g. system:deskops, topic:templates). Tags do "
            "not encode lifecycle, relations, evidence, or materialization."
        ),
    )
    provenance: str | None = Field(
        default=None,
        description=(
            "Optional URL or path to the authoritative source of this atom's "
            "knowledge. Used for traceability and provenance tracking."
        ),
    )
