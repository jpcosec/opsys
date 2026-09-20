"""Derived task status: a projection of the store, not a state machine.

F3 T3.2. spec/world/deskops-world.yaml §derived_status declares the ladder
(drawer, active, planning, execution, testing, closeout, closed) and which
predicate each rung answers. This module evaluates that ladder over the
conditions in `deskops.derived_conditions`; it never writes `TaskDoc.status`.

The rungs are cumulative: each one implies the previous, so the derived status
is the deepest rung whose condition holds. A rung's own condition:

- drawer: no BoardDoc routes the task.
- active: routed, and no plan target or contract has been declared yet.
- planning: some target with change_kind add|modify lacks a complete contract.
- execution: no such target, at least one contract declared, not all implemented.
- testing: every declared contract is implemented, its tests are not proven.
- closeout: the contract tests pass, closeout evidence is not recorded yet.
- closed: contract tests pass and evidence with done_when is present.

The literal spec wording for `execution` ("plan_targets_without_contract == 0")
alone cannot be a rung: it is the negation of `planning`, so it always holds
once planning fails and no later rung would ever be reachable. The cumulative
reading above is what the spec now states.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
from typing import Any

from deskops.bootstrap import read_world_spec
from deskops.derived_conditions import ConditionReport
from deskops.derived_conditions import TaskSlice
from deskops.derived_conditions import condition_values_for
from deskops.derived_conditions import refs_in
from deskops.derived_conditions import split_ref
from deskops.derived_conditions import task_slice
from deskops.world import World

# The ladder in code. `ladder()` checks it against the spec on every import site.
CODE_LADDER: tuple[str, ...] = (
    "drawer",
    "active",
    "planning",
    "execution",
    "testing",
    "closeout",
    "closed",
)


class SpecDriftError(RuntimeError):
    """The code ladder and the world spec declare different status values."""


@dataclass(frozen=True)
class StatusDerivation:
    """A derived status with the conditions and reasons that produced it."""

    task_id: str
    status: str
    conditions: dict[str, ConditionReport] = field(default_factory=dict)
    reasons: tuple[str, ...] = ()

    def value_of(self, condition: str) -> Any:
        """The computed value of one condition (None when it was not evaluated)."""
        report = self.conditions.get(condition)
        return None if report is None else report.value


@lru_cache(maxsize=1)
def ladder() -> tuple[str, ...]:
    """The status ladder, read from the world spec and checked against the code."""
    declared = tuple((read_world_spec().get("derived_status") or {}).get("values", {}))
    if declared and declared != CODE_LADDER:
        raise SpecDriftError(
            f"spec derived_status declares {declared}, code ladder is {CODE_LADDER}"
        )
    return CODE_LADDER


def is_routed(world: World, task_id: str) -> bool:
    """Whether any BoardDoc routes the task (its `tasks` list names the task)."""
    task_name = split_ref(task_id if ":" in task_id else f"TaskDoc:{task_id}")[1]
    for doc in world.store.docs_of("BoardDoc"):
        payload = dict(doc.payload)
        if any(split_ref(ref)[1] == task_name for ref in refs_in(payload, "tasks", "task")):
            return True
    return False


def closeout_evidence_present(world: World, slice_: TaskSlice) -> bool:
    """Whether the task records closeout evidence together with its done_when rules.

    Read from its AcceptanceDoc documents, falling back to the fields the task
    itself carries (the pre-F4 task documents keep them in the body).
    """
    for acceptance in slice_.acceptances:
        payload = acceptance.payload
        if refs_in(payload, "evidence") and refs_in(payload, "done_when"):
            return True
    payload = slice_.task.payload
    return bool(refs_in(payload, "evidence", "closeout_evidence") and refs_in(payload, "done_when"))


def derive_status(world: World, task_id: str) -> StatusDerivation:
    """Derive one task's status by evaluating the ladder over the store.

    Raises deskops.derived_conditions.UnknownTaskError when the task is untracked.
    """
    slice_ = task_slice(world, task_id)
    conditions = condition_values_for(world, slice_)

    gaps = int(conditions["plan_targets_without_contract"].value)
    declared = int(conditions["contracts_declared"].value)
    implemented = int(conditions["contracts_implemented"].value)
    tests_pass = bool(conditions["tests_from_contracts_passing"].value)

    reasons: list[str] = []
    status = "drawer"
    if is_routed(world, task_id):
        status = "active"
        if slice_.targets or declared:
            if gaps > 0:
                status = "planning"
                reasons.append(
                    f"{gaps} plan target(s) with change_kind add|modify lack a complete contract"
                )
            else:
                status = "execution"
                if declared and implemented < declared:
                    reasons.append(f"{declared - implemented} of {declared} contracts are not implemented")
                if declared and implemented == declared:
                    status = "testing"
                    if tests_pass:
                        status = "closeout"
                        if closeout_evidence_present(world, slice_):
                            status = "closed"
                        else:
                            reasons.append("contract tests pass; closeout evidence is missing")
                    else:
                        reasons.append("all contracts implemented; contract tests are not proven")
        else:
            reasons.append("routed by a board; no plan target or contract declared yet")
    else:
        reasons.append("no BoardDoc routes this task")

    return StatusDerivation(
        task_id=slice_.task.ref,
        status=status,
        conditions=conditions,
        reasons=tuple(reasons),
    )


def tasks_in_status(world: World, status: str) -> list[str]:
    """Every tracked TaskDoc whose derived status is `status`, in store order.

    This is the store-side answer to the F3 gate question ("which tasks are in
    planning?"), equivalent to what `pron say` resolves once a model is wired.
    """
    found: list[str] = []
    for doc in world.store.docs_of("TaskDoc"):
        if derive_status(world, f"TaskDoc:{doc.name}").status == status:
            found.append(doc.name)
    return found
