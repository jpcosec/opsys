"""ProtoAtomDoc: buffer de captura antes de tipar un átomo."""

from pydantic import Field

from .base import PrimitiveDoc


class ProtoAtomDoc(PrimitiveDoc):
    __semantics__ = {"type": ["knowledge", "proto_atom"], "workspace": ["desk", "atoms"]}
    __containment__ = {}
    __template__ = """---
# proto-atom-xxx
id: ⸢rev•id⸥
# draft | active | complete | archived
status: ⸢rev•status⸥
# Qué tipo de átomo aspira a ser
typed_as: ⸢rev•typed_as⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢rev•title⸥

## Content

⸢rev•content⸥
""".strip()

    content: str = Field(description="Raw capture before typing into an AtomDoc.")
    typed_as: str = Field(default="", description="The atom type this buffer aspires to.")
    provenance: str | None = Field(
        default=None,
        description="Optional URL or path to the authoritative source.",
    )