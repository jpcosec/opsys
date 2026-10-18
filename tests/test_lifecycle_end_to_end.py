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

    install = _cli(root, "init", str(root))
    assert "Initialization complete." in install.stdout

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
    assert active_task.exists()
    assert not (root / "desk" / "routines").exists(), "a task writes no routine"
    assert not (root / "desk" / "primitives").exists(), "a task writes no primitives"
    assert "desk/drawer/tasks/task-lifecycle-e2e.md" in active_task.read_text(encoding="utf-8")
    assert drawer_task.exists(), "the drawer candidate is kept for manual cleanup"

    board_text = (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-lifecycle-e2e.md" in board_text

    first_advance = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: active" in first_advance.stdout
    assert "Current node: ritual-testing" in first_advance.stdout

    second_advance = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root))
    assert "Status: ready_for_testing" in second_advance.stdout
    assert "Current node: ritual-closeout" in second_advance.stdout

    blocked_closeout = _cli(root, "advance", "task", "task-lifecycle-e2e", "--root", str(root), check=False)
    assert blocked_closeout.returncode == 1
    assert "Status: ready_for_testing" in blocked_closeout.stdout
    assert "Current node: ritual-closeout" in blocked_closeout.stdout
    assert "is not complete" in blocked_closeout.stdout

    _write(root, "tests/test_lifecycle_smoke.py", "def test_lifecycle_smoke():\n    assert True\n")
    seed_commit = _git(root, "rev-parse", "HEAD")
    references = (
        '["desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md", '
        '"pytest tests/test_lifecycle_smoke.py::test_lifecycle_smoke", '
        f'"{seed_commit}"]'
    )
    files = '["desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md"]'

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

    closed = _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-lifecycle-e2e",
        "--no-run",
        "--reason",
        "Lifecycle smoke test closes without a subagent run",
        "--paths",
        "desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md",
        "tests/test_lifecycle_smoke.py",
    )
    assert "Closing commit " in closed.stdout

    assert not active_task.exists()

    final_board_text = (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-lifecycle-e2e.md" not in final_board_text

    closing_message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-lifecycle-e2e" in closing_message
    assert "Task-Id: task-lifecycle-e2e" in closing_message

    committed_files = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "desk/tasks/Board.md" in committed_files
    assert "desk/atoms/atom-lifecycle-cli-end-to-end-evidence.md" in committed_files
    assert "tests/test_lifecycle_smoke.py" in committed_files

def test_closeout_amends_only_head_with_its_own_task_id(tmp_path: Path) -> None:
    """A closeout amends HEAD only when HEAD's Task-Id trailer is its own."""
    root = _make_repo(tmp_path)
    _cli(root, "init", str(root))
    _cli(
        root,
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        "Closeout amend ownership evidence",
        "--five-wh-one-plus",
        "what",
        "--answer",
        "A closeout never amends another task's closeout commit.",
    )
    _cli(
        root,
        "add",
        "task",
        "--root",
        str(root),
        '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", '
        '"implementation_path": "i", "done_when": "d", "validation": ["pytest"]}',
    )
    _cli(root, "advance", "task", "task-foo", "--root", str(root))
    _cli(root, "advance", "task", "task-foo", "--root", str(root))

    _write(root, "tests/test_amend_owner_smoke.py", "def test_smoke():\n    assert True\n")
    seed_commit = _git(root, "rev-parse", "HEAD")
    _cli(
        root,
        "edit",
        "task",
        "task-foo",
        "references",
        '["desk/atoms/atom-closeout-amend-ownership-evidence.md", '
        '"pytest tests/test_amend_owner_smoke.py::test_smoke", '
        f'"{seed_commit}"]',
        "--root",
        str(root),
    )
    _cli(
        root,
        "edit",
        "task",
        "task-foo",
        "files",
        '["desk/atoms/atom-closeout-amend-ownership-evidence.md"]',
        "--root",
        str(root),
    )

    _git(
        root,
        "commit",
        "--allow-empty",
        "-q",
        "-m",
        "closeout: task-foo-bar\n\nTask-Id: task-foo-bar",
    )
    other_closeout = _git(root, "rev-parse", "HEAD")

    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-foo",
        "--no-run",
        "--reason",
        "Amend ownership smoke test",
        "--paths",
        "desk/atoms/atom-closeout-amend-ownership-evidence.md",
        "tests/test_amend_owner_smoke.py",
    )

    assert _git(root, "rev-parse", "HEAD~1") == other_closeout, (
        "closing task-foo must not amend another task's closeout commit"
    )
    closing_message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-foo" in closing_message
    assert "Task-Id: task-foo" in closing_message


def test_auto_commit_task_closure_commits_only_its_own_paths(tmp_path: Path) -> None:
    """A closeout commit never sweeps in unrelated staged changes."""
    root = _make_repo(tmp_path)
    _cli(root, "init", str(root))
    _cli(
        root,
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        "Closeout commit pathspec evidence",
        "--five-wh-one-plus",
        "what",
        "--answer",
        "A closeout commit contains only the closing task's paths.",
    )
    atom = "desk/atoms/atom-closeout-commit-pathspec-evidence.md"
    test_file = "tests/test_pathspec_smoke.py"

    _cli(
        root,
        "add",
        "task",
        "--root",
        str(root),
        '{"id": "task-pathspec-commit", "title": "Pathspec commit", "goal": "g", "scope": "s", '
        '"implementation_path": "i", "done_when": "d", "validation": ["pytest"]}',
    )
    _cli(root, "advance", "task", "task-pathspec-commit", "--root", str(root))
    _cli(root, "advance", "task", "task-pathspec-commit", "--root", str(root))

    _write(root, test_file, "def test_smoke():\n    assert True\n")
    seed_commit = _git(root, "rev-parse", "HEAD")
    _cli(
        root,
        "edit",
        "task",
        "task-pathspec-commit",
        "references",
        f'["{atom}", "pytest {test_file}::test_smoke", "{seed_commit}"]',
        "--root",
        str(root),
    )
    _cli(
        root,
        "edit",
        "task",
        "task-pathspec-commit",
        "files",
        f'["{atom}"]',
        "--root",
        str(root),
    )

    # Track the task bundle so the closeout records its deletion; the atom and
    # the test stay untracked so the commit also has to pick up new files.
    task_a = root / "desk" / "tasks" / "task-pathspec-commit.md"
    _git(root, "add", task_a.relative_to(root).as_posix())
    _git(root, "commit", "-q", "-m", "track task")

    _write(root, "unrelated.txt", "unrelated\n")
    _git(root, "add", "unrelated.txt")

    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-pathspec-commit",
        "--no-run",
        "--reason",
        "Pathspec smoke test",
        "--paths",
        atom,
        test_file,
    )
    assert not task_a.exists()

    staged = _git(root, "diff", "--cached", "--name-only").split()
    assert "unrelated.txt" in staged, "unrelated staged work must stay staged"
    committed = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "unrelated.txt" not in committed, "unrelated staged work must stay out of the closeout"
    assert "desk/tasks/Board.md" in committed
    assert atom in committed
    assert test_file in committed
    status = _git(root, "show", "--name-status", "--format=", "HEAD")
    assert f"D\tdesk/tasks/task-pathspec-commit.md" in status

    # The amend branch must also be limited to the task's paths.
    _cli(
        root,
        "add",
        "atom",
        "--root",
        str(root),
        "--title",
        "Closeout amend pathspec evidence",
        "--five-wh-one-plus",
        "what",
        "--answer",
        "An amended closeout commit contains only the closing task's paths.",
    )
    amend_atom = "desk/atoms/atom-closeout-amend-pathspec-evidence.md"
    amend_test = "tests/test_pathspec_amend_smoke.py"
    _cli(
        root,
        "add",
        "task",
        "--root",
        str(root),
        '{"id": "task-pathspec-amend", "title": "Pathspec amend", "goal": "g", "scope": "s", '
        '"implementation_path": "i", "done_when": "d", "validation": ["pytest"]}',
    )
    _cli(root, "advance", "task", "task-pathspec-amend", "--root", str(root))
    _cli(root, "advance", "task", "task-pathspec-amend", "--root", str(root))
    _write(root, amend_test, "def test_smoke():\n    assert True\n")
    seed_commit = _git(root, "rev-parse", "HEAD")
    _cli(
        root,
        "edit",
        "task",
        "task-pathspec-amend",
        "references",
        f'["{amend_atom}", "pytest {amend_test}::test_smoke", "{seed_commit}"]',
        "--root",
        str(root),
    )
    _cli(
        root,
        "edit",
        "task",
        "task-pathspec-amend",
        "files",
        f'["{amend_atom}"]',
        "--root",
        str(root),
    )
    task_b = root / "desk" / "tasks" / "task-pathspec-amend.md"
    _git(root, "add", task_b.relative_to(root).as_posix(), "desk/tasks/Board.md")
    _git(root, "commit", "-q", "-m", "track amend task")
    _git(root, "commit", "--allow-empty", "-q", "-m", "closeout: task-pathspec-amend\n\nTask-Id: task-pathspec-amend")
    fake_closeout = _git(root, "rev-parse", "HEAD")

    _write(root, "unrelated-amend.txt", "unrelated\n")
    _git(root, "add", "unrelated-amend.txt")

    _cli(
        root,
        "closeout",
        "commit",
        "--root",
        str(root),
        "--task",
        "task-pathspec-amend",
        "--no-run",
        "--reason",
        "Amend pathspec smoke test",
        "--paths",
        amend_atom,
        amend_test,
    )
    assert not task_b.exists()

    assert _git(root, "rev-parse", "HEAD~1") == _git(root, "rev-parse", f"{fake_closeout}~1"), (
        "the amend branch must amend the existing closeout commit"
    )
    staged = _git(root, "diff", "--cached", "--name-only").split()
    assert "unrelated-amend.txt" in staged
    committed = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "unrelated-amend.txt" not in committed
    assert "desk/tasks/Board.md" in committed
    assert amend_atom in committed
    assert amend_test in committed
    status = _git(root, "show", "--name-status", "--format=", "HEAD")
    assert f"D\tdesk/tasks/task-pathspec-amend.md" in status


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


def test_deleting_the_drawer_entry_leaves_the_task_valid(tmp_path: Path) -> None:
    """from_drawer records provenance; it is not a live reference that must resolve."""
    root = _make_repo(tmp_path)
    _cli(root, "init", str(root))
    _write(
        root,
        "desk/inbox/20260901-000000-suggestion-drawer-provenance.md",
        "---\nkind: suggestion\nsender_project: sibling\ncreated_at: 2026-09-01T00:00:00\nstatus: open\n---\n\n"
        "# Drawer provenance\n\nA task authored from this entry must outlive it.\n",
    )
    _cli(root, "promote", "inbox-to-drawer-task", "drawer-provenance", "--root", str(root))
    drawer_entry = root / "desk" / "drawer" / "tasks" / "task-drawer-provenance.md"
    _cli(
        root, "add", "task", "--root", str(root),
        "--title", "Drawer provenance",
        "--why", "w", "--goal", "g", "--scope", "s",
        "--implementation-path", "i", "--done-when", "d",
        "--from-drawer", "drawer-provenance",
        "--validation", "pytest",
    )
    assert _cli(root, "graph", "missing", "--root", str(root)).returncode == 0

    drawer_entry.unlink()

    missing = _cli(root, "graph", "missing", "--root", str(root), check=False)
    assert missing.returncode == 0, missing.stdout
    assert "task-drawer-provenance.md" not in missing.stdout
    shown = _cli(root, "show", "task", "task-drawer-provenance", "--root", str(root))
    assert "From drawer: desk/drawer/tasks/task-drawer-provenance.md" in shown.stdout
