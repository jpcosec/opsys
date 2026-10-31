"""Closeout evidence is declared when the task is created, and closeout checks exactly that.

Four classes of task (code, docs, spec/design, external), the legacy migration that
treats a task without the field as code, the never-silent .py alert, the
'esta tarea declaró X; encontré Y' line, and the add-task failure without a declaration.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from test_closeout import _git, _make_repo, _write, _write_board

CLI = [sys.executable, "-m", "deskops"]
TASK_ID = "task-x"
TASK_REL = f"desk/tasks/{TASK_ID}.md"
URL = "https://linear.app/example/issue/LIN-1"


def _write_declared_task(
    root: Path,
    *,
    evidence: list[str] | None,
    references: list[str],
    files: list[str],
) -> None:
    """A routed, committed task; `evidence=None` writes a task that predates the field."""
    payload: dict = {
        "id": TASK_ID,
        "status": "active",
        "references": references,
        "depends_on": [],
        "pills": [],
        "files": files,
        "tags": [],
    }
    if evidence is not None:
        payload["closeout_evidence"] = evidence
    _write(
        root / TASK_REL,
        "---\n" + yaml.safe_dump(payload, sort_keys=False) + "---\n\n# Task X\n\n"
        "## Rationale\n\nNot provided.\n\n## Goal\n\nClose.\n\n## Scope\n\nScoped.\n\n"
        "## Implementation Path\n\nDo it.\n\n## Validation\n\n- pytest\n\n## Done When\n\nClosed.\n",
    )
    _write_board(root, TASK_ID)
    _git(root, "add", "desk/tasks")
    _git(root, "commit", "-q", "-m", "route task")


def _cli(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*CLI, *argv, "--root", str(root)], cwd=root, capture_output=True, text=True)


def _verify(root: Path) -> tuple[dict, subprocess.CompletedProcess[str]]:
    result = _cli(root, "closeout", "verify", "--task", TASK_ID)
    assert result.stdout.strip(), result.stderr
    return json.loads(result.stdout), result


def _commit_no_run(root: Path, *paths: str) -> subprocess.CompletedProcess[str]:
    argv = ["closeout", "commit", "--task", TASK_ID, "--no-run", "--reason", "closed by the supervisor"]
    if paths:
        argv += ["--paths", *paths]
    return _cli(root, *argv)


# ---------------------------------------------------------------- external
def test_external_task_with_a_url_closes_with_no_run(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write_declared_task(root, evidence=["external"], references=[URL], files=[])

    report, result = _verify(root)
    assert report["ok"], report
    assert report["declared"] == ["external"]
    assert report["found"] == ["external"]
    assert set(report["gates"]) == {"external"}
    assert report["alerts"] == []
    assert "Closeout gate: esta tarea declaró external; encontré external" in result.stderr

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró external; encontré external" in closed.stdout
    assert not (root / TASK_REL).exists()
    message = _git(root, "log", "-1", "--format=%B")
    assert f"Task-Id: {TASK_ID}" in message and "Closeout-Mode: manual" in message


def test_external_task_without_a_url_stays_blocked(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write_declared_task(root, evidence=["external"], references=["not a url"], files=[])
    before = _git(root, "rev-parse", "HEAD")

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["found"] == []
    assert report["summary"] == "esta tarea declaró external; encontré nada"
    assert [item["code"] for item in report["findings"]] == ["missing_external_evidence"]

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 1
    assert "esta tarea declaró external; encontré nada" in closed.stdout
    assert _git(root, "rev-parse", "HEAD") == before
    assert (root / TASK_REL).exists()


# ---------------------------------------------------------------- code
def test_code_task_without_tests_stays_blocked(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write(root / "feature.py", "x = 1\n")
    commit = _git(root, "rev-parse", "HEAD")
    _write_declared_task(
        root, evidence=["tests", "commit", "atom", "materialization"], references=[commit], files=["feature.py"]
    )
    before = _git(root, "rev-parse", "HEAD")

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["declared"] == ["tests", "commit", "atom", "materialization"]
    assert "tests" not in report["found"] and "commit" in report["found"]
    assert not report["gates"]["tests"]["ok"]
    assert "missing_tests_evidence" in {item["code"] for item in report["findings"]}
    assert "esta tarea declaró tests, commit, atom|materialization; encontré " in report["summary"]

    closed = _commit_no_run(root, "feature.py", TASK_REL)
    assert closed.returncode == 1
    assert "missing_tests_evidence" in closed.stdout
    assert "esta tarea declaró tests, commit, atom|materialization" in closed.stdout
    assert _git(root, "rev-parse", "HEAD") == before


def test_code_task_with_declared_evidence_closes(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    (root / "tests").mkdir()
    shutil.copyfile(__file__, root / "tests" / Path(__file__).name)
    _write(root / "feature.py", "x = 1\n")
    _git(root, "add", "tests", "feature.py")
    _git(root, "commit", "-q", "-m", "feature")
    refs = [f"tests/{Path(__file__).name}", _git(root, "rev-parse", "HEAD")]
    _write_declared_task(root, evidence=["tests", "commit"], references=refs, files=["feature.py"])

    report, _ = _verify(root)
    assert report["ok"], report
    assert report["found"] == ["tests", "commit"]
    assert report["alerts"] == []

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró tests, commit; encontré tests, commit" in closed.stdout


def test_python_changes_without_declared_tests_alert_but_do_not_block(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    _write_declared_task(root, evidence=["commit"], references=[commit], files=["feature.py"])

    report, result = _verify(root)
    assert report["ok"], report
    assert set(report["gates"]) == {"commit"}
    assert [alert["code"] for alert in report["alerts"]] == ["python_changes_without_declared_tests"]
    assert "feature.py" in report["alerts"][0]["message"]
    assert "ALERTA python_changes_without_declared_tests" in result.stderr

    _write(root / "feature.py", "x = 1\n")
    closed = _commit_no_run(root, "feature.py", TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "ALERTA python_changes_without_declared_tests" in closed.stdout


def test_task_without_the_field_is_gated_as_code_with_an_alert(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write_declared_task(root, evidence=None, references=[], files=["seed.txt"])

    report, result = _verify(root)
    assert not report["ok"]
    assert report["implicit_code"] is True
    assert report["declared"] == ["tests", "commit", "atom", "materialization"]
    assert "closeout_evidence_not_declared" in {alert["code"] for alert in report["alerts"]}
    assert "ALERTA closeout_evidence_not_declared" in result.stderr
    assert "missing_tests_evidence" in {item["code"] for item in report["findings"]}


# ---------------------------------------------------------------- docs, spec, design
@pytest.mark.parametrize("suffix", ["docs", "spec", "design"])
def test_document_class_task_closes_with_commit_and_document(tmp_path: Path, suffix: str) -> None:
    root = _make_repo(tmp_path)
    _write(root / "docs" / f"{suffix}.md", f"# {suffix}\n")
    _git(root, "add", "docs")
    _git(root, "commit", "-q", "-m", suffix)
    refs = [_git(root, "rev-parse", "HEAD"), f"docs/{suffix}.md"]
    _write_declared_task(root, evidence=["commit", "document"], references=refs, files=[f"docs/{suffix}.md"])

    report, _ = _verify(root)
    assert report["ok"], report
    assert set(report["gates"]) == {"commit", "document"}
    assert report["found"] == ["commit", "document"]
    assert report["alerts"] == []

    closed = _commit_no_run(root, TASK_REL)
    assert closed.returncode == 0, closed.stdout + closed.stderr
    assert "esta tarea declaró commit, document; encontré commit, document" in closed.stdout


def test_document_task_without_a_document_stays_blocked(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    commit = _git(root, "rev-parse", "HEAD")
    # A test source and a missing path are not documents.
    _write(root / "tests" / "test_a.py", "")
    _write_declared_task(
        root, evidence=["commit", "document"], references=[commit, "tests/test_a.py", "docs/missing.md"], files=[]
    )

    report, _ = _verify(root)
    assert not report["ok"]
    assert report["found"] == ["commit"]
    assert [item["code"] for item in report["findings"]] == ["missing_document_evidence"]


def test_unknown_declared_evidence_is_a_finding(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _write_declared_task(root, evidence=["vibes"], references=[], files=[])

    report, _ = _verify(root)
    assert not report["ok"]
    assert "unknown_closeout_evidence" in {item["code"] for item in report["findings"]}


# ---------------------------------------------------------------- add task
@pytest.fixture
def desk_repo(lifecycle_desk: Path) -> Path:
    return lifecycle_desk


def _declared(root: Path, task_id: str) -> list[str]:
    frontmatter = (root / "desk" / "tasks" / f"{task_id}.md").read_text(encoding="utf-8").split("---", 2)[1]
    return yaml.safe_load(frontmatter).get("closeout_evidence") or []


def test_add_task_without_evidence_nor_task_type_fails_and_explains(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Undeclared")
    assert result.returncode == 1
    assert "--evidence" in result.stdout and "--task-type" in result.stdout
    assert "tests, commit, atom, materialization, document, external" in result.stdout
    assert not (desk_repo / "desk" / "tasks" / "task-undeclared.md").exists()


def test_add_task_with_an_unknown_task_type_and_no_evidence_fails(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Odd", "--task-type", "reflection")
    assert result.returncode == 1
    assert "reflection" in result.stdout and "--evidence" in result.stdout


def test_add_task_rejects_evidence_outside_the_vocabulary(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Bad", "--evidence", "vibes")
    assert result.returncode == 1
    assert "Unknown closeout evidence 'vibes'" in result.stdout


@pytest.mark.parametrize(
    "task_type,expected",
    [
        ("code", ["tests", "commit", "atom", "materialization"]),
        ("docs", ["commit", "document"]),
        ("spec", ["commit", "document"]),
        ("design", ["commit", "document"]),
        ("external", ["external"]),
    ],
)
def test_add_task_fills_evidence_from_task_type(desk_repo: Path, task_type: str, expected: list[str]) -> None:
    result = _cli(desk_repo, "add", "task", "--title", f"Typed {task_type}", "--task-type", task_type)
    assert result.returncode == 0, result.stdout + result.stderr
    assert _declared(desk_repo, f"task-typed-{task_type}") == expected


def test_explicit_evidence_wins_over_task_type(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Explicit", "--task-type", "code", "--evidence", "commit", "document")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _declared(desk_repo, "task-explicit") == ["commit", "document"]
    shown = _cli(desk_repo, "show", "task", "task-explicit")
    assert "Closeout evidence: commit, document" in shown.stdout


def test_add_task_with_evidence_alone_is_enough(desk_repo: Path) -> None:
    result = _cli(desk_repo, "add", "task", "--title", "Only evidence", "--evidence", "external")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _declared(desk_repo, "task-only-evidence") == ["external"]
