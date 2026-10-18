from __future__ import annotations

from pathlib import Path

import pytest

from deskops import lifecycle
from deskops.cli.main import main
from deskops.lifecycle_migration import inspect_legacy_lifecycle
from deskops.lifecycle_migration import legacy_node_to_ritual
from deskops.lifecycle_migration import migrate_legacy_lifecycle
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations


def _task(operations: DeskopsOperations, title: str, **extra: object) -> str:
    payload = {
        "title": title,
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
        **extra,
    }
    return operations.create_task_bundle(payload).task_id


def test_the_lifecycle_graph_lives_in_the_store_as_rituals_and_relation_docs(lifecycle_desk: Path) -> None:
    from sldb.api import doc_exists

    store = lifecycle_desk / ".sldb"
    for ritual in ("ritual-execution", "ritual-testing", "ritual-closeout"):
        assert doc_exists(store, f"RitualDoc/{ritual}")
    for name in ("task_activates", "task_hands_to_closeout", "task_completes"):
        assert doc_exists(store, f"RelationTypeDoc/type-{name}")
    edges = lifecycle.transitions_from(lifecycle_desk, "ritual-testing")
    assert [(e.relation_type, e.target, e.condition) for e in edges] == [
        ("task_hands_to_closeout", "ritual-closeout", "nonempty(validation)")
    ]
    closing = lifecycle.transitions_from(lifecycle_desk, "ritual-closeout")
    assert closing[0].target == "ritual-closeout" and closing[0].terminal, "completion is a self-loop"


def test_ensure_lifecycle_graph_is_idempotent(lifecycle_desk: Path) -> None:
    assert lifecycle.ensure_lifecycle_graph(lifecycle_desk) == []
    assert lifecycle.lifecycle_graph_present(lifecycle_desk)


def test_an_old_ritual_without_step_details_is_rerendered_before_tracking(tmp_path: Path) -> None:
    from deskops.bootstrap import SLDBBootstrap
    from deskops.doc_readability import is_unreadable_by_model
    from deskops.models import RitualDoc
    from deskops.workspace import scaffold_desk
    from sldb.runtime.validation import render_model_markdown

    root = tmp_path / "repo"
    root.mkdir()
    assert SLDBBootstrap().init_local_store(root) == 0
    scaffold_desk(root)
    ritual = root / "desk" / "rituals" / "execution.md"
    current = render_model_markdown(
        RitualDoc,
        {
            "id": "ritual-execution",
            "title": "Execution ritual",
            "tags": ["workspace:desk"],
            "purpose": "Carry one active task through scoped implementation.",
            "trigger": "Start when a task is active.",
            "preconditions": ["A task exists."],
            "validation": ["The task is explicit."],
            "failure_modes": ["Skipping the task."],
            "completion": "The implementation is ready for testing.",
        },
    )
    old_style = current.split("## Step Details")[0].rstrip() + "\n"
    ritual.write_text(old_style, encoding="utf-8")
    assert is_unreadable_by_model(RitualDoc, old_style), "the old-style ritual is the failure case"

    changes = lifecycle.ensure_lifecycle_graph(root)

    assert any("re-rendered desk/rituals/execution.md" in change for change in changes)
    text = ritual.read_text(encoding="utf-8")
    assert "## Step Details" in text
    assert is_unreadable_by_model(RitualDoc, text) == []
    assert main(["doctor", "--root", str(root)]) == 0


@pytest.mark.parametrize(
    "legacy",
    [
        "# Execution ritual\n\nReview the board and implement only the active task.\n",
        "---\nid: ritual-execution\ntags:\n- workspace:desk\n---\n\n# Execution ritual\n\n"
        "Execute one task at a time.\n\n## Pre-flight\n\n1. Recover board state.\n",
    ],
    ids=["no-frontmatter", "own-sections"],
)
def test_a_ritual_the_model_cannot_carry_is_archived_and_replaced(tmp_path: Path, legacy: str) -> None:
    from deskops.bootstrap import SLDBBootstrap
    from deskops.workspace import scaffold_desk
    from sldb.api import doc_exists

    root = tmp_path / "repo"
    root.mkdir()
    assert SLDBBootstrap().init_local_store(root) == 0
    scaffold_desk(root)
    ritual = root / "desk" / "rituals" / "execution.md"
    ritual.write_text(legacy, encoding="utf-8")

    changes = lifecycle.ensure_lifecycle_graph(root)

    archived = root / "desk" / "drawer" / "rituals" / "legacy-execution.md"
    assert archived.read_text(encoding="utf-8") == legacy
    assert any("archived desk/rituals/execution.md" in change for change in changes)
    assert "id: ritual-execution" in ritual.read_text(encoding="utf-8")
    assert doc_exists(root / ".sldb", "RitualDoc/ritual-execution")
    assert main(["doctor", "--root", str(root)]) == 0


def test_advance_walks_the_graph_and_sets_status_per_transition(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Walk the graph")

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status, result.progressed) == ("ritual-testing", "active", True)

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status) == ("ritual-closeout", "ready_for_testing")

    task, result = operations.advance_task(task_id)
    assert result.blocked and not result.progressed
    assert "task_completes" in result.message, "the blocked gate is named"
    payload = operations._read_doc(lifecycle_desk / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    assert payload["history"] == ["task_activates", "task_hands_to_closeout"]


def test_testing_gate_needs_validation(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "No validation", validation=[])
    operations.advance_task(task_id)

    task, result = operations.advance_task(task_id)

    assert result.blocked
    assert task.current_node == "ritual-testing"


def test_show_task_reports_the_gates_leaving_the_current_node(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Show gates")
    operations.advance_task(task_id)

    _task_obj, gates = operations.show_task(task_id)

    assert gates == [
        {"relation_type": "task_hands_to_closeout", "target": "ritual-closeout", "condition": "nonempty(validation)", "holds": True}
    ]


def test_advance_without_a_lifecycle_graph_says_how_to_get_one(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    task_id = _task(operations, "No graph")

    with pytest.raises(lifecycle.LifecycleGraphMissing, match="deskops init"):
        operations.advance_task(task_id)


@pytest.mark.parametrize(
    ("legacy", "expected"),
    [
        ("checklist-task-x-execution-ready", "ritual-execution"),
        ("checklist-task-foo-bar-testing-ready", "ritual-testing"),
        ("checklist-task-x-closeout-ready", "ritual-closeout"),
        ("complete", "complete"),
        ("ritual-testing", "ritual-testing"),
    ],
)
def test_legacy_nodes_map_onto_rituals(legacy: str, expected: str) -> None:
    assert legacy_node_to_ritual(legacy) == expected


def test_migration_removes_primitives_rewrites_tasks_and_writes_the_graph(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    (root / "desk" / "routines").mkdir()
    (root / "desk" / "routines" / "routine-task-old.md").write_text("---\nid: routine-task-old\n---\n", encoding="utf-8")
    checklists = root / "desk" / "primitives" / "checklists"
    checklists.mkdir(parents=True)
    (checklists / "checklist-task-old-testing-ready.md").write_text("---\nid: checklist-task-old-testing-ready\n---\n", encoding="utf-8")
    task = root / "desk" / "tasks" / "task-old.md"
    task.write_text(
        "---\nid: task-old\nstatus: active\nroutine: routine-task-old\n"
        "current_node: checklist-task-old-testing-ready\nchecklists:\n- checklist-task-old-testing-ready\n"
        "closeout_evidence_verified: false\npill_graduation_verified: true\n---\n\n# Old\n\nBody stays.\n",
        encoding="utf-8",
    )

    report = inspect_legacy_lifecycle(root)
    assert report.needs_migration
    assert len(report.primitive_docs) == 2 and report.tasks_to_rewrite == [task]

    migrate_legacy_lifecycle(root)

    assert not (root / "desk" / "routines").exists()
    assert not (root / "desk" / "primitives").exists()
    text = task.read_text(encoding="utf-8")
    for key in ("routine:", "checklists:", "closeout_evidence_verified", "pill_graduation_verified"):
        assert key not in text
    assert "current_node: ritual-testing" in text
    assert text.endswith("# Old\n\nBody stays.\n")
    assert not inspect_legacy_lifecycle(root).needs_migration
    assert migrate_legacy_lifecycle(root)[-1] == "updated store indexes", "a second run changes nothing else"
