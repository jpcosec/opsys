"""A free atom: a knowledge unit captured before it has a fixed type."""
from __future__ import annotations

from pydantic import Field
from sldb import StructuredNLDoc

from .atom import AtomTag


class ProtoAtomDoc(StructuredNLDoc):
    """A free knowledge unit: a title, free content and tags.

    Unlike AtomDoc it answers no fixed 5WH1+ question. Its ``domain:`` tag hangs
    it from a crossroad of the domain tree. Typing it into another sldb model
    keeps it as a redirect stub whose ``typed_as`` names the typed document.
    """

    __semantics__ = {
        "type": ["knowledge", "protoatom"],
        "workspace": ["desk", "atoms"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
tags: ⸢rev•tags⸥
typed_as: ⸢optrev•typed_as⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Content

⸢rev,markdown•content⸥
""".strip()

    id: str = Field(description="Stable, unique protoatom identifier, conventionally 'proto-<slug>'.")
    title: str = Field(description="Short title of the free knowledge unit.")
    content: str = Field(default="", description="Free markdown content, with no fixed question or structure.")
    tags: list[AtomTag] = Field(
        default_factory=list,
        description="Namespaced tags; a single domain:<path> tag places the protoatom in the domain tree.",
    )
    typed_as: str | None = Field(
        default=None,
        description="Model:id of the document this protoatom was typed into; when set, the protoatom is a redirect stub.",
    )
    provenance: str | None = Field(default=None, description="Optional URL or path to the source of this knowledge.")
