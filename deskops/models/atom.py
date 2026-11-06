from enum import StrEnum
import re
from typing import Annotated

from pydantic import Field, field_validator

from sldb import StructuredNLDoc

from .crossroad import check_domain_path

ATOM_TAG_PATTERN = r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$"
DOMAIN_NAMESPACE = "domain"
_ATOM_TAG = re.compile(ATOM_TAG_PATTERN)


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
        pattern=ATOM_TAG_PATTERN,
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


def check_slug_id(value: object, prefix: str, label: str) -> object:
    """``<prefix><slug>``, where the slug is already in slug form. Anything else is left to pydantic."""
    if not isinstance(value, str):
        return value
    # Lazy: doc_access imports the models, and the slug form is defined once, there.
    from deskops.doc_access import slugify

    slug = value.removeprefix(prefix)
    if not value.startswith(prefix) or not slug or slug != slugify(slug):
        raise ValueError(f"{label} id must follow slug convention {prefix}<slug>: {value}")
    return value


def check_atom_tags(tags: object) -> object:
    """Each tag is ``namespace:value``; each ``domain:`` value is a domain path. Anything that is
    not a list of strings is left to pydantic."""
    if not isinstance(tags, list):
        return tags
    for tag in tags:
        if not isinstance(tag, str):
            continue
        if _ATOM_TAG.fullmatch(tag) is None:
            raise ValueError(f"Invalid atom tag '{tag}'. Expected namespace:value.")
        namespace, value = tag.split(":", 1)
        if namespace == DOMAIN_NAMESPACE:
            check_domain_path(value)
    return tags


def domain_paths(tags: list[str]) -> list[str]:
    """Values of the ``domain:`` tags, in order."""
    values: list[str] = []
    for tag in tags:
        match = _ATOM_TAG.fullmatch(str(tag))
        if match is not None and str(tag).split(":", 1)[0] == DOMAIN_NAMESPACE:
            values.append(str(tag).split(":", 1)[1])
    return values


class AtomDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "atom-{slug}",
        "status_default": None,
        "tags": ["system:deskops", "topic:atoms"],
    }
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

    @field_validator("id", mode="before")
    @classmethod
    def _id_follows_the_slug_convention(cls, value: object) -> object:
        return check_slug_id(value, "atom-", "atom")

    @field_validator("tags", mode="before")
    @classmethod
    def _tags_are_namespaced(cls, tags: object) -> object:
        return check_atom_tags(tags)
