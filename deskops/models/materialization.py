from pydantic import Field

from sldb import StructuredNLDoc

from .atom import AtomTag


class MaterializationContractDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["knowledge", "materialization_contract"],
        "workspace": ["desk", "materializations"],
    }
    __template__ = """---
id: ⸢rev•id⸥
title: ⸢rev•title⸥
source_atoms: ⸢rev•source_atoms⸥
target_kind: ⸢rev•target_kind⸥
target_identity: ⸢rev•target_identity⸥
validation: ⸢rev•validation⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•title⸥

## Intent

⸢rev•intent⸥
""".strip()

    id: str = Field(
        description="Stable, unique materialization contract identifier, conventionally 'materialization-<slug>'."
    )
    title: str = Field(
        description="Short, descriptive title for the materialization contract."
    )
    source_atoms: list[str] = Field(
        default_factory=list,
        description="Source atom identifiers that this materialization contract derives from."
    )
    target_kind: str = Field(
        description="Kind of artifact or surface targeted by this materialization contract."
    )
    target_identity: str = Field(
        description="Stable target node id or path that this materialization contract must resolve to."
    )
    intent: str = Field(
        description="Human-readable intent describing how the target materializes the source atoms."
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Validation commands or checks expected for this materialization contract."
    )
    tags: list[AtomTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags for retrieval and grouping, each in the form namespace:value."
    )
    provenance: str | None = Field(
        default=None,
        description="Optional URL or path to the authoritative source for this materialization contract."
    )
