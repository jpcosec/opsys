"""CC33b: the closeout gate of each task type is a ``RuleDoc`` over the ``task_completes`` edge.

``deskops/data/rules/rule-closeout-task-<type>.md`` (managed seeds written to
``desk/lifecycle/`` by ``deskops desk update --apply``) are ``on_transition`` rules read at
``ritual-closeout`` that ask for the evidence receipts ``deskops closeout verify`` writes
(CC33a), accepted and with an intact anchor on the task's contract. ``closeout commit`` writes
no receipt: it evaluates the rule (b2). ``closeout-evidence.yaml`` is the table the producers
read (c3); this file checks the rules against it, the edge the rule blocks (G_CONSUMER), the
exempt link receipt (b3), the added kinds that only alert (c5) and the two ``on_write`` alerts.
"""

from __future__ import annotations

import json
from pathlib import Path
import re

import pytest
import yaml

from deskops import lifecycle
from deskops.models.task_types import TASK_TYPE_MODELS
from deskops.models.task_types import closeout_evidence_table
from deskops.operations import DeskopsOperations
from deskops.paths import data_path
from deskops.paths import package_pythonpath
from test_closeout_evidence_receipts import ATOM
from test_closeout_evidence_receipts import _desk
from test_closeout_evidence_receipts import _git
from test_closeout_evidence_receipts import _receipts
from test_closeout_evidence_receipts import _run

RULES = data_path("data", "rules")
EVIDENCE_CLAUSE = re.compile(
    r'any\(\^subject: kind = "evidence" and fact = "(\w+)" and anchor_state = "intact" and verdict = "accepted"\)'
)
LINK_CLAUSE = (
    r'\(any\(\^subject: kind = "evidence" and fact = "atom" and anchor_state = "intact" and verdict = "accepted"\)'
    r' or any\(\^subject: kind = "evidence" and fact = "materialization" and anchor_state = "intact" and verdict = "accepted"\)\)'
)
GOLDENS_CLAUSE = 'any(^subject: kind = "goldens" and anchor_state = "intact" and verdict = "accepted")'


def _rule(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])


def _closeout_rules() -> dict[str, dict]:
    return {path.stem: _rule(path) for path in sorted(RULES.glob("rule-closeout-task-*.md"))}


# ------------------------------------------------------------------ c3: table against the rules
def test_each_type_has_one_closeout_rule_on_the_closeout_node() -> None:
    rules = _closeout_rules()
    assert sorted(rules) == sorted(f"rule-closeout-{name.replace('.', '-')}" for name in TASK_TYPE_MODELS)
    for name, model in TASK_TYPE_MODELS.items():
        rule = rules[f"rule-closeout-{name.replace('.', '-')}"]
        assert rule["subject"] == f"model <= {model.__name__}"
        # task_completes leaves ritual-closeout (its source_id), so the rule reads the task there.
        assert rule["where"] == 'current_node = "ritual-closeout"'
        assert rule["moment"] == "on_transition" and rule["severity"] == "error"
        assert name in rule["message"]


def test_the_rules_ask_for_exactly_the_kinds_of_the_table() -> None:
    """Per type, the clauses of every closeout rule whose family holds it (refactor inherits
    task.code's) are the table's kinds; atom|materialization is one ``or`` of two ``any``."""
    rules = _closeout_rules()
    table = closeout_evidence_table()
    assert set(table) == set(TASK_TYPE_MODELS)
    for name, model in TASK_TYPE_MODELS.items():
        conditions = [
            rule["condition"]
            for rule in rules.values()
            if any(cls.__name__ == rule["subject"].removeprefix("model <= ") for cls in model.__mro__)
        ]
        kinds: list[str] = []
        for condition in conditions:
            kinds += EVIDENCE_CLAUSE.findall(condition)
            if GOLDENS_CLAUSE in condition:
                kinds.append("goldens")
            if 'fact = "atom"' in condition:
                # atom|materialization is one parenthesized `or` of the two receipts.
                assert re.search(LINK_CLAUSE, condition), condition
        assert sorted(kinds) == sorted(table[name]), name


def test_the_edge_condition_no_longer_reads_a_fact() -> None:
    edge = _rule(data_path("data", "lifecycle", "closeout-task_completes.md"))
    assert edge["condition"] == 'status = "ready_for_testing"'


# ------------------------------------------------------------------ seeds
def test_desk_update_writes_the_closeout_rules_and_a_second_run_changes_nothing(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    for path in RULES.glob("rule-closeout-*.md"):
        written = root / "desk" / "lifecycle" / path.name
        assert written.read_text(encoding="utf-8") == path.read_text(encoding="utf-8")
        written.unlink()
    changes = lifecycle.write_lifecycle_graph(root)
    assert {f"wrote desk/lifecycle/{path.name}" for path in RULES.glob("rule-closeout-*.md")} <= set(changes)
    assert lifecycle.write_lifecycle_graph(root) == []


# ------------------------------------------------------------------ G_CONSUMER: the edge the rule blocks
def _at_closeout(root: Path, task_id: str) -> dict:
    """The task's payload as the edge reads it at ritual-closeout (what advance gets there)."""
    from deskops import doc_access
    from deskops.models import TaskDoc

    payload = doc_access.read_doc(root / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    return {**payload, "current_node": "ritual-closeout", "status": "ready_for_testing"}


def _blocked(root: Path, task_id: str) -> list[lifecycle.Transition]:
    document = lifecycle.task_document(root, root / "desk" / "tasks" / f"{task_id}.md")
    assert document is not None
    return lifecycle.transitions_blocked(root, "ritual-closeout", _at_closeout(root, task_id), document)


def test_without_an_accepted_commit_receipt_task_completes_is_blocked_on_the_commit_clause(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root, with_commit=False)
    code, _ = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    assert code == 1
    assert _receipts(root, task_id)["evidence-commit-1"]["verdict"] == "rejected"

    blocked = _blocked(root, task_id)
    assert [t.relation_type for t in blocked] == ["task_completes"]
    errors = [f for f in blocked[0].findings if f["level"] == "error"]
    assert errors and all(f["code"] == "rules/rule-closeout-task-code" for f in errors)
    assert any('fact = "commit"' in f["what"] for f in errors), errors


def test_with_every_receipt_the_edge_holds_and_editing_the_goal_blocks_it_again(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root)
    code, _ = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    assert code == 0
    assert _blocked(root, task_id) == []
    document = lifecycle.task_document(root, root / "desk" / "tasks" / f"{task_id}.md")
    holding = lifecycle.transitions_holding(root, "ritual-closeout", _at_closeout(root, task_id), document)
    assert [t.relation_type for t in holding] == ["task_completes"]

    code, out = _run(["edit", "task", task_id, "goal", "a different goal", "--root", str(root)])
    assert code == 0, out
    blocked = _blocked(root, task_id)
    assert [t.relation_type for t in blocked] == ["task_completes"]
    assert any('anchor_state = "intact"' in f["what"] for f in blocked[0].findings)


# ------------------------------------------------------------------ closeout commit (b2)
def _route(root: Path, task_id: str) -> None:
    from deskops import doc_access
    from deskops.models import BoardDoc

    board = root / "desk" / "tasks" / "Board.md"
    payload = doc_access.read_doc(board, BoardDoc)
    rel = f"desk/tasks/{task_id}.md"
    if rel not in (payload.get("tasks") or []):
        payload["tasks"] = [*(payload.get("tasks") or []), rel]
        doc_access.write_doc(root, board, BoardDoc, payload)


def test_closeout_commit_writes_no_receipt_and_blocks_until_verify_wrote_them(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root)
    _route(root, task_id)
    before = _git(root, "rev-parse", "HEAD")

    code, out = _run(["closeout", "commit", "--task", task_id, "--no-run", "--reason", "rule test", "--root", str(root)])
    assert code == 1, out
    assert f"Closeout gate blocked {task_id}; the closing commit was not made." in out
    assert "[rules/rule-closeout-task-code]" in out and 'fact = "tests"' in out
    assert f"Run 'deskops closeout verify --task {task_id}'" in out
    assert not (root / "desk" / "reviews" / task_id).exists(), "closeout commit writes no receipt"
    assert _git(root, "rev-parse", "HEAD") == before

    code, _ = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    assert code == 0
    code, out = _run(["closeout", "commit", "--task", task_id, "--no-run", "--reason", "rule test", "--paths", "desk", "--root", str(root)])
    assert code == 0, out
    assert "Closeout gate: esta tarea declaró tests, commit, atom|materialization" in out
    assert not (root / "desk" / "tasks" / f"{task_id}.md").exists()


# ------------------------------------------------------------------ b3: exempt link receipt
def test_an_exempt_link_gate_writes_an_accepted_atom_receipt_naming_why(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    test_file = root / "tests" / "test_feature.py"
    test_file.parent.mkdir(parents=True, exist_ok=True)
    test_file.write_text("def test_feature() -> None:\n    assert True\n", encoding="utf-8")
    _git(root, "add", "--", "tests/test_feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": "Exempt", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d",
         "validation": ["pytest"], "task_type": "task.code"}
    ).task_id
    references = ["tests/test_feature.py", _git(root, "rev-parse", "HEAD")]
    code, out = _run(["edit", "task", task_id, "references", json.dumps(references), "--root", str(root)])
    assert code == 0, out

    code, out = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    report = json.loads(out)
    assert code == 0 and report["ok"], report
    assert "atom|materialization (exento: sin atoms locales)" in report["found"]
    atom = _receipts(root, task_id)["evidence-atom-1"]
    assert atom["verdict"] == "accepted"
    assert atom["value"] == "exempt: knowledge-coverage-exempt: no local atom documents"
    assert _blocked(root, task_id) == []


# ------------------------------------------------------------------ c5: --evidence only adds
def test_an_added_kind_that_fails_alerts_and_writes_its_receipt_but_does_not_block(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    reference_task = _desk(root)  # an atom, a test and a HEAD commit to reference
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": "Added kind", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d",
         "validation": ["pytest"], "task_type": "task.code",
         "closeout_evidence": ["tests", "commit", "atom", "materialization", "external"]}
    ).task_id
    from deskops import doc_access
    from deskops.models import TaskDoc

    references = doc_access.read_doc(root / "desk" / "tasks" / f"{reference_task}.md", TaskDoc)["references"]
    code, out = _run(["edit", "task", task_id, "references", json.dumps(references), "--root", str(root)])
    assert code == 0, out
    code, out = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    report = json.loads(out)
    assert code == 0 and report["ok"], report
    assert report["declared"] == ["tests", "commit", "atom", "materialization", "external"]
    assert "added_closeout_evidence_not_verified" in {alert["code"] for alert in report["alerts"]}
    assert _receipts(root, task_id)["evidence-external-1"]["verdict"] == "rejected"
    assert _blocked(root, task_id) == []


# ------------------------------------------------------------------ b7: field rules as on_write alerts
@pytest.mark.parametrize(
    "rule,good,bad",
    [
        (
            "rule-closeout-alert-implicit-code",
            {"task_type": "task.code"},
            {"task_type": "", "closeout_evidence": []},
        ),
        (
            "rule-closeout-alert-pill-graduation",
            {"pills": []},
            {"pills": ["desk/contexts/pill-x.md"], "references": []},
        ),
    ],
)
def test_the_field_alerts_hold_on_a_good_payload_and_fail_on_a_bad_one(rule: str, good: dict, bad: dict) -> None:
    from sldb.api import where_matches

    spec = _rule(RULES / f"{rule}.md")
    assert spec["moment"] == "on_write" and spec["severity"] == "alert"
    assert spec["subject"] == "model <= TaskDoc"
    assert where_matches(spec["condition"], good)
    assert not where_matches(spec["condition"], bad)


def test_the_pill_graduation_alert_follows_the_reference_to_an_atom(lifecycle_desk: Path) -> None:
    from sldb.api import rules_explain

    root = lifecycle_desk
    task_id = _desk(root)
    # The rule follows the references sldb resolves to a document: the atom's path (a bare
    # atom id is not a reference the store resolves; see the report's sldb hypotheses).
    code, out = _run(["edit", "task", task_id, "references", json.dumps([f"desk/atoms/{ATOM}.md"]), "--root", str(root)])
    assert code == 0, out
    pill = DeskopsOperations(root).create_artifact(
        "artifact.pill",
        {"title": "Graduated pill", "summary": "s", "what": "w", "why": "y", "when": "n", "where": "h", "how": "o", "how_not": "x"},
    )
    DeskopsOperations(root).bind_pill_to_task(task_id, pill.doc_id)
    explained = rules_explain(root / ".sldb", "RuleDoc:rule-closeout-alert-pill-graduation", f"TaskCodeDoc:{task_id}", pythonpath=package_pythonpath())
    assert explained["finding"]["holds"] == "true", explained
    references = ["tests/test_feature.py"]
    code, out = _run(["edit", "task", task_id, "references", json.dumps(references), "--root", str(root)])
    assert code == 0, out
    explained = rules_explain(root / ".sldb", "RuleDoc:rule-closeout-alert-pill-graduation", f"TaskCodeDoc:{task_id}", pythonpath=package_pythonpath())
    assert explained["finding"]["holds"] == "false", explained
