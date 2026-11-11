"""deskops view: board and task are sldb ViewDocs evaluated by run_view (CC34), drawer, inbox
and agents read what is not in the store; all over real temporary desks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from sldb import api

from deskops.cli.commands.view import ViewError
from deskops.cli.commands.view import board_view
from deskops.cli.commands.view import drawer_view
from deskops.cli.commands.view import inbox_view
from deskops.cli.commands.view import project
from deskops.cli.commands.view import run_view
from deskops.cli.commands.view import task_view
from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from deskops.runtime.desk_agents import agents_view
from tests.view_desk import VIEWS_DIR
from tests.view_desk import build_view_desk

REPO = Path(__file__).resolve().parents[1]


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
def desk(lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch) -> dict:
    ids = build_view_desk(lifecycle_desk, monkeypatch)
    return {"root": lifecycle_desk, "ops": DeskopsOperations(lifecycle_desk), **ids}


def test_the_seed_viewdocs_are_board_and_task_and_list_in_the_store(desk: dict) -> None:
    assert sorted(p.stem for p in VIEWS_DIR.glob("*.md")) == ["board", "task"]
    listed = {view["name"]: view for view in api.list_views(desk["root"] / ".sldb")}
    assert listed["board"]["sections"] == ["board", "tasks", "pills", "atoms"]
    assert listed["task"]["sections"] == ["board", "task", "pills", "atoms"]
    assert [param["name"] for param in listed["task"]["params"]] == ["id"]


def test_board_groups_by_current_node_in_spec_order_and_gates_are_show_task(desk: dict) -> None:
    view = board_view(desk["root"])
    assert [column["node"] for column in view["columns"]] == ["ritual-execution", "ritual-testing", "ritual-closeout"]
    by_node = {column["node"]: [card["id"] for card in column["tasks"]] for column in view["columns"]}
    assert by_node == {"ritual-execution": [desk["execution"]], "ritual-testing": [desk["testing"]], "ritual-closeout": [desk["closeout"]]}
    groups = run_view(desk["root"], "board")["sections"]["tasks"]["groups"]
    assert [(group["value"], [row["name"] for row in group["rows"]]) for group in groups] == list(by_node.items())
    for column in view["columns"]:
        for card in column["tasks"]:
            _, gates = desk["ops"].show_task(card["id"])
            assert card["gates"] == gates and card["gates_total"] == len(gates)
            report = desk["ops"].verify_task_closeout(card["id"])
            assert card["closeout"]["declared"] == report["declared"] and card["closeout"]["found"] == report["found"]


def test_unresolvable_pill_and_atom_go_to_errors_not_to_the_card(desk: dict) -> None:
    view = board_view(desk["root"])
    cards = {card["id"]: card for column in view["columns"] for card in column["tasks"]}
    first, second = cards[desk["execution"]], cards[desk["testing"]]
    assert [(p["id"], p["title"]) for p in first["pills"]] == [(desk["pill"], "Guardrail: view pill")]
    assert [a["id"] for a in first["atoms"]] == [desk["atom"]]
    assert second["pills"] == [] and second["atoms"] == []
    references = {item["reference"]: item.get("task") for item in view["errors"]}
    assert references["pill-does-not-exist"] == desk["testing"]
    assert references["atom-does-not-exist"] == desk["testing"]


def test_project_of_the_run_view_result_is_the_cli_payload(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    """c6: what graph_ui gets from GET /views/<view> (run_view) projects to `deskops view`."""
    root = desk["root"]
    assert project("board", run_view(root, "board"), root) == _cli_json(capsys, "view", "board", "--root", str(root), "--format", "json")
    task = _cli_json(capsys, "view", "task", desk["execution"], "--root", str(root), "--format", "json")
    assert project("task", run_view(root, "task", {"id": desk["execution"]}), root) == task


def test_task_revision_is_the_etag_of_the_task_view(desk: dict) -> None:
    root = desk["root"]
    view = task_view(root, desk["execution"])
    task = view["task"]
    assert task["goal"] == "goal of View golden execution" and task["on_board"] is True
    assert task["pills"][0]["how_not"] == "how not text" and task["atoms"][0]["answer"] == "the answer"
    assert view["next"]["next_actions"] and view["next"]["advance_when"]
    assert view["revision"] == run_view(root, "task", {"id": desk["execution"]})["revision"]
    assert main(["edit", "task", desk["execution"], "goal", "a new goal", "--root", str(root)]) == 0
    moved = task_view(root, desk["execution"])
    assert moved["task"]["goal"] == "a new goal" and moved["revision"] != view["revision"]


def test_unknown_task_raises(desk: dict) -> None:
    with pytest.raises(ViewError):
        task_view(desk["root"], "task-nope")


def test_a_desk_without_board_is_a_view_error(tmp_path: Path) -> None:
    with pytest.raises(ViewError, match="No desk board"):
        board_view(tmp_path)


def test_drawer_inbox_and_agents_read_what_is_on_disk(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    root = desk["root"]
    runs = root / "runs/subagents/index.jsonl"
    runs.parent.mkdir(parents=True)
    runs.write_text(
        json.dumps({"task_id": desk["execution"], "run_id": None, "run_dir": None, "mode": "manual", "commit": None}) + "\n"
        + json.dumps({"task_id": "task-gone", "run_id": "r1", "run_dir": "runs/subagents/x", "commit": None}) + "\n",
        encoding="utf-8",
    )
    drawer = drawer_view(root)
    [entry] = drawer["tasks"]
    assert entry["title"] == "Deferred idea" and entry["status"] == "deferred"
    assert entry["markdown"] == (root / entry["path"]).read_text(encoding="utf-8")
    assert entry["command"].startswith(f"deskops add task --root . --from-drawer {entry['path']} --title ")

    inbox = inbox_view(root)
    listed = _cli_json(capsys, "message", "list", "--root", str(root), "--format", "json")["notes"]
    assert [note["id"] for note in inbox["notes"]] == [note["id"] for note in listed]
    [note] = inbox["notes"]
    assert note["title"] == "Open question" and note["body"] == "Question body" and note["date"] == "2026-11-04T10:16:00"
    assert note["revision"] == hashlib.sha256((root / note["path"]).read_bytes()).hexdigest()

    agents = agents_view(root, workers_provider=lambda: [{"pane_id": "w1:p1", "agent": "pi", "agent_status": "idle", "cwd": str(root)}])
    assert agents["live_workers"] == 1 and agents["workers"][0]["pane"] == "w1:p1"
    assert [run["task_id"] for run in agents["runs"]] == ["task-gone", desk["execution"]]
    assert [run["on_board"] for run in agents["runs"]] == [False, True]


def test_agents_without_herdr_reports_the_cause(desk: dict) -> None:
    def broken() -> list:
        raise RuntimeError("herdr not running")

    agents = agents_view(desk["root"], workers_provider=broken)
    assert agents["workers"] is None and "herdr not running" in agents["workers_error"]
    assert agents["errors"][0]["reference"] == "runtime workers"


def test_no_view_writes(desk: dict) -> None:
    root = desk["root"]
    board_view(root)  # the first read may build the store's caches
    before = _tree_hash(root)
    board_view(root)
    task_view(root, desk["execution"])
    drawer_view(root)
    inbox_view(root)
    agents_view(root, workers_provider=lambda: [])
    assert _tree_hash(root) == before


def test_view_text_lists_the_board(desk: dict, capsys: pytest.CaptureFixture[str]) -> None:
    capsys.readouterr()
    assert main(["view", "board", "--root", str(desk["root"])]) == 0
    assert desk["execution"] in capsys.readouterr().out


def test_a_store_without_the_viewdocs_is_an_error_envelope(lifecycle_desk: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch) -> None:
    """A store where sldb finds no ViewDoc `board` (neither its own nor a linked one) is sldb's
    error in the envelope, not an invented view. Since sldb resolves a ViewDoc of a linked store
    (H9, sldb 04a0e94e), whether a test desk finds the package's views depends on whether the
    deskops repo's own store was built (CI builds it first), so the missing view is simulated at
    sldb's API instead of relied on."""
    from sldb.core.exceptions import SLDBDocumentTargetError

    def no_view(store, name, params=None):
        raise SLDBDocumentTargetError(f"Unknown view: {name}")

    monkeypatch.setattr(api, "run_view", no_view)
    capsys.readouterr()
    assert main(["view", "board", "--root", str(lifecycle_desk), "--format", "json"]) == 1
    error = json.loads(capsys.readouterr().out)["error"]
    assert error["message"] == "Unknown view: board"


def test_view_is_registered_read_only() -> None:
    from deskops.cli.registry import command_registry

    view_commands = [command for command in command_registry() if command.path[0] == "view"]
    assert {command.path for command in view_commands} == {
        ("view",), ("view", "board"), ("view", "task"), ("view", "drawer"), ("view", "inbox"), ("view", "agents")
    }
    assert not any(command.mutates for command in view_commands)


def test_the_old_view_service_is_gone() -> None:
    hits = [
        f"{path.relative_to(REPO)}"
        for path in (REPO / "deskops").rglob("*.py")
        if "desk_view" in path.read_text(encoding="utf-8") or "DeskView" in path.read_text(encoding="utf-8")
    ]
    assert hits == []
