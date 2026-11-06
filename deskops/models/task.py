from pydantic import Field, model_serializer, model_validator

from .base import OperationalArtifactDoc


# An absent `optrev` frontmatter key extracts as None, not as "missing": drop
# those keys before validation so the field default applies and the re-rendered
# document keeps the bytes it had before the marker existed.
_ABSENT_FRONTMATTER_DEFAULTS = frozenset({
    "status",
    "summary",
    "current_node",
    "history",
    "references",
    "depends_on",
    "pills",
    "files",
    "task_type",
    "inherits_from",
    "inherit_acceptance_context",
    "atoms",
    "from_drawer",
    "closeout_evidence",
    "tags",
})


class TaskDoc(OperationalArtifactDoc):
    # Artifact-level defaults `deskops add` applies (formerly one YAML spec per artifact):
    # the id built from the slug, the status a new document gets, and its default tags.
    __artifact__ = {
        "id_pattern": "task-{slug}",
        "status_default": "draft",
        "tags": ["workspace:desk", "artifact:task"],
    }
    # The contract fields: editing any of these changes the task contract and (once sldb reads
    # GO02 (e)) leaves receipts `changed`; editing references/pills/status/history/tags does not.
    __contract__ = ["title", "goal", "scope", "implementation_path", "files", "validation", "done_when"]
    __references__ = ["references", "depends_on", "inherits_from", "current_node", "pills", "atoms"]
    __reference_models__ = {
        "depends_on": ["TaskDoc"],
        "inherits_from": ["TaskDoc"],
        "current_node": ["RitualDoc"],
        "pills": ["PillDoc"],
        "atoms": ["AtomDoc"],
    }
    model_config = {"extra": "ignore"}
    __semantics__ = {"type": ["workflow", "task"], "workspace": ["desk"]}

    __template__ = """---
id: ⸢rev•id⸥
status: ⸢optrev•status⸥
summary: ⸢optrev•summary⸥
tags: ⸢optrev,list•tags⸥
current_node: ⸢optrev•current_node⸥
history: ⸢optrev,list•history⸥
references: ⸢optrev,list•references⸥
depends_on: ⸢optrev,list•depends_on⸥
pills: ⸢optrev,list•pills⸥
files: ⸢optrev,list•files⸥
task_type: ⸢optrev•task_type⸥
inherits_from: ⸢optrev,list•inherits_from⸥
inherit_acceptance_context: ⸢optrev•inherit_acceptance_context⸥
atoms: ⸢optrev,list•atoms⸥
from_drawer: ⸢optrev•from_drawer⸥
closeout_evidence: ⸢optrev,list•closeout_evidence⸥
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

    @model_validator(mode="before")
    @classmethod
    def _apply_absent_frontmatter_defaults(cls, data: dict) -> dict:
        if isinstance(data, dict):
            return {
                key: value
                for key, value in data.items()
                if not (value is None and key in _ABSENT_FRONTMATTER_DEFAULTS)
            }
        return data

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

    closeout_evidence: list[str] = Field(
        default_factory=list,
        description=(
            "Evidence the closeout gate requires, declared when the task is created. "
            "Closed vocabulary: tests, commit, atom, materialization, document, external. "
            "Empty means the task predates the field and is gated as code."
        ),
    )

    @model_serializer(mode="wrap")
    def _omit_unset_optional_fields(self, handler):
        """Serialize from_drawer and closeout_evidence only when they are set.

        The same holds for closeout_evidence: tasks that predate it stay byte-identical.

        A field that always serialized would add ``from_drawer: ''`` to every task
        that has no drawer origin. Omitting it when empty keeps those documents
        byte-identical when re-rendered. It does not keep the contract hash stable:
        the field itself is part of the model contract and is hashed whether or not
        it serializes.
        """
        data = handler(self)
        if not data.get("from_drawer"):
            data.pop("from_drawer", None)
        if not data.get("closeout_evidence"):
            data.pop("closeout_evidence", None)
        return data
