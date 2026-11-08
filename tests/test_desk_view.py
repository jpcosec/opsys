"""deskops view: the read-only views the deskops UI draws, over real temporary desks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations
from tests.activation_receipts import accept_receipts
from deskops.services.desk_view import DeskView
from deskops.services.desk_view import DeskViewError


def _task(operations: DeskopsOperations, title: str, **extra: object) -> str:
    payload = {
        "title": title,
        "goal": f"goal of {title}",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest -q tests/test_x.py"],
        "task_type": "code",
        **extra,
    }
    return operations.create_task_bundle(payload).task_id


def _pill(operations: DeskopsOperations, title: str) -> str:
    record = operations.create_artifact(
        "artifact.pill",
        {
            "title": title,
            "what": "what text",
            "why": "why text",
            "when": "when text",
            "where": "where text",
            "how": "how text",
            "how_not": "how not text",
            "tags": ["topic:view"],
        },
    )
    return record.doc_id


def _atom(operations: DeskopsOperations, title: str) -> str:
    record = operations.create_artifact(
        "artifact.atom",
        {"title": title, "five_wh_one_plus": "what", "answer": "the answer", "tags": ["topic:view"]},
    )
    return record.doc_id


def _tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.relative_to(root).parts):
        digest.update(path.relative_to(root).as_posix().encode() + b"\0" + path.read_bytes())
    return digest.hexdigest()


def _cli_json(capsys: pytest.CaptureFixture[str], *argv: str) -> dict:
    capsys.readouterr()
    assert main(list(argv)) == 0
    return json.loads(capsys.readouterr().out)


@pytest.fixture
def desk(lifecycle_desk: Path) -> dict:
    ops = DeskopsOperations(lifecycle_desk)
    pill = _pill(ops, "Guardrail: view pill")
    atom = _atom(ops, "Atom for the view")
    first = _task(ops, "First task", pills=[pill], atoms=[atom])
    second = _task(ops, "Second task", pills=["pill-does-not-exist"], atoms=["atom-does-not-exist"])
    accept_receipts(lifecycle_desk, second)
    ops.advance_task(second)
    return {"root": lifecycle_desk, "ops": ops, "first": first, "second": second, "pill": pill, "atom": atom}


def test_board_groups_by_current_node_in_spec_order_and_counts_gates_like_show_task(desk: dict) -> None:
    view = DeskView(desk["root"]).board()

    assert [column["node"] for column in view["columns"]] == ["ritual-execution", "ritual-testing", "ritual-closeout"]
    by_node = {column["node"]: [card["id"] for card in column["tasks"]] for column in view["columns"]}
    assert by_node == {"ritual-execution": [desk["first"]], "ritual-testing": [desk["second"]], "ritual-closeout": []}
    assert view["counts"]["by_node"] == {"ritual-execution": 1, "ritual-testing": 1, "ritual-closeout": 0}
    for column in view["columns"]:
        for card in column["tasks"]:
            _, gates = desk["ops"].show_task(card["id"])
            assert card["gates"] == gates
            assert card["gates_holding"] == sum(1 for gate in gates if gate["holds"])
            assert card["gates_total"] == len(gates)
            report = desk["ops"].verify_task_closeout(card["id"])
            assert card["closeout"]["declared"] == report["declared"]
            assert card["closeout"]["found"] == report["found"]


def test_unresolvable_pill_and_atom_go_to_errors_not_to_the_card(desk: dict) -> None:
    view = DeskView(desk["root"]).board()
    cards = {card["id"]: card for column in view["columns"] for card in column["tasks"]}

    first, second = cards[desk["first"]], cards[desk["second"]]
    assert [p["id"] for p in first["pills"]] == [desk["pill"]]
    assert first["pills"][0]["title"] == "Guardrail: view pill"
    assert [a["id"] for a in first["atoms"]] == [desk["atom"]]
    assert second["pills"] == [] and second["atoms"] == []
    references = {item["reference"]: item.get("task") for item in view["errors"]}
    assert references["pill-does-not-exist"] == desk["second"]
    assert references["atom-does-not-exist"] == desk["second"]
    assert all(item["cause"] for item in view["errors"])


def test_task_view_carries_the_fields_and_the_graph_ui_revision(desk: dict) -> None:
    root = desk["root"]
    view = DeskView(root).task(desk["first"])
    task = view["task"]

    for key in ("goal", "scope", "implementation_path", "validation", "done_when", "why", "references", "files",
                "depends_on", "inherits_from", "gates", "closeout", "pills", "atoms"):
        assert key in task
    assert task["goal"] == "goal of First task"
    assert task["pills"][0]["what"] == "what text" and task["pills"][0]["when"] == "when text"
    assert task["pills"][0]["how_not"] == "how not text"
    assert task["atoms"][0]["answer"] == "the answer"
    assert view["next"]["next_actions"] and view["next"]["advance_when"]
    task_path = root / task["path"]
    expected = hashlib.sha256((root / "desk/tasks/Board.md").read_bytes() + b"\0" + task_path.read_bytes()).hexdigest()
    assert view["revision"] == expected


def test_task_view_revision_matches_graph_ui_desk_routes_when_available(desk: dict) -> None:
    routes = pytest.importorskip("frontends.mindmap.deskops_routes", reason="graph_ui is not importable here")
    detail = routes.DeskRoutes(desk["root"]).detail(desk["first"])
    assert DeskView(desk["root"]).task(desk["first"])["revision"] == detail["revision"]


def test_unknown_task_raises(desk: dict) -> None:
    with pytest.raises(DeskViewError):
        DeskView(desk["root"]).task("task-nope")


def test_drawer_inbox_and_agents_return_what_is_on_disk(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = desk["root"]
    assert main(["message", "send", "--root", str(root), "--title", "Deferred idea", "--kind", "suggestion", "Body of the idea"]) == 0
    assert main(["message", "send", "--root", str(root), "--title", "Open question", "--kind", "unclear", "Question body"]) == 0
    deferred = next(p for p in (root / "desk/inbox").glob("*.md") if "deferred-idea" in p.name)
    assert main(["promote", "inbox-to-drawer-task", deferred.stem, "--root", str(root)]) == 0
    question = next((root / "desk/inbox").glob("*.md"))
    assert main(["message", "ack", question.stem, "--root", str(root)]) == 0
    runs = root / "runs/subagents/index.jsonl"
    runs.parent.mkdir(parents=True)
    runs.write_text(
        json.dumps({"task_id": desk["first"], "run_id": None, "run_dir": None, "mode": "manual", "commit": None}) + "\n"
        + json.dumps({"task_id": "task-gone", "run_id": "r1", "run_dir": "runs/subagents/x", "commit": None}) + "\n",
        encoding="utf-8",
    )
    view = DeskView(root, workers_provider=lambda: [{"pane_id": "w1:p1", "agent": "pi", "agent_status": "idle", "cwd": str(root)}])

    drawer = view.drawer()
    files = sorted(p for p in (root / "desk/drawer/tasks").glob("*.md") if p.name not in {"Board.md", "README.md"})
    assert [entry["path"] for entry in drawer["tasks"]] == [p.relative_to(root).as_posix() for p in files]
    entry = drawer["tasks"][0]
    assert entry["title"] == "Deferred idea" and entry["status"] == "deferred"
    assert entry["markdown"] == (root / entry["path"]).read_text(encoding="utf-8")
    assert entry["command"].startswith(f"deskops add task --root . --from-drawer {entry['path']} --title ")

    inbox = view.inbox()
    listed = _cli_json(capsys, "message", "list", "--root", str(root), "--format", "json")["notes"]
    assert [note["id"] for note in inbox["notes"]] == [note["id"] for note in listed]
    assert inbox["notes"][0]["title"] == "Open question" and inbox["notes"][0]["acknowledged"]
    assert inbox["notes"][0]["body"] == "Question body"
    assert inbox["open"] == 0 and inbox["notes"][0]["date"]
    note_path = root / inbox["notes"][0]["path"]
    assert inbox["notes"][0]["revision"] == hashlib.sha256(note_path.read_bytes()).hexdigest()

    agents = view.agents()
    assert agents["live_workers"] == 1 and agents["workers"][0]["pane"] == "w1:p1"
    assert [run["task_id"] for run in agents["runs"]] == ["task-gone", desk["first"]]
    assert [run["on_board"] for run in agents["runs"]] == [False, True]


def test_agents_without_herdr_reports_the_cause(desk: dict) -> None:
    def broken() -> list:
        raise RuntimeError("herdr not running")

    agents = DeskView(desk["root"], workers_provider=broken).agents()
    assert agents["workers"] is None and "herdr not running" in agents["workers_error"]
    assert agents["errors"][0]["reference"] == "runtime workers"


def test_no_view_writes(desk: dict) -> None:
    root = desk["root"]
    view = DeskView(root, workers_provider=lambda: [])
    before = _tree_hash(root)
    view.board()
    view.task(desk["first"])
    view.drawer()
    view.inbox()
    view.agents()
    assert _tree_hash(root) == before


def test_cli_view_json_matches_the_service(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = str(desk["root"])
    assert _cli_json(capsys, "view", "board", "--root", root, "--format", "json") == DeskView(desk["root"]).board()
    task = _cli_json(capsys, "view", "task", desk["first"], "--root", root, "--format", "json")
    assert task == DeskView(desk["root"]).task(desk["first"])
    capsys.readouterr()
    assert main(["view", "board", "--root", root]) == 0
    assert desk["first"] in capsys.readouterr().out


def test_view_is_registered_read_only() -> None:
    from deskops.cli.registry import command_registry

    view_commands = [command for command in command_registry() if command.path[0] == "view"]
    assert {command.path for command in view_commands} == {
        ("view",), ("view", "board"), ("view", "task"), ("view", "drawer"), ("view", "inbox"), ("view", "agents")
    }
    assert not any(command.mutates for command in view_commands)
