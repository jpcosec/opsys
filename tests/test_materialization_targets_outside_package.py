"""Tests for materialization targets outside the indexed package.

These tests verify that MaterializationContractDoc.target_identity values pointing
to repo-relative paths outside desk/ and deskops/ become source_file graph nodes.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))


def _git(root: Path, *argv: str) -> str:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "deskops", *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )


def _sldb_cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", *argv],
        cwd=root,
        capture_output=True,
        text=True,
    )


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    (root / "seed.txt").write_text("seed\n", encoding="utf-8")
    (root / ".gitignore").write_text(".deskops.log\n", encoding="utf-8")
    _git(root, "add", "seed.txt", ".gitignore")
    _git(root, "commit", "-q", "-m", "seed")
    return root


# --- Graph missing tests ---


def test_declared_target_outside_package_becomes_graph_node(tmp_path: Path) -> None:
    """A materialization target outside desk/ and deskops/ becomes a source_file node."""
    root = _make_repo(tmp_path)

    # Initialize deskops
    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create real target files
    _write(root / "src/vsm/organs/links.py", "# Source\n")
    _write(root / ".github/workflows/pulse.yml", "name: Pulse\n")

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "CI/CD workflow",
        "--five-wh-one-plus", "how",
        "--answer", "The CI/CD workflow is defined by the pulse and ci YAML files.",
        "--tags", "topic:ci",
    )
    assert result.returncode == 0, result.stderr

    # Create materializations pointing to those files
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Links implementation",
        "--source-atoms", "atom-ci-cd-workflow",
        "--target-kind", "source_file",
        "--target-identity", "src/vsm/organs/links.py",
        "--intent", "The links module implements the CI/CD workflow.",
    )
    assert result.returncode == 0, result.stderr

    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Pulse workflow",
        "--source-atoms", "atom-ci-cd-workflow",
        "--target-kind", "config_file",
        "--target-identity", ".github/workflows/pulse.yml",
        "--intent", "The pulse workflow defines CI/CD.",
    )
    assert result.returncode == 0, result.stderr

    # graph missing should exit 0 (no missing targets)
    result = _cli(root, "graph", "missing", "--root", str(root))
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"


def test_declared_target_missing_file_stays_missing(tmp_path: Path) -> None:
    """A materialization target pointing to a nonexistent file is missing_declared_target."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Missing file test",
        "--five-wh-one-plus", "what",
        "--answer", "Test for missing target.",
        "--tags", "topic:test",
    )
    assert result.returncode == 0, result.stderr

    # Create a materialization pointing to a nonexistent file
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Missing target",
        "--source-atoms", "atom-missing-file-test",
        "--target-kind", "source_file",
        "--target-identity", "src/missing.py",
        "--intent", "This target does not exist.",
    )
    assert result.returncode == 0, result.stderr

    # graph missing should exit 1 with missing_declared_target
    result = _cli(root, "graph", "missing", "--root", str(root))
    assert result.returncode == 1, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    assert "missing_declared_target" in result.stdout
    assert "src/missing.py" in result.stdout


# --- Materialization tracking tests ---


def test_add_materialization_tracks_document_in_store(tmp_path: Path) -> None:
    """deskops add materialization tracks the created document in the .sldb store."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create an atom first
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Tracking test atom",
        "--five-wh-one-plus", "what",
        "--answer", "Test for store tracking.",
        "--tags", "topic:test",
    )
    assert result.returncode == 0, result.stderr

    # Create a target file
    _write(root / "src/tracked.py", "# Source\n")

    # Create a materialization
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Tracked materialization",
        "--source-atoms", "atom-tracking-test-atom",
        "--target-kind", "source_file",
        "--target-identity", "src/tracked.py",
        "--intent", "Test that materializations are tracked.",
    )
    assert result.returncode == 0, result.stderr

    # Check store tracking with sldb stores check
    result = _sldb_cli(root, "stores", "check", "--store", str(root / ".sldb"), "--format", "json")
    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"

    check_data = json.loads(result.stdout)
    models = check_data.get("models", [])

    # Find MaterializationContractDoc in models
    materialization_model = next(
        (m for m in models if m.get("name") == "MaterializationContractDoc"),
        None,
    )
    assert materialization_model is not None, f"MaterializationContractDoc not found in {models}"

    # The materialization should be tracked
    documents = materialization_model.get("documents", [])
    assert any(
        "materialization-tracked-materialization" in str(doc)
        for doc in documents
    ), f"Materialization not tracked: {documents}"


# --- Closeout tests ---


def test_closeout_verify_accepts_materialization_coverage(tmp_path: Path) -> None:
    """closeout verify accepts materializations as changed-file coverage."""
    root = _make_repo(tmp_path)

    result = _cli(root, "init", str(root))
    assert result.returncode == 0, result.stderr

    # Create target files
    _write(root / "src/vsm/organs/links.py", "# Links source\n")
    _write(root / ".github/workflows/pulse.yml", "name: Pulse\n")

    # Create an atom
    result = _cli(
        root,
        "add", "atom",
        "--root", str(root),
        "--title", "Closeout test atom",
        "--five-wh-one-plus", "how",
        "--answer", "Atom for closeout verification.",
        "--tags", "topic:closeout",
    )
    assert result.returncode == 0, result.stderr

    # Create materializations for those files
    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Links materialization",
        "--source-atoms", "atom-closeout-test-atom",
        "--target-kind", "source_file",
        "--target-identity", "src/vsm/organs/links.py",
        "--intent", "Links implementation materialization.",
    )
    assert result.returncode == 0, result.stderr

    result = _cli(
        root,
        "add", "materialization",
        "--root", str(root),
        "--title", "Pulse materialization",
        "--source-atoms", "atom-closeout-test-atom",
        "--target-kind", "config_file",
        "--target-identity", ".github/workflows/pulse.yml",
        "--intent", "Pulse workflow materialization.",
    )
    assert result.returncode == 0, result.stderr

    # Create a task that lists those files
    _write(
        root / "desk/tasks/task-closeout-test.md",
        """---
id: task-closeout-test
status: active
references:
- tests/test_materialization_targets_outside_package.py
depends_on: []
pills: []
files:
- src/vsm/organs/links.py
- .github/workflows/pulse.yml
tags: []
---

# Closeout Test Task

## Rationale

Test closeout verification.

## Goal

Verify closeout works.

## Scope

In scope.

## Implementation Path

Implement.

## Validation

- pytest

## Done When

Done.
""",
    )

    # Create board
    _write(
        root / "desk/tasks/Board.md",
        """---
id: Board
title: Board
scope: test
purpose: test
tasks:
- desk/tasks/task-closeout-test.md
tags: []
---

# Board
""",
    )

    # Commit everything so we have a commit reference
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "setup closeout test")
    commit_sha = _git(root, "rev-parse", "HEAD")

    # Add commit to task references
    _write(
        root / "desk/tasks/task-closeout-test.md",
        f"""---
id: task-closeout-test
status: active
references:
- tests/test_materialization_targets_outside_package.py
- {commit_sha}
depends_on: []
pills: []
files:
- src/vsm/organs/links.py
- .github/workflows/pulse.yml
tags: []
---

# Closeout Test Task

## Rationale

Test closeout verification.

## Goal

Verify closeout works.

## Scope

In scope.

## Implementation Path

Implement.

## Validation

- pytest

## Done When

Done.
""",
    )

    # Copy test file as evidence
    import shutil
    (root / "tests").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)

    # Commit the task update
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", "add commit reference")

    # closeout verify should have no missing_changed_file_link
    result = _cli(
        root,
        "closeout", "verify",
        "--root", str(root),
        "--task", "task-closeout-test",
    )
    output = json.loads(result.stdout)

    # Check that there's no missing_changed_file_link finding
    findings = output.get("findings", [])
    missing_link_findings = [
        f for f in findings
        if f.get("code") == "missing_changed_file_link"
    ]
    assert not missing_link_findings, f"Unexpected missing_changed_file_link: {missing_link_findings}"
