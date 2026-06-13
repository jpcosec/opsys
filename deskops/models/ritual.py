from pydantic import Field

from .base import OperationalArtifactDoc


class RitualDoc(OperationalArtifactDoc):
    __semantics__ = {"type": ["workflow", "ritual"], "workspace": ["desk"]}
    __compositions__ = {
        "step_details": {
            "source_field": "steps",
            "model": "deskops.models:StepDoc",
            "template": "1. {title}: {action} -> {outcome}",
        }
    }
    __template__ = """---
id: ⸢rev•id⸥
steps: ⸢rev•steps⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Purpose

_Explain why this ritual exists._

⸢rev•purpose⸥

## Trigger

_State when this ritual should start._

⸢rev•trigger⸥

## Preconditions

_List the conditions that must hold before running the ritual._

- ⸢rev,list•preconditions⸥

## Validation

_List the checks that prove the ritual was performed correctly._

- ⸢rev,list•validation⸥

## Failure Modes

_List common mistakes this ritual prevents._

- ⸢rev,list•failure_modes⸥

## Completion

_Describe what completion looks like._

⸢rev•completion⸥

## Step Details

_Generated from the step references above._

⸢render•step_details⸥

""".strip()

    title: str = Field(description="Short ritual title.")
    id: str = Field(description="Stable ritual identifier.")
    purpose: str = Field(description="Why the ritual exists.")
    trigger: str = Field(description="When the ritual should be started.")
    preconditions: list[str] = Field(
        default_factory=list,
        description="Conditions that must hold before running the ritual.",
    )
    steps: list[str] = Field(
        default_factory=list,
        description="Ordered steps to execute as part of the ritual.",
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Checks that confirm the ritual was performed correctly.",
    )
    failure_modes: list[str] = Field(
        default_factory=list,
        description="Common mistakes, drifts, or anti-patterns to avoid.",
    )
    completion: str = Field(
        description="What indicates that the ritual has been completed."
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'layer:workflow' or 'system:sldb'.",
    )
