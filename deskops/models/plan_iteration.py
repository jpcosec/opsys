"""PlanIterationDoc: una vuelta de la rutina — qué se intentó, qué se aprendió,
qué cambió del plan."""

from pydantic import Field

from sldb import StructuredNLDoc


class PlanIterationDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "plan_iteration"], "workspace": ["desk", "planning"]}
    __containment__ = {}
    __template__ = """---
# plan-iteration-xxx
id: ⸢rev•id⸥
# Número de vuelta de la rutina
round: ⸢rev•round⸥
# e.g., system:deskops
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Trigger

_Describe what triggered this iteration._

⸢rev•trigger⸥

## Findings

_Record what this iteration found._

⸢rev•findings⸥

## Plan Delta

_Describe what changed from the previous iteration._

⸢rev•plan_delta⸥

## Outcome

_Record the outcome of this iteration._

⸢rev•outcome⸥
""".strip()

    id: str = Field(description="Stable plan iteration identifier.")
    title: str = Field(description="Short plan iteration title.")
    round: int = Field(description="Iteration round number.")
    trigger: str = Field(description="What triggered this iteration.")
    findings: str = Field(description="What this iteration found.")
    plan_delta: str = Field(description="What changed from the previous iteration.")
    outcome: str = Field(description="Outcome of this iteration.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms.",
    )