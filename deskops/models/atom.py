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
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_-]*$",
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


class AtomDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["knowledge", "atom"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
# atom-xxx, unique identifier
id: ⸢rev•id⸥
# Short, descriptive title
title: ⸢rev•title⸥
# what | why | how | how_not | when | where | for_whom
five_wh_one_plus: ⸢rev•five_wh_one_plus⸥
# e.g., system:deskops, topic:templates
tags: ⸢rev•tags⸥
# Optional URL or path to the authoritative source of this knowledge
provenance: ⸢rev•provenance⸥
---

# ⸢render•title⸥

## Answer

_Answer the selected 5WH1+ question as one stable knowledge unit._

⸢rev•answer⸥
""".strip()

    id: str = Field(description="Stable atom identifier.")
    title: str = Field(description="Short title for the atomic knowledge unit.")
    five_wh_one_plus: AtomQuestion = Field(
        description="The single 5WH1+ question this atom answers."
    )
    answer: str = Field(description="The curated raw answer to the selected question.")
    tags: list[AtomTag] = Field(
        default_factory=list,
        description=(
            "Namespaced semantic tags used for retrieval and grouping. Tags do not "
            "encode lifecycle, relations, evidence, or materialization."
        ),
    )
    provenance: str = Field(
        default="",
        description=(
            "URL or path to the authoritative source of this atom's knowledge. "
            "Used for traceability and provenance tracking."
        ),
    )
