"""``deskops review record``: reproduction, goldens and owner receipts without a model call.

Follow-up of CC32 (decisions r1-r8, precisions b1-b4 of the TaskDoc). The receipt is written
by whoever operates the desk with the evidence they checked: ``verdict: pending``,
``engine: human``, ``actor`` from the desk identity, ``input_sha256`` over the sorted evidence
(b1) and the evidence paths in ``summary`` (b4). ``deskops review dispose`` gives the verdict.
A ``pi`` that only logs its calls is first on ``PATH``, so a test would see a model call.
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.api import check_doc_anchors
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SHA256 = re.compile(r"^[0-9a-f]{64}$")

LOGGING_PI = """#!/usr/bin/env python3
import os
import sys

with open(os.environ["FAKE_PI_LOG"], "a", encoding="utf-8") as handle:
    handle.write(" ".join(sys.argv[1:]) + "\\n")
sys.exit(1)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return env


def _deskops(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*CLI, *argv, "--root", str(root)], cwd=root, env=_env(), capture_output=True, text=True
    )


@pytest.fixture
def pi_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(LOGGING_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return log


@pytest.fixture
def desk(lifecycle_desk: Path, pi_log: Path) -> Path:
    result = _deskops(
        lifecycle_desk,
        "add",
        "task",
        "--title",
        "X",
        "--goal",
        "record goal",
        "--scope",
        "record scope",
        "--validation",
        "pytest",
        "--task-type",
        "task.code",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return lifecycle_desk


def _review_files(root: Path) -> list[Path]:
    reviews = root / "desk" / "reviews"
    return sorted(reviews.rglob("*.md")) if reviews.exists() else []


def _review(root: Path, review_id: str) -> dict:
    docs = [
        doc
        for doc in (extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")) for path in _review_files(root))
        if doc["id"] == review_id
    ]
    assert len(docs) == 1, review_id
    return docs[0]


def _evidence(root: Path, rel: str, text: str) -> str:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return rel


def test_reproduction_with_evidence_writes_a_pending_well_formed_receipt(desk: Path, pi_log: Path) -> None:
    root = desk
    b = _evidence(root, "runs/repro/b.log", "second\n")
    a = _evidence(root, "runs/repro/a.log", "first\n")

    result = _deskops(
        root,
        "review",
        "record",
        "task-x",
        "--kind",
        "reproduction",
        "--evidence",
        b,
        "--evidence",
        a,
        "--evidence",
        str(root / b),  # the same file again, absolute: counted once (b1)
        "--reason",
        "reproduced on main",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "review: review-task-x-reproduction-1" in result.stdout

    doc = _review(root, "review-task-x-reproduction-1")
    expected = hashlib.sha256(
        b"runs/repro/a.log\nfirst\n" + b"\n" + b"runs/repro/b.log\nsecond\n" + b"\n"
    ).hexdigest()
    assert doc["kind"] == "reproduction"
    assert doc["verdict"] == "pending"
    assert doc["engine"] == "human"
    assert doc["actor"] == "repo"
    assert doc["reason"] == "reproduced on main"
    assert doc["run_dir"] == ""
    assert doc["output_sha256"] == ""
    assert doc["input_sha256"] == expected
    assert doc["summary"] == "reproduction receipt recorded by repo; evidence: runs/repro/a.log, runs/repro/b.log"
    assert doc["disposed_at"] == "" and doc["disposed_by"] == ""
    assert doc["subject_ref"] == ""
    assert (root / "desk" / "reviews" / "task-x" / "reproduction-1.md").is_file()
    assert not (root / "runs" / "subagents").exists()
    assert not pi_log.exists()


def test_goldens_with_evidence_is_numbered_by_its_kind(desk: Path) -> None:
    root = desk
    rel = _evidence(root, "tests/fixtures/golden/out.txt", "golden\n")
    result = _deskops(root, "review", "record", "task-x", "--kind", "goldens", "--evidence", rel, "--reason", "goldens unchanged")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review(root, "review-task-x-goldens-1")
    assert doc["kind"] == "goldens"
    assert SHA256.match(doc["input_sha256"])


@pytest.mark.parametrize("kind", ["preflight", "bundle", "node"])
def test_model_kinds_are_refused_and_nothing_is_written(desk: Path, pi_log: Path, kind: str) -> None:
    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(root, "review", "record", "task-x", "--kind", kind, "--evidence", rel, "--reason", "r")
    assert result.returncode == 2
    assert "invalid choice" in result.stderr
    assert _review_files(root) == []
    assert not pi_log.exists()


@pytest.mark.parametrize("kind", ["reproduction", "goldens"])
def test_reproduction_and_goldens_require_evidence(desk: Path, kind: str) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", kind, "--reason", "no evidence")
    assert result.returncode == 2
    assert f"--kind {kind} requires at least one --evidence" in result.stdout
    assert _review_files(root) == []


def test_missing_evidence_fails_without_writing(desk: Path) -> None:
    root = desk
    good = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(
        root, "review", "record", "task-x", "--kind", "reproduction",
        "--evidence", good, "--evidence", "runs/repro/missing.log", "--reason", "r",
    )
    assert result.returncode == 1
    assert "Error: evidence not found: runs/repro/missing.log" in result.stdout
    assert _review_files(root) == []


@pytest.mark.parametrize("where", ["dotdot", "absolute", "symlink", "directory"])
def test_evidence_outside_the_root_or_not_a_file_fails_without_writing(desk: Path, tmp_path: Path, where: str) -> None:
    root = desk
    outside = tmp_path / "outside.log"
    outside.write_text("outside\n", encoding="utf-8")
    if where == "dotdot":
        ref = "../outside.log"
    elif where == "absolute":
        ref = str(outside)
    elif where == "symlink":
        (root / "runs").mkdir(exist_ok=True)
        (root / "runs" / "link.log").symlink_to(outside)
        ref = "runs/link.log"
    else:
        (root / "runs" / "dir").mkdir(parents=True)
        ref = "runs/dir"
    result = _deskops(root, "review", "record", "task-x", "--kind", "goldens", "--evidence", ref, "--reason", "r")
    assert result.returncode == 1
    assert f"Error: evidence not found: {ref}" in result.stdout
    assert _review_files(root) == []


def test_owner_without_evidence_records_the_reason_alone(desk: Path) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner", "--reason", "approved by the owner")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review(root, "review-task-x-owner-1")
    assert doc["kind"] == "owner"
    assert doc["verdict"] == "pending"
    assert doc["engine"] == "human"
    assert doc["input_sha256"] == ""
    assert doc["reason"] == "approved by the owner"
    assert doc["summary"] == "owner receipt recorded by repo; evidence: (none)"


def test_record_requires_a_reason(desk: Path) -> None:
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner")
    assert result.returncode == 2
    assert _review_files(root) == []


def test_dispose_accepts_a_recorded_receipt(desk: Path) -> None:
    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    assert _deskops(root, "review", "record", "task-x", "--kind", "reproduction", "--evidence", rel, "--reason", "r").returncode == 0

    disposed = _deskops(
        root, "review", "dispose", "review-task-x-reproduction-1", "--verdict", "accepted", "--reason", "reproduction checked",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    doc = _review(root, "review-task-x-reproduction-1")
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "reproduction checked"
    assert doc["disposed_at"]
    assert doc["disposed_by"] == "repo"
    assert doc["engine"] == "human"


def test_subject_is_pinned_and_the_anchor_is_intact(desk: Path) -> None:
    """sldb pins `__doc_anchors__` on save (`save_document_payload`), not on
    `create_document`: the recorded receipt carries the bare anchor, like every other
    receipt, and the disposition write pins it against the task's contract."""
    root = desk
    result = _deskops(root, "review", "record", "task-x", "--kind", "owner", "--reason", "approved")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _review(root, "review-task-x-owner-1")["subject"] == "doc:TaskCodeDoc:task-x"

    disposed = _deskops(root, "review", "dispose", "review-task-x-owner-1", "--verdict", "accepted", "--reason", "ok")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    doc = _review(root, "review-task-x-owner-1")
    assert re.fullmatch(r"doc:TaskCodeDoc:task-x@sha256:[0-9a-f]{64}", doc["subject"]), doc["subject"]

    findings = check_doc_anchors(root / ".sldb", pythonpath=str(ROOT))
    assert [f for f in findings if f.subject.endswith("review-task-x-owner-1")] == []


def test_json_output_reports_the_receipt(desk: Path) -> None:
    import json

    root = desk
    rel = _evidence(root, "runs/repro/a.log", "first\n")
    result = _deskops(
        root, "review", "record", "task-x", "--kind", "reproduction", "--evidence", rel, "--reason", "r", "--format", "json",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    payload = data.get("data", data)
    assert payload["review_id"] == "review-task-x-reproduction-1"
    assert payload["evidence"] == ["runs/repro/a.log"]
