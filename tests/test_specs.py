from __future__ import annotations

import pytest
from pydantic import ValidationError

from deskops.models import TaskDoc
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.cli.model_introspection import artifact_id_pattern
from deskops.cli.model_introspection import artifact_status_default
from deskops.cli.model_introspection import artifact_tags_default
from deskops.operations import ARTIFACT_MODELS
from deskops.specs.compiler import compile_artifact_spec
from deskops.specs.compiler import compile_task_spec


ARTIFACT_KEYS = {"id_pattern", "status_default", "tags"}


def test_every_artifact_model_declares_its_artifact_defaults() -> None:
    for artifact_id, model in ARTIFACT_MODELS.items():
        if artifact_id == "artifact.review":
            # Reviews are written by `deskops review`, never by `deskops add`.
            assert not hasattr(model, "__artifact__")
            continue
        artifact = getattr(model, "__artifact__", None)
        assert isinstance(artifact, dict), artifact_id
        assert set(artifact) == ARTIFACT_KEYS, artifact_id
        assert artifact["id_pattern"].endswith("-{slug}"), artifact_id
        assert isinstance(artifact["tags"], list) and artifact["tags"], artifact_id


def test_task_artifact_defaults_are_inherited_by_every_task_type() -> None:
    assert TaskDoc.__artifact__ == {
        "id_pattern": "task-{slug}",
        "status_default": "draft",
        "tags": ["workspace:desk", "artifact:task"],
    }
    for model in TASK_TYPE_MODELS.values():
        assert model.__artifact__ is TaskDoc.__artifact__


def test_task_spec_compiler_builds_only_the_task_at_the_lifecycle_entry() -> None:
    compiled = compile_task_spec(
        {
            "title": "Spec authored task",
            "goal": "Drive task creation from YAML specs.",
            "scope": "Task pipeline only.",
            "implementation_path": "Compile artifact spec into runtime-ready docs.",
            "done_when": "The task is produced from specs.",
            "validation": ["pytest"],
        },
        entry_node="ritual-execution",
    )

    assert compiled.task_payload["id"] == "task-spec-authored-task"
    assert compiled.task_payload["current_node"] == "ritual-execution"
    assert "routine" not in compiled.task_payload
    assert "checklists" not in compiled.task_payload
    assert "field_refs" not in compiled.task_payload
    assert compiled.task_payload["title"] == "Spec authored task"
    assert compiled.task_payload["goal"] == "Drive task creation from YAML specs."
    assert compiled.task_payload["scope"] == "Task pipeline only."
    assert compiled.task_payload["implementation_path"] == "Compile artifact spec into runtime-ready docs."
    assert compiled.task_payload["validation"] == ["pytest"]
    assert compiled.task_payload["done_when"] == "The task is produced from specs."
    assert compiled.task_payload["status"] == "draft"
    assert compiled.task_payload["tags"] == ["workspace:desk", "artifact:task"]


def test_task_spec_compiler_is_the_one_task_normalization() -> None:
    """What `_normalize_task_payload` used to do now happens in the compiler."""
    with pytest.raises(KeyError, match="must include 'title'"):
        compile_task_spec({"goal": "no title"}, entry_node="ritual-execution")
    # A blank title is the model's refusal (TaskDoc.title), not the compiler's.
    with pytest.raises(ValidationError, match="Task title cannot be empty"):
        TaskDoc(**compile_task_spec({"title": "   "}, entry_node="ritual-execution").task_payload)

    compiled = compile_task_spec(
        {
            "title": "  Padded title  ",
            "references": "one-reference",
            "closeout_evidence": [" commit ", "", "document"],
            "current_node": "",
        },
        entry_node="ritual-execution",
    )
    assert compiled.task_payload["title"] == "Padded title"
    assert compiled.task_payload["references"] == ["one-reference"]
    assert compiled.task_payload["closeout_evidence"] == ["commit", "document"]
    assert compiled.task_payload["current_node"] == "ritual-execution"
    assert compiled.task_payload["why"] == "Not provided."

    stored = compile_task_spec({"title": "Stored task", "current_node": "ritual-testing"}, entry_node="")
    assert stored.task_payload["current_node"] == "ritual-testing"
    assert compile_task_spec({"title": "Stored task"}, entry_node="").task_payload["current_node"] == ""


def test_artifact_spec_compiler_reads_the_model_defaults() -> None:
    pill = compile_artifact_spec("artifact.pill", {"title": "A pill"}, model_fields=ARTIFACT_MODELS["artifact.pill"].model_fields.keys())
    assert pill.artifact_payload["id"] == "pill-a-pill"
    assert pill.artifact_payload["status"] == "active"

    atom = compile_artifact_spec(
        "artifact.atom",
        {"title": "An atom", "five_wh_one_plus": "what", "answer": "the answer"},
        model_fields=ARTIFACT_MODELS["artifact.atom"].model_fields.keys(),
    )
    assert atom.artifact_payload["id"] == "atom-an-atom"
    # The model's own `tags` default factory wins over the artifact default, as before.
    assert atom.artifact_payload["tags"] == []
    assert artifact_id_pattern("artifact.atom") == "atom-{slug}"
    assert artifact_status_default("artifact.atom") is None
    assert artifact_tags_default("artifact.atom") == ["system:deskops", "topic:atoms"]
    assert artifact_id_pattern("artifact.review") == "{slug}"
