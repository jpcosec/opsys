"""GC02: ``ReviewDoc`` as a review receipt anchored to the reviewed document's contract.

Covers each Done When line of task-gc02: the model roundtrip, the closed ``kind`` and
``verdict`` vocabularies, the subject form and its exclusivity with ``subject_ref``, the
review subject registered for ``deskops edit review`` (where the verdict is refused and
written by ``deskops review dispose`` instead), the receipt tracked as
``ReviewDoc:<id>`` in a temporary desk, ``desk/reviews/`` created by ``init`` and
``desk update``, and the ``sldb edges show`` anchor link that stays an ``xfail`` until
sldb GO07 treats ``__doc_anchors__`` as references (``G_SLDB_ANCHORS``).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError
from sldb.api import doc_status
from sldb.api import track_document_file
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
SLDB = [sys.executable, "-m", "sldb"]


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return env


def _run(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [*argv], cwd=root, env=_env(), capture_output=True, text=True
    )


def _deskops(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root))


def _sldb(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    return _run(root, *SLDB, *argv)


def _init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    result = _run(root, *CLI, "init", str(root))
    assert result.returncode == 0, result.stdout + result.stderr


def _payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": "review-task-x-preflight-1",
        "title": "Preflight of task-x",
        "kind": "preflight",
        "subject": "doc:TaskCodeDoc:task-x",
        "subject_ref": "",
        "engine": "pi",
        "actor": "robocop2",
        "run_dir": "runs/subagents/20260101-preflight/context-review/task-x/abc/attempt-1",
        "input_sha256": "a" * 64,
        "output_sha256": "b" * 64,
        "verdict": "pending",
        "reason": "",
        "created_at": "2026-01-01T00:00:00Z",
        "disposed_at": "",
        "disposed_by": "",
        "summary": "Reviewed only the task document.",
        "disposition": "No disposition yet.",
        "tags": ["workspace:desk"],
    }
    payload.update(overrides)
    return payload


def _write_review(root: Path, **overrides: object) -> Path:
    payload = _payload(**overrides)
    review_id = str(payload["id"])
    kind = str(payload["kind"])
    task_id = "task-x"
    path = root / "desk" / "reviews" / task_id / f"{kind}-1.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_model_markdown(ReviewDoc, payload) + "\n", encoding="utf-8")
    track_document_file(root / ".sldb", "ReviewDoc", path, name=review_id, pythonpath=str(ROOT), force=True)
    return path


# ------------------------------------------------------------------ model
def test_review_doc_roundtrips_a_payload() -> None:
    payload = _payload()
    expected = ReviewDoc(**payload).model_dump()
    rendered = render_model_markdown(ReviewDoc, payload)
    extracted = extract_model_data(ReviewDoc, rendered)

    assert ReviewDoc(**extracted).model_dump() == expected
    assert getattr(ReviewDoc, "__doc_anchors__") == ["subject"]
    assert "subject" not in getattr(ReviewDoc, "__references__")


def test_review_kind_outside_the_closed_vocabulary_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(kind="cold-bundle"))
    assert "kind" in str(excinfo.value)


def test_review_accepted_without_reason_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(verdict="accepted", reason="", disposed_by="robocop2"))
    assert "reason" in str(excinfo.value)


def test_review_subject_without_the_doc_prefix_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(subject="task-x", subject_ref=""))
    assert "subject" in str(excinfo.value)


def test_review_subject_with_doc_prefix_validates() -> None:
    review = ReviewDoc(**_payload(subject="doc:TaskCodeDoc:task-x", subject_ref=""))
    assert review.subject == "doc:TaskCodeDoc:task-x"

    pinned = ReviewDoc(**_payload(subject=f"doc:TaskCodeDoc:task-x@sha256:{'c' * 64}"))
    assert pinned.subject.endswith("@" + "sha256:" + "c" * 64)


def test_review_plan_node_subject_ref_is_the_alternative_to_subject() -> None:
    review = ReviewDoc(
        **_payload(subject="", subject_ref="desk/drawer/plans/gates-por-tipo/dag.yaml#node:GC02")
    )
    assert review.subject == ""
    assert review.subject_ref.endswith("#node:GC02")

    with pytest.raises(ValidationError):
        ReviewDoc(**_payload(subject="doc:TaskCodeDoc:task-x", subject_ref="plan/dag.yaml#node:GC02"))


# ------------------------------------------------------------------ desk
def test_review_doc_is_tracked_as_review_doc_in_a_temporary_desk(lifecycle_desk: Path) -> None:
    root = lifecycle_desk

    path = _write_review(root)

    status = doc_status(root / ".sldb", "ReviewDoc/review-task-x-preflight-1")
    assert status.exists
    assert status.model == "ReviewDoc"
    assert status.path and path.resolve() == (root / status.path).resolve()

    shown = _sldb(root, "find", "review-task-x-preflight-1", "--in", "physical", "--type", "doc", "--store", ".sldb", "--format", "json")
    assert shown.returncode == 0, shown.stdout + shown.stderr
    results = json.loads(shown.stdout)["results"]
    assert [(item["name"], item["model"]) for item in results] == [
        ("review-task-x-preflight-1", "ReviewDoc")
    ]


def test_init_creates_the_reviews_directory(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    _init(root)
    assert (root / "desk" / "reviews").is_dir()


def test_desk_update_recreates_the_reviews_directory(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    assert (root / "desk" / "reviews").is_dir()

    (root / "desk" / "reviews").rmdir()
    assert not (root / "desk" / "reviews").exists()

    updated = _deskops(root, "desk", "update", "--apply")
    assert updated.returncode == 0, updated.stdout + updated.stderr
    assert (root / "desk" / "reviews").is_dir()


@pytest.mark.xfail(strict=True, reason="G_SLDB_ANCHORS: sldb GO07")
def test_sldb_edges_show_links_the_review_to_the_task_by_subject(lifecycle_desk: Path) -> None:
    root = lifecycle_desk

    created = _deskops(
        root,
        "add",
        "task",
        "--title",
        "Task x",
        "--goal",
        "g",
        "--scope",
        "s",
        "--task-type",
        "task.code",
    )
    assert created.returncode == 0, created.stdout + created.stderr
    _write_review(root)

    shown = _sldb(root, "edges", "show", "ReviewDoc:review-task-x-preflight-1", "--store", ".sldb")
    assert shown.returncode == 0, shown.stdout + shown.stderr
    edges = json.loads(shown.stdout)
    assert any(
        edge["relation"] == "references"
        and edge.get("field") == "subject"
        and edge["target"] == "sldb://document/TaskCodeDoc:task-x"
        for edge in edges
    ), edges


# ------------------------------------------------------------------ edit surface
@pytest.mark.parametrize("field", ["verdict", "reason", "disposed_at", "disposed_by"])
def test_edit_review_refuses_the_disposition_fields(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str], field: str
) -> None:
    root = lifecycle_desk
    _write_review(root)
    capsys.readouterr()

    result = main(["edit", "review", "review-task-x-preflight-1", field, "accepted", "--root", str(root)])
    captured = capsys.readouterr()

    assert result == 1
    assert "verdict is written by deskops review dispose (GC03); a new review is a new document" in captured.out


# ------------------------------------------------------------------ kind evidence (CC33a)
def _evidence(**overrides: object) -> dict[str, object]:
    fields: dict[str, object] = dict(
        id="review-task-x-evidence-tests-1",
        kind="evidence",
        fact="tests",
        value="tests/test_a.py\ntests/test_b.py",
        engine="deskops-closeout",
        run_dir="",
        output_sha256="",
        verdict="accepted",
        reason="verified: tests tests/test_a.py\ntests/test_b.py",
        disposed_at="2026-01-01T00:00:00Z",
        disposed_by="robocop2",
    )
    fields.update(overrides)
    return _payload(**fields)


def test_evidence_receipt_roundtrips_fact_and_a_multiline_value() -> None:
    payload = _evidence()
    rendered = render_model_markdown(ReviewDoc, payload)
    extracted = extract_model_data(ReviewDoc, rendered)
    assert extracted["fact"] == "tests"
    assert extracted["value"] == "tests/test_a.py\ntests/test_b.py"
    assert ReviewDoc(**extracted).model_dump() == ReviewDoc(**payload).model_dump()


def test_evidence_receipt_requires_fact() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_evidence(fact=""))
    assert "requires fact" in str(excinfo.value)


def test_fact_outside_the_evidence_vocabulary_fails() -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_evidence(fact="goldens"))
    assert "fact" in str(excinfo.value)


@pytest.mark.parametrize("field", ["fact", "value"])
def test_fact_and_value_are_refused_outside_kind_evidence(field: str) -> None:
    with pytest.raises(ValidationError) as excinfo:
        ReviewDoc(**_payload(**{field: "tests"}))
    assert "only for kind 'evidence'" in str(excinfo.value)


def test_a_receipt_written_before_kind_evidence_still_reads_with_empty_fact_and_value() -> None:
    rendered = render_model_markdown(ReviewDoc, _payload())
    legacy = "\n".join(
        line for line in rendered.splitlines() if not line.startswith(("fact:", "value:", "# kind evidence only"))
    )
    extracted = extract_model_data(ReviewDoc, legacy)
    assert extracted["fact"] == "" and extracted["value"] == ""
    assert ReviewDoc(**extracted).kind == "preflight"
