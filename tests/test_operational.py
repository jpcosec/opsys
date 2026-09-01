from __future__ import annotations

from pathlib import Path

import pytest

from deskops.models.task import TaskDoc
from deskops.operations import DeskopsOperations
from deskops.runtime.primitives import Checklist
from deskops.runtime.primitives import Condition
from deskops.runtime.primitives import Edge
from deskops.runtime.primitives import Operator
from deskops.runtime.primitives import Routine


def test_create_artifact_rolls_back_file_when_tracking_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)

    def fail_tracking(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("tracking failed")

    monkeypatch.setattr(operations, "_track_created_artifact", fail_tracking)

    with pytest.raises(RuntimeError, match="tracking failed"):
        operations.create_artifact(
            "artifact.atom",
            {
                "title": "Rollback atom",
                "five_wh_one_plus": "what",
                "answer": "Created files must disappear if tracking fails.",
            },
        )

    assert not list((tmp_path / "desk" / "atoms").glob("atom-rollback-atom.md"))


def test_create_primitive_rolls_back_partial_file_when_write_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)
    original_write_doc = operations._write_doc

    def fail_after_write(path: Path, model: type[object], payload: dict[str, object]) -> None:
        original_write_doc(path, model, payload)
        raise RuntimeError("write failed")

    monkeypatch.setattr(operations, "_write_doc", fail_after_write)

    with pytest.raises(RuntimeError, match="write failed"):
        operations.create_primitive(
            "condition",
            {
                "title": "Rollback condition",
                "subject": "status",
                "predicate": "truthy",
            },
        )

    assert not (tmp_path / "desk" / "primitives" / "conditions" / "condition-rollback-condition.md").exists()


def test_create_routine_rolls_back_partial_file_when_write_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)
    original_write_doc = operations._write_doc

    def fail_after_write(path: Path, model: type[object], payload: dict[str, object]) -> None:
        original_write_doc(path, model, payload)
        raise RuntimeError("write failed")

    monkeypatch.setattr(operations, "_write_doc", fail_after_write)

    with pytest.raises(RuntimeError, match="write failed"):
        operations.create_routine(
            {
                "title": "Rollback routine",
                "entrypoint": "checklist-ready",
                "decomposition": ["checklist-ready"],
                "edges": [],
                "terminal_nodes": ["complete"],
            },
        )

    assert not (tmp_path / "desk" / "routines" / "routine-rollback-routine.md").exists()


def test_create_task_bundle_rolls_back_files_when_later_write_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)
    original_write_doc = operations._write_doc

    def fail_on_checklist(path: Path, model: type[object], payload: dict[str, object]) -> None:
        original_write_doc(path, model, payload)
        if path.name == "checklist-task-rollback-bundle-execution-ready.md":
            raise RuntimeError("checklist write failed")

    monkeypatch.setattr(operations, "_write_doc", fail_on_checklist)

    with pytest.raises(RuntimeError, match="checklist write failed"):
        operations.create_task_bundle(
            {
                "title": "Rollback bundle",
                "goal": "Prove rollback.",
                "scope": "Task bundle creates.",
                "implementation_path": "deskops/operations.py",
                "done_when": "No orphan files remain.",
            }
        )

    assert not list((tmp_path / "desk" / "tasks").glob("task-rollback-bundle.md"))
    assert not list((tmp_path / "desk" / "routines").glob("routine-task-rollback-bundle.md"))
    assert not list((tmp_path / "desk" / "primitives").rglob("*task-rollback-bundle*.md"))
    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-rollback-bundle.md" not in board_text


def test_create_task_bundle_restores_board_when_append_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.ensure_workspace()
    board_path = tmp_path / "desk" / "tasks" / "Board.md"
    original_board_text = board_path.read_text(encoding="utf-8")
    original_append = operations._append_task_to_board

    def fail_after_append(task_id: str) -> None:
        original_append(task_id)
        raise RuntimeError("board append failed")

    monkeypatch.setattr(operations, "_append_task_to_board", fail_after_append)

    with pytest.raises(RuntimeError, match="board append failed"):
        operations.create_task_bundle(
            {
                "title": "Rollback board",
                "goal": "Prove board rollback.",
                "scope": "Board mutation.",
                "implementation_path": "deskops/operations.py",
                "done_when": "Board is restored.",
            }
        )

    assert board_path.read_text(encoding="utf-8") == original_board_text
    assert not list((tmp_path / "desk" / "tasks").glob("task-rollback-board.md"))
    assert not list((tmp_path / "desk").rglob("*task-rollback-board*.md"))


def test_create_primitive_refuses_existing_file_without_overwriting(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    created = operations.create_primitive(
        "condition",
        {
            "title": "Existing condition",
            "subject": "status",
            "predicate": "truthy",
        },
    )
    original_text = created.path.read_text(encoding="utf-8")

    with pytest.raises(FileExistsError):
        operations.create_primitive(
            "condition",
            {
                "title": "Existing condition",
                "subject": "changed",
                "predicate": "equals",
                "expected": "done",
            },
        )

    assert created.path.read_text(encoding="utf-8") == original_text


def test_condition_and_checklist_evaluate_against_payload() -> None:
    payload = {
        "status": "draft",
        "validation": ["pytest"],
        "references": ["pytest tests/test_operational.py"],
        "implementation_path": "Ship the runtime.",
    }
    conditions = {
        "condition-has-validation": Condition(
            id="condition-has-validation",
            title="Has validation",
            status="active",
            summary="Validation must be present.",
            tags=[],
            subject="validation",
            predicate="not_empty",
            expected="",
        ),
        "condition-has-implementation": Condition(
            id="condition-has-implementation",
            title="Has implementation path",
            status="active",
            summary="Implementation path must be present.",
            tags=[],
            subject="implementation_path",
            predicate="truthy",
            expected="",
        ),
    }
    checklist = Checklist(
        id="checklist-ready",
        title="Ready checklist",
        status="active",
        summary="Checks the task contract.",
        tags=[],
        items=["Validation exists", "Implementation path exists"],
        condition_refs=list(conditions),
        mode="all",
    )

    assert conditions["condition-has-validation"].evaluate(payload) is True
    assert checklist.is_complete(payload, conditions) is True


def test_routine_advance_runs_operators_until_next_gate() -> None:
    payload = {
        "status": "draft",
        "implementation_path": "Create the runtime.",
        "validation": ["pytest"],
        "references": [],
        "closeout_evidence_verified": False,
        "done_when": "The task reaches closed.",
        "current_node": "checklist-execution",
    }
    conditions = {
        "condition-has-implementation": Condition(
            id="condition-has-implementation",
            title="Has implementation",
            status="active",
            summary="",
            tags=[],
            subject="implementation_path",
            predicate="truthy",
            expected="",
        ),
        "condition-has-validation": Condition(
            id="condition-has-validation",
            title="Has validation",
            status="active",
            summary="",
            tags=[],
            subject="validation",
            predicate="not_empty",
            expected="",
        ),
        "condition-has-closeout-evidence": Condition(
            id="condition-has-closeout-evidence",
            title="Durable evidence is verified",
            status="active",
            summary="",
            tags=[],
            subject="closeout_evidence_verified",
            predicate="truthy",
            expected="",
        ),
        "condition-ready-for-closeout": Condition(
            id="condition-ready-for-closeout",
            title="Ready for closeout",
            status="active",
            summary="",
            tags=[],
            subject="status",
            predicate="equals",
            expected="ready_for_testing",
        ),
    }
    checklists = {
        "checklist-execution": Checklist(
            id="checklist-execution",
            title="Execution gate",
            status="active",
            summary="",
            tags=[],
            items=["Implementation path exists"],
            condition_refs=["condition-has-implementation"],
            mode="all",
        ),
        "checklist-testing": Checklist(
            id="checklist-testing",
            title="Testing gate",
            status="active",
            summary="",
            tags=[],
            items=["Validation exists"],
            condition_refs=["condition-has-validation"],
            mode="all",
        ),
        "checklist-closeout": Checklist(
            id="checklist-closeout",
            title="Closeout gate",
            status="active",
            summary="",
            tags=[],
            items=["Task is ready for closeout", "Durable evidence is verified"],
            condition_refs=["condition-ready-for-closeout", "condition-has-closeout-evidence"],
            mode="all",
        ),
    }
    operators = {
        "operator-activate": Operator(
            id="operator-activate",
            title="Activate",
            status="active",
            summary="",
            tags=[],
            action="set_field",
            target="status",
            value="active",
        ),
        "operator-ready-for-testing": Operator(
            id="operator-ready-for-testing",
            title="Ready for testing",
            status="active",
            summary="",
            tags=[],
            action="set_field",
            target="status",
            value="ready_for_testing",
        ),
        "operator-close": Operator(
            id="operator-close",
            title="Close",
            status="active",
            summary="",
            tags=[],
            action="set_field",
            target="status",
            value="closed",
        ),
    }
    routine = Routine(
        id="routine-task",
        title="Task routine",
        status="active",
        summary="Task lifecycle",
        tags=[],
        entrypoint="checklist-execution",
        decomposition=[
            "checklist-execution",
            "operator-activate",
            "checklist-testing",
            "operator-ready-for-testing",
            "checklist-closeout",
            "operator-close",
        ],
        edges=[
            Edge(
                id="edge-1",
                title="Execution to activate",
                status="active",
                summary="",
                tags=[],
                source="checklist-execution",
                target="operator-activate",
                condition_ref="",
            ),
            Edge(
                id="edge-2",
                title="Activate to testing",
                status="active",
                summary="",
                tags=[],
                source="operator-activate",
                target="checklist-testing",
                condition_ref="",
            ),
            Edge(
                id="edge-3",
                title="Testing to ready",
                status="active",
                summary="",
                tags=[],
                source="checklist-testing",
                target="operator-ready-for-testing",
                condition_ref="",
            ),
            Edge(
                id="edge-4",
                title="Ready to closeout",
                status="active",
                summary="",
                tags=[],
                source="operator-ready-for-testing",
                target="checklist-closeout",
                condition_ref="",
            ),
            Edge(
                id="edge-5",
                title="Closeout to close",
                status="active",
                summary="",
                tags=[],
                source="checklist-closeout",
                target="operator-close",
                condition_ref="",
            ),
        ],
        terminal_nodes=["complete"],
    )

    first = routine.advance(
        payload,
        conditions=conditions,
        operators=operators,
        checklists=checklists,
    )
    assert first.current_node == "checklist-testing"
    assert payload["status"] == "active"

    second = routine.advance(
        payload,
        conditions=conditions,
        operators=operators,
        checklists=checklists,
    )
    assert second.current_node == "checklist-closeout"
    assert payload["status"] == "ready_for_testing"

    third = routine.advance(
        payload,
        conditions=conditions,
        operators=operators,
        checklists=checklists,
    )
    assert third.current_node == "checklist-closeout"
    assert third.blocked is True
    assert payload["status"] == "ready_for_testing"

    payload["references"] = ["pytest tests/test_operational.py::test_routine_advance_runs_operators_until_next_gate"]
    payload["closeout_evidence_verified"] = True
    fourth = routine.advance(
        payload,
        conditions=conditions,
        operators=operators,
        checklists=checklists,
    )
    assert fourth.current_node == "complete"
    assert payload["status"] == "closed"


def test_routine_advance_rejects_missing_edge_target() -> None:
    routine = Routine(
        id="routine-task",
        title="Task routine",
        status="active",
        summary="",
        tags=[],
        entrypoint="checklist-execution",
        decomposition=["checklist-execution"],
        edges=[
            Edge(
                id="edge-missing-target",
                title="Bad edge",
                status="active",
                summary="",
                tags=[],
                source="checklist-execution",
                target="operator-missing",
                condition_ref="",
            )
        ],
        terminal_nodes=["complete"],
    )
    checklists = {
        "checklist-execution": Checklist(
            id="checklist-execution",
            title="Execution gate",
            status="active",
            summary="",
            tags=[],
            items=[],
            condition_refs=[],
            mode="all",
        )
    }

    with pytest.raises(
        ValueError,
        match="edge edge-missing-target targets unknown node operator-missing",
    ):
        routine.advance({}, conditions={}, operators={}, checklists=checklists)


def test_routine_advance_rejects_missing_checklist_condition() -> None:
    routine = Routine(
        id="routine-task",
        title="Task routine",
        status="active",
        summary="",
        tags=[],
        entrypoint="checklist-execution",
        decomposition=["checklist-execution"],
        edges=[],
        terminal_nodes=["complete"],
    )
    checklists = {
        "checklist-execution": Checklist(
            id="checklist-execution",
            title="Execution gate",
            status="active",
            summary="",
            tags=[],
            items=["Implementation exists"],
            condition_refs=["condition-missing"],
            mode="all",
        )
    }

    with pytest.raises(
        ValueError,
        match="checklist checklist-execution references unknown condition condition-missing",
    ):
        routine.advance({}, conditions={}, operators={}, checklists=checklists)


def test_advance_task_sets_pill_graduation_verified_when_bound_pills_have_atom_reference(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.create_artifact(
        "artifact.atom",
        {
            "title": "Graduated knowledge",
            "five_wh_one_plus": "what",
            "answer": "Atom references satisfy pill knowledge graduation.",
        },
    )
    operations.create_task_bundle(
        {
            "title": "Pill graduation with atom",
            "goal": "Prove atom-backed graduation.",
            "scope": "Closeout payload only.",
            "implementation_path": "deskops/operations.py",
            "validation": ["pytest"],
            "done_when": "Payload records the verified graduation state.",
            "pills": ["desk/contexts/pill-example.md"],
            "references": ["desk/atoms/atom-graduated-knowledge.md"],
        }
    )

    task, result = operations.advance_task("task-pill-graduation-with-atom")

    assert result is not None
    assert task is not None
    payload = operations._read_doc(
        tmp_path / "desk" / "tasks" / "task-pill-graduation-with-atom.md",
        TaskDoc,
    )
    assert payload["pill_graduation_verified"] is True


def test_bound_pills_without_atom_reference_leave_graduation_item_unaffirmed_but_non_blocking(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    test_file = tmp_path / "tests" / "test_runtime.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("def test_runtime():\n    assert True\n", encoding="utf-8")
    operations.create_task_bundle(
        {
            "title": "Pill graduation without atom",
            "goal": "Keep the closeout graduation item soft.",
            "scope": "Checklist and condition generation.",
            "implementation_path": "deskops/operations.py",
            "validation": ["pytest"],
            "done_when": "The graduation item is visible without becoming a hard gate.",
            "pills": ["desk/contexts/pill-example.md"],
            "references": ["tests/test_runtime.py::test_runtime"],
        }
    )

    assert operations.advance_task("task-pill-graduation-without-atom")[1] is not None
    task, result = operations.advance_task("task-pill-graduation-without-atom")

    assert result is not None
    assert task is not None
    payload = operations._read_doc(
        tmp_path / "desk" / "tasks" / "task-pill-graduation-without-atom.md",
        TaskDoc,
    )
    assert payload["pill_graduation_verified"] is False

    conditions = operations._load_conditions(task)
    checklists = operations._load_checklists(task)
    graduation_condition_id = "condition-task-pill-graduation-without-atom-pill-knowledge-graduated"
    closeout_checklist_id = "checklist-task-pill-graduation-without-atom-closeout-ready"

    assert conditions[graduation_condition_id].evaluate(payload) is False
    assert "Pill knowledge is graduated to atoms when required" in checklists[closeout_checklist_id].items
    assert checklists[closeout_checklist_id].is_complete(payload, conditions) is True


def test_advance_task_trivially_verifies_pill_graduation_when_no_pills_are_bound(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.create_task_bundle(
        {
            "title": "Pill graduation without pills",
            "goal": "Skip the graduation check when no pills are bound.",
            "scope": "Closeout payload only.",
            "implementation_path": "deskops/operations.py",
            "validation": ["pytest"],
            "done_when": "Tasks without pills pass the graduation check trivially.",
        }
    )

    task, result = operations.advance_task("task-pill-graduation-without-pills")

    assert result is not None
    assert task is not None
    payload = operations._read_doc(
        tmp_path / "desk" / "tasks" / "task-pill-graduation-without-pills.md",
        TaskDoc,
    )
    assert payload["pill_graduation_verified"] is True


def test_create_task_bundle_generates_pill_graduation_condition_and_closeout_item(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.create_task_bundle(
        {
            "title": "Generated pill graduation primitives",
            "goal": "Create the closeout graduation surfaces.",
            "scope": "Default task bundle primitives.",
            "implementation_path": "deskops/operations.py",
            "done_when": "The condition and checklist item are generated.",
        }
    )

    condition_payload = operations.show_primitive(
        "condition",
        "condition-task-generated-pill-graduation-primitives-pill-knowledge-graduated",
    )
    checklist_payload = operations.show_primitive(
        "checklist",
        "checklist-task-generated-pill-graduation-primitives-closeout-ready",
    )

    assert condition_payload["subject"] == "pill_graduation_verified"
    assert condition_payload["predicate"] == "truthy"
    assert "Pill knowledge is graduated to atoms when required" in checklist_payload["items"]
    assert "condition-task-generated-pill-graduation-primitives-pill-knowledge-graduated" not in checklist_payload["condition_refs"]
