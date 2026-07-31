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
