"""PlanDoc: lo que un agente planificador produce cuando el supervisor lo suelta."""

from pydantic import Field

from .base import OperationalArtifactDoc


class PlanDoc(OperationalArtifactDoc):
    __semantics__ = {"type": ["workflow", "plan"], "workspace": ["desk", "planning"]}
    __containment__ = {
        "targets": ["PlanTargetDoc"],
        "iterations": ["PlanIterationDoc"],
    }
    __template__ = """---
# plan-xxx
id: ⸢rev•id⸥
# Contención: refs a los PlanTargetDoc que este plan contiene
# e.g., plan-target-xxx
# e.g., system:deskops, workspace:desk
tags: ⸢rev•tags⸥
targets: ⸢rev•targets⸥
# Contención: refs a los PlanIterationDoc que este plan contiene
# e.g., plan-iteration-xxx
iterations: ⸢rev•iterations⸥
---

# ⸢rev•title⸥

## Goal

_Describe the concrete result this plan works toward._

⸢rev•goal⸥

## Context Findings

_Summarize what already exists and shapes this plan._

⸢rev•context_findings⸥

## Interpretation

_Explain why the task is read this way._

⸢rev•interpretation⸥

## Risks

_Describe the risks this plan must account for._

⸢rev•risks⸥

## Ambiguities

_List what must not be decided alone._

- ⸢rev,list•ambiguities⸥
""".strip()

    goal: str = Field(description="Concrete result the plan works toward.")
    context_findings: str = Field(
        description="What already exists — the most useful section today."
    )
    interpretation: str = Field(description="Why the task is read this way.")
    risks: str = Field(description="Risks the plan must account for.")
    ambiguities: list[str] = Field(
        default_factory=list,
        description="Things that must not be decided alone.",
    )
    targets: list[str] = Field(
        default_factory=list,
        description="Refs to the PlanTargetDoc documents this plan contains (spec §PlanDoc contains.targets).",
    )
    iterations: list[str] = Field(
        default_factory=list,
        description="Refs to the PlanIterationDoc documents this plan contains (spec §PlanDoc contains.iterations).",
    )