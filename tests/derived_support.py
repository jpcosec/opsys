"""Shared store fixtures for the F3 derived-condition/status tests.

Builds a throwaway store with only the models those tests need, instead of a
full `bootstrap_world` (4s per store).
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.relations import register_relation_types  # noqa: E402
from deskops.world import DocId  # noqa: E402
from deskops.world import ensure_store_root  # noqa: E402
from deskops.world import get_world  # noqa: E402

DESKOPS_MODELS = (
    "TaskDoc",
    "PlanDoc",
    "PlanTargetDoc",
    "SymbolContractDoc",
    "AcceptanceDoc",
    "BoardDoc",
    "TestCoverageDoc",
    "RunDoc",
)

EXTERNAL_MODELS = {"PythonSymbolDoc": "sldb.models.knowledge_surface:PythonSymbolDoc"}


def make_world(tmp_path: Path):
    """A pron World over a fresh store in `tmp_path` with the F3 models registered."""
    world = get_world(ensure_store_root(tmp_path))
    for name in DESKOPS_MODELS:
        world.store.register_model(f"deskops.models:{name}")
    for name, ref in EXTERNAL_MODELS.items():
        registered = world.store.register_model(ref)
        assert registered or name in world.store.model_names(), f"{name} did not register"
    return world


def create(world, model: str, name: str, payload: dict[str, Any], folder: str = "desk") -> str:
    """Track one document and return its export id."""
    world.store.create(DocId.of(model, name), payload, Path(folder) / f"{name}.md")
    return f"{model}:{name}"


def task_payload(task_id: str, **extra: Any) -> dict[str, Any]:
    payload = {
        "id": task_id,
        "title": "Derived task",
        "status": "active",
        "goal": "Prove the derivation.",
        "scope": "F3 tests.",
        "tags": ["workspace:desk"],
    }
    payload.update(extra)
    return payload


def contract_payload(contract_id: str, qualname: str, **extra: Any) -> dict[str, Any]:
    payload = {
        "id": contract_id,
        "title": "Contract",
        "qualname": qualname,
        "kind": "function",
        "signature": "def derived() -> None",
        "docstring": "Does the derived thing.",
        "purpose": "Derive.",
        "architecture": "Projects the store.",
        "invariants": ["no state"],
        "lint_rules": ["max-complexity 10"],
        "test_plan": ["planning task derives planning"],
        "test_qualname": "tests/test_derived.py::test_x",
        "tags": ["workspace:desk"],
    }
    payload.update(extra)
    return payload


def target_payload(
    name: str, change_kind: str = "modify", contract: str | None = None
) -> dict[str, Any]:
    """A PlanTargetDoc payload; `contract` is the contained SymbolContractDoc ref."""
    payload = {
        "id": name,
        "title": name,
        "surface": "deskops/derived_conditions.py",
        "symbol": "deskops.derived_conditions:task_slice",
        "change_kind": change_kind,
        "rationale": "because",
        "acceptance": "green",
        "tags": ["workspace:desk"],
    }
    if contract:
        payload["contract"] = [contract]
    return payload


def store_task_with_plan(
    world,
    task_id: str,
    plan_id: str,
    targets: list[dict[str, Any]],
    acceptance: str | None = None,
) -> str:
    """A task containing one plan whose `targets` are the given payloads; returns its export id."""
    extra: dict[str, Any] = {"plan": [f"PlanDoc:{plan_id}"]}
    if acceptance:
        extra["acceptance"] = [acceptance]
    create(world, "TaskDoc", task_id, task_payload(task_id, **extra), "desk/tasks")
    create(
        world,
        "PlanDoc",
        plan_id,
        {
            "id": plan_id,
            "title": "Plan",
            "goal": "g",
            "context_findings": "c",
            "interpretation": "i",
            "risks": "r",
            "ambiguities": [],
            "tags": ["workspace:desk"],
            "targets": [f"PlanTargetDoc:{target['id']}" for target in targets],
        },
        "desk/plans",
    )
    for target in targets:
        create(world, "PlanTargetDoc", target["id"], target, "desk/plans")
    return f"TaskDoc:{task_id}"


def route(world, board_id: str, task_id: str) -> str:
    """A BoardDoc that routes the given task; returns the board's export id."""
    return create(
        world,
        "BoardDoc",
        board_id,
        {
            "id": board_id,
            "title": "Board",
            "scope": "desk",
            "purpose": "Route the work.",
            "tasks": [f"TaskDoc:{task_id}"],
            "pills": [],
            "rituals": [],
            "notes": "",
            "tags": ["workspace:desk"],
        },
        "desk",
    )


def document_symbol(world, qualname: str, docstring: str = "Does the thing.") -> None:
    """Track a PythonSymbolDoc for `qualname` with a real docstring."""
    create(
        world,
        "PythonSymbolDoc",
        qualname,
        {
            "id": qualname,
            "system": "deskops",
            "module": qualname.split(":")[0],
            "qualname": qualname,
            "kind": "function",
            "source_path": f"{qualname.split(':')[0].replace('.', '/')}.py",
            "source_span": "1-2",
            "source_sha256": "0" * 64,
            "signature": "def derived() -> None",
            "docstring": docstring,
            "imports": "",
            "purpose": "Not documented.",
            "architecture": "Not documented.",
            "provenance": "tests/derived_support.py",
            "tags": ["type:python-symbol"],
        },
        "desk/code",
    )


def cover_and_prove(world, contract: dict[str, Any], task_id: str, run_id: str = "run-one") -> None:
    """A TestCoverageDoc verifying the contract plus a successful RunDoc evidencing the task."""
    create(
        world,
        "TestCoverageDoc",
        f"coverage-{run_id}",
        {
            "id": f"coverage-{run_id}",
            "title": "Coverage",
            "test_qualname": contract["test_qualname"],
            "covers_symbol": f"PythonSymbolDoc:{contract['qualname']}",
            "granularity": "module",
            "source": "import_decl",
            "tags": ["workspace:desk"],
        },
        "desk/code",
    )
    create(
        world,
        "RunDoc",
        run_id,
        {
            "id": run_id,
            "title": "Run",
            "kind": "execution",
            "run_dir": f"runs/subagents/{run_id}",
            "herdr_pane_id": "pane-1",
            "session_path": f"runs/subagents/{run_id}/session.json",
            "session_sha256": "0" * 64,
            "started_at": "2026-09-20T00:00:00",
            "ended_at": "2026-09-20T00:01:00",
            "outcome": "success",
            "commit_sha": "0" * 40,
            "move_id": "move-1",
            "model": "deepseek-flash",
            "tokens_in": 1,
            "tokens_out": 1,
            "cost_usd": 0.0,
            "result_summary": "Green.",
            "validation_log": "pytest -q: green",
            "tags": ["type:run"],
        },
        "desk/runs",
    )
    world.ensure_ready()  # registers RelationTypeDoc / RelationDoc
    register_relation_types(world)
    create(
        world,
        "RelationDoc",
        f"rel-{run_id}-evidences-{task_id}",
        {
            "title": f"{run_id} evidences the task",
            "source_id": f"RunDoc:{run_id}",
            "target_id": f"TaskDoc:{task_id}",
            "relation_type": "evidences",
            "tags": ["layer.topology"],
        },
        "desk/relation_types",
    )
