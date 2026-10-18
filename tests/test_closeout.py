from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops.cli.commands.closeout import CloseoutCLI
from deskops.cli.main import main


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


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


def _make_run_dir(root: Path, name: str = "20260729-120000-task-x") -> Path:
    run_dir = root / "runs" / "subagents" / name
    run_dir.mkdir(parents=True)
    for fname in ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]:
        (run_dir / fname).write_text(f"{fname}\n", encoding="utf-8")
    return run_dir


def _args(root: Path, **overrides) -> SimpleNamespace:
    base = {
        "closeout_command": "commit",
        "root": str(root),
        "run_dir": "runs/subagents/20260729-120000-task-x",
        "task": "task-x",
        "message": None,
        "paths": None,
        "run_id": None,
        "session": None,
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_atom(root: Path, atom_id: str = "atom-evidence") -> None:
    _write(
        root / "desk" / "atoms" / f"{atom_id}.md",
        f"""---
id: {atom_id}
title: Evidence Atom
five_wh_one_plus: what
tags: []
provenance: null
---

# Evidence Atom

## Answer

Closeout evidence.
""",
    )


def _write_task(root: Path, references: list[str], files: list[str], *, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / f"{task_id}.md",
        f"""---
id: {task_id}
status: active
references:
{yaml.safe_dump(references, sort_keys=False).rstrip()}
depends_on: []
pills: []
files:
{yaml.safe_dump(files, sort_keys=False).rstrip()}
checklists: []
tags: []
---

# Task X

## Rationale

Not provided.

## Goal

Verify closeout.

## Scope

Stay scoped.

## Implementation Path

Implement verify.

## Validation

- pytest

## Done When

Verified.
""",
    )


def test_closeout_commit_links_commit_to_run(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    run_dir = _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    session = tmp_path / "session.jsonl"
    session.write_text('{"type":"session"}\n', encoding="utf-8")

    rc = CloseoutCLI().run(
        _args(
            root,
            paths=["feature.py"],
            run_id="6046eaef",
            session=str(session),
        )
    )

    assert rc == 0
    message = _git(root, "log", "-1", "--format=%B")
    assert "closeout: task-x" in message
    assert "Task-Id: task-x" in message
    assert "Run-Dir: runs/subagents/20260729-120000-task-x" in message
    assert "Run-Id: 6046eaef" in message
    assert "Session-Sha256:" in message

    commit = _git(root, "rev-parse", "HEAD")
    index = (root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").strip()
    entry = json.loads(index.splitlines()[-1])
    assert entry["commit"] is None
    assert entry["run_id"] == "6046eaef"
    assert entry["task_id"] == "task-x"
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == commit

    manifest = yaml.safe_load((run_dir / "run.yaml").read_text(encoding="utf-8"))
    assert manifest["run_id"] == "6046eaef"
    assert manifest["session_sha256"] == entry["session_sha256"]

    committed_files = _git(root, "show", "--name-only", "--format=", "HEAD").split()
    assert "feature.py" in committed_files
    assert "runs/subagents/20260729-120000-task-x/run.yaml" in committed_files


def test_closeout_commit_requires_evidence(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    run_dir = root / "runs" / "subagents" / "20260729-120000-task-x"
    run_dir.mkdir(parents=True)

    rc = CloseoutCLI().run(_args(root, paths=["feature.py"]))

    assert rc == 1


def test_closeout_commit_rejects_run_dir_outside_surface(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    elsewhere = root / "tmp" / "fake-run"
    elsewhere.mkdir(parents=True)
    for fname in ["board.txt", "task.txt", "git-status.txt", "result-summary.md"]:
        (elsewhere / fname).write_text("x\n", encoding="utf-8")

    rc = CloseoutCLI().run(_args(root, run_dir="tmp/fake-run", paths=["feature.py"]))

    assert rc == 1


def test_closeout_commit_uses_staged_index_without_paths(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    _git(root, "add", "feature.py")

    rc = CloseoutCLI().run(_args(root))

    assert rc == 0
    assert "closeout: task-x" in _git(root, "log", "-1", "--format=%B")


def _closeout_main(root: Path, *argv: str) -> int:
    return main(["closeout", "commit", "--root", str(root), "--task", "task-x", *argv])


def test_closeout_commit_no_run_makes_a_manual_commit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", "Fixed by the supervisor; no subagent ran", "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: manual" in message
    assert "Closeout-Reason: Fixed by the supervisor; no subagent ran" in message
    assert "Run-Dir:" not in message
    trailers = _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)")
    assert trailers == "manual", "Closeout-Mode must parse as a git trailer"

    commit = _git(root, "rev-parse", "HEAD")
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "manual",
    }
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == commit
    assert _git(root, "show", "--name-only", "--format=", "HEAD").split() == [
        "feature.py",
        "runs/subagents/index.jsonl",
    ]


@pytest.mark.parametrize("reason", [None, "", "   "])
def test_closeout_commit_no_run_requires_a_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], reason: str | None
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    extra = [] if reason is None else ["--reason", reason]
    rc = _closeout_main(root, "--no-run", *extra, "--paths", "feature.py")

    assert rc == 1
    assert "--no-run needs a non-empty --reason" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def test_closeout_commit_rejects_run_dir_and_no_run_together(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(
        root, "--run-dir", "runs/subagents/20260729-120000-task-x",
        "--no-run", "--reason", "r", "--paths", "feature.py",
    )
    assert rc == 2
    assert "argument --no-run: not allowed with argument --run-dir" in capsys.readouterr().err

    # Direct callers that bypass argparse get the same refusal.
    rc = CloseoutCLI().run(_args(root, no_run=True, reason="r", paths=["feature.py"]))
    assert rc == 1
    assert "either --run-dir or --no-run, not both" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_commit_without_a_route_names_both_routes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(root, "--paths", "feature.py")

    assert rc == 1
    out = capsys.readouterr().out
    assert "--run-dir" in out and "--no-run --reason" in out
    assert _git(root, "rev-parse", "HEAD") == head


@pytest.mark.parametrize(
    ("argv", "message"),
    [
        (["--no-run", "--reason", "r", "--run-id", "6046eaef"], "--run-id applies only to --run-dir"),
        (["--run-dir", "runs/subagents/20260729-120000-task-x", "--reason", "r"], "--reason applies only to --no-run"),
    ],
)
def test_closeout_commit_rejects_flags_from_the_other_route(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], argv: list[str], message: str
) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")
    head = _git(root, "rev-parse", "HEAD")

    rc = _closeout_main(root, *argv, "--paths", "feature.py")

    assert rc == 1
    assert message in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_commit_run_dir_through_main_is_unchanged(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _make_run_dir(root)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--run-dir", "runs/subagents/20260729-120000-task-x", "--paths", "feature.py")

    assert rc == 0
    message = _git(root, "log", "-1", "--format=%B")
    assert message == (
        "closeout: task-x\n\n"
        "Task-Id: task-x\n"
        "Run-Dir: runs/subagents/20260729-120000-task-x"
    )
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert set(entry) == {"task_id", "run_id", "run_dir", "commit", "session_sha256"}
    assert entry["run_dir"] == "runs/subagents/20260729-120000-task-x"
    assert entry["commit"] is None


@pytest.mark.parametrize("route", ["run-dir", "no-run"])
def test_closeout_commit_leaves_the_working_tree_clean(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], route: str
) -> None:
    root = _make_repo(tmp_path)
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    if route == "run-dir":
        _make_run_dir(root)
        rc = _closeout_main(root, "--run-dir", "runs/subagents/20260729-120000-task-x", "--paths", "feature.py")
    else:
        rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert _git(root, "status", "--porcelain") == ""
    assert _git(root, "ls-files", "runs/subagents/index.jsonl") == "runs/subagents/index.jsonl"
    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry["task_id"] == "task-x"
    assert entry["commit"] is None
    head = _git(root, "rev-parse", "HEAD")
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == head


def test_closeout_verify_passes_with_complete_evidence(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
            commit,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 0
    report = json.loads(out.out)
    assert report["ok"] is True
    assert report["gates"]["tests"]["ok"] is True
    assert report["gates"]["atom_or_materialization_link"]["ok"] is True
    assert report["gates"]["commit"]["ok"] is True


def test_closeout_verify_rejects_loose_commit_and_test_references(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    ancestor = _git(root, "rev-parse", "HEAD")
    _git(root, "commit", "--allow-empty", "-q", "-m", "later")
    _write_atom(root)
    _write(root / "deskops" / "x.py", "x = 1\n")
    _write(root / "tests" / "test_x.py", "def test_y():\n    assert True\n")
    _write_task(
        root,
        references=[
            "HEAD",
            "main",
            "deskops/x.py",
            str(root / "tests" / "test_x.py"),
            "tests/../deskops/x.py",
            ancestor,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert report["gates"]["tests"]["evidence"] == []
    assert report["gates"]["commit"]["evidence"] == [ancestor]


def test_closeout_verify_accepts_ancestor_commit_and_test_node(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    ancestor = _git(root, "rev-parse", "HEAD")
    _git(root, "commit", "--allow-empty", "-q", "-m", "later")
    _write_atom(root)
    _write(root / "tests" / "test_x.py", "def test_y():\n    assert True\n")
    _write_task(
        root,
        references=[
            "pytest tests/test_x.py::test_y",
            ancestor,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 0
    report = json.loads(out.out)
    assert report["gates"]["tests"]["evidence"] == ["pytest tests/test_x.py::test_y"]
    assert report["gates"]["commit"]["evidence"] == [ancestor]
    assert report["ok"] is True


def test_closeout_verify_fails_non_zero_when_required_gate_is_missing(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert report["ok"] is False
    assert report["gates"]["commit"]["ok"] is False
    assert report["findings"][0]["code"] == "missing_commit_evidence"


def test_closeout_verify_reports_structured_generated_artifact_findings(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_task(
        root,
        references=[
            "pytest tests/test_diagram.py::test_diagram",
            commit,
            "task:task-follow-up",
        ],
        files=["docs/diagrams/example.md"],
    )
    _write(
        root / "desk" / "tasks" / "task-follow-up.md",
        """---
id: task-follow-up
status: active
references: []
depends_on: []
pills: []
files: []
checklists: []
tags: []
---

# Task Follow Up

## Rationale

Not provided.

## Goal

Follow up.

## Scope

Scoped.

## Implementation Path

Route follow-up.

## Validation

- pytest

## Done When

Done.
""",
    )
    _write(root / "tests" / "test_diagram.py", "def test_diagram():\n    assert True\n")
    _write(root / "docs" / "diagrams" / "example.mmd", "flowchart TD\n    A-->B\n")
    _write(root / "docs" / "diagrams" / "example.md", "# Example\n")

    rc = main(["closeout", "verify", "--root", str(root), "--task", "task-x"])
    out = capsys.readouterr()

    assert rc == 1
    report = json.loads(out.out)
    assert set(report["gates"].keys()) == {"tests", "atom_or_materialization_link", "commit"}
    assert report["gates"]["tests"]["ok"] is True
    assert report["gates"]["commit"]["ok"] is True
    assert report["gates"]["atom_or_materialization_link"]["ok"] is False
    assert any(item["code"] == "generated_artifact_missing_declared_sources" for item in report["findings"])
    assert any("follow-up:task:task-follow-up -> docs/diagrams/example.md" == item for item in report["gates"]["atom_or_materialization_link"]["evidence"])


def test_closeout_verify_tolerates_multi_document_yaml(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_atom(root)
    _write_task(
        root,
        references=[
            "pytest tests/test_feature.py::test_feature",
            "desk/atoms/atom-evidence.md",
            commit,
        ],
        files=["desk/atoms/atom-evidence.md"],
    )
    _write(root / "tests" / "test_feature.py", "def test_feature():\n    assert True\n")
    # Graph extraction scans docs/ Markdown for fenced YAML blocks and spec/
    # YAML files for metadata. A block or file that holds several documents is
    # not evidence of atom declarations; verify must skip it, not abort.
    _write(
        root / "docs" / "vocabulario.md",
        "# Vocabulario\n\n```yaml\nname: uml-clases\n---\nname: glyph-interfaz\n```\n",
    )
    _write(root / "spec" / "vocabulario.yaml", "name: a\n---\nname: b\n")

    result = subprocess.run(
        [sys.executable, "-m", "deskops", "closeout", "verify", "--root", str(root), "--task", "task-x"],
        cwd=root,
        capture_output=True,
        text=True,
    )

    assert "Unexpected" not in result.stderr
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["ok"] is True


@pytest.mark.parametrize("committed", [False, True], ids=["new-task", "committed-task"])
def test_closeout_commit_accepts_a_directory_holding_the_task(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], committed: bool
) -> None:
    root = _make_repo(tmp_path)
    _write_task(root, references=[], files=[])
    if committed:
        _git(root, "add", "desk/tasks/task-x.md")
        _git(root, "commit", "-q", "-m", "add task")
    (root / "feature.py").write_text("x = 1\n", encoding="utf-8")

    rc = _closeout_main(root, "--no-run", "--reason", "no subagent ran", "--paths", "desk/tasks", "feature.py")

    assert rc == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert _git(root, "status", "--porcelain") == ""
    assert "feature.py" in _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()


def _write_board(root: Path, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / "Board.md",
        f"""---
id: board-tasks
scope: desk
tasks:
- desk/tasks/{task_id}.md
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
""",
    )


def _write_lifecycle_task(root: Path, task_id: str = "task-x") -> None:
    _write(
        root / "desk" / "tasks" / f"{task_id}.md",
        f"""---
id: {task_id}
status: active
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task X

## Rationale

The subject was removed.

## Goal

Close it honestly.

## Scope

Stay scoped.

## Implementation Path

Supersede it.

## Validation

- pytest

## Done When

Closed.
""",
    )


def _commit_task_on_board(root: Path, task_id: str = "task-x") -> None:
    _write_lifecycle_task(root, task_id)
    _write_board(root, task_id)
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "add task and board")


def _supersede_main(root: Path, *argv: str) -> int:
    return main(["closeout", "supersede", "--root", str(root), "--task", "task-x", *argv])


def test_closeout_supersede_closes_a_task_with_a_reason_and_commit_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    ref = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--reason", "The owner removed the subject", "--ref", ref)

    assert rc == 0, capsys.readouterr().out
    message = _git(root, "log", "-1", "--format=%B")
    assert message.splitlines()[0] == "closeout: task-x"
    assert "Task-Id: task-x" in message
    assert "Closeout-Mode: superseded" in message
    assert "Closeout-Reason: The owner removed the subject" in message
    assert f"Closeout-Ref: {ref}" in message
    assert _git(root, "log", "-1", "--format=%(trailers:key=Closeout-Mode,valueonly)") == "superseded"

    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (root / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert _git(root, "status", "--porcelain") == ""

    entry = json.loads((root / "runs" / "subagents" / "index.jsonl").read_text(encoding="utf-8").splitlines()[-1])
    assert entry == {
        "task_id": "task-x",
        "run_id": None,
        "run_dir": None,
        "commit": None,
        "session_sha256": None,
        "mode": "superseded",
    }
    assert _git(root, "log", "-1", "--format=%H", "--grep", "Task-Id: task-x") == _git(root, "rev-parse", "HEAD")
    assert sorted(_git(root, "show", "--name-only", "--format=", "HEAD").splitlines()) == [
        "desk/tasks/Board.md",
        "desk/tasks/task-x.md",
        "runs/subagents/index.jsonl",
    ]


def test_closeout_supersede_accepts_an_existing_path_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)

    rc = _supersede_main(root, "--reason", "subject path was deleted", "--ref", "desk/tasks/Board.md")

    assert rc == 0, capsys.readouterr().out
    assert not (root / "desk" / "tasks" / "task-x.md").exists()
    assert "Closeout-Ref: desk/tasks/Board.md" in _git(root, "log", "-1", "--format=%B")


@pytest.mark.parametrize("reason", ["", "   "])
def test_closeout_supersede_requires_a_reason(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], reason: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")
    ref = "desk/tasks/Board.md"

    rc = _supersede_main(root, "--reason", reason, "--ref", ref)

    assert rc == 1
    assert "Supersede needs a non-empty --reason" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").exists()
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


@pytest.mark.parametrize("ref", ["does-not-exist.txt", "deadbeef", "0" * 40])
def test_closeout_supersede_refuses_an_unresolvable_ref_and_leaves_the_tree_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], ref: str
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--reason", "subject removed", "--ref", ref)

    assert rc == 1
    assert "Unresolvable --ref" in capsys.readouterr().out
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""
    assert (root / "desk" / "tasks" / "task-x.md").read_text(encoding="utf-8").count("status: active") == 1
    assert not (root / "runs" / "subagents" / "index.jsonl").exists()


def test_closeout_supersede_requires_at_least_one_ref(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = main(["closeout", "supersede", "--root", str(root), "--task", "task-x", "--reason", "subject removed"])

    assert rc == 2
    assert "--ref" in capsys.readouterr().err
    assert _git(root, "rev-parse", "HEAD") == head


def test_closeout_supersede_requires_the_reason_flag(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _make_repo(tmp_path)
    _commit_task_on_board(root)
    head = _git(root, "rev-parse", "HEAD")

    rc = _supersede_main(root, "--ref", "desk/tasks/Board.md")

    assert rc == 2
    assert "--reason" in capsys.readouterr().err
    assert _git(root, "rev-parse", "HEAD") == head
