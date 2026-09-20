"""F3 T3.3: the derived conditions of spec §derived_conditions."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import derived_conditions as dc
from derived_support import contract_payload
from derived_support import cover_and_prove
from derived_support import create
from derived_support import document_symbol
from derived_support import make_world
from derived_support import store_task_with_plan
from derived_support import target_payload


TASK = "task-derived-conditions"


def test_condition_names_match_the_world_spec() -> None:
    declared = tuple(entry["name"] for entry in _spec_conditions())

    assert declared == dc.DERIVED_CONDITIONS


def _spec_conditions() -> list[dict]:
    from deskops.bootstrap import read_world_spec

    return read_world_spec()["derived_conditions"]


def test_missing_contract_counts_thetarget_payload(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    task_ref = store_task_with_plan(world, TASK, "plan-one", [target_payload("plan-target-one")])

    report = dc.plan_targets_without_contract(world, dc.task_slice(world, task_ref))

    assert report.value == 1
    assert report.detail["open_targets"][0]["gaps"] == ["missing_contract"]


def test_incomplete_contract_counts_with_its_gaps(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    task_ref = store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract="SymbolContractDoc:contract-one")]
    )
    create(
        world,
        "SymbolContractDoc",
        "contract-one",
        contract_payload("contract-one", "deskops.derived_conditions:task_slice", docstring="", test_plan=[]),
        "desk/plans",
    )

    report = dc.plan_targets_without_contract(world, dc.task_slice(world, task_ref))

    assert report.value == 1
    assert report.detail["open_targets"][0]["gaps"] == ["docstring", "test_plan"]


def test_complete_contract_closes_the_target_and_counts_as_declared(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    task_ref = store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract="SymbolContractDoc:contract-one")]
    )
    create(world, "SymbolContractDoc", "contract-one", contract_payload("contract-one", "deskops.x:y"), "desk/plans")

    conditions = dc.condition_values(world, task_ref)

    assert conditions["plan_targets_without_contract"].value == 0
    assert conditions["contracts_declared"].value == 1


def test_contracts_implemented_needs_a_documented_symbol(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    task_ref = store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract="SymbolContractDoc:contract-one")]
    )
    create(world, "SymbolContractDoc", "contract-one", contract_payload("contract-one", "deskops.x:y"), "desk/plans")

    before = dc.contracts_implemented(world, dc.task_slice(world, task_ref))

    document_symbol(world, "deskops.x:y", "Does y.")
    after = dc.contracts_implemented(world, dc.task_slice(world, task_ref))

    assert before.value == 0
    assert before.detail["pending"][0]["reason"] == "symbol_missing"
    assert after.value == 1


def test_tests_from_contracts_passing_is_false_until_covered_and_run(tmp_path: Path) -> None:
    world = make_world(tmp_path)
    contract = contract_payload("contract-one", "deskops.x:y")
    task_ref = store_task_with_plan(
        world, TASK, "plan-one", [target_payload("plan-target-one", contract="SymbolContractDoc:contract-one")]
    )
    create(world, "SymbolContractDoc", "contract-one", contract, "desk/plans")

    before = dc.tests_from_contracts_passing(world, dc.task_slice(world, task_ref))

    cover_and_prove(world, contract, TASK)
    after = dc.tests_from_contracts_passing(world, dc.task_slice(world, task_ref))

    assert before.value is False
    assert before.detail["uncovered_contracts"] == ["SymbolContractDoc:contract-one"]
    assert after.value is True


def test_unknown_task_raises(tmp_path: Path) -> None:
    world = make_world(tmp_path)

    with pytest.raises(dc.UnknownTaskError):
        dc.task_slice(world, "task-not-there")


@pytest.mark.parametrize(
    ("ref", "expected"),
    [
        ("PlanDoc:plan-one", ("PlanDoc", "plan-one")),
        ("sldb://document/PlanDoc:plan-one", ("PlanDoc", "plan-one")),
    ],
)
def test_split_ref_accepts_node_qualified_ids(ref: str, expected: tuple[str, str]) -> None:
    assert dc.split_ref(ref) == expected
