from __future__ import annotations

from dataclasses import dataclass, field

from deskops.lifecycle import TransitionResult


@dataclass(slots=True)
class Task:
    """A task as deskops reads it: the TaskDoc fields plus inherited (``effective_*``) context.

    Its lifecycle position is ``current_node``, a ritual of the desk's lifecycle graph
    (deskops/lifecycle.py) or ``complete``.
    """

    id: str
    title: str
    status: str
    summary: str
    tags: list[str]
    current_node: str
    history: list[str]
    goal: str
    scope: str
    references: list[str]
    depends_on: list[str]
    pills: list[str]
    files: list[str]
    implementation_path: str
    validation: list[str]
    done_when: str
    task_type: str = ""
    inherits_from: list[str] = field(default_factory=list)
    inherit_acceptance_context: bool = False
    atoms: list[str] = field(default_factory=list)
    from_drawer: str = ""
    effective_references: list[str] = field(default_factory=list)
    effective_pills: list[str] = field(default_factory=list)
    effective_tags: list[str] = field(default_factory=list)
    effective_atoms: list[str] = field(default_factory=list)
    effective_validation: list[str] = field(default_factory=list)
    effective_done_when: str = ""


__all__ = ["Task", "TransitionResult"]
