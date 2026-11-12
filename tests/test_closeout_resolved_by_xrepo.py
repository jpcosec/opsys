"""``deskops closeout resolved-by`` with references qualified by a registered repository.

A task.code of one desk whose code entered another repository closes with
``--ref <repo-id>:<sha>`` and ``--test <repo-id>:<test path>``, checked in the root that
the desk's own registry (``desk/registry/repo-*.md``, written by ``deskops repo register``)
gives that repository.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.bootstrap import SLDBBootstrap
from deskops.cli.main import main

DESK_ID = "governance"
OTHER_ID = "infra"
OTHER_TEST = "tests/test_infra.py"
LOCAL_TEST = "tests/test_thing.py"
PR_URL = "https://github.com/example/infra/pull/7"


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _init_git(root: Path) -> None:
    root.mkdir(parents=True)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")


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

TASK = """---
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
files:
- infra/declared_check.py
- checks/check_thing.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task X

## Rationale

The code entered the infra repository.

## Goal

Close it from the governance desk.

## Scope

Stay scoped.

## Implementation Path

Already merged in infra.

## Validation

- pytest

## Done When

Closed.
"""


@pytest.fixture
def ecosystem(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    """A desk repo (governance) and the repo its task's code entered (infra), registered with the CLI."""
    monkeypatch.setattr("deskops.cli.main.SLDBBootstrap.ensure_sldb_available", lambda self: 0)

    other = tmp_path / "infra"
    _init_git(other)
    _write(other / "src" / "infra.py", "VALUE = 1\n")
    _write(other / OTHER_TEST, "def test_infra():\n    assert True\n")
    _write(other / "declared_check.py", "def test_declared():\n    assert True\n")
    _git(other, "add", "src", "tests", "declared_check.py")
    _git(other, "commit", "-q", "-m", "infra work")
    work = _git(other, "rev-parse", "HEAD")
    _git(other, "checkout", "-q", "-b", "side")
    _write(other / "src" / "side.py", "SIDE = 1\n")
    _git(other, "add", "src/side.py")
    _git(other, "commit", "-q", "-m", "not merged")
    side = _git(other, "rev-parse", "HEAD")
    _git(other, "checkout", "-q", "-")

    desk = tmp_path / "governance"
    _init_git(desk)
    _write(desk / ".gitignore", ".deskops.log\n")
    _write(desk / "pkg" / "thing.py", "VALUE = 1\n")
    _write(desk / LOCAL_TEST, "def test_thing():\n    assert True\n")
    _write(desk / "checks" / "check_thing.py", "def test_check():\n    assert True\n")
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(desk) == 0
    _write(desk / "desk" / "config.json", json.dumps({"project_identity": DESK_ID}, indent=2) + "\n")
    store = str(desk / ".sldb")
    gone = tmp_path / "gone"
    with contextlib.redirect_stdout(io.StringIO()):
        assert main(["repo", "register", OTHER_ID, "--path", str(other), "--id", OTHER_ID, "--store", store]) == 0
        assert main(["repo", "register", "gone", "--path", str(gone), "--id", "gone", "--store", store]) == 0
    assert (desk / "desk" / "registry" / f"repo-{OTHER_ID}.md").is_file()
    _git(desk, "add", "-A")
    _git(desk, "commit", "-q", "-m", "desk with its registry")
    local = _git(desk, "rev-parse", "HEAD")
    _write(desk / "desk" / "tasks" / "Board.md", BOARD)
    _write(desk / "desk" / "tasks" / "task-x.md", TASK)
    _git(desk, "add", "desk/tasks")
    _git(desk, "commit", "-q", "-m", "add task and board")
    return {"desk": desk, "other": other, "work": work, "side": side, "local": local, "gone": gone}


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


def _refuses(desk: Path, capsys: pytest.CaptureFixture[str], *argv: str) -> str:
    before = _snapshot(desk)
    rc = _resolved_by(desk, "--reason", "Merged in infra", *argv)
    out = capsys.readouterr().out
    assert rc == 1, out
    assert _snapshot(desk) == before
    assert (desk / "desk" / "tasks" / "task-x.md").is_file()
    return out


def test_resolved_by_closes_with_a_commit_and_a_test_of_another_registered_repo(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    ref = f"{OTHER_ID}:{str(ecosystem['work'])[:8]}"
    test = f"{OTHER_ID}:{OTHER_TEST}::test_infra"
    head_before = _git(desk, "rev-parse", "HEAD")

    rc = _resolved_by(desk, "--reason", "Merged in infra", "--ref", ref, "--ref", PR_URL, "--test", test)

    out = capsys.readouterr().out
    assert rc == 0, out
    assert "resolved-by mode: Merged in infra" in out
    assert _git(desk, "rev-parse", "HEAD~1") == head_before
    message = _git(desk, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "resolved-by"
    refs = _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Ref,valueonly)").splitlines()
    assert refs == [ref, PR_URL]
    tests = _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Test,valueonly)").splitlines()
    assert tests == [test]
    assert not (desk / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (desk / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    entry = json.loads((desk / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry["mode"] == "resolved-by"
    assert _git(desk, "status", "--porcelain") == ""


def test_resolved_by_mixes_a_local_and_a_qualified_reference(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    local = str(ecosystem["local"])
    ref = f"{OTHER_ID}:{ecosystem['work']}"

    rc = _resolved_by(
        desk, "--reason", "Split work", "--ref", local, "--ref", ref,
        "--test", LOCAL_TEST, "--test", f"{OTHER_ID}:{OTHER_TEST}",
    )

    assert rc == 0, capsys.readouterr().out
    refs = _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Ref,valueonly)").splitlines()
    assert refs == [local, ref]


def test_resolved_by_treats_the_desk_own_identity_prefix_as_local(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    ref = f"{DESK_ID}:{ecosystem['local']}"
    test = f"{DESK_ID}:checks/check_thing.py"

    rc = _resolved_by(desk, "--reason", "Merged here", "--ref", ref, "--test", test)

    assert rc == 0, capsys.readouterr().out
    assert _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Ref,valueonly)") == ref
    assert _git(desk, "log", "-1", "--format=%(trailers:key=Closeout-Test,valueonly)") == test


def test_resolved_by_refuses_a_sha_that_is_not_an_ancestor_of_the_other_head(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    side = f"{OTHER_ID}:{ecosystem['side']}"

    out = _refuses(desk, capsys, "--ref", side, "--test", f"{OTHER_ID}:{OTHER_TEST}")

    assert f"Unresolvable --ref: {side}" in out


def test_resolved_by_refuses_a_local_sha_qualified_by_the_other_repo(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    ref = f"{OTHER_ID}:{ecosystem['local']}"

    out = _refuses(desk, capsys, "--ref", ref, "--test", LOCAL_TEST)

    assert f"Unresolvable --ref: {ref}" in out


@pytest.mark.parametrize(
    "test",
    [
        f"{OTHER_ID}:tests/test_missing.py",
        f"{OTHER_ID}:src/infra.py",
        # The task's files widen where tests live in the desk's repo only.
        f"{OTHER_ID}:declared_check.py",
        # A path that leaves the other repo's root is not its test.
        f"{OTHER_ID}:../governance/{LOCAL_TEST}",
    ],
)
def test_resolved_by_refuses_a_test_the_other_repo_does_not_accept(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str], test: str
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)

    out = _refuses(desk, capsys, "--ref", f"{OTHER_ID}:{ecosystem['work']}", "--test", test)

    assert f"Unresolvable --test: {test}" in out


def test_resolved_by_treats_an_unregistered_prefix_as_local_and_fails_as_today(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str]
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    ref = f"nope:{ecosystem['work']}"
    test = f"nope:{OTHER_TEST}"

    out = _refuses(desk, capsys, "--ref", ref, "--test", LOCAL_TEST)
    assert f"Unresolvable --ref: {ref}" in out

    out = _refuses(desk, capsys, "--ref", str(ecosystem["local"]), "--test", test)
    assert f"Unresolvable --test: {test}" in out


@pytest.mark.parametrize("flag", ["--ref", "--test"])
def test_resolved_by_refuses_a_registered_root_missing_on_this_machine(
    ecosystem: dict[str, object], capsys: pytest.CaptureFixture[str], flag: str
) -> None:
    desk = ecosystem["desk"]
    assert isinstance(desk, Path)
    gone = ecosystem["gone"]
    if flag == "--ref":
        argv = ["--ref", f"gone:{ecosystem['work']}", "--test", LOCAL_TEST]
    else:
        argv = ["--ref", str(ecosystem["local"]), "--test", f"gone:{OTHER_TEST}"]

    out = _refuses(desk, capsys, *argv)

    assert f"Registered repository gone is not at {Path(str(gone)).resolve()} on this machine." in out
