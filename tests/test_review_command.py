"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
PLAN_SRC = ROOT / "desk" / "drawer" / "plans" / "gates-por-tipo"


FAKE_PI = """#!/usr/bin/env python3
import os
import sys
import time

log = os.environ.get("FAKE_PI_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(sys.argv[1:]) + "\\n")

mode = os.environ.get("FAKE_PI_MODE", "ok")
if mode == "fail":
    sys.exit(1)
if mode == "no-reformulacion":
    print("sin seccion")
    sys.exit(0)
if mode == "sleep":
    time.sleep(5)
    print("REFORMULACION\\nDRY-RUN: nada.")
    sys.exit(0)
print(
    "REFORMULACION\\n"
    "Propósito: revisar el encargo.\\n"
    "AMBIGUEDADES: ninguna.\\n"
    "DRY-RUN: leer, proponer, validar, sin ejecutar.\\n"
    "FUTURO: otro nodo o un humano."
)
sys.exit(0)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(ROOT), env.get("PYTHONPATH"))))
    return env


def _run(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*argv], cwd=root, env=env or _env(), capture_output=True, text=True)


def _deskops(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root), env=env)


@pytest.fixture
def fake_pi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(FAKE_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("FAKE_PI_MODE", "ok")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return bin_dir, log


def _pi_calls(log: Path) -> int:
    if not log.exists():
        return 0
    return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


def _add_task(root: Path, *, title: str = "X", task_type: str = "task.code") -> str:
    result = _deskops(
        root,
        "add",
        "task",
        "--title",
        title,
        "--goal",
        "review goal",
        "--scope",
        "review scope",
        "--validation",
        "pytest",
        "--task-type",
        task_type,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return f"task-{title.lower().replace(' ', '-')}"


def _attempt_dirs(root: Path, key: str) -> list[Path]:
    base = root / "runs" / "subagents"
    if not base.exists():
        return []
    return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))


def _review_docs(root: Path) -> list[dict]:
    reviews = root / "desk" / "reviews"
    if not reviews.exists():
        return []
    docs: list[dict] = []
    for path in sorted(reviews.rglob("*.md")):
        docs.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
    return docs


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_writes_attempt_evidence_and_receipt(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 1
    attempt = attempts[0]
    assert attempt.name == "attempt-1"
    for name in ("input.md", "manifest.json", "output.md", "stderr.log", "receipt.json"):
        assert (attempt / name).is_file(), name

    input_bytes = (attempt / "input.md").read_bytes()
    assert input_bytes.decode().startswith("FILE:desk/tasks/task-x.md\n")

    manifest = _json(attempt / "manifest.json")
    assert manifest["input_sha256"] == __import__("hashlib").sha256(input_bytes).hexdigest()
    assert manifest["sources"][0]["path"] == "desk/tasks/task-x.md"
    assert manifest["argv"][0] == "pi"
    assert manifest["argv"][-1].startswith("@")

    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is True
    assert receipt["returncode"] == 0
    assert receipt["input_sha256"] == manifest["input_sha256"]

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "pending"
    assert doc["subject"] == "doc:TaskCodeDoc:task-x"
    assert doc["run_dir"] == attempt.relative_to(root).as_posix()
    assert doc["input_sha256"] == manifest["input_sha256"]
    assert doc["output_sha256"] == receipt["output_sha256"]


def test_unchanged_second_run_is_reviewed_and_does_not_call_the_model(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    calls_after_first = _pi_calls(_log)
    assert calls_after_first == 1

    second = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout
    assert _pi_calls(_log) == calls_after_first
    assert len(_attempt_dirs(root, "task-x/preflight")) == 1

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "reviewed"


def test_edited_goal_is_stale_and_next_run_uses_a_new_sha(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    first_sha = _attempt_dirs(root, "task-x/preflight")[0].parent.name

    edit = _deskops(root, "edit", "task", "task-x", "goal", "goal changed")
    assert edit.returncode == 0, edit.stdout + edit.stderr

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "stale"

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    new_shas = {attempt.parent.name for attempt in attempts}
    assert first_sha in new_shas
    assert len(new_shas) == 2


def test_bundle_includes_rituals_pills_and_files_in_order(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    pill = _deskops(
        root,
        "add",
        "pill",
        "--title",
        "Guardrail",
        "--what",
        "keep layers clean",
        "--why",
        "safety",
        "--when",
        "always",
        "--where",
        "desk",
        "--how",
        "read first",
        "--how-not",
        "skip it",
    )
    assert pill.returncode == 0, pill.stdout + pill.stderr
    assert _deskops(root, "bind", "pill", "task-x", "pill-guardrail").returncode == 0

    doc = root / "docs" / "foo.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Foo\nsmall file\n", encoding="utf-8")
    edit = _deskops(root, "edit", "task", "task-x", "files", '["docs/foo.md"]')
    assert edit.returncode == 0, edit.stdout + edit.stderr

    assert _deskops(root, "review", "bundle", "task-x", "--run", "test-run").returncode == 0

    attempt = _attempt_dirs(root, "task-x/bundle")[0]
    input_text = (attempt / "input.md").read_text(encoding="utf-8")
    file_headers = [line for line in input_text.splitlines() if line.startswith("FILE:")]
    assert file_headers[0] == "FILE:desk/tasks/task-x.md"
    assert "FILE:desk/rituals/phase.md" in file_headers
    assert "FILE:desk/rituals/execution.md" in file_headers
    assert "FILE:desk/rituals/testing.md" in file_headers
    assert "FILE:desk/rituals/closeout.md" in file_headers
    assert "FILE:desk/contexts/pill-guardrail.md" in file_headers
    assert "FILE:docs/foo.md" in file_headers
    assert file_headers[-1] == "FILE:instruccion"

    # Order: task, rituals, pill, file, instruction.
    ordered = [
        "FILE:desk/tasks/task-x.md",
        "FILE:desk/rituals/phase.md",
        "FILE:desk/rituals/execution.md",
        "FILE:desk/rituals/testing.md",
        "FILE:desk/rituals/closeout.md",
        "FILE:desk/contexts/pill-guardrail.md",
        "FILE:docs/foo.md",
        "FILE:instruccion",
    ]
    assert file_headers == ordered


def test_node_writes_one_review_doc_per_node(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)

    result = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    node_ids = [doc["id"] for doc in node_docs]
    assert "review-deskops-gates-por-tipo-gc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-pc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-root-node-1" in node_ids
    for doc in node_docs:
        assert doc["subject"] == ""
        assert doc["subject_ref"].startswith("desk/drawer/plans/gates-por-tipo/dag.yaml#node:")
        assert doc["verdict"] == "pending"


def test_dispose_writes_the_verdict_and_a_second_dispose_fails(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0

    disposed = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "accepted",
        "--reason",
        "looks right",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "looks right"
    assert doc["disposed_at"]
    assert doc["disposed_by"]

    again = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "rejected",
        "--reason",
        "changed my mind",
    )
    assert again.returncode == 1
    assert "already has verdict" in again.stdout


def test_third_good_attempt_on_the_same_key_fails_without_force(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)
    brief = plan_dir / "brief.md"
    log = fake_pi[1]

    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change one\n", encoding="utf-8")
    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    assert _pi_calls(log) == 2

    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change two\n", encoding="utf-8")
    third = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r")
    assert third.returncode == 1
    assert "tope --max-attempts" in third.stdout
    assert _pi_calls(log) == 2


def test_transport_failure_leaves_technical_failure_and_incomplete(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "fail")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is False
    assert receipt["returncode"] == 1

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_output_without_reformulacion_is_a_transport_failure(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "no-reformulacion")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    assert _json(attempt / "receipt.json")["technical_ok"] is False
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_force_requires_reason(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--run", "test-run")
    assert result.returncode == 2
    assert "--force requires --reason" in result.stdout


def test_force_with_reason_retries_the_same_input(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    assert _pi_calls(log) == 1

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--reason", "again", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _pi_calls(log) == 2

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    manifest = _json(attempts[1] / "manifest.json")
    assert manifest["retry_reason"] == "again"
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-2"]
    assert len(docs) == 1
    assert docs[0]["reason"] == "again"


def test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently(
    tmp_path: Path,
) -> None:
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0

    profile = root / "desk" / "runtimes" / "runtime-pi-deepseek-flash.md"
    assert profile.is_file()
    first = profile.read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == first

    # An existing profile is never overwritten.
    profile.write_text("# my own profile\n", encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == "# my own profile\n"


@pytest.mark.parametrize(
    ("receipts", "expected"),
    [
        ([], "missing"),
        ([("old", "accepted"), ("old", "rejected"), ("old", "incomplete")], "stale"),
        ([("current", "incomplete")], "technical_failure"),
        ([("current", "incomplete"), ("current", "pending")], "reviewed"),
        ([("current", "pending"), ("current", "rejected")], "rejected"),
        ([("current", "accepted"), ("current", "rejected"), ("current", "pending"),
          ("current", "incomplete"), ("old", "rejected")], "accepted"),
        ([("old", "accepted"), ("current", "rejected")], "rejected"),
    ],
)
def test_status_classifies_only_current_receipts_without_mutating_evidence(
    lifecycle_desk: Path, receipts: list[tuple[str, str]], expected: str
) -> None:
    from deskops.cli.main import main
    from deskops.services.review import ReviewService, _sha

    root = lifecycle_desk
    assert main([
        "add", "task", "--title", "Status", "--goal", "review goal",
        "--scope", "review scope", "--validation", "pytest", "--task-type", "task.code",
        "--root", str(root),
    ]) == 0
    service = ReviewService(root)
    task_path, task_id = service._resolve_task("task-status")
    input_data, _, _ = service._preflight_input(task_path, task_id)
    for index, (identity, verdict) in enumerate(receipts):
        evidence = root / "runs" / "subagents" / f"receipt-{index}"
        evidence.mkdir(parents=True)
        (evidence / "input.md").write_bytes(input_data if identity == "current" else b"old input\n")
        (evidence / "manifest.json").write_text(json.dumps({"profile": "test", "attempt": index}))
        review_id, _ = service._write_review(
            kind="preflight", subject=f"doc:TaskCodeDoc:{task_id}", subject_ref="",
            engine="test", run_dir=evidence.relative_to(root).as_posix(),
            input_sha256=_sha(input_data) if identity == "current" else _sha(b"old input\n"),
            output_sha256=_sha(b"review output"),
            verdict="pending" if verdict in {"accepted", "rejected"} else verdict, reason="test evidence",
            node_id=None,
        )
        if verdict in {"accepted", "rejected"}:
            service.dispose(review_id, verdict, "test disposition")
    preserved = {
        path: path.read_bytes()
        for directory in (root / "desk" / "reviews", root / "runs")
        if directory.exists() for path in directory.rglob("*") if path.is_file()
    }
    reports = {item["key"]: item for item in service.status("task-status")}
    assert reports["task-status/preflight"] == {
        "key": "task-status/preflight", "state": expected, "input_sha256": _sha(input_data),
    }
    assert reports["task-status/bundle"]["state"] == "missing"
    assert all(path.read_bytes() == content for path, content in preserved.items())


@pytest.mark.parametrize("tracked", [False, True], ids=["plain", "pinned"])
def test_disposed_review_status_uses_task_identity(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], tracked: bool
) -> None:
    root = lifecycle_desk
    if not tracked:
        shutil.rmtree(root / ".sldb")
    _add_task(root, title="Identity")
    result = _deskops(root, "review", "preflight", "task-identity", "--run", "identity")
    assert result.returncode == 0, result.stdout + result.stderr
    doc = _review_docs(root)[0]
    assert doc["subject"].startswith("doc:TaskCodeDoc:task-identity" if tracked else "doc:TaskDoc:task-identity")
    disposed = _deskops(root, "review", "dispose", doc["id"], "--verdict", "accepted", "--reason", "correct")
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr
    subject = _review_docs(root)[0]["subject"]
    if tracked:
        # GO07 pins the actual stored subject on disposition, not a parser fixture.
        assert "@sha256:" in subject
    else:
        assert "@" not in subject
    for target in [("task-identity",), ()]:
        status = _deskops(root, "review", "status", *target, "--format", "json")
        assert status.returncode == 0, status.stdout + status.stderr
        report = next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")
        assert report["state"] == "accepted"
    edit = _deskops(root, "edit", "task", "task-identity", "goal", "changed input")
    assert edit.returncode == 0, edit.stdout + edit.stderr
    status = _deskops(root, "review", "status", "task-identity", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    assert next(item for item in json.loads(status.stdout) if item["key"] == "task-identity/preflight")["state"] == "stale"
