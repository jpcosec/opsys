from pydantic import Field, model_serializer, model_validator

from .base import OperationalArtifactDoc


class TaskDoc(OperationalArtifactDoc):
    __containment__ = {"checklists": ["ChecklistDoc"], "pills": ["PillDoc"], "atoms": ["AtomDoc"]}
    __references__ = ["references", "depends_on", "inherits_from", "from_drawer"]
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

    def render_payload(self) -> dict:
        data = super().model_dump(mode="json")
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
    from_drawer: str = Field(
        default="",
        description="Repo-relative path of the desk/drawer/ file this task was authored from; empty when it was not.",
    )

    @model_serializer(mode="wrap")
    def _omit_unset_from_drawer(self, handler):
        """Serialize from_drawer only when it is set.

        TaskDoc is tracked by every desk on the machine (123 tasks across 13
        stores). A field that always serialized would change the hash of every
        one of them and put each store in FAIL until migrated. Omitting it when
        empty keeps existing tasks byte-identical, so no store needs migrating.
        """
        data = handler(self)
        if not data.get("from_drawer"):
            data.pop("from_drawer", None)
        return data
