"""``deskops closeout resolved-by``: close a task whose work already entered the history."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService

PR_URL = "https://github.com/example/repo/pull/42"
TEST_REF = "tests/test_thing.py"


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


BOARD = """---
id: board-tasks
scope: desk
tasks:
- desk/tasks/task-x.md
pills: []
rituals: []
tags: []
---

# Repo Board

## Purpose

Route the active task.

## Notes

No additional notes.

## Task Details
"""


def _task(files: list[str]) -> str:
    files_yaml = "files: []" if not files else "files:\n" + "".join(f"- {entry}\n" for entry in files).rstrip("\n")
    return f"""---
id: task-x
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
{files_yaml}
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task X

## Rationale

The work entered main through a PR before the closeout.

## Goal

Close it honestly.

## Scope

Stay scoped.

## Implementation Path

Already merged.

## Validation

- pytest

## Done When

Closed.
"""


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """A git repo whose history already holds the task's work and its test."""
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _write(root / ".gitignore", ".deskops.log\n")
    _write(root / "pkg" / "thing.py", "VALUE = 1\n")
    _write(root / "pkg" / "other.py", "def test_other():\n    assert True\n")
    _write(root / TEST_REF, "def test_thing():\n    assert True\n")
    _write(root / "checks" / "check_thing.py", "def test_check():\n    assert True\n")
    _git(root, "add", ".gitignore", "pkg", "tests", "checks")
    _git(root, "commit", "-q", "-m", "work merged through the PR")
    _write(root / "desk" / "tasks" / "Board.md", BOARD)
    _write(root / "desk" / "tasks" / "task-x.md", _task(["pkg/thing.py", "checks/check_thing.py"]))
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add task and board")
    return root


def _work_commit(root: Path) -> str:
    return _git(root, "rev-parse", "HEAD~1")


def _resolved_by(root: Path, *argv: str) -> int:
    return main(["closeout", "resolved-by", "--root", str(root), "--task", "task-x", *argv])


def _snapshot(root: Path) -> tuple[str, str, str]:
    """sha256 over desk/ (paths and bytes), git status and HEAD."""
    digest = hashlib.sha256()
    for path in sorted(p for p in (root / "desk").rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8") + b"\0")
        digest.update(path.read_bytes() + b"\0")
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    return digest.hexdigest(), status, _git(root, "rev-parse", "HEAD")


def _capture_task_before_close(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Record the task file as the closing commit sees it, before it is removed."""
    seen: dict[str, str] = {}
    original = ClosureService._close

    def spy(self: ClosureService, task_id: str, **kwargs):  # type: ignore[no-untyped-def]
        seen["task"] = self._task_path(task_id).read_text(encoding="utf-8")
        seen["route"] = kwargs["route"]
        return original(self, task_id, **kwargs)

    monkeypatch.setattr(ClosureService, "_close", spy)
    return seen


def test_resolved_by_closes_with_an_ancestor_commit_and_an_accepted_test(
    repo: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    seen = _capture_task_before_close(monkeypatch)
    ref = _work_commit(repo)
    head_before = _git(repo, "rev-parse", "HEAD")

    rc = _resolved_by(repo, "--reason", "Merged through PR 42", "--ref", ref, "--test", TEST_REF)

    out = capsys.readouterr().out
    assert rc == 0, out
    assert "resolved-by mode: Merged through PR 42" in out

    assert seen["route"] == "resolved-by"
    assert "status: resolved" in seen["task"]
    assert "- resolved-by" in seen["task"]

    assert _git(repo, "rev-parse", "HEAD~1") == head_before
    message = _git(repo, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: resolved-by" in message
    assert "Closeout-Reason: Merged through PR 42" in message
    assert f"Closeout-Ref: {ref}" in message
    assert f"Closeout-Test: {TEST_REF}" in message
    assert _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "resolved-by"

    assert not (repo / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (repo / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(repo, "status", "--porcelain") == ""

    entry = json.loads((repo / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "resolved-by",
    }
    assert sorted(_git(repo, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def test_resolved_by_accepts_a_pr_url_as_an_additional_ref(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ref = _work_commit(repo)

    rc = _resolved_by(
        repo, "--reason", "Merged through PR 42", "--ref", ref, "--ref", PR_URL, "--test", TEST_REF
    )

    assert rc == 0, capsys.readouterr().out
    message = _git(repo, "log", "-1", "--format=%B")
    assert f"Closeout-Ref: {ref}" in message
    assert f"Closeout-Ref: {PR_URL}" in message
    refs = _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Ref,valueonly)").splitlines()
    assert refs == [ref, PR_URL]


def test_resolved_by_accepts_a_test_declared_in_the_task_files_and_several_tests(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = _resolved_by(
        repo,
        "--reason",
        "Merged through PR 42",
        "--ref",
        _work_commit(repo),
        "--test",
        TEST_REF,
        "--test",
        "checks/check_thing.py",
    )

    assert rc == 0, capsys.readouterr().out
    tests = _git(repo, "log", "-1", "--format=%(trailers:key=Closeout-Test,valueonly)").splitlines()
    assert tests == [TEST_REF, "checks/check_thing.py"]


def test_resolved_by_passes_paths_and_message_to_the_closing_commit(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _write(repo / "notes.txt", "closing note\n")

    rc = _resolved_by(
        repo,
        "--reason",
        "Merged through PR 42",
        "--ref",
        _work_commit(repo),
        "--test",
        TEST_REF,
        "--message",
        "closeout: work merged in PR 42",
        "--paths",
        "notes.txt",
    )

    assert rc == 0, capsys.readouterr().out
    assert _git(repo, "log", "-1", "--format=%s") == "closeout: work merged in PR 42"
    assert "notes.txt" in _git(repo, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert _git(repo, "status", "--porcelain") == ""


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        pytest.param(
            ["--reason", "Merged", "--ref", PR_URL, "--test", TEST_REF],
            "at least one --ref naming a commit",
            id="no-commit-ref-only-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--ref", "desk/tasks/Board.md", "--test", TEST_REF],
            "Unresolvable --ref: desk/tasks/Board.md",
            id="ref-is-a-path-not-commit-or-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "not-a-ref", "--test", TEST_REF],
            "Unresolvable --ref: not-a-ref",
            id="ref-is-neither-commit-nor-url",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "0" * 40, "--test", TEST_REF],
            "Unresolvable --ref",
            id="ref-is-an-unknown-commit",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", "tests/test_missing.py"],
            "Unresolvable --test: tests/test_missing.py",
            id="test-does-not-exist",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", "pkg/other.py"],
            "Unresolvable --test: pkg/other.py",
            id="test-is-not-a-test-location",
        ),
        pytest.param(
            ["--reason", "Merged", "--ref", "{commit}", "--test", TEST_REF, "--test", "tests/test_missing.py"],
            "Unresolvable --test: tests/test_missing.py",
            id="one-test-does-not-exist",
        ),
        pytest.param(
            ["--reason", "   ", "--ref", "{commit}", "--test", TEST_REF],
            "Resolved-by needs a non-empty --reason",
            id="blank-reason",
        ),
    ],
)
def test_resolved_by_refuses_and_writes_nothing(
    repo: Path, capsys: pytest.CaptureFixture[str], argv: list[str], expected: str
) -> None:
    commit = _work_commit(repo)
    argv = [commit if item == "{commit}" else item for item in argv]
    before = _snapshot(repo)

    rc = _resolved_by(repo, *argv)

    assert rc == 1
    assert expected in capsys.readouterr().out
    assert _snapshot(repo) == before
    assert not (repo / "runs").exists()


@pytest.mark.parametrize(
    ("argv", "flag"),
    [
        pytest.param(["--ref", "{commit}", "--test", TEST_REF], "--reason", id="no-reason"),
        pytest.param(["--reason", "Merged", "--test", TEST_REF], "--ref", id="no-ref"),
        pytest.param(["--reason", "Merged", "--ref", "{commit}"], "--test", id="no-test"),
    ],
)
def test_resolved_by_requires_reason_ref_and_test_flags(
    repo: Path, capsys: pytest.CaptureFixture[str], argv: list[str], flag: str
) -> None:
    commit = _work_commit(repo)
    argv = [commit if item == "{commit}" else item for item in argv]
    before = _snapshot(repo)

    rc = _resolved_by(repo, *argv)

    assert rc == 2
    assert flag in capsys.readouterr().err
    assert _snapshot(repo) == before


@pytest.mark.parametrize(
    ("refs", "tests", "expected"),
    [
        pytest.param(None, [TEST_REF], "at least one --ref naming a commit", id="service-no-refs"),
        pytest.param(["{commit}"], None, "at least one --test", id="service-no-tests"),
        pytest.param(["{commit}"], ["  "], "at least one --test", id="service-blank-test"),
    ],
)
def test_resolved_by_service_refuses_missing_evidence_and_writes_nothing(
    repo: Path, refs: list[str] | None, tests: list[str] | None, expected: str
) -> None:
    commit = _work_commit(repo)
    refs = None if refs is None else [commit if item == "{commit}" else item for item in refs]
    before = _snapshot(repo)

    outcome = ClosureService(repo, DeskopsOperations(repo)).close_resolved_by(
        "task-x", reason="Merged", refs=refs, tests=tests
    )

    assert outcome.exit_code == 1
    assert any(expected in line for line in outcome.messages)
    assert _snapshot(repo) == before


def test_resolved_by_refuses_an_unknown_task_and_writes_nothing(
    repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    before = _snapshot(repo)

    rc = main(
        [
            "closeout",
            "resolved-by",
            "--root",
            str(repo),
            "--task",
            "task-missing",
            "--reason",
            "Merged",
            "--ref",
            _work_commit(repo),
            "--test",
            TEST_REF,
        ]
    )

    assert rc == 1
    assert "Task not found: task-missing" in capsys.readouterr().out
    assert _snapshot(repo) == before
