"""The public extension registries must agree as one contract.

Models, spec artifacts, artifact maps, and CLI handlers are declared in separate
places and maintained by convention. These tests fail when one of them drifts,
so a new model or command cannot land half-registered.
"""

from __future__ import annotations

import importlib

from sldb import StructuredNLDoc

from deskops import models
from deskops.bootstrap import MODEL_REFS
from deskops.cli.registry import command_registry
from deskops.operations import ARTIFACT_MODELS
from deskops.operations import ARTIFACT_PATHS
from deskops.operations import ARTIFACT_SUBJECTS

TASK_ARTIFACT = "artifact.task"


def test_every_artifact_model_has_a_path() -> None:
    assert set(ARTIFACT_MODELS) <= set(ARTIFACT_PATHS)
    assert set(ARTIFACT_PATHS) <= set(ARTIFACT_MODELS)


def test_every_artifact_except_task_has_a_subject() -> None:
    assert set(ARTIFACT_MODELS) - set(ARTIFACT_SUBJECTS) == {TASK_ARTIFACT}
    assert set(ARTIFACT_SUBJECTS) <= set(ARTIFACT_MODELS)


def test_model_refs_are_exported_structured_documents() -> None:
    for name in MODEL_REFS:
        assert name in models.__all__, f"{name} is registered but not exported"
        model = getattr(models, name)
        assert isinstance(model, type)
        assert issubclass(model, StructuredNLDoc)


def test_every_creatable_artifact_model_declares_its_defaults() -> None:
    for artifact_id, model in ARTIFACT_MODELS.items():
        creatable = ARTIFACT_SUBJECTS.get(artifact_id, {}).get("create", True)
        if not creatable:
            continue
        artifact = getattr(model, "__artifact__", None)
        assert isinstance(artifact, dict), f"{artifact_id} ({model.__name__}) declares no __artifact__"
        assert {"id_pattern", "status_default", "tags"} <= set(artifact), artifact_id


def test_every_command_handler_resolves() -> None:
    commands = command_registry()
    assert commands

    for command in commands:
        module_name, separator, attribute = command.handler.partition(":")
        assert separator and module_name and attribute, (
            f"{command.path} handler is not module:attribute: {command.handler}"
        )
        module = importlib.import_module(module_name)
        handler = getattr(module, attribute)
        assert callable(handler), f"{command.path} handler is not callable: {command.handler}"
