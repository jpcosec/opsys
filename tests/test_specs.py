from __future__ import annotations

from pathlib import Path

from deskops.specs.compiler import compile_task_bundle_spec
from deskops.specs.loader import SpecRegistry
from deskops.specs.mermaid import render_artifact_structure_mermaid
from deskops.specs.mermaid import render_task_routine_mermaid


ROOT = Path(__file__).resolve().parents[1]


def test_spec_registry_loads_fields_primitives_and_artifacts() -> None:
    registry = SpecRegistry.load(ROOT / "spec")

    assert "field.goal" in registry.fields
    assert "field.validation" in registry.fields
    assert "primitive.task.activate" in registry.primitives
    assert "artifact.task" in registry.artifacts
    assert "artifact.pill" in registry.artifacts
    assert "artifact.ritual" in registry.artifacts
    assert "artifact.board" in registry.artifacts
    assert "artifact.atom" in registry.artifacts
    assert "artifact.repository" in registry.artifacts
    assert "artifact.inbox_note" in registry.artifacts
    assert "artifact.faq" in registry.artifacts
    assert "artifact.step" in registry.artifacts
    assert "field.description" in registry.fields
    assert "field.related_atoms" in registry.fields
    assert "field.created_at" in registry.fields


def test_task_spec_compiler_builds_bundle_from_yaml_specs() -> None:
    registry = SpecRegistry.load(ROOT / "spec")
    compiled = compile_task_bundle_spec(
        registry,
        {
            "title": "Spec authored task",
            "goal": "Drive task creation from YAML specs.",
            "scope": "Task pipeline only.",
            "implementation_path": "Compile artifact spec into runtime-ready docs.",
            "done_when": "The task bundle is produced from specs.",
            "validation": ["pytest"],
        },
    )

    assert compiled.task_payload["id"] == "task-spec-authored-task"
    assert compiled.task_payload["current_node"] == "checklist-task-spec-authored-task-execution-ready"
    assert compiled.routine_payload["id"] == "routine-task-spec-authored-task"
    assert "field_refs" not in compiled.task_payload
    assert compiled.task_payload["title"] == "Spec authored task"
    assert compiled.task_payload["goal"] == "Drive task creation from YAML specs."
    assert compiled.task_payload["scope"] == "Task pipeline only."
    assert compiled.task_payload["implementation_path"] == "Compile artifact spec into runtime-ready docs."
    assert compiled.task_payload["validation"] == ["pytest"]
    assert compiled.task_payload["done_when"] == "The task bundle is produced from specs."
    assert compiled.condition_payloads[0]["id"] == "condition-task-spec-authored-task-has-implementation-path"
    assert any(item["id"] == "condition-task-spec-authored-task-has-closeout-evidence" for item in compiled.condition_payloads)
    assert compiled.checklist_payloads[0]["condition_refs"] == []
    assert compiled.checklist_payloads[-1]["condition_refs"] == [
        "condition-task-spec-authored-task-ready-for-closeout",
        "condition-task-spec-authored-task-has-closeout-evidence",
    ]
    assert compiled.operator_payloads[-1]["value"] == "closed"


def test_mermaid_views_render_from_task_specs() -> None:
    registry = SpecRegistry.load(ROOT / "spec")
    structure = render_artifact_structure_mermaid(registry, "artifact.task")
    routine = render_task_routine_mermaid(registry, "artifact.task")

    assert "artifact.task[Task Artifact]" in structure
    assert "field.goal[field.goal]" in structure
    assert "Execution Ready" in routine
    assert "operator-task-id-close" in routine
