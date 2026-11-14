"""CC37: a task's lifecycle is a validator of TaskDoc, so no write leaves it outside the rules.

``status``, ``current_node`` and ``history`` must form a state the lifecycle graph (the
``RelationDoc`` seeds of ``deskops/data/lifecycle/``) or closeout can produce, and
``task_type`` must match the document's model. sldb builds the model on every write, so
``sldb fields update``, ``sldb docs update`` and ``sldb serve``'s ``/save`` reject an
inconsistent task with the validator's message.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.models.task_lifecycle import CLOSEOUT_STATES, DRAWER_STATUSES, ENTRY_STATUSES, lifecycle_table
from deskops.models.task_types import TaskCodeDoc, TaskDocsDoc
from deskops.models.validation import validation_messages
from deskops.operations import DeskopsOperations
from sldb.cli import main as sldb_main

BASE = {"title": "T", "id": "task-t", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d"}
ENTRY = {**BASE, "status": "draft", "current_node": "ritual-execution", "history": []}
ENTRY_ERROR = (
    "status: 'closed' is not an entry status; a task with an empty history at 'ritual-execution' has "
    "status 'draft' (status changes only through deskops advance and deskops closeout)"
)


def _rejects(model, payload: dict, *texts: str) -> str:
    with pytest.raises(ValidationError) as excinfo:
        model(**payload)
    [message] = validation_messages(excinfo.value)
    for text in texts:
        assert text in message
    return message


# ------------------------------------------------------------------ the table
def test_the_table_is_read_from_the_package_relation_docs() -> None:
    table = lifecycle_table()
    assert table.entry_node == "ritual-execution"
    edges = {name: (edge.target, edge.status) for name, edge in table.edges.items()}
    assert edges == {
        "task_activates": ("ritual-testing", "active"),
        "task_hands_to_closeout": ("ritual-closeout", "ready_for_testing"),
        "task_completes": ("complete", "closed"),
    }
    assert ENTRY_STATUSES == {"draft"}
    assert DRAWER_STATUSES == {"deferred", "candidate"}
    assert {s: h for s, (h, _) in CLOSEOUT_STATES.items()} == {
        "closed": "task_completes",
        "superseded": "superseded",
        "resolved": "resolved-by",
    }


# ------------------------------------------------------------------ (i) entry state
def test_entry_state_is_valid() -> None:
    assert TaskCodeDoc(**ENTRY).status == "draft"
    # An empty current_node is the entry node (deskops advance reads it so).
    assert TaskCodeDoc(**{**ENTRY, "current_node": ""}).current_node == ""


def test_a_drawer_task_outside_the_lifecycle_may_be_deferred() -> None:
    """``promote inbox-to-drawer-task`` writes ``deferred`` with no current_node and no history."""
    assert TaskDoc(**{**ENTRY, "status": "deferred", "current_node": ""}).status == "deferred"
    # The drawer candidates of the workspace-documental plan (CC37 c4, revisable).
    assert TaskDoc(**{**ENTRY, "status": "candidate", "current_node": ""}).status == "candidate"
    _rejects(TaskDoc, {**ENTRY, "status": "deferred"}, "status: 'deferred' is not an entry status")
    _rejects(TaskDoc, {**ENTRY, "status": "active", "current_node": ""}, "status: 'active' is not an entry status; a task with an empty history and no current_node has status 'cancelled', 'candidate', 'closed', 'complete', 'deferred', 'done', 'draft', 'resolved'")


@pytest.mark.parametrize("status", ["resolved", "closed", "done", "complete", "cancelled"])
def test_a_task_resolved_before_the_lifecycle_is_valid_only_outside_it(status: str) -> None:
    """``closeout retire`` removes tasks resolved before the lifecycle: no current_node, no history."""
    assert TaskDoc(**{**ENTRY, "status": status, "current_node": ""}).status == status
    _rejects(TaskDoc, {**ENTRY, "status": status}, f"status: '{status}' is not an entry status")


def test_entry_state_rejects_a_status_outside_the_entry_set() -> None:
    _rejects(TaskCodeDoc, {**ENTRY, "status": "closed"}, "Task task-t lifecycle is inconsistent:", ENTRY_ERROR)
    _rejects(TaskCodeDoc, {**ENTRY, "status": "active"}, "status: 'active' is not an entry status")


def test_entry_state_rejects_a_later_node_without_history() -> None:
    _rejects(
        TaskCodeDoc,
        {**ENTRY, "current_node": "ritual-testing"},
        "current_node: 'ritual-testing' needs a history; with an empty history a task is at the entry node 'ritual-execution'",
    )


# ------------------------------------------------------------------ (ii) after transitions
@pytest.mark.parametrize(
    ("history", "node", "status"),
    [
        (["task_activates"], "ritual-testing", "active"),
        (["task_activates", "task_hands_to_closeout"], "ritual-closeout", "ready_for_testing"),
        (["task_activates", "task_hands_to_closeout", "task_completes"], "complete", "closed"),
    ],
)
def test_state_after_each_transition_is_valid(history: list[str], node: str, status: str) -> None:
    task = TaskCodeDoc(**{**BASE, "status": status, "current_node": node, "history": history})
    assert (task.status, task.current_node) == (status, node)


def test_status_must_be_the_sets_status_of_the_last_transition() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "draft", "current_node": "ritual-testing", "history": ["task_activates"]},
        "status: 'draft' does not follow history 'task_activates'; expected 'active'",
    )


def test_current_node_must_be_the_target_of_the_last_transition() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "active", "current_node": "ritual-closeout", "history": ["task_activates"]},
        "current_node: 'ritual-closeout' does not follow history 'task_activates'; expected 'ritual-testing'",
    )


def test_last_history_item_must_be_a_transition_or_a_closeout_record() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "active", "current_node": "ritual-testing", "history": ["jumped"]},
        "history: last item 'jumped' is neither a lifecycle transition",
    )


# ------------------------------------------------------------------ (iii) closed by closeout
@pytest.mark.parametrize(("status", "record"), [("superseded", "superseded"), ("resolved", "resolved-by")])
@pytest.mark.parametrize("node", ["ritual-execution", "ritual-testing", "ritual-closeout"])
def test_closeout_records_are_valid_from_any_node(status: str, record: str, node: str) -> None:
    history = [] if node == "ritual-execution" else ["task_activates"]
    task = TaskCodeDoc(**{**BASE, "status": status, "current_node": node, "history": [*history, record]})
    assert task.history[-1] == record


def test_closeout_status_needs_its_own_record() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "resolved", "current_node": "ritual-execution", "history": ["superseded"]},
        "history: last item 'superseded' is neither",
    )
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "superseded", "current_node": "ritual-execution", "history": []},
        "status: 'superseded' is not an entry status",
    )


def test_closed_needs_the_terminal_transition_and_the_complete_node() -> None:
    _rejects(
        TaskCodeDoc,
        {**BASE, "status": "closed", "current_node": "ritual-closeout", "history": ["task_activates", "task_completes"]},
        "current_node: 'ritual-closeout' does not follow history 'task_completes'; expected 'complete'",
    )


# ------------------------------------------------------------------ (iv) task_type matches the model
def test_task_type_matches_the_typed_model() -> None:
    assert TaskDocsDoc(**ENTRY).task_type == "task.docs"
    with pytest.raises(ValidationError) as excinfo:
        TaskCodeDoc(**{**ENTRY, "task_type": "task.docs"})
    assert excinfo.value.errors()[0]["loc"] == ("task_type",)


@pytest.mark.parametrize("task_type", ["", "code", "implementation", "task.code"])
def test_generic_task_doc_accepts_empty_legacy_or_any_task_type(task_type: str) -> None:
    assert TaskDoc(**{**ENTRY, "task_type": task_type}).task_type == task_type


# ------------------------------------------------------------------ sldb applies it on every write
def _sldb_run(argv: list[str]) -> tuple[int, str]:
    try:
        return int(sldb_main(argv) or 0), ""
    except SystemExit as exc:
        if isinstance(exc.code, int) or exc.code is None:
            return int(exc.code or 0), ""
        return 1, str(exc.code)


@pytest.fixture
def task_desk(lifecycle_desk: Path) -> tuple[Path, Path]:
    payload = {
        "title": "Probe",
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
        "task_type": "task.code",
    }
    task_id = DeskopsOperations(lifecycle_desk).create_task_bundle(payload).task_id  # tracked as TaskCodeDoc
    return lifecycle_desk, lifecycle_desk / "desk" / "tasks" / f"{task_id}.md"


def _store_args(root: Path) -> list[str]:
    return ["--store", str(root / ".sldb"), "--pythonpath", str(ROOT)]


def _current_payload(root: Path) -> dict:
    """The task's payload as sldb holds it (what ``/save``'s ``expected`` guard compares)."""
    from sldb.cli.model_utils import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    [doc] = [d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(ROOT)) if d.name == "task-probe"]
    return dict(doc.payload)


def test_sldb_fields_update_of_status_to_closed_at_ritual_execution_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    code, message = _sldb_run(["fields", "update", "docs/TaskCodeDoc/task-probe/status", '"closed"', *_store_args(root)])
    out = capsys.readouterr()
    assert code != 0
    assert ENTRY_ERROR in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


def test_sldb_fields_update_of_current_node_without_a_coherent_status_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    code, message = _sldb_run(
        ["fields", "update", "docs/TaskCodeDoc/task-probe/current_node", '"ritual-closeout"', *_store_args(root)]
    )
    out = capsys.readouterr()
    assert code != 0
    assert (
        "current_node: 'ritual-closeout' needs a history; with an empty history a task is at the entry node "
        "'ritual-execution'"
    ) in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


def test_sldb_docs_update_with_the_inconsistent_payload_is_rejected(task_desk, capsys) -> None:
    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    payload = json.dumps({**_current_payload(root), "status": "closed"})
    code, message = _sldb_run(["docs", "update", "task-probe", payload, *_store_args(root)])
    out = capsys.readouterr()
    assert code != 0
    assert ENTRY_ERROR in message + out.out + out.err
    assert task.read_text(encoding="utf-8") == before


@pytest.mark.parametrize("batched", [False, True])
def test_sldb_serve_save_with_the_inconsistent_payload_is_rejected(task_desk, batched: bool) -> None:
    """``save_request`` is what ``sldb serve`` runs for ``POST /save`` (single and batched)."""
    from sldb.cli.serve.save_routes import save_request

    root, task = task_desk
    before = task.read_text(encoding="utf-8")
    current = _current_payload(root)
    payload = {**current, "status": "closed"}
    if batched:
        change = {"id": "task-probe", "action": "update", "model": "TaskCodeDoc", "payload": payload, "expected": current}
        request = {"changes": [change]}
    else:
        request = {"doc": "task-probe", "payload": payload}
    try:
        response, code = save_request(request, root / ".sldb", root, str(ROOT))
        message = json.dumps(response, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001 - the single route raises what the HTTP layer turns into a 4xx
        code, message = 400, str(exc)
    assert code >= 400
    assert ENTRY_ERROR in message
    assert task.read_text(encoding="utf-8") == before


def test_a_consistent_direct_write_is_accepted(task_desk, capsys) -> None:
    """DA6: no "transition only" field; a coherent state written without a transition is fine."""
    root, task = task_desk
    code, _ = _sldb_run(["fields", "update", "docs/TaskCodeDoc/task-probe/summary", '"probe"', *_store_args(root)])
    capsys.readouterr()
    assert code == 0
    assert "summary: probe" in task.read_text(encoding="utf-8")


# ------------------------------------------------------------------ desk update reports, never writes
#: A non-empty history with an incoherent status: the migration table leaves it to its owner (an
#: empty history with a non-terminal status is migrated to draft instead, task.debug of
#: non-terminal tasks).
ACTIVE_ERROR = "status: 'ready_for_testing' does not follow history 'task_activates'; expected 'active'"


def test_desk_update_reports_an_inconsistent_task_and_does_not_write_it(lifecycle_desk: Path, capsys) -> None:
    """An untracked task with a legacy task_type (a pending migration) and a status no transition
    wrote nor the legacy table decides: desk update lists it and --apply neither migrates nor
    tracks it, and exits 1 while it waits for its owner."""
    from deskops.models.task_lifecycle import UNMIGRATABLE_SUGGESTION

    root = lifecycle_desk
    text = (
        "---\nid: task-legacy\nstatus: ready_for_testing\ncurrent_node: ritual-testing\nhistory:\n- task_activates\ntask_type: code\n---\n\n"
        "# Legacy\n\n## Goal\n\ng\n"
    )
    task = root / "desk" / "tasks" / "task-legacy.md"
    task.write_text(text, encoding="utf-8")
    line = f"  - desk/tasks/task-legacy.md: {ACTIVE_ERROR}. To fix it, {UNMIGRATABLE_SUGGESTION}."

    assert main(["desk", "update", "--root", str(root)]) == 1
    out = capsys.readouterr().out
    assert "- Invalid task documents (not written): 1 task(s)" in out
    assert line in out
    assert "Pending task type migration" not in out

    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    assert line in capsys.readouterr().out
    assert task.read_text(encoding="utf-8") == text
    code, _ = _sldb_run(["docs", "list", "--store", str(root / ".sldb")])
    assert "task-legacy" not in capsys.readouterr().out


def test_desk_update_names_a_tracked_inconsistent_task_and_writes_nothing(task_desk, capsys, sldb_cache) -> None:
    """A tracked task edited by hand outside the rules: sldb names it store/doc-invalid and goes
    on, so desk update reports the validator's message, writes nothing to the task, and keeps the
    other repairs instead of skipping them (g2)."""
    root, task = task_desk
    sldb_cache(root)
    text = task.read_text(encoding="utf-8")
    assert text.count("status: draft\n") == 1 and text.count("current_node: ritual-execution\n") == 1
    assert text.count("history: []\n") == 1
    text = (
        text.replace("status: draft\n", "status: ready_for_testing\n")
        .replace("current_node: ritual-execution\n", "current_node: ritual-testing\n")
        .replace("history: []\n", "history:\n- task_activates\n")
    )
    task.write_text(text, encoding="utf-8")
    capsys.readouterr()
    assert main(["desk", "update", "--root", str(root), "--apply"]) == 1
    out = capsys.readouterr().out
    rel = task.relative_to(root).as_posix()
    assert f"  - {rel}: {ACTIVE_ERROR}." in out
    assert "- Store check failed" not in out
    assert "Skipped the other repairs" not in out
    assert task.read_text(encoding="utf-8") == text
