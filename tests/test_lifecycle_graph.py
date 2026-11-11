from __future__ import annotations

from pathlib import Path

import pytest

from deskops import lifecycle
from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations
from deskops.paths import package_pythonpath
from tests.activation_receipts import accept_receipts

LIFECYCLE_TEMPLATES = Path(__file__).resolve().parents[1] / "deskops" / "data" / "lifecycle"
RULE_TEMPLATES = Path(__file__).resolve().parents[1] / "deskops" / "data" / "rules"
RELATION_DOCS = ("execution-task_activates", "testing-task_hands_to_closeout", "closeout-task_completes")


def _run(argv: list[str]) -> tuple[int, str]:
    import contextlib
    import io

    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


def _lifecycle_tree(root: Path) -> dict[str, bytes]:
    return {path.name: path.read_bytes() for path in sorted((root / "desk" / "lifecycle").glob("*.md"))}


def _managed_templates() -> dict[str, bytes]:
    """What `desk/lifecycle/` holds: the graph's six documents and the activation rules (CC32)."""
    return {p.name: p.read_bytes() for folder in (LIFECYCLE_TEMPLATES, RULE_TEMPLATES) for p in folder.glob("*.md")}


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


def test_write_lifecycle_graph_is_idempotent(lifecycle_desk: Path) -> None:
    assert lifecycle.write_lifecycle_graph(lifecycle_desk) == []
    assert _lifecycle_tree(lifecycle_desk) == _managed_templates()


def test_the_seeds_declare_the_effects_of_each_transition_and_one_edge_per_ritual(lifecycle_desk: Path) -> None:
    """GO09: each RelationDoc carries `attributes.sets.status` and `terminal`; `task_completes` is the
    terminal one. One edge leaves each ritual, so the order sldb returns holding edges in decides
    nothing (k4, n3)."""
    from sldb.models.relation_doc import RelationDoc
    from sldb.runtime.validation import extract_model_data

    edges = {
        name: extract_model_data(RelationDoc, (lifecycle_desk / "desk" / "lifecycle" / f"{name}.md").read_text(encoding="utf-8"))
        for name in RELATION_DOCS
    }
    assert {name: edge["attributes"] for name, edge in edges.items()} == {
        "execution-task_activates": {"sets": {"status": "active"}, "terminal": False},
        "testing-task_hands_to_closeout": {"sets": {"status": "ready_for_testing"}, "terminal": False},
        "closeout-task_completes": {"sets": {"status": "closed"}, "terminal": True},
    }
    sources = [edge["source_id"] for edge in edges.values()]
    assert sorted(sources) == sorted(f"RitualDoc:{node}" for node in lifecycle.load_lifecycle_spec().rituals)
    assert len(set(sources)) == len(sources), "one edge leaves each ritual"
    for node in lifecycle.load_lifecycle_spec().rituals:
        assert len(lifecycle.transitions_from(lifecycle_desk, node)) == 1, node


def test_desk_update_apply_rewrites_a_relation_doc_without_attributes_and_then_changes_nothing(
    lifecycle_desk: Path,
) -> None:
    """A RelationDoc of the version before GO09 (no `attributes`) differs from the managed seed:
    `desk update` names it, `--apply` rewrites and reports it, and a second run changes nothing."""
    import re

    edge = lifecycle_desk / "desk" / "lifecycle" / "testing-task_hands_to_closeout.md"
    old_version = re.sub(r"^attributes:\n(?:  .*\n)+", "", edge.read_text(encoding="utf-8"), flags=re.M)
    edge.write_text(old_version, encoding="utf-8")
    assert "attributes" not in edge.read_text(encoding="utf-8") and "relation_type: task_hands_to_closeout" in old_version

    code, out = _run(["desk", "update", "--root", str(lifecycle_desk)])
    assert code == 1
    assert "- Lifecycle documents to rewrite: desk/lifecycle/testing-task_hands_to_closeout.md" in out

    code, out = _run(["desk", "update", "--root", str(lifecycle_desk), "--apply"])
    assert code == 0, out
    assert "Lifecycle graph: rewrote desk/lifecycle/testing-task_hands_to_closeout.md" in out
    assert edge.read_bytes() == (LIFECYCLE_TEMPLATES / edge.name).read_bytes()
    assert lifecycle.transitions_from(lifecycle_desk, "ritual-testing")[0].sets == {"status": "ready_for_testing"}

    before = _lifecycle_tree(lifecycle_desk)
    code, out = _run(["desk", "update", "--root", str(lifecycle_desk), "--apply"])
    assert (code, out.strip()) == (0, "Desk is up to date.")
    assert _lifecycle_tree(lifecycle_desk) == before
    assert main(["doctor", "--root", str(lifecycle_desk)]) == 0


def test_a_desk_edge_whose_sets_differ_from_the_package_is_refused_before_the_write(lifecycle_desk: Path) -> None:
    """The effect is the edge's, but the task's lifecycle is checked against the package's edges
    (CC37 a1: ``desk update --apply`` restores a managed edge a desk changed). An edge edited
    through sldb's API to set another status makes ``advance`` refuse the transition before any
    write: since the advance/doctor task.debug (d2) the refusal is ``LifecycleSeedOutOfDate``,
    naming the edge and ``desk update --apply``, instead of the model's ValidationError. The task
    stays as it was; no YAML of the package changes."""
    from sldb.api import save_document_payload
    from sldb.models.relation_doc import RelationDoc
    from sldb.runtime.validation import extract_model_data

    spec_before = lifecycle.SPEC_PATH.read_bytes()
    edge = lifecycle_desk / "desk" / "lifecycle" / "execution-task_activates.md"
    payload = extract_model_data(RelationDoc, edge.read_text(encoding="utf-8"))
    payload["attributes"]["sets"]["status"] = "in_review"
    save_document_payload(lifecycle_desk / ".sldb", "RelationDoc", "execution-task_activates", payload, pythonpath=package_pythonpath())

    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Declared effect")  # the first desk operation scaffolds only what is missing
    accept_receipts(lifecycle_desk, task_id)
    with pytest.raises(lifecycle.LifecycleSeedOutOfDate) as excinfo:
        operations.advance_task(task_id)

    assert "does not set status active (attributes.sets.status is in_review)" in str(excinfo.value)
    assert "deskops desk update --apply" in str(excinfo.value)
    stored = operations._read_doc(lifecycle_desk / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    assert (stored["status"], stored["current_node"], stored["history"]) == ("draft", "ritual-execution", [])
    assert lifecycle.SPEC_PATH.read_bytes() == spec_before
    assert "in_review" not in lifecycle.SPEC_PATH.read_text(encoding="utf-8")


def test_advance_walks_the_graph_and_sets_status_per_transition(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Walk the graph")
    accept_receipts(lifecycle_desk, task_id)

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status, result.progressed) == ("ritual-testing", "active", True)

    task, result = operations.advance_task(task_id)
    assert (task.current_node, task.status) == ("ritual-closeout", "ready_for_testing")

    task, result = operations.advance_task(task_id)
    assert result.blocked and not result.progressed
    # Without the evidence receipts closeout verify writes, the type's closeout rule holds
    # task_completes back (CC33b) and the message names the rule and its clause.
    assert "rules/rule-closeout-task-code" in result.message, "the blocking rule is named"
    assert 'fact = "tests"' in result.message
    payload = operations._read_doc(lifecycle_desk / "desk" / "tasks" / f"{task_id}.md", TaskDoc)
    assert payload["history"] == ["task_activates", "task_hands_to_closeout"]


def test_testing_gate_needs_validation(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "No validation", validation=[])
    accept_receipts(lifecycle_desk, task_id)
    operations.advance_task(task_id)

    task, result = operations.advance_task(task_id)

    assert result.blocked
    assert task.current_node == "ritual-testing"


def test_show_task_reports_the_gates_leaving_the_current_node(lifecycle_desk: Path) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    task_id = _task(operations, "Show gates")
    accept_receipts(lifecycle_desk, task_id)
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
