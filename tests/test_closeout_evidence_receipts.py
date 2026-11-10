"""CC33a: ``deskops closeout verify`` writes one pinned evidence receipt per declared kind.

Each receipt is a ``ReviewDoc`` kind ``evidence`` (``fact``, ``value``, ``verdict`` accepted or
rejected by the producer verify already runs) anchored on the task's contract. A repeated
verify without changes writes nothing; an edited contract leaves the receipts ``changed`` and
the next verify writes new ones. The envelope verify prints is the one it printed before.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess

from deskops.cli.main import main
from deskops.models.review import ReviewDoc
from deskops.operations import DeskopsOperations
from deskops.paths import package_pythonpath
from deskops import doc_access

ATOM = "atom-closeout-receipts"
TEST_FILE = "tests/test_feature.py"


def _git(root: Path, *argv: str) -> str:
    return subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def _run(argv: list[str]) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = main(argv)
    return code, out.getvalue()


def _desk(root: Path, *, with_commit: bool = True) -> str:
    """A task.code task referencing an existing test, an atom and (optionally) a HEAD commit."""
    from sldb.api import track_document_file

    atom = root / "desk" / "atoms" / f"{ATOM}.md"
    atom.parent.mkdir(parents=True, exist_ok=True)
    atom.write_text(
        f"---\nid: {ATOM}\ntitle: Receipts atom\nfive_wh_one_plus: what\ntags: []\n---\n\n"
        "# Receipts atom\n\n## Answer\n\nVerify writes receipts.\n",
        encoding="utf-8",
    )
    track_document_file(root / ".sldb", "AtomDoc", atom, name=ATOM, pythonpath=package_pythonpath(), force=True)
    test = root / TEST_FILE
    test.parent.mkdir(parents=True, exist_ok=True)
    test.write_text("def test_feature() -> None:\n    assert True\n", encoding="utf-8")
    _git(root, "add", "--", TEST_FILE)
    _git(root, "commit", "-q", "-m", "feature")
    sha = _git(root, "rev-parse", "--short", "HEAD")
    task_id = DeskopsOperations(root).create_task_bundle(
        {
            "title": "Receipts",
            "goal": "g",
            "scope": "s",
            "implementation_path": "i",
            "done_when": "d",
            "validation": ["pytest"],
            "task_type": "task.code",
        }
    ).task_id
    references = [TEST_FILE, ATOM, *([sha] if with_commit else [])]
    code, out = _run(["edit", "task", task_id, "references", json.dumps(references), "--root", str(root)])
    assert code == 0, out
    return task_id


def _verify(root: Path, task_id: str) -> tuple[int, dict]:
    code, out = _run(["closeout", "verify", "--task", task_id, "--root", str(root)])
    return code, json.loads(out)


def _receipts(root: Path, task_id: str) -> dict[str, dict]:
    directory = root / "desk" / "reviews" / task_id
    return {
        path.stem: doc_access.read_doc(path, ReviewDoc)
        for path in sorted(directory.glob("evidence-*.md"))
    }


def _not_intact(root: Path) -> dict[str, str]:
    from sldb.api.anchors.check_doc_anchors import check_doc_anchors

    findings = check_doc_anchors(root / ".sldb", pythonpath=package_pythonpath())
    return {finding.subject.rsplit(":", 1)[-1]: finding.code for finding in findings}


def test_verify_writes_three_accepted_pinned_receipts_and_the_same_envelope(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root)
    before = DeskopsOperations(root).verify_task_closeout(task_id)
    assert not (root / "desk" / "reviews" / task_id).exists(), "the read-only call writes no receipt"

    code, report = _verify(root, task_id)
    assert code == 0
    assert report == before

    receipts = _receipts(root, task_id)
    assert sorted(receipts) == ["evidence-atom-1", "evidence-commit-1", "evidence-tests-1"]
    for name, receipt in receipts.items():
        assert receipt["kind"] == "evidence" and receipt["verdict"] == "accepted", name
        assert receipt["engine"] == "deskops-closeout"
        assert receipt["subject"].startswith(f"doc:TaskCodeDoc:{task_id}@sha256:"), receipt["subject"]
        assert receipt["id"] == f"review-{task_id}-{name}"
        assert receipt["reason"] == f"verified: {receipt['fact']} {receipt['value']}"
    head = _git(root, "rev-parse", "HEAD")
    assert receipts["evidence-commit-1"]["value"] == head
    assert receipts["evidence-atom-1"]["value"] == ATOM
    assert receipts["evidence-tests-1"]["value"] == TEST_FILE
    file_sha = hashlib.sha256((root / TEST_FILE).read_bytes()).hexdigest()
    expected = hashlib.sha256(f"tests\n{TEST_FILE}\n{TEST_FILE}\n{file_sha}\n".encode()).hexdigest()
    assert receipts["evidence-tests-1"]["input_sha256"] == expected
    assert receipts["evidence-commit-1"]["input_sha256"] == hashlib.sha256(f"commit\n{head}\n".encode()).hexdigest()
    assert not set(_not_intact(root)) & {receipt["id"] for receipt in receipts.values()}


def test_without_a_commit_the_commit_receipt_is_rejected(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root, with_commit=False)
    code, report = _verify(root, task_id)
    assert code == 1 and report["ok"] is False
    receipts = _receipts(root, task_id)
    commit = receipts["evidence-commit-1"]
    assert commit["verdict"] == "rejected"
    assert commit["reason"] == "No resolvable commit reference found."
    assert commit["value"] == ""
    assert receipts["evidence-tests-1"]["verdict"] == "accepted"
    assert receipts["evidence-atom-1"]["verdict"] == "accepted"


def test_a_second_verify_without_changes_writes_no_receipt(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root)
    _verify(root, task_id)
    first = _receipts(root, task_id)
    _, report = _verify(root, task_id)
    assert report["ok"] is True
    assert _receipts(root, task_id) == first


def test_editing_the_goal_leaves_the_receipts_changed_and_verify_writes_new_ones(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    task_id = _desk(root)
    _verify(root, task_id)
    first = _receipts(root, task_id)
    code, out = _run(["edit", "task", task_id, "goal", "a different goal", "--root", str(root)])
    assert code == 0, out

    states = _not_intact(root)
    for receipt in first.values():
        assert states.get(receipt["id"]) == "anchors/doc_changed", receipt["id"]

    _verify(root, task_id)
    after = _receipts(root, task_id)
    assert sorted(after) == sorted([*first, "evidence-atom-2", "evidence-commit-2", "evidence-tests-2"])
    for name, receipt in first.items():
        assert after[name] == receipt, "the old receipt stays as it was"
        renewed = after[name[:-1] + "2"]
        assert renewed["input_sha256"] == receipt["input_sha256"]
        assert renewed["subject"] != receipt["subject"]
    assert not set(_not_intact(root)) & {after[name]["id"] for name in after if name.endswith("-2")}


def test_verify_without_a_store_writes_no_receipt(tmp_path: Path) -> None:
    root = tmp_path / "bare"
    (root / "desk" / "tasks").mkdir(parents=True)
    _git(root, "init", "-q")
    ops = DeskopsOperations(root)
    assert ops.closure._write_evidence_receipts(root / "desk" / "tasks" / "task-x.md", "task-x", ["tests"], {}) == []
    assert not (root / "desk" / "reviews").exists()
