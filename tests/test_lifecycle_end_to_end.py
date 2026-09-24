from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest

from deskops.operations import DeskopsOperations


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([*CLI, *argv], cwd=root, capture_output=True, text=True)
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
    root = _make_repo(tmp_path)

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

    # There is no direct drawer -> task promotion: the task is authored
    # explicitly from the loose drawer candidate, every structured field
    # written by hand. --validation takes nargs="+", so it goes last.
    _cli(
        root, "add", "task", "--root", str(root),
        "--title", "Lifecycle E2E",
        "--why", "Prove the real CLI lifecycle end to end.",
        "--goal", "Close a task authored from a drawer candidate.",
        "--scope", "The lifecycle CLI only.",
        "--implementation-path", "Author the task, advance it, close it out.",
        "--done-when", "The task closes with a commit.",
        "--from-drawer", "lifecycle-e2e",
        "--validation", "pytest tests/test_lifecycle_smoke.py",
    )
    active_task = root / "desk" / "tasks" / "task-lifecycle-e2e.md"
    routine = root / "desk" / "routines" / "routine-task-lifecycle-e2e.md"
    assert active_task.exists()
    assert routine.exists()
    assert "desk/drawer/tasks/task-lifecycle-e2e.md" in active_task.read_text(encoding="utf-8")
    assert drawer_task.exists(), "the drawer candidate is kept for manual cleanup"

    board_text = (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-lifecycle-e2e.md" in board_text

    first_advance = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: active" in first_advance.stdout
    assert "Current node: checklist-task-lifecycle-e2e-testing-ready" in first_advance.stdout

    second_advance = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: ready_for_testing" in second_advance.stdout
    assert "Current node: checklist-task-lifecycle-e2e-closeout-ready" in second_advance.stdout

    blocked_closeout = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert blocked_closeout.returncode == 1
    assert "Status: ready_for_testing" in blocked_closeout.stdout
    assert "Current node: checklist-task-lifecycle-e2e-closeout-ready" in blocked_closeout.stdout
    assert "is not complete" in blocked_closeout.stdout

    _write(root, "tests/test_lifecycle_smoke.py", "def test_lifecycle_smoke():\n    assert True\n")
    seed_commit = _git(root, "rev-parse", "HEAD")
    references = (
        '["desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md", '
        '"pytest tests/test_lifecycle_smoke.py::test_lifecycle_smoke", '
        f'"{seed_commit}"]'
    )
    files = '["desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md", "tests/test_lifecycle_smoke.py"]'

    edit_references = _cli(
        root,
        "edit",
        "task",
        "task-lifecycle-e2e",
        "references",
        references,
        "--root",
        str(root),
    )
    assert "Updated task task-lifecycle-e2e field references" in edit_references.stdout
    assert "desk/drawer/tasks/task-lifecycle-e2e.md" in active_task.read_text(encoding="utf-8"), (
        "from_drawer must survive replacing references"
    )

    edit_files = _cli(
        root,
        "edit",
        "task",
        "task-lifecycle-e2e",
        "files",
        files,
        "--root",
        str(root),
    )
    assert "Updated task task-lifecycle-e2e field files" in edit_files.stdout

    closed = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: closed" in closed.stdout
    assert "Current node: complete" in closed.stdout

    assert not active_task.exists()
    assert not routine.exists()
    primitive_dirs = [
        root / "desk" / "primitives" / "conditions",
        root / "desk" / "primitives" / "operators",
        root / "desk" / "primitives" / "checklists",
        root / "desk" / "primitives" / "edges",
        root / "desk" / "primitives" / "hooks",
    ]
    assert all(not list(directory.glob("*task-lifecycle-e2e*.md")) for directory in primitive_dirs)

    final_board_text = (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-lifecycle-e2e.md" not in final_board_text

    closing_message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-lifecycle-e2e" in closing_message
    assert "Task-Id: task-lifecycle-e2e" in closing_message

    committed_files = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "desk/tasks/Board.md" in committed_files
    assert "desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md" in committed_files
    assert "tests/test_lifecycle_smoke.py" in committed_files

def test_auto_commit_task_closure_failure_path_keeps_bundle(tmp_path: Path) -> None:
    """A closeout that cannot commit must leave the desk exactly as it found it."""
    root = _make_repo(tmp_path)

    task_id = "task-fail-commit"
    task_path = root / "desk" / "tasks" / f"{task_id}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        "---\n"
        f"id: {task_id}\n"
        "status: active\n"
        "current_node: closeout-ready\n"
        "routine: ''\n"
        "files: []\n"
        "---\n\n# Fail task\n",
        encoding="utf-8",
    )
    board_path = root / "desk" / "tasks" / "Board.md"
    board_path.write_text(
        "---\n"
        "id: Board\n"
        "scope: ''\n"
        "tasks: ['desk/tasks/task-fail-commit.md']\n"
        "pills: []\n"
        "rituals: []\n"
        "tags: []\n"
        "---\n\n# Board\n",
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "init task")
    board_before = board_path.read_text(encoding="utf-8")

    # A hook that rejects the commit stands in for any commit that cannot be made.
    pre_commit = root / ".git" / "hooks" / "pre-commit"
    pre_commit.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
    pre_commit.chmod(0o755)

    operations = DeskopsOperations(root)
    with pytest.raises(RuntimeError, match="Failed to commit task closure"):
        operations._auto_commit_task_closure(
            {"id": task_id, "routine": "", "files": []}, task_path
        )

    assert task_path.exists(), "the task bundle must survive a failed closure commit"
    assert board_path.read_text(encoding="utf-8") == board_before, (
        "the board must be left as it was when the commit fails"
    )
