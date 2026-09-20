"""The derived conditions of spec/world/deskops-world.yaml §derived_conditions.

F3 T3.3. Every value here is a projection over the documents already in the
store, recomputed from zero on each call: nothing advances a state and nothing
is cached.

The task slice feeding the predicates is resolved two ways, on purpose:

1. Payload fields (containment: TaskDoc -> PlanDoc -> PlanTargetDoc ->
   SymbolContractDoc). This is the route that works today: sldb's edge index
   does not consume `__containment__` / `__references__` yet (gap-log,
   desk/pron-gap-log.md), so containment is not an edge.
2. Authored relations (`RelationDoc` documents: `contracts`, `evidences`,
   `verifies`). Picked up through the graph whenever someone writes them, so
   the predicates need no change when F4 starts authoring edges.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

from deskops.world import DocId
from deskops.world import World

# Node ids in the sldb graph carry this prefix; payload refs do not.
NODE_PREFIX = "sldb://document/"

# change_kind values whose target requires a SymbolContractDoc before execution.
CONTRACT_CHANGE_KINDS = frozenset({"add", "modify"})

# What sldb writes in the authored fields of a PythonSymbolDoc it has not been
# told about yet: it counts as "the contract is not implemented".
NOT_DOCUMENTED = "not documented."

# The derived condition names, in spec order (a test pins them against the spec).
DERIVED_CONDITIONS: tuple[str, ...] = (
    "plan_targets_without_contract",
    "contracts_declared",
    "contracts_implemented",
    "tests_from_contracts_passing",
)


class UnknownTaskError(LookupError):
    """The store does not track a TaskDoc under the requested id."""


@dataclass(frozen=True)
class DocumentRef:
    """One resolved document: its export id `Model:name` and its payload."""

    ref: str
    payload: dict[str, Any]


@dataclass(frozen=True)
class ConditionReport:
    """One derived condition: spec name, computed value, and the detail behind it."""

    name: str
    value: Any
    detail: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TaskSlice:
    """The documents a task's derived conditions are computed over."""

    task: DocumentRef
    plans: tuple[DocumentRef, ...] = ()
    targets: tuple[DocumentRef, ...] = ()
    contracts: tuple[DocumentRef, ...] = ()
    acceptances: tuple[DocumentRef, ...] = ()


def split_ref(ref: str) -> tuple[str, str]:
    """`Model:name`, optionally node-qualified as `sldb://document/Model:name`, -> `(model, name)`."""
    clean = str(ref).strip()
    if clean.startswith(NODE_PREFIX):
        clean = clean[len(NODE_PREFIX) :]
    model, _, name = clean.partition(":")
    return model, name


def refs_in(payload: dict[str, Any], *fields: str) -> list[str]:
    """Every ref held by the named payload fields, in declared order, deduplicated."""
    found: list[str] = []
    for name in fields:
        value = payload.get(name)
        items = [value] if isinstance(value, str) else value if isinstance(value, (list, tuple)) else []
        for item in items:
            text = str(item).strip()
            if text and text not in found:
                found.append(text)
    return found


def resolve(world: World, ref: str) -> DocumentRef | None:
    """The document a ref points to, or None when the store does not track it."""
    model, name = split_ref(ref)
    if not model or not name:
        return None
    doc = world.store.doc(DocId.of(model, name))
    if doc is None:
        return None
    return DocumentRef(ref=f"{model}:{name}", payload=dict(doc.payload))


def linked_refs(world: World, ref: str, relation: str, model: str) -> list[str]:
    """Targets of `relation` from `ref` on the graph, kept only when they are `model` documents.

    Returns [] when the relation type was never initialized or nothing authored
    an edge of it: an unauthored edge is not an error, it is an absent fact.
    """
    try:
        nodes = world.graph.targets(ref, relation)
    except Exception:  # noqa: BLE001 - an unknown relation is an absent fact, not a failure
        return []
    found: list[str] = []
    for node in nodes:
        node_model, node_name = split_ref(node)
        if node_model == model and node_name:
            found.append(f"{node_model}:{node_name}")
    return found


def source_refs(world: World, ref: str, relation: str, model: str) -> list[str]:
    """Sources of `relation` into `ref` on the graph, kept only when they are `model` documents."""
    try:
        nodes = world.graph.sources(ref, relation)
    except Exception:  # noqa: BLE001 - as in linked_refs
        return []
    found: list[str] = []
    for node in nodes:
        node_model, node_name = split_ref(node)
        if node_model == model and node_name:
            found.append(f"{node_model}:{node_name}")
    return found


def _docs_naming_task(world: World, model: str, task_name: str, fields: tuple[str, ...]) -> list[str]:
    """Refs of `model` documents whose named payload fields point at the task.

    Bridge for documents written before the task was rebound to its plan or
    acceptance doc (the planning routine writes the plan first).
    """
    found: list[str] = []
    for doc in world.store.docs_of(model):
        payload = dict(doc.payload)
        for candidate in refs_in(payload, *fields):
            if split_ref(candidate)[1] == task_name:
                found.append(f"{model}:{doc.name}")
                break
    return found


def task_slice(world: World, task_id: str) -> TaskSlice:
    """Resolve the task plus the plans, targets, contracts and acceptances it contains.

    Raises UnknownTaskError when no TaskDoc is tracked under `task_id`.
    """
    task_ref = task_id if ":" in task_id else f"TaskDoc:{task_id}"
    task = resolve(world, task_ref)
    if task is None:
        raise UnknownTaskError(task_id)
    task_name = split_ref(task.ref)[1]

    plan_refs = refs_in(task.payload, "plan", "plans") + linked_refs(
        world, task.ref, "contains", "PlanDoc"
    )
    if not plan_refs:
        plan_refs = _docs_naming_task(world, "PlanDoc", task_name, ("task", "task_id", "task_ref"))
    plans = tuple(doc for doc in (resolve(world, ref) for ref in plan_refs) if doc is not None)

    target_refs: list[str] = []
    for plan in plans:
        for ref in refs_in(plan.payload, "targets", "target") + linked_refs(
            world, plan.ref, "contains", "PlanTargetDoc"
        ):
            if ref not in target_refs:
                target_refs.append(ref)
    targets = tuple(doc for doc in (resolve(world, ref) for ref in target_refs) if doc is not None)

    contract_refs: list[str] = refs_in(task.payload, "contract", "contracts")
    for target in targets:
        for ref in refs_in(target.payload, "contract", "contracts") + linked_refs(
            world, target.ref, "contains", "SymbolContractDoc"
        ):
            if ref not in contract_refs:
                contract_refs.append(ref)
    contracts = tuple(doc for doc in (resolve(world, ref) for ref in contract_refs) if doc is not None)

    acceptance_refs = refs_in(task.payload, "acceptance", "acceptances") + linked_refs(
        world, task.ref, "contains", "AcceptanceDoc"
    )
    if not acceptance_refs:
        acceptance_refs = _docs_naming_task(
            world, "AcceptanceDoc", task_name, ("task", "task_id", "task_ref")
        )
    acceptances = tuple(
        doc for doc in (resolve(world, ref) for ref in acceptance_refs) if doc is not None
    )

    return TaskSlice(
        task=task, plans=plans, targets=targets, contracts=contracts, acceptances=acceptances
    )


def contract_gaps(payload: dict[str, Any]) -> list[str]:
    """The contract fields the planning gate requires and the author left empty.

    A contract with any gap cannot carry its target from planning into
    execution: if the planner cannot say what the symbol does, it did not
    understand the change.
    """
    gaps: list[str] = []
    if not str(payload.get("docstring", "")).strip():
        gaps.append("docstring")
    if not refs_in(payload, "test_plan"):
        gaps.append("test_plan")
    if not refs_in(payload, "lint_rules"):
        gaps.append("lint_rules")
    return gaps


def _symbol_for_contract(world: World, contract: DocumentRef) -> dict[str, Any] | None:
    """The PythonSymbolDoc a contract names, by direct id or by `qualname` scan."""
    qualname = str(contract.payload.get("qualname", "")).strip()
    if not qualname:
        return None
    direct = resolve(world, qualname if ":" in qualname else f"PythonSymbolDoc:{qualname}")
    if direct is not None:
        return direct.payload
    for doc in world.store.docs_of("PythonSymbolDoc"):
        payload = dict(doc.payload)
        if str(payload.get("qualname", "")).strip() == qualname:
            return payload
    return None


def _is_documented(payload: dict[str, Any]) -> bool:
    """True when a symbol carries a real docstring, purpose or architecture note."""
    for field_name in ("docstring", "purpose", "architecture"):
        text = str(payload.get(field_name, "")).strip()
        if text and text.lower() != NOT_DOCUMENTED:
            return True
    return False


def plan_targets_without_contract(world: World, slice_: TaskSlice) -> ConditionReport:
    """How many plan targets still lack a complete contract.

    Counts PlanTargetDoc with change_kind add|modify whose contract is missing
    or incomplete (empty docstring, test_plan or lint_rules).
    """
    open_targets: list[dict[str, Any]] = []
    for target in slice_.targets:
        if str(target.payload.get("change_kind", "")).strip() not in CONTRACT_CHANGE_KINDS:
            continue
        contracts = [
            contract
            for contract in slice_.contracts
            if target.ref in refs_in(contract.payload, "target", "target_ref")
            or contract.ref in refs_in(target.payload, "contract", "contracts")
        ]
        if not contracts:
            open_targets.append({"target": target.ref, "gaps": ["missing_contract"]})
            continue
        gaps = sorted({gap for contract in contracts for gap in contract_gaps(contract.payload)})
        if gaps:
            open_targets.append({"target": target.ref, "gaps": gaps})
    return ConditionReport(
        name="plan_targets_without_contract",
        value=len(open_targets),
        detail={"open_targets": open_targets},
    )


def contracts_declared(world: World, slice_: TaskSlice) -> ConditionReport:
    """How many SymbolContractDoc documents the task declares."""
    return ConditionReport(
        name="contracts_declared",
        value=len(slice_.contracts),
        detail={"contracts": [contract.ref for contract in slice_.contracts]},
    )


def contracts_implemented(world: World, slice_: TaskSlice) -> ConditionReport:
    """How many declared contracts the code already implements.

    A contract counts as implemented when its PythonSymbolDoc exists and
    carries a real docstring, purpose or architecture note.
    """
    implemented: list[str] = []
    pending: list[dict[str, Any]] = []
    for contract in slice_.contracts:
        symbol = _symbol_for_contract(world, contract)
        if symbol is not None and _is_documented(symbol):
            implemented.append(contract.ref)
        else:
            pending.append(
                {
                    "contract": contract.ref,
                    "reason": "symbol_missing" if symbol is None else "symbol_undocumented",
                }
            )
    return ConditionReport(
        name="contracts_implemented",
        value=len(implemented),
        detail={"implemented": implemented, "pending": pending},
    )


def _evidencing_runs(world: World, slice_: TaskSlice) -> set[str]:
    """RunDoc refs that evidence this task: payload fields plus authored `evidences` edges."""
    task_name = split_ref(slice_.task.ref)[1]
    runs: set[str] = set()
    for doc in world.store.docs_of("RunDoc"):
        payload = dict(doc.payload)
        if any(split_ref(ref)[1] == task_name for ref in refs_in(payload, "task", "task_id", "evidence_for")):
            runs.add(f"RunDoc:{doc.name}")
    runs.update(source_refs(world, slice_.task.ref, "evidences", "RunDoc"))
    return runs


def tests_from_contracts_passing(world: World, slice_: TaskSlice) -> ConditionReport:
    """Whether every declared contract has a test and a successful run proves it.

    Needs two derived layers that F5 populates: TestCoverageDoc (verifying each
    contract's `test_qualname`) and a successful RunDoc evidencing the task.
    Until then a task with contracts reports False, never a false positive.
    """
    coverages = [dict(doc.payload) for doc in world.store.docs_of("TestCoverageDoc")]
    passing_runs: list[str] = []
    for ref in sorted(_evidencing_runs(world, slice_)):
        _, name = split_ref(ref)
        doc = world.store.doc(DocId.of("RunDoc", name))
        if doc is not None and str(dict(doc.payload).get("outcome", "")).strip().lower() == "success":
            passing_runs.append(ref)

    uncovered: list[str] = []
    for contract in slice_.contracts:
        qualname = str(contract.payload.get("qualname", "")).strip()
        test_qualname = str(contract.payload.get("test_qualname", "")).strip()
        covered = False
        for coverage in coverages:
            if test_qualname and str(coverage.get("test_qualname", "")).strip() == test_qualname:
                covered = True
                break
            covers = str(coverage.get("covers_symbol", "")).strip()
            if covers and qualname and split_ref(covers)[1] in {qualname, split_ref(qualname)[1]}:
                covered = True
                break
        if not covered:
            uncovered.append(contract.ref)

    value = bool(slice_.contracts) and not uncovered and bool(passing_runs)
    return ConditionReport(
        name="tests_from_contracts_passing",
        value=value,
        detail={
            "uncovered_contracts": uncovered,
            "passing_runs": passing_runs,
            "coverage_docs": len(coverages),
        },
    )


def condition_values_for(world: World, slice_: TaskSlice) -> dict[str, ConditionReport]:
    """Every derived condition of the spec, computed over an already-resolved slice."""
    return {
        "plan_targets_without_contract": plan_targets_without_contract(world, slice_),
        "contracts_declared": contracts_declared(world, slice_),
        "contracts_implemented": contracts_implemented(world, slice_),
        "tests_from_contracts_passing": tests_from_contracts_passing(world, slice_),
    }


def condition_values(world: World, task_id: str) -> dict[str, ConditionReport]:
    """Every derived condition of the spec, computed for one task, by name."""
    return condition_values_for(world, task_slice(world, task_id))
