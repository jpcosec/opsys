"""The mandatory parent of a domain path."""
from __future__ import annotations

from typing import Annotated

from pydantic import Field, field_validator

from .base import PrimitiveDoc

DOMAIN_PATH_PATTERN = r"^[a-z][a-z0-9_-]*(\.[a-z][a-z0-9_-]*)*$"

DomainPath = Annotated[
    str,
    Field(pattern=DOMAIN_PATH_PATTERN, description="Dot-separated domain path such as pizzeria.carta."),
]


class CrossroadDoc(PrimitiveDoc):
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
tags: ⸢rev•tags⸥
---

# ⸢render•title⸥

## Content

⸢rev,markdown•content⸥
""".strip()

    id: str = Field(description="Stable identifier: 'crossroad-' plus the path with dots written as '--'.")
    path: DomainPath = Field(description="Domain path this crossroad describes, e.g. pizzeria.carta.")
    title: str = Field(description="Short title of the domain area.")
    content: str = Field(description="Written description of what hangs below this path; must not be empty.")

    @field_validator("content")
    @classmethod
    def _content_is_written(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a crossroad must describe its children: content cannot be empty")
        return value