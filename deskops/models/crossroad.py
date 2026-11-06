"""The mandatory parent of a domain path."""
from __future__ import annotations

import re
from typing import Annotated

from pydantic import Field, field_validator, model_validator
from sldb import StructuredNLDoc

DOMAIN_PATH_PATTERN = r"^[a-z][a-z0-9_-]*(\.[a-z][a-z0-9_-]*)*$"
CROSSROAD_PREFIX = "crossroad-"
_DOMAIN_PATH = re.compile(DOMAIN_PATH_PATTERN)

DomainPath = Annotated[
    str,
    Field(pattern=DOMAIN_PATH_PATTERN, description="Dot-separated domain path such as pizzeria.carta."),
]


def crossroad_id(path: str) -> str:
    """The id of the crossroad for ``path``: ``crossroad-`` plus the path with dots as ``--``."""
    return CROSSROAD_PREFIX + str(path).replace(".", "--")


def check_domain_path(value: object) -> object:
    """A domain path is lowercase segments separated by dots. Anything else is left to pydantic."""
    if isinstance(value, str) and _DOMAIN_PATH.fullmatch(value) is None:
        raise ValueError(f"Invalid domain path '{value}': use lowercase segments separated by dots.")
    return value


class CrossroadDoc(StructuredNLDoc):
    """Describes what hangs below one domain path.

    Every document tagged ``domain:a.b.c`` needs a crossroad for ``a``, ``a.b``
    and ``a.b.c``, each with written content: a KB cannot describe children
    before it describes their parent.
    """

    __semantics__ = {
        "type": ["knowledge", "crossroad"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
id: ⸢rev•id⸥
path: ⸢rev•path⸥
title: ⸢rev•title⸥
---

# ⸢render•title⸥

## Content

⸢rev,markdown•content⸥
""".strip()

    id: str = Field(description="Stable identifier: 'crossroad-' plus the path with dots written as '--'.")
    path: DomainPath = Field(description="Domain path this crossroad describes, e.g. pizzeria.carta.")
    title: str = Field(description="Short title of the domain area.")
    content: str = Field(description="Written description of what hangs below this path; must not be empty.")

    @field_validator("path", mode="before")
    @classmethod
    def _path_is_a_domain_path(cls, value: object) -> object:
        return check_domain_path(value)

    @field_validator("content")
    @classmethod
    def _content_is_written(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a crossroad must describe its children: content cannot be empty")
        return value

    @model_validator(mode="after")
    def _id_names_the_path(self) -> "CrossroadDoc":
        if self.id != crossroad_id(self.path):
            raise ValueError(f"crossroad id must be {crossroad_id(self.path)}")
        return self
