"""CC32: the activation gate of each factory task type is a RuleDoc seed of the desk.

Each ``deskops/data/rules/rule-activation-<type>.md`` is a managed seed written to
``desk/lifecycle/`` by ``deskops init`` / ``desk update --apply`` and tracked as a ``RuleDoc``:
``on_transition`` over ``ritual-execution``, subject ``model <= <TypeDoc>``, requiring the
review receipts the type asks for (``accepted`` and ``intact``) and the dependencies closed.
sldb evaluates it when ``deskops advance`` asks for the holding edges (GO08); the findings of
the blocked edge are what ``advance``, ``next`` and ``show`` print. These tests cover the
G_CONSUMER gate (three steps), the per-type rules, the desk subtype inheritance, the open
dependency, the idempotent seeding and the removal of ``__activation_receipts__``.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from deskops.paths import package_pythonpath
from tests.activation_receipts import accept_receipts

ROOT = Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "deskops" / "data" / "rules"
FACTORY_RULES = {
    "task.code": "rule-activation-task-code",
    "task.docs": "rule-activation-task-docs",
    "task.debug": "rule-activation-task-debug",
    "task.refactor": "rule-activation-task-refactor",
    "task.decision": "rule-activation-task-decision",
    "task.aggregate": "rule-activation-task-aggregate",
    "task.external": "rule-activation-task-external",
}
PREFLIGHT_CLAUSE = 'any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight")'


def _run(argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


def _task(root: Path, title: str, **extra: object) -> str:
    payload = {
        "title": title,
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
        "task_type": "task.code",
        **extra,
    }
    return DeskopsOperations(root).create_task_bundle(payload).task_id


def _advance(root: Path, task_id: str) -> tuple[int, str]:
    return _run(["advance", "task", task_id, "--root", str(root)])


# ------------------------------------------------------------------ the seeds
def test_one_rule_per_factory_type_is_seeded_and_tracked(lifecycle_desk: Path) -> None:
    from sldb.api import doc_exists
    from sldb.runtime.validation import extract_model_data
    from sldb.models.rule_doc import RuleDoc

    for task_type, name in FACTORY_RULES.items():
        source = RULES_DIR / f"{name}.md"
        seeded = lifecycle_desk / "desk" / "lifecycle" / f"{name}.md"
        assert seeded.read_bytes() == source.read_bytes(), name
        assert doc_exists(lifecycle_desk / ".sldb", f"RuleDoc/{name}")
        rule = extract_model_data(RuleDoc, seeded.read_text(encoding="utf-8"))
        assert rule["moment"] == "on_transition" and rule["severity"] == "error"
        assert rule["where"] == 'current_node = "ritual-execution"'
        assert task_type in rule["message"], "the message names the type"
        if task_type != "task.refactor":
            assert 'all(depends_on: status = "closed")' in rule["condition"]


def test_desk_update_apply_changes_nothing_on_a_seeded_desk_and_rules_check_passes(lifecycle_desk: Path) -> None:
    from sldb.api import rules_check

    code, out = _run(["desk", "update", "--root", str(lifecycle_desk), "--apply"])
    assert code == 0, out
    assert "Desk is up to date." in out
    # The activation rules are on_transition: `rules check` without --subject (on_check only)
    # reports nothing, and no error.
    assert rules_check(lifecycle_desk / ".sldb") == []


def test_no_activation_receipts_attribute_remains_in_the_package() -> None:
    hits = [path for path in (ROOT / "deskops").rglob("*.py") if "__activation_receipts__" in path.read_text(encoding="utf-8")]
    assert hits == []


# ------------------------------------------------------------------ G_CONSUMER
def test_g_consumer_activation_gate_in_three_steps(lifecycle_desk: Path) -> None:
    from sldb.api import rules_explain

    root = lifecycle_desk
    task_id = _task(root, "Consumer gate")

    # 1. No receipts: advance fails naming the preflight clause of the task.code rule.
    code, out = _advance(root, task_id)
    assert code == 1
    assert "Current node: ritual-execution" in out
    assert "rules/rule-activation-task-code" in out
    assert 'any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "preflight")' in out
    assert "Una tarea task.code se activa" in out
    explained = rules_explain(root / ".sldb", "RuleDoc:rule-activation-task-code", f"TaskCodeDoc:{task_id}", pythonpath=package_pythonpath())
    assert explained["finding"]["holds"] == "false"
    assert explained["finding"]["clause"] == PREFLIGHT_CLAUSE

    # 2. Preflight and bundle accepted and intact (pinned on the task's contract): it activates.
    accept_receipts(root, task_id, ("preflight", "bundle"))
    receipts = sorted((root / "desk" / "reviews" / task_id).glob("*.md"))
    assert len(receipts) == 2 and all("@sha256:" in path.read_text(encoding="utf-8") for path in receipts)
    code, out = _advance(root, task_id)
    assert code == 0, out
    assert "Status: active" in out and "Current node: ritual-testing" in out
    assert "Advanced to ritual-testing via task_activates." in out

    # 3. The contract changes under the receipts: they are `changed` and the gate blocks again.
    other = _task(root, "Consumer gate changed")
    accept_receipts(root, other, ("preflight", "bundle"))
    code, out = _run(["edit", "task", other, "goal", "a different goal", "--root", str(root)])
    assert code == 0, out
    code, out = _advance(root, other)
    assert code == 1
    assert "Current node: ritual-execution" in out
    assert '"anchor_state":"changed"' in out, out


# ------------------------------------------------------------------ per type
def test_task_debug_requires_reproduction_and_not_bundle(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _task(root, "Debug it", task_type="task.debug")
    accept_receipts(root, task_id, ("preflight", "bundle"))

    code, out = _advance(root, task_id)
    assert code == 1
    assert "rules/rule-activation-task-debug" in out
    assert 'kind = "reproduction"' in out and "rule-activation-task-code" not in out

    accept_receipts(root, task_id, ("reproduction",))
    code, out = _advance(root, task_id)
    assert code == 0, out


def test_task_refactor_inherits_task_code_and_adds_goldens(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _task(root, "Refactor it", task_type="task.refactor")

    code, out = _advance(root, task_id)
    assert code == 1
    assert "rules/rule-activation-task-code" in out, "the task.code rule applies by family (model <= TaskCodeDoc)"
    assert "rules/rule-activation-task-refactor" in out and 'kind = "goldens"' in out

    accept_receipts(root, task_id, ("preflight", "bundle"))
    code, out = _advance(root, task_id)
    assert code == 1
    assert "rule-activation-task-code" not in out
    assert "rules/rule-activation-task-refactor" in out and 'kind = "goldens"' in out

    accept_receipts(root, task_id, ("goldens",))
    code, out = _advance(root, task_id)
    assert code == 0, out


def test_open_dependency_blocks_activation_and_the_finding_names_it(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    blocker = _task(root, "Blocker")
    task_id = _task(root, "Depends on blocker", depends_on=[blocker])
    accept_receipts(root, task_id)

    code, out = _advance(root, task_id)
    assert code == 1
    assert 'all(depends_on: status = "closed")' in out
    assert f"witness: TaskCodeDoc:{blocker}" in out and '"status":"draft"' in out


def test_task_aggregate_needs_only_its_dependencies_closed(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _task(root, "Aggregate", task_type="task.aggregate")
    code, out = _advance(root, task_id)
    assert code == 0, out


# ------------------------------------------------------------------ show and next
def test_show_and_next_print_the_findings_of_the_blocked_gate(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _task(root, "Show me")

    code, out = _run(["show", "task", task_id, "--root", str(root), "--format", "json"])
    assert code == 0
    gates = json.loads(out)["lifecycle_gates"]
    assert gates[0]["relation_type"] == "task_activates"
    assert [f["code"] for f in gates[0]["findings"]] == ["rules/rule-activation-task-code"]
    assert gates[0]["findings"][0]["subject"] == f"TaskCodeDoc:{task_id}"

    code, out = _run(["show", "task", task_id, "--root", str(root)])
    assert "  blocked by: error: [rules/rule-activation-task-code]" in out

    code, out = _run(["next", task_id, "--root", str(root)])
    assert code == 0
    assert "Blocked by:\n- error: [rules/rule-activation-task-code]" in out

    accept_receipts(root, task_id)
    code, out = _run(["show", "task", task_id, "--root", str(root), "--format", "json"])
    assert "findings" not in json.loads(out)["lifecycle_gates"][0]
    code, out = _run(["next", task_id, "--root", str(root)])
    assert "Blocked by:" not in out


# ------------------------------------------------------------------ desk subtype
CLI = [sys.executable, "-m", "deskops"]


def _cli(root: Path, *argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    result = subprocess.run([*CLI, *argv, "--root", str(root)], cwd=root, capture_output=True, text=True, env=env)
    if check:
        assert result.returncode == 0, f"deskops {' '.join(argv)} failed:\n{result.stdout}\n{result.stderr}"
    return result


def test_desk_subtype_inherits_the_rules_and_a_desk_rule_adds_a_clause(tmp_path: Path) -> None:
    from sldb.api import transaction

    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    init = subprocess.run([*CLI, "init", str(root)], capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(ROOT)})
    assert init.returncode == 0, init.stdout + init.stderr

    models_dir = root / "desk" / "models"
    models_dir.mkdir()
    (models_dir / "cli_types.py").write_text(
        """from typing import Literal

from pydantic import Field

from deskops.models import TaskCodeDoc


class TaskCliDoc(TaskCodeDoc):
    task_type: Literal["task.code.cli"] = Field(default="task.code.cli", description="CLI subtype.")
""",
        encoding="utf-8",
    )
    _cli(root, "desk", "update", "--apply")

    add = _cli(root, "add", "task", "--title", "Cli one", "--goal", "g", "--scope", "s", "--implementation-path", "i",
               "--done-when", "d", "--validation", "pytest", "--task-type", "task.code.cli")
    assert "task-cli-one" in add.stdout

    # No code names task.code.cli: the task.code rule applies through model <= TaskCodeDoc.
    blocked = _cli(root, "advance", "task", "task-cli-one", check=False)
    assert blocked.returncode == 1
    assert "rules/rule-activation-task-code" in blocked.stdout and 'kind = "preflight"' in blocked.stdout

    # A rule the desk authors itself (through sldb) adds a clause to the subtype.
    with transaction(root / ".sldb", pythonpath=str(root / "desk")) as tx:
        tx.create(
            "RuleDoc",
            "rule-cli-needs-owner",
            {
                "title": "CLI tasks need an owner receipt",
                "subject": "model <= TaskCliDoc",
                "where": 'current_node = "ritual-execution"',
                "condition": 'any(^subject: anchor_state = "intact" and verdict = "accepted" and kind = "owner")',
                "severity": "error",
                "moment": "on_transition",
                "message": "Una tarea task.code.cli se activa además con un recibo owner aceptado e intacto.",
            },
            path="desk/lifecycle/rule-cli-needs-owner.md",
        )
    accept_receipts(root, "task-cli-one", ("preflight", "bundle"))
    blocked = _cli(root, "advance", "task", "task-cli-one", check=False)
    assert blocked.returncode == 1
    assert "rule-activation-task-code" not in blocked.stdout
    assert "rules/rule-cli-needs-owner" in blocked.stdout and 'kind = "owner"' in blocked.stdout

    accept_receipts(root, "task-cli-one", ("owner",))
    activated = _cli(root, "advance", "task", "task-cli-one")
    assert "Current node: ritual-testing" in activated.stdout
