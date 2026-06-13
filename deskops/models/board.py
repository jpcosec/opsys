from pydantic import Field

from .base import OperationalArtifactDoc


class BoardDoc(OperationalArtifactDoc):
    __semantics__ = {"type": ["workflow", "board"], "workspace": ["desk"]}
    __compositions__ = {
        "task_summaries": {
            "source_field": "tasks",
            "model": "deskops.models:TaskDoc",
            "template": "- {title} [{status}] - {goal}",
        }
    }
    __template__ = """---
id: ⸢rev•id⸥
scope: ⸢rev•scope⸥
tasks: ⸢rev•tasks⸥
pills: ⸢rev•pills⸥
rituals: ⸢rev•rituals⸥
tags: ⸢rev•tags⸥
---

# ⸢rev•title⸥

## Purpose

_Explain what this board routes and why it exists._

⸢rev•purpose⸥

## Notes

_Add short operational notes about the current routed set._

⸢rev•notes⸥

## Task Details

_Generated from the task references above._

⸢render•task_summaries⸥

""".strip()

    title: str = Field(description="Board title for one active routing surface.")
    id: str = Field(description="Stable board identifier.")
    scope: str = Field(description="What area or workspace this board routes.")
    purpose: str = Field(description="Why this board exists and what it indexes.")
    tasks: list[str] = Field(
        default_factory=list,
        description="Active task document references routed by this board.",
    )
    pills: list[str] = Field(
        default_factory=list,
        description="Active pill document references routed by this board.",
    )
    rituals: list[str] = Field(
        default_factory=list,
        description="Ritual document references relevant to this board.",
    )
    notes: str = Field(
        default="No additional notes.",
        description="Short operational notes about the current routed set.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb' or 'workspace:desk'.",
    )
