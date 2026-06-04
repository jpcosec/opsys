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
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
5WH1+: ⸢rev•five_wh_one_plus⸥

## Answer

⸢rev•answer⸥

## Tags

- ⸢rev,list•tags⸥
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
