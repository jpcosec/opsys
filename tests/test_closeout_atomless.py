"""Exercise atomless closeout against real repositories and the installed CLI."""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from test_closeout import _git, _make_repo, _write, _write_atom, _write_board, _write_task as _write_existing_task


def _write_task(root: Path, refs: list[str], files: list[str]) -> None:
    _write_existing_task(root, refs, files or ["seed.txt"])
    path = root / "desk/tasks/task-x.md"
    _, frontmatter, body = path.read_text().split("---", 2)
    payload = yaml.safe_load(frontmatter)
    payload["files"] = files
    path.write_text("---\n" + yaml.safe_dump(payload, sort_keys=False) + "---" + body)


def _cli(root: Path, command: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", "closeout", command,
         "--root", str(root), "--task", "task-x", *args],
        capture_output=True, text=True,
    )


def _repo(tmp_path: Path) -> tuple[Path, list[str]]:
    root = _make_repo(tmp_path)
    (root / "tests").mkdir()
    # Real regression source is resolvable evidence; no fake runtime/test stub.
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)
    refs = [f"tests/{Path(__file__).name}", _git(root, "rev-parse", "HEAD")]
    _write_task(root, refs, ["seed.txt"])
    return root, refs


def _verify(root: Path) -> dict:
    result = _cli(root, "verify")
    assert result.stdout.strip(), result.stderr
    report = json.loads(result.stdout)
    assert result.returncode == (0 if report["ok"] else 1), result.stderr
    return report


@pytest.mark.parametrize("layout", ["missing", "empty", "readme"])
@pytest.mark.parametrize("files", [[], ["seed.txt"]])
def test_atomless_coverage_is_optional(tmp_path: Path, layout: str, files: list[str]) -> None:
    root, refs = _repo(tmp_path)
    if layout != "missing":
        (root / "desk/atoms").mkdir()
    if layout == "readme":
        _write(root / "desk/atoms/README.md", "# Local atom guide\n")
        (root / "desk/atoms/atom-directory.md").mkdir()
    _write_task(root, refs, files)
    report = _verify(root)
    assert report["ok"]
    assert any("no local atom documents" in item for item in report["gates"]["atom_or_materialization_link"]["evidence"])


@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.parametrize("files,code", [([], "missing_atom_or_materialization_link"), (["seed.txt"], "missing_changed_file_link")])
def test_local_atoms_preserve_strict_coverage(tmp_path: Path, nested: bool, files: list[str], code: str) -> None:
    root, refs = _repo(tmp_path)
    _write_atom(root)
    if nested:
        target = root / "desk/atoms/domain/topic/atom-evidence.md"
        target.parent.mkdir(parents=True)
        (root / "desk/atoms/atom-evidence.md").rename(target)
    _write_task(root, refs, files)
    report = _verify(root)
    assert not report["ok"]
    assert code in {finding["code"] for finding in report["findings"]}


@pytest.mark.parametrize("missing", ["tests", "commit", "nonancestor"])
def test_atomless_desk_keeps_evidence_gates(tmp_path: Path, missing: str) -> None:
    root, refs = _repo(tmp_path)
    if missing == "tests":
        refs = refs[1:]
    elif missing == "commit":
        refs = refs[:1]
    else:
        _git(root, "checkout", "-q", "-b", "unmerged")
        _git(root, "commit", "--allow-empty", "-q", "-m", "not an ancestor")
        refs[1] = _git(root, "rev-parse", "HEAD")
        _git(root, "checkout", "-q", "HEAD~1")
    _write_task(root, refs, ["seed.txt"])
    _write_board(root)
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "route task")
    before = _git(root, "rev-parse", "HEAD")
    report = _verify(root)
    gate = "tests" if missing == "tests" else "commit"
    assert not report["gates"][gate]["ok"]
    result = _cli(root, "commit", "--no-run", "--reason", "CLI regression exercised directly", "--paths", "seed.txt")
    assert result.returncode == 1, result.stdout
    assert _git(root, "rev-parse", "HEAD") == before
    assert (root / "desk/tasks/task-x.md").exists()


def test_atomless_paths_and_generated_provenance_still_fail(tmp_path: Path) -> None:
    root, refs = _repo(tmp_path)
    _write(root / "docs/example.mmd", "flowchart TD\n    A-->B\n")
    _write(root / "docs/example.md", "# Example\n")
    _write_task(root, refs, ["../outside.txt", "docs/example.md"])
    report = _verify(root)
    codes = [finding["code"] for finding in report["findings"]]
    assert codes.count("changed_file_missing") == 1
    assert "generated_artifact_missing_declared_sources" in codes
    assert "missing_changed_file_link" not in codes
    _write(root / "docs/example.md", "---\nprovenance: docs/example.mmd\n---\n# Example\n")
    _write_task(root, refs, ["docs/example.md"])
    assert _verify(root)["ok"]


def test_atomless_board_routed_task_closes_with_one_commit(tmp_path: Path) -> None:
    root, _refs = _repo(tmp_path)
    _write_board(root)
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "route task")
    before = _git(root, "rev-parse", "HEAD")
    result = _cli(root, "commit", "--no-run", "--reason", "CLI regression exercised directly", "--paths", "seed.txt")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _git(root, "rev-list", "--count", f"{before}..HEAD") == "1"
    assert "Task-Id: task-x" in _git(root, "log", "-1", "--format=%B")
    assert not (root / "desk/tasks/task-x.md").exists()
    assert "desk/tasks/task-x.md" not in (root / "desk/tasks/Board.md").read_text()
    assert _git(root, "status", "--porcelain") == ""
