from pydantic import Field

from .base import OperationalArtifactDoc


class PillDoc(OperationalArtifactDoc):
    __semantics__ = {"type": ["workflow", "pill"], "workspace": ["desk"]}
    __template__ = """---
id: ⸢rev•id⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## What

_Define the context or guardrail this pill carries._

⸢rev•what⸥

## Why

_Explain why this context matters for safe execution._

⸢rev•why⸥

## When

_Describe when an agent should apply this pill._

⸢rev•when⸥

## Where

_Name the files, surfaces, or scope this pill applies to._

⸢rev•where⸥

## How

_Describe the correct way to apply this guidance._

⸢rev•how⸥

## How Not

_Describe the shortcut or failure mode to avoid._

⸢rev•how_not⸥

""".strip()

    title: str = Field(
        description="Pill title, including semantic prefix when useful, such as 'ADR:' or 'Pattern:'."
    )
    id: str = Field(description="Stable pill identifier.")
    what: str = Field(description="What the pill defines or clarifies.")
    why: str = Field(
        description="Why this context matters for implementation or refactoring."
    )
    when: str = Field(description="When this pill should be applied.")
    where: str = Field(
        description="Where this pill applies, either as general scope or as references to existing code or docs."
    )
    how: str = Field(description="How to apply the guidance in practice.")
    how_not: str = Field(description="How not to apply the guidance or what to avoid.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'language:python' or 'library:pydantic'.",
    )
