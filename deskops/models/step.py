from pydantic import Field

from sldb import StructuredNLDoc


class StepDoc(StructuredNLDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "step-{slug}",
        "status_default": "active",
        "tags": ["workspace:desk", "artifact:step"],
    }
    __semantics__ = {"type": ["workflow", "step"], "workspace": ["desk"]}
    __template__ = """---
# step-xxx
id: ⸢rev•id⸥
# e.g., topic:testing, workspace:desk
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Action

_Describe the action this step performs._

⸢rev•action⸥

## Outcome

_Describe the result or evidence this step should produce._

⸢rev•outcome⸥

""".strip()

    title: str = Field(description="Short step title.")
    id: str = Field(description="Stable step identifier.")
    action: str = Field(description="What the step should do.")
    outcome: str = Field(description="What the step should produce or confirm.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'topic:testing' or 'workspace:desk'.",
    )
