from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    # The plan's env rule: a stale deskops 0.1.0 in site-packages hijacks the
    # subprocess unless the worktree is on PYTHONPATH.
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    result = subprocess.run([*CLI, *argv], cwd=root, capture_output=True, text=True, env=env)
    if check:
        assert result.returncode == 0, result.stderr or result.stdout
    return result


def _write(root: Path, relative_path: str, content: str) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(root, "add", "seed.txt")
    _git(root, "commit", "-q", "-m", "seed")
    return root


def test_task_lifecycle_runs_from_intake_to_closeout_via_real_cli(tmp_path: Path) -> None:
    """Intake -> drawer -> routed -> derived status ladder -> closed commit.

    The CLI drives intake, promotion and the advance gates; the documents a
    task needs to climb the ladder (plan, target, contract, symbol, coverage,
    run, acceptance) are written through the library, which is what the plan's
    F5/F6 commands will wrap.
    """
    root = _make_repo(tmp_path)
    sys.path.insert(0, str(ROOT / "tests"))

    install = _cli(root, "desk", "install", str(root))
    assert "Scaffold complete." in install.stdout

    _cli(
        root,
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        "Lifecycle CLI end to end evidence",
        "--five-wh-one-plus",
        "what",
        "--answer",
        "The task lifecycle is runnable through the real CLI from intake to closeout.",
    )

    inbox_note = _write(
        root,
        "desk/inbox/20260901-000000-suggestion-lifecycle-e2e.md",
        "---\n"
        "kind: suggestion\n"
        "sender_project: sibling\n"
        "created_at: 2026-09-01T00:00:00\n"
        "status: open\n"
        "---\n\n"
        "# Lifecycle E2E\n\n"
        "Prove the real CLI can promote this note and close the resulting task.\n",
    )

    first_promote = _cli(root, "promote", "inbox-to-drawer-task", "lifecycle-e2e", "--root", str(root))
    drawer_task = root / "desk" / "drawer" / "tasks" / "task-lifecycle-e2e.md"
    assert "Created drawer task candidate task-lifecycle-e2e" in first_promote.stdout
    assert drawer_task.exists()
    assert not inbox_note.exists()

    # An unrouted task cannot advance: the gate names the routing.
    blocked = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert blocked.returncode == 1
    assert "Status: drawer" in blocked.stdout
    assert "not routed by a board" in blocked.stdout

    second_promote = _cli(root, "promote", "drawer-task-to-active-task", "lifecycle-e2e", "--root", str(root))
    active_task = root / "desk" / "tasks" / "task-lifecycle-e2e.md"
    assert "Promoted task task-lifecycle-e2e" in second_promote.stdout
    assert active_task.exists()
    assert not drawer_task.exists()
    assert not list((root / "desk" / "routines").glob("routine-task-lifecycle-e2e.md"))
    primitive_dirs = [
        root / "desk" / "primitives" / "conditions",
        root / "desk" / "primitives" / "operators",
        root / "desk" / "primitives" / "checklists",
        root / "desk" / "primitives" / "edges",
        root / "desk" / "primitives" / "hooks",
    ]
    assert all(not list(directory.glob("*task-lifecycle-e2e*.md")) for directory in primitive_dirs)

    routed = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert routed.returncode == 1
    assert "Status: active" in routed.stdout
    assert "No plan targets are declared" in routed.stdout

    # The documents that climb the ladder, written through the library.
    from derived_support import bind_task_plan, contract_payload, cover_and_prove, create, document_symbol, target_payload
    from deskops import forms

    world = forms.world_for(root)
    contract = contract_payload("contract-lifecycle-e2e", "deskops.forms:advance_task")
    create(world, "SymbolContractDoc", "contract-lifecycle-e2e", contract, "desk/plans")
    bind_task_plan(
        world,
        "task-lifecycle-e2e",
        "plan-lifecycle-e2e",
        [target_payload("plan-target-lifecycle-e2e", contract="SymbolContractDoc:contract-lifecycle-e2e")],
    )

    execution = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert execution.returncode == 1
    assert "Status: execution" in execution.stdout
    assert "contracts are not implemented" in execution.stdout

    document_symbol(world, "deskops.forms:advance_task")
    testing = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert testing.returncode == 1
    assert "Status: testing" in testing.stdout
    assert "tests are not proven" in testing.stdout

    _write(root, "tests/test_lifecycle_smoke.py", "def test_lifecycle_smoke():\n    assert True\n")
    cover_and_prove(world, contract, "task-lifecycle-e2e", run_id="run-lifecycle-e2e")
    closeout = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert closeout.returncode == 1
    assert "Status: closeout" in closeout.stdout
    assert "Closeout evidence is missing" in closeout.stdout

    create(
        world,
        "AcceptanceDoc",
        "acceptance-task-lifecycle-e2e",
        {
            "id": "acceptance-task-lifecycle-e2e",
            "title": "Acceptance",
            "status": "complete",
            "summary": "Closing rules.",
            "validation": ["pytest tests/test_lifecycle_smoke.py::test_lifecycle_smoke"],
            "done_when": ["the suite is green"],
            "evidence": ["desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md", "run-lifecycle-e2e"],
            "tags": ["workspace:desk"],
        },
        "desk/tasks",
    )
    bind_task_plan(
        world,
        "task-lifecycle-e2e",
        "plan-lifecycle-e2e",
        [target_payload("plan-target-lifecycle-e2e", contract="SymbolContractDoc:contract-lifecycle-e2e")],
        acceptance="AcceptanceDoc:acceptance-task-lifecycle-e2e",
    )

    closed = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: closed" in closed.stdout

    # The closing commit is the operator's move in the new architecture: the
    # status is derived, so the ledger entry names the task and its evidence.
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "closeout: task-lifecycle-e2e\n\nTask-Id: task-lifecycle-e2e")
    closing_message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-lifecycle-e2e" in closing_message
    assert "Task-Id: task-lifecycle-e2e" in closing_message

    committed_files = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "desk/tasks/task-lifecycle-e2e.md" in committed_files
    assert "desk/tasks/Board.md" in committed_files
    assert "desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md" in committed_files
    assert "tests/test_lifecycle_smoke.py" in committed_files
