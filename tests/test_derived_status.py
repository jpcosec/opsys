"""F3 T3.2: the derived status ladder."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import derived_conditions as dc
from deskops import derived_status as ds
from deskops.bootstrap import read_world_spec
from derived_support import contract_payload
from derived_support import cover_and_prove
from derived_support import create
from derived_support import document_symbol
from derived_support import make_world
from derived_support import route
from derived_support import store_task_with_plan
from derived_support import target_payload
from derived_support import task_payload

TASK = "task-derived-status"
CONTRACT = "contract-one"
SYMBOL = "deskops.derived_status:derive_status"


def test_code_ladder_matches_the_world_spec() -> None:
    declared = tuple(read_world_spec()["derived_status"]["values"])

    assert declared == ds.CODE_LADDER
    assert ds.ladder() == ds.CODE_LADDER


def test_ladder_answers_every_declared_condition(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    store_task_with_plan(world, TASK, "plan-one", [target_payload("plan-target-one")])
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert set(derivation.conditions) == set(dc.DERIVED_CONDITIONS)


def test_untracked_or_unrouted_task_is_drawer(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    create(world, "TaskDoc", TASK, task_payload(TASK), "desk/tasks")

    assert ds.derive_status(world, TASK).status == "drawer"


def test_routed_task_without_a_plan_is_active(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    create(world, "TaskDoc", TASK, task_payload(TASK), "desk/tasks")
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert derivation.status == "active"
    assert derivation.reasons == (
        "routed by a board; no plan target or contract declared yet",
    )


def test_target_without_contract_is_planning(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    store_task_with_plan(world, TASK, "plan-one", [target_payload("plan-target-one")])
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert derivation.status == "planning"
    assert derivation.value_of("plan_targets_without_contract") == 1


def test_complete_contract_not_yet_implemented_is_execution(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract=f"SymbolContractDoc:{CONTRACT}")]
    )
    create(world, "SymbolContractDoc", CONTRACT, contract_payload(CONTRACT, SYMBOL), "desk/plans")
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert derivation.status == "execution"
    assert derivation.value_of("contracts_declared") == 1
    assert derivation.value_of("contracts_implemented") == 0


def test_implemented_contract_is_testing(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract=f"SymbolContractDoc:{CONTRACT}")]
    )
    create(world, "SymbolContractDoc", CONTRACT, contract_payload(CONTRACT, SYMBOL), "desk/plans")
    document_symbol(world, SYMBOL)
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert derivation.status == "testing"
    assert derivation.value_of("contracts_implemented") == 1


def test_proven_tests_without_evidence_is_closeout(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    contract = contract_payload(CONTRACT, SYMBOL)
    store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract=f"SymbolContractDoc:{CONTRACT}")]
    )
    create(world, "SymbolContractDoc", CONTRACT, contract, "desk/plans")
    document_symbol(world, SYMBOL)
    cover_and_prove(world, contract, TASK)
    route(world, "board-001", TASK)

    derivation = ds.derive_status(world, TASK)

    assert derivation.status == "closeout"
    assert derivation.reasons == ("contract tests pass; closeout evidence is missing",)


def test_evidence_with_done_when_closes_the_task(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    contract = contract_payload(CONTRACT, SYMBOL)
    acceptance_ref = f"AcceptanceDoc:acceptance-{TASK}"
    store_task_with_plan(
        world,
        TASK,
        "plan-one",
        [target_payload("plan-target-one", contract=f"SymbolContractDoc:{CONTRACT}")],
        acceptance=acceptance_ref,
    )
    create(world, "SymbolContractDoc", CONTRACT, contract, "desk/plans")
    document_symbol(world, SYMBOL)
    cover_and_prove(world, contract, TASK)
    route(world, "board-001", TASK)
    create(
        world,
        "AcceptanceDoc",
        f"acceptance-{TASK}",
        {
            "id": f"acceptance-{TASK}",
            "title": "Acceptance",
            "status": "complete",
            "summary": "Closing rules.",
            "validation": ["pytest -q"],
            "done_when": ["the suite is green"],
            "evidence": ["commit 0" * 1],
            "tags": ["workspace:desk"],
        },
        "desk/tasks",
    )

    assert ds.derive_status(world, TASK).status == "closed"


def test_tasks_in_status_filters_by_the_derived_value(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    store_task_with_plan(world, TASK, "plan-one", [target_payload("plan-target-one")])
    route(world, "board-001", TASK)
    create(world, "TaskDoc", "task-unrouted", task_payload("task-unrouted"), "desk/tasks")

    assert ds.tasks_in_status(world, "planning") == [TASK]
    assert ds.tasks_in_status(world, "drawer") == ["task-unrouted"]


def test_unknown_task_raises(tmp_path: Path) -> None:
    world = make_world(tmp_path)

    with pytest.raises(dc.UnknownTaskError):
        ds.derive_status(world, "task-not-there")
