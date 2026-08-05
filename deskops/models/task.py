from pydantic import Field, model_validator

from .base import OperationalArtifactDoc


class TaskDoc(OperationalArtifactDoc):
    model_config = {"extra": "allow"}
    __semantics__ = {"type": ["workflow", "task"], "workspace": ["desk"]}
    
    frontmatter: dict | None = Field(default=None, description="YAML frontmatter containing task metadata", exclude=True)

    @model_validator(mode="before")
    @classmethod
    def _merge_frontmatter(cls, data: dict) -> dict:
        if isinstance(data, dict) and "frontmatter" in data and isinstance(data["frontmatter"], dict):
            fm = data.pop("frontmatter")
            for k, v in fm.items():
                if k not in data or data[k] is None:
                    data[k] = v
        return data

    def model_dump(self, **kwargs) -> dict:
        data = super().model_dump(**kwargs)
        body_fields = {"title", "why", "goal", "scope", "implementation_path", "validation", "done_when"}
        data["frontmatter"] = {k: v for k, v in data.items() if k not in body_fields}
        return data

    __template__ = """---
⸢rev,dict•frontmatter⸥
---

# ⸢rev•title⸥

## Rationale

_Explain why this task exists or the business driver behind it._

⸢rev•why⸥

## Goal

_Describe the concrete result this task must produce._

⸢rev•goal⸥

## Scope

_State what is in scope and what is out of scope._

⸢rev•scope⸥

## Implementation Path

_Outline the expected implementation route or affected surface._

⸢rev•implementation_path⸥

## Validation

_List the checks required before this task can close._

- ⸢rev,list•validation⸥

## Done When

_Name the observable condition that makes the task complete._

⸢rev•done_when⸥

""".strip()

    title: str = Field(description="Short action-oriented task title.")
    why: str | None = Field(default="Not provided.", description="Rationale or business driver behind the task.")
    id: str = Field(description="Stable task identifier.")
    status: str = Field(description="Current task state, typically active or blocked.")
    goal: str = Field(description="Concrete intended result for the task.")
    scope: str = Field(description="What is in and out of scope for the task.")
    references: list[str] = Field(
        default_factory=list,
        description="Relevant references such as files, docs, commits, or commands.",
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="Task identifiers that must complete first.",
    )
    pills: list[str] = Field(
        default_factory=list,
        description="Pill identifiers required for safe execution of the task.",
    )
    files: list[str] = Field(
        default_factory=list,
        description="Files or paths expected to change during the task.",
    )
    checklists: list[str] = Field(
        default_factory=list,
        description="Checklist identifiers that verify the task's operational routine.",
    )
    implementation_path: str = Field(
        description="Suggested implementation path for completing the task."
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Tests, checks, or commands required before closure.",
    )
    done_when: str = Field(description="Observable completion rule for the task.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb' or 'language:python'.",
    )
    task_type: str = Field(
        default="",
        description="Workflow task type such as design, implementation, test, reflection, or closeout.",
    )
    inherits_from: list[str] = Field(
        default_factory=list,
        description="Task identifiers that provide inherited workflow context.",
    )
    inherit_acceptance_context: bool = Field(
        default=False,
        description="Whether validation and done-when context should be inherited from referenced tasks.",
    )
    atoms: list[str] = Field(
        default_factory=list,
        description="Workflow or knowledge atoms explicitly bound to the task.",
    )
