from __future__ import annotations

from deskops.runtime.primitives import Checklist
from deskops.runtime.primitives import Condition
from deskops.runtime.primitives import Edge
from deskops.runtime.primitives import Operator
from deskops.runtime.primitives import Routine


def test_condition_and_checklist_evaluate_against_payload() -> None:
    payload = {
        "status": "draft",
        "validation": ["pytest"],
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
            items=["Task is ready for closeout"],
            condition_refs=["condition-ready-for-closeout"],
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
    assert third.current_node == "complete"
    assert payload["status"] == "closed"
