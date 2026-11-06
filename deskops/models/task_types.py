"""Factory task types: ``TaskDoc`` subclasses that fix ``task_type`` and declare their gates.

A task type is a model, not a string: the family ``model <= TaskCodeDoc`` names the
documents of ``task.code`` and of every subtype that extends it (``task.refactor``), while
``task.debug`` deliberately extends ``TaskDoc`` instead of ``TaskCodeDoc`` because it swaps
``bundle`` for ``reproduction`` — a subtype only ever *adds* gates, it cannot remove one
(brief.md §Tipos, decisions.md DC1/D2).

Each concrete type fixes ``task_type`` to its name with a ``Literal`` default and declares two
class attributes:

- ``__closeout_evidence__``: the closeout evidence kinds ``deskops closeout verify`` checks.
  It uses the vocabulary of ``deskops.services.closeout_gates.CLOSEOUT_EVIDENCE_VOCABULARY``
  (tests, commit, atom, materialization, document, external) plus, for this node, ``children``
  (the aggregate) and ``goldens`` (the refactor) — both are only *declared* here; their
  verification lands in GC09 and a later node (TaskDoc precisión 3).
- ``__activation_receipts__``: the ``ReviewDoc`` kinds the GC05 activation rule will require
  (preflight, bundle, reproduction, goldens, owner). Declared here, evaluated later.

``TaskDoc`` itself keeps ``task_type: str`` so old documents still read, and declares
``__contract__`` (the contract fields; sldb GO02 (e)).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from .task import TaskDoc


class TaskCodeDoc(TaskDoc):
    """``task.code``: code changes gated by tests, a commit and an atom|materialization link."""

    task_type: Literal["task.code"] = Field(
        default="task.code",
        description="Workflow task type; fixed to 'task.code' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")
    __activation_receipts__ = ("preflight", "bundle")


class TaskDocsDoc(TaskDoc):
    """``task.docs``: document-only work gated by a commit and a document."""

    task_type: Literal["task.docs"] = Field(
        default="task.docs",
        description="Workflow task type; fixed to 'task.docs' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")
    __activation_receipts__ = ("preflight",)


class TaskDebugDoc(TaskDoc):
    """``task.debug``: gated like ``task.code`` but activated by a reproduction, not a bundle.

    It extends ``TaskDoc`` directly: a subtype only adds gates, and this type replaces the
    ``bundle`` receipt of ``task.code`` with ``reproduction``, so it cannot be a ``task.code``.
    """

    task_type: Literal["task.debug"] = Field(
        default="task.debug",
        description="Workflow task type; fixed to 'task.debug' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization")
    __activation_receipts__ = ("preflight", "reproduction")


class TaskRefactorDoc(TaskCodeDoc):
    """``task.refactor``: a ``task.code`` that additionally requires goldens before and after."""

    task_type: Literal["task.refactor"] = Field(
        default="task.refactor",
        description="Workflow task type; fixed to 'task.refactor' for this model.",
    )
    __closeout_evidence__ = ("tests", "commit", "atom", "materialization", "goldens")
    __activation_receipts__ = ("preflight", "bundle", "goldens")


class TaskDecisionDoc(TaskDoc):
    """``task.decision``: gated by an owner receipt, a commit and a document."""

    task_type: Literal["task.decision"] = Field(
        default="task.decision",
        description="Workflow task type; fixed to 'task.decision' for this model.",
    )
    __closeout_evidence__ = ("commit", "document")
    __activation_receipts__ = ("owner",)


class TaskAggregateDoc(TaskDoc):
    """``task.aggregate``: closes when its children do (``children`` is declared, GC09 verifies it)."""

    task_type: Literal["task.aggregate"] = Field(
        default="task.aggregate",
        description="Workflow task type; fixed to 'task.aggregate' for this model.",
    )
    __closeout_evidence__ = ("children", "commit")
    __activation_receipts__ = ()


class TaskExternalDoc(TaskDoc):
    """``task.external``: external work evidenced by an http(s) URL."""

    task_type: Literal["task.external"] = Field(
        default="task.external",
        description="Workflow task type; fixed to 'task.external' for this model.",
    )
    __closeout_evidence__ = ("external",)
    __activation_receipts__ = ("preflight",)


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


def task_type_closeout_evidence(task_type: str) -> tuple[str, ...] | None:
    """The ``__closeout_evidence__`` a factory type declares, or ``None`` when unknown."""
    model = factory_task_type_model(task_type)
    if model is None:
        return None
    return tuple(getattr(model, "__closeout_evidence__", ()))


def task_type_activation_receipts(task_type: str) -> tuple[str, ...]:
    """The ``__activation_receipts__`` a factory type declares (empty when unknown)."""
    model = factory_task_type_model(task_type)
    if model is None:
        return ()
    return tuple(getattr(model, "__activation_receipts__", ()))


def declared_evidence_list(value: object) -> list[str]:
    """The stored ``closeout_evidence`` as plain strings; the vocabulary is checked where it is used."""
    if isinstance(value, list):
        items = [str(item) for item in value]
    elif value in (None, ""):
        items = []
    else:
        items = [str(value)]
    return [item.strip() for item in items if item.strip()]
