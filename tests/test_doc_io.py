from __future__ import annotations

import ast
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops import doc_io
from deskops.models import AtomDoc
from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService

WRITE_MODULE_PREFIXES = ("create_", "delete_", "update_", "track_", "untrack_")


def _git(root: Path, *argv: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(["git", *argv], cwd=root, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return result


def _imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            modules.append(node.module)
    return modules


def _is_write_side_module(module: str) -> bool:
    if module == "sldb.store.ops" or module.startswith("sldb.store.ops."):
        return True
    if module == "sldb.cli.commands" or module.startswith("sldb.cli.commands."):
        return True
    if module.startswith("sldb.api.documents."):
        leaf = module.rsplit(".", 1)[-1]
        return leaf.startswith(WRITE_MODULE_PREFIXES)
    return False


def test_only_doc_io_imports_write_side_sldb_modules() -> None:
    offenders: list[str] = []
    for path in sorted((ROOT / "deskops").rglob("*.py")):
        if path.name == "doc_io.py":
            continue
        for module in _imported_modules(path):
            if _is_write_side_module(module):
                offenders.append(f"{path.relative_to(ROOT)} imports {module}")
    assert offenders == []


def test_doc_io_imports_sldb_api_or_declared_private_modules_only() -> None:
    offenders: list[str] = []
    for module in _imported_modules(ROOT / "deskops" / "doc_io.py"):
        if not module.startswith("sldb"):
            continue
        allowed = module in {"sldb", "sldb.api"} or module.startswith("sldb.api.")
        if not allowed and module not in doc_io.PRIVATE_SLDB_IMPORTS:
            offenders.append(module)
    assert offenders == []


def _store_check(root: Path) -> dict:
    from sldb.api import check_store

    return check_store(root / ".sldb", root, pythonpath=str(ROOT))


def _atom(operations: DeskopsOperations, title: str) -> Path:
    record = operations.create_artifact(
        "artifact.atom",
        {
            "title": title,
            "five_wh_one_plus": "what",
            "answer": "An atom whose store entry must survive a failed write.",
        },
    )
    return record.path


def _fail_first_call(monkeypatch: pytest.MonkeyPatch, name: str) -> dict[str, int]:
    calls = {"count": 0}
    original = getattr(doc_io, name)

    def flaky(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError(f"injected {name} failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(doc_io, name, flaky)
    return calls


def test_write_restores_file_bytes_and_store_when_retracking_fails(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    path = _atom(operations, "Rollback tracked write")
    before_bytes = path.read_bytes()
    before_check = _store_check(lifecycle_desk)
    payload = operations._read_doc(path, AtomDoc)
    payload["answer"] = "This content must not survive the failed write."

    _fail_first_call(monkeypatch, "track_document_file")

    with pytest.raises(RuntimeError, match="injected track_document_file failure"):
        with doc_io.DocTransaction(lifecycle_desk) as transaction:
            transaction.write(path, AtomDoc, payload)

    assert path.read_bytes() == before_bytes
    assert _store_check(lifecycle_desk) == before_check


def test_track_failure_removes_the_file_created_in_the_transaction(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = lifecycle_desk / "desk" / "atoms" / "atom-rollback-new.md"
    before_check = _store_check(lifecycle_desk)
    _fail_first_call(monkeypatch, "track_document_file")

    with pytest.raises(RuntimeError, match="injected track_document_file failure"):
        with doc_io.DocTransaction(lifecycle_desk) as transaction:
            transaction.write(
                path,
                AtomDoc,
                {
                    "id": "atom-rollback-new",
                    "title": "Rollback new atom",
                    "five_wh_one_plus": "what",
                    "answer": "A failed track must not leave the file behind.",
                    "tags": [],
                },
            )
            transaction.track(path, AtomDoc)

    assert not path.exists()
    assert _store_check(lifecycle_desk) == before_check


def test_delete_failure_keeps_the_file_and_the_store_entry(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    path = _atom(operations, "Rollback delete")
    before_bytes = path.read_bytes()
    before_check = _store_check(lifecycle_desk)
    _fail_first_call(monkeypatch, "untrack_document")

    with pytest.raises(RuntimeError, match="injected untrack_document failure"):
        with doc_io.DocTransaction(lifecycle_desk) as transaction:
            transaction.delete(path)

    assert path.read_bytes() == before_bytes
    assert _store_check(lifecycle_desk) == before_check


def test_untrack_failure_restores_the_recorded_tracking(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    path = _atom(operations, "Rollback untrack")
    before_check = _store_check(lifecycle_desk)
    _fail_first_call(monkeypatch, "untrack_document")

    with pytest.raises(RuntimeError, match="injected untrack_document failure"):
        with doc_io.DocTransaction(lifecycle_desk) as transaction:
            transaction.untrack(path)

    assert doc_io.is_tracked(lifecycle_desk, path)
    assert _store_check(lifecycle_desk) == before_check


def test_an_inner_transaction_joins_the_outer_one(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    path = _atom(operations, "Rollback nested write")
    before_bytes = path.read_bytes()
    payload = operations._read_doc(path, AtomDoc)
    payload["answer"] = "Nested writes share one rollback."
    _fail_first_call(monkeypatch, "track_document_file")

    with pytest.raises(RuntimeError, match="injected track_document_file failure"):
        with doc_io.DocTransaction(lifecycle_desk):
            with doc_io.DocTransaction(lifecycle_desk) as inner:
                inner.write(path, AtomDoc, payload)

    assert path.read_bytes() == before_bytes


def test_closeout_commit_includes_the_store_delta_it_causes(lifecycle_desk: Path) -> None:
    root = lifecycle_desk
    (root / ".gitignore").write_text(".sldb/runtime/\n", encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_evidence.py").write_text("def test_evidence():\n    assert True\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "desk")

    operations = DeskopsOperations(root)
    task_id = operations.create_task_bundle(
        {
            "title": "Closeout store delta",
            "goal": "The closeout commit carries the .sldb changes.",
            "scope": "Closeout commit only.",
            "implementation_path": "deskops/operations.py",
            "validation": ["pytest"],
            "references": ["tests/test_evidence.py"],
        }
    ).task_id
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "task")

    atom_path = _atom(operations, "Closeout store delta evidence")
    atom_rel = atom_path.relative_to(root).as_posix()
    commit = _git(root, "rev-parse", "HEAD").stdout.strip()
    operations.edit_artifact_field(
        "task",
        task_id,
        "references",
        f'["{atom_rel}", "pytest tests/test_evidence.py::test_evidence", "{commit}"]',
    )
    operations.edit_artifact_field("task", task_id, "files", f'["{atom_rel}"]')

    operations.advance_task(task_id)
    operations.advance_task(task_id)
    refused, result = operations.advance_task(task_id)
    assert result is not None and result.blocked
    assert refused is not None and refused.current_node == "ritual-closeout"

    outcome = ClosureService(root, operations).close_manual(
        task_id,
        reason="Store delta smoke test",
        paths=[atom_rel, "tests/test_evidence.py"],
    )
    assert outcome.exit_code == 0, outcome.messages

    status = _git(root, "status", "--porcelain", "--", ".sldb")
    assert status.stdout == ""
