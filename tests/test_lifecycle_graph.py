from __future__ import annotations

from pathlib import Path

import pytest

from deskops import lifecycle
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
