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
    assert entry["commit"] == commit
    assert entry["run_id"] == "6046eaef"
    assert entry["task_id"] == "task-x"

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
