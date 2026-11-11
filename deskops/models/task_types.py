"""Factory task types: ``TaskDoc`` subclasses that fix ``task_type`` and declare their gates.

A task type is a model, not a string: the family ``model <= TaskCodeDoc`` names the
documents of ``task.code`` and of every subtype that extends it (``task.refactor``), while
``task.debug`` deliberately extends ``TaskDoc`` instead of ``TaskCodeDoc`` because it swaps
``bundle`` for ``reproduction`` — a subtype only ever *adds* gates, it cannot remove one
(brief.md §Tipos, decisions.md DC1/D2).

Each concrete type fixes ``task_type`` to its name with a ``Literal`` default. Its closeout
evidence is data, not a class attribute: ``deskops/data/rules/closeout-evidence.yaml`` maps
each factory type to the kinds ``deskops closeout verify`` checks (``closeout_evidence_kinds``;
a desk subtype reads its nearest factory ancestor's), and the closeout gate is the ``RuleDoc``
seed ``deskops/data/rules/rule-closeout-<type>.md`` (CC33b) that asks for those receipts.

The activation gate of a type is not Python either: it is the ``RuleDoc`` seed
``deskops/data/rules/rule-activation-<type>.md`` (CC32), whose subject ``model <= <TypeDoc>``
names the family, so it needs no attribute here and a subtype inherits it.

``TaskDoc`` itself keeps ``task_type: str`` so old documents still read, and declares
``__contract__`` (the contract fields; sldb GO02 (e)).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Literal

from pydantic import Field
import yaml

from deskops.paths import data_path

from .task import TaskDoc


class TaskCodeDoc(TaskDoc):
    """``task.code``: code changes gated by tests, a commit and an atom|materialization link."""

    task_type: Literal["task.code"] = Field(
        default="task.code",
        description="Workflow task type; fixed to 'task.code' for this model.",
    )


class TaskDocsDoc(TaskDoc):
    """``task.docs``: document-only work gated by a commit and a document."""

    task_type: Literal["task.docs"] = Field(
        default="task.docs",
        description="Workflow task type; fixed to 'task.docs' for this model.",
    )


class TaskDebugDoc(TaskDoc):
    """``task.debug``: gated like ``task.code`` but activated by a reproduction, not a bundle.

    It extends ``TaskDoc`` directly: a subtype only adds gates, and this type replaces the
    ``bundle`` receipt of ``task.code`` with ``reproduction``, so it cannot be a ``task.code``.
    """

    task_type: Literal["task.debug"] = Field(
        default="task.debug",
        description="Workflow task type; fixed to 'task.debug' for this model.",
    )


class TaskRefactorDoc(TaskCodeDoc):
    """``task.refactor``: a ``task.code`` that additionally requires goldens before and after."""

    task_type: Literal["task.refactor"] = Field(
        default="task.refactor",
        description="Workflow task type; fixed to 'task.refactor' for this model.",
    )


class TaskDecisionDoc(TaskDoc):
    """``task.decision``: gated by an owner receipt, a commit and a document."""

    task_type: Literal["task.decision"] = Field(
        default="task.decision",
        description="Workflow task type; fixed to 'task.decision' for this model.",
    )


class TaskAggregateDoc(TaskDoc):
    """``task.aggregate``: closes when its children do (``children`` is declared, GC09 verifies it)."""

    task_type: Literal["task.aggregate"] = Field(
        default="task.aggregate",
        description="Workflow task type; fixed to 'task.aggregate' for this model.",
    )


class TaskExternalDoc(TaskDoc):
    """``task.external``: external work evidenced by an http(s) URL."""

    task_type: Literal["task.external"] = Field(
        default="task.external",
        description="Workflow task type; fixed to 'task.external' for this model.",
    )


#: Factory task type name -> model class. Desk-local types extend this set through
#: ``desk/models/*.py`` and are registered into the store by ``deskops desk update --apply``.
TASK_TYPE_MODELS: dict[str, type[TaskDoc]] = {
    "task.code": TaskCodeDoc,
    "task.docs": TaskDocsDoc,
    "task.debug": TaskDebugDoc,
    "task.refactor": TaskRefactorDoc,
    "task.decision": TaskDecisionDoc,
    "task.aggregate": TaskAggregateDoc,
    "task.external": TaskExternalDoc,
}

#: Legacy ``task_type`` strings -> canonical factory type name. Mirrors the migration in
#: ``deskops desk update --apply`` (TaskDoc precisión 4).
LEGACY_TASK_TYPE_MAP: dict[str, str] = {
    "code": "task.code",
    "implementation": "task.code",
    "test": "task.code",
    "docs": "task.docs",
    "spec": "task.docs",
    "design": "task.docs",
    "external": "task.external",
    "": "task.code",
}


def canonical_task_type_name(task_type: str) -> str:
    """Map a stored ``task_type`` to its canonical factory type name.

    A value that is already a factory type name is kept; a known legacy string is mapped;
    anything else (including an unknown value) resolves to ``task.code``, matching the
    ``desk update --apply`` migration.
    """
    name = str(task_type or "").strip().lower()
    if name in TASK_TYPE_MODELS:
        return name
    return LEGACY_TASK_TYPE_MAP.get(name, "task.code")


def factory_task_type_model(task_type: str) -> type[TaskDoc] | None:
    """The factory model class a canonical task type name resolves to, if any."""
    return TASK_TYPE_MODELS.get(canonical_task_type_name(task_type))


CLOSEOUT_EVIDENCE_TABLE = data_path("data", "rules", "closeout-evidence.yaml")


@lru_cache(maxsize=1)
def closeout_evidence_table() -> dict[str, tuple[str, ...]]:
    """``deskops/data/rules/closeout-evidence.yaml``: factory task type -> its closeout evidence kinds."""
    payload = yaml.safe_load(CLOSEOUT_EVIDENCE_TABLE.read_text(encoding="utf-8")) or {}
    return {str(name): tuple(str(kind) for kind in kinds or ()) for name, kinds in payload.items()}


def closeout_evidence_kinds(model: type[Any]) -> tuple[str, ...] | None:
    """The closeout evidence kinds of a task model: the table's entry for the nearest class of
    its MRO whose ``task_type`` default is a factory type (a desk subtype reads its ancestor's);
    ``None`` when no class of the MRO is a factory type."""
    table = closeout_evidence_table()
    for cls in getattr(model, "__mro__", ()):
        field = getattr(cls, "model_fields", {}).get("task_type")
        name = getattr(field, "default", None)
        if isinstance(name, str) and name in table:
            return table[name]
    return None


def declared_evidence_list(value: object) -> list[str]:
    """The stored ``closeout_evidence`` as plain strings; the vocabulary is checked where it is used."""
    if isinstance(value, list):
        items = [str(item) for item in value]
    elif value in (None, ""):
        items = []
    else:
        items = [str(value)]
    return [item.strip() for item in items if item.strip()]
