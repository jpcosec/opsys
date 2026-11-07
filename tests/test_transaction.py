"""Every deskops write goes through ``sldb.api.transaction`` (CC35a).

- No deskops module imports sldb's write-side internals (the public ``sldb.api`` only).
- A failure injected in the middle of ``atoms merge`` leaves ``desk/`` and ``.sldb/core/``
  byte for byte as they were, and ``sldb stores check`` says the same.
- An update whose ``expected_source_hash`` is stale fails with the deskops conflict message.
- A document edited by hand and not reindexed still takes ``deskops edit``.
- A failure inside sldb during split or merge rolls the created and rewritten files back.
- The closeout commit carries the store delta it causes.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from deskops import doc_access
from deskops.cli.main import main
from deskops.errors import DomainError
from deskops.models import AtomDoc
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations
from deskops.services.closure import ClosureService

WRITE_MODULE_PREFIXES = ("create_", "delete_", "update_", "track_", "untrack_")


# ------------------------------------------------------------------ helpers
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


def _store_check(root: Path) -> dict:
    from sldb.api import check_store

    return check_store(root / ".sldb", root, pythonpath=str(ROOT))


def _stores_check_output(root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb")],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def _tree_hashes(root: Path) -> dict[str, str]:
    """sha256 of every file under desk/ and .sldb/core/, by path relative to root."""
    hashes: dict[str, str] = {}
    for base in (root / "desk", root / ".sldb" / "core"):
        for path in sorted(base.rglob("*")):
            if path.is_file():
                hashes[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _create_atom(operations: DeskopsOperations, atom_id: str, title: str, *, answer: str) -> Path:
    record = operations.create_artifact(
        "artifact.atom",
        {"id": atom_id, "title": title, "five_wh_one_plus": "how", "answer": answer, "tags": []},
    )
    return record.path


def _create_task(operations: DeskopsOperations, title: str, **fields: object) -> tuple[str, Path]:
    bundle = operations.create_task_bundle(
        {
            "title": title,
            "goal": "A task the store tracks.",
            "scope": "This test.",
            "implementation_path": "deskops/doc_access.py",
            "validation": ["pytest"],
            **fields,
        }
    )
    return bundle.task_id, bundle.task_path


def _fail_sldb_call(monkeypatch: pytest.MonkeyPatch, name: str, fail_at: int) -> dict[str, int]:
    """Make the ``fail_at``-th call of ``sldb.api.documents.transaction_ops.<name>`` raise."""
    from sldb.api.documents import transaction_ops

    calls = {"count": 0}
    original = getattr(transaction_ops, name)

    def flaky(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == fail_at:
            raise RuntimeError(f"injected {name} failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(transaction_ops, name, flaky)
    return calls


# ------------------------------------------------------------------ boundary
def test_no_deskops_module_imports_write_side_sldb_internals() -> None:
    offenders: list[str] = []
    for path in sorted((ROOT / "deskops").rglob("*.py")):
        for module in _imported_modules(path):
            if _is_write_side_module(module):
                offenders.append(f"{path.relative_to(ROOT)} imports {module}")
    assert offenders == []


def test_doc_io_is_gone() -> None:
    assert not (ROOT / "deskops" / "doc_io.py").exists()
    mentions = [
        f"{path.relative_to(ROOT)}"
        for path in sorted((ROOT / "deskops").rglob("*.py"))
        if "doc_io" in path.read_text(encoding="utf-8") or "DocTransaction" in path.read_text(encoding="utf-8")
    ]
    assert mentions == []


# ------------------------------------------------------------------ merge: injected failure (a6, b2)
def test_merge_failure_at_the_source_write_leaves_desk_and_store_as_they_were(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The failure hits the write of the SOURCE atom, after the referrers were rewritten and
    the target atom written: the transaction puts every file and index entry back."""
    root = lifecycle_desk
    operations = DeskopsOperations(root)
    source_path = _create_atom(operations, "atom-source-guidance", "Source Guidance", answer="Prefer explicit redirects.")
    target_path = _create_atom(operations, "atom-target-guidance", "Target Guidance", answer="Keep canonical guidance here.")
    _task_id, referrer_path = _create_task(operations, "Referrer", goal="Depends on atom:atom-source-guidance today.")
    target_before = target_path.read_text(encoding="utf-8")
    referrer_before = referrer_path.read_text(encoding="utf-8")

    before_hashes = _tree_hashes(root)
    before_check = _stores_check_output(root)
    assert before_check[0] == 0, before_check[1]

    original_write = doc_access.write_doc
    seen_at_failure: dict[str, str] = {}

    def failing_source_write(write_root: Path, path: Path, model: type, payload: dict) -> None:
        if path.resolve() == source_path.resolve():
            seen_at_failure["target"] = target_path.read_text(encoding="utf-8")
            seen_at_failure["referrer"] = referrer_path.read_text(encoding="utf-8")
            raise RuntimeError("injected failure writing the source atom")
        original_write(write_root, path, model, payload)

    monkeypatch.setattr(doc_access, "write_doc", failing_source_write)

    with pytest.raises(RuntimeError, match="injected failure writing the source atom"):
        operations.merge_atom("atom-source-guidance", into_selector="atom-target-guidance")

    # The failure came after the referrer and the target had been written...
    assert seen_at_failure["target"] != target_before
    assert "atom:atom-target-guidance" in seen_at_failure["referrer"]
    # ...and the transaction restored them all, store entries included.
    assert _tree_hashes(root) == before_hashes
    assert referrer_path.read_text(encoding="utf-8") == referrer_before
    assert _stores_check_output(root) == before_check


# ------------------------------------------------------------------ conflict (a5, b1)
def test_update_with_a_stale_source_hash_is_the_deskops_conflict(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = lifecycle_desk
    task_id, task_path = _create_task(DeskopsOperations(root), "Guarded edit")
    before = task_path.read_bytes()
    capsys.readouterr()

    original_read = doc_access.read_doc

    def read_then_forget_the_index(path: Path, model: type) -> dict:
        payload = original_read(path, model)
        # What deskops read no longer matches the store's index: a stale guard.
        doc_access._READ_HASHES[str(path.resolve())] = "0" * 64
        return payload

    monkeypatch.setattr(doc_access, "read_doc", read_then_forget_the_index)

    code = main(["edit", "task", task_id, "summary", "A summary nobody will see.", "--root", str(root)])
    captured = capsys.readouterr()

    assert code == 1
    assert captured.out == ""
    assert captured.err == (
        f"Error: desk/tasks/{task_id}.md changed since deskops read it; nothing was written. Re-run the command.\n"
    )
    assert task_path.read_bytes() == before


def test_a_document_the_store_rewrote_after_deskops_read_it_is_refused(lifecycle_desk: Path) -> None:
    from sldb.api import transaction

    root = lifecycle_desk
    task_id, task_path = _create_task(DeskopsOperations(root), "Concurrent edit")
    payload = doc_access.read_doc(task_path, TaskDoc)

    with transaction(root / ".sldb", pythonpath=str(ROOT)) as tx:
        tx.update(task_id, {**payload, "summary": "Written by another process."})

    payload["summary"] = "Written by deskops after its read."
    with pytest.raises(DomainError, match=f"Error: desk/tasks/{task_id}.md changed since deskops read it; nothing was written"):
        doc_access.write_doc(root, task_path, TaskDoc, payload)
    assert "Written by another process." in task_path.read_text(encoding="utf-8")
    assert "after its read" not in task_path.read_text(encoding="utf-8")


def test_a_conflict_inside_a_compound_write_writes_nothing(lifecycle_desk: Path) -> None:
    """The guard fails on the second document of one transaction: the first is restored."""
    from sldb.api import transaction

    root = lifecycle_desk
    operations = DeskopsOperations(root)
    first_id, first_path = _create_task(operations, "First")
    second_id, second_path = _create_task(operations, "Second")
    first_payload = doc_access.read_doc(first_path, TaskDoc)
    second_payload = doc_access.read_doc(second_path, TaskDoc)
    first_before = first_path.read_bytes()
    with transaction(root / ".sldb", pythonpath=str(ROOT)) as tx:
        tx.update(second_id, {**second_payload, "summary": "Moved under deskops's feet."})
    before_check = _store_check(root)

    with pytest.raises(DomainError, match="changed since deskops read it"):
        with doc_access.desk_transaction(root):
            doc_access.write_doc(root, first_path, TaskDoc, {**first_payload, "summary": "First, written."})
            doc_access.write_doc(root, second_path, TaskDoc, {**second_payload, "summary": "Second, refused."})

    assert first_path.read_bytes() == first_before
    assert _store_check(root) == before_check
    assert first_id in first_path.read_text(encoding="utf-8")


# ------------------------------------------------------------------ hand edit (b3)
def test_a_document_edited_by_hand_still_takes_a_deskops_edit(
    lifecycle_desk: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from sldb.api import doc_status

    root = lifecycle_desk
    task_id, task_path = _create_task(DeskopsOperations(root), "Hand edited")
    text = task_path.read_text(encoding="utf-8")
    assert "A task the store tracks." in text
    task_path.write_text(text.replace("A task the store tracks.", "A goal rewritten by hand."), encoding="utf-8")
    capsys.readouterr()

    code = main(["edit", "task", task_id, "summary", "Edited after the hand edit.", "--root", str(root)])
    captured = capsys.readouterr()

    assert code == 0, captured.err
    assert captured.err == ""
    after = task_path.read_text(encoding="utf-8")
    assert "A goal rewritten by hand." in after
    assert "Edited after the hand edit." in after
    assert doc_status(root / ".sldb", task_id).status == "ok"
    returncode, output = _stores_check_output(root)
    assert returncode == 0 and "PASS" in output, output


# ------------------------------------------------------------------ rollback when sldb fails inside
def test_merge_restores_referrers_and_atoms_when_the_target_update_fails(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    operations = DeskopsOperations(root)
    source_path = _create_atom(operations, "atom-source-guidance", "Source Guidance", answer="Prefer explicit redirects.")
    target_path = _create_atom(operations, "atom-target-guidance", "Target Guidance", answer="Keep canonical guidance here.")
    _task_id, referrer_path = _create_task(operations, "Referrer", goal="Depends on atom:atom-source-guidance today.")

    originals = {path: path.read_bytes() for path in (source_path, target_path, referrer_path)}
    before_check = _store_check(root)
    calls = _fail_sldb_call(monkeypatch, "save_document_payload", 1)

    with pytest.raises(RuntimeError, match="injected save_document_payload failure"):
        operations.merge_atom("atom-source-guidance", into_selector="atom-target-guidance")

    assert calls["count"] == 1
    for path, original in originals.items():
        assert path.read_bytes() == original, f"{path} was not restored"
    assert "atom:atom-source-guidance" in referrer_path.read_text(encoding="utf-8")
    assert _store_check(root) == before_check


def test_split_restores_source_and_store_when_the_second_atom_create_fails(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sldb.api import track_document_file
    from sldb.runtime.validation import render_model_markdown

    root = lifecycle_desk
    operations = DeskopsOperations(root)
    # An atom whose answer carries section headings is what split works on. sldb refuses
    # such headings on `create` (structural noise under the default policy), so the atom
    # is written and tracked the way `desk update --apply` tracks a hand-written one.
    source_path = root / "desk" / "atoms" / "atom-splittable-guidance.md"
    source_path.write_text(
        render_model_markdown(
            AtomDoc,
            {
                "id": "atom-splittable-guidance",
                "title": "Splittable Guidance",
                "five_wh_one_plus": "how",
                "answer": (
                    "### Rerouting\n\n"
                    "Preserve downstream resolution by keeping a redirect stub.\n\n"
                    "### Validation\n\n"
                    "Block mutation when inbound references are still present.\n"
                ),
                "tags": [],
            },
        )
        + "\n",
        encoding="utf-8",
    )
    track_document_file(root / ".sldb", "AtomDoc", source_path, name="atom-splittable-guidance", pythonpath=str(ROOT), force=True)
    created_paths = [
        root / "desk" / "atoms" / "atom-rerouting-guidance.md",
        root / "desk" / "atoms" / "atom-validation-guidance.md",
    ]
    original_source = source_path.read_bytes()
    before_check = _store_check(root)
    calls = _fail_sldb_call(monkeypatch, "create_document", 2)

    with pytest.raises(RuntimeError, match="injected create_document failure"):
        operations.split_atom("atom-splittable-guidance", into_ids=["atom-rerouting-guidance", "atom-validation-guidance"])

    assert calls["count"] == 2
    assert source_path.read_bytes() == original_source
    for path in created_paths:
        assert not path.exists(), f"{path} survived the failed split"
    assert _store_check(root) == before_check


def test_delete_failure_keeps_the_file_and_the_store_entry(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from sldb.api import doc_status

    root = lifecycle_desk
    operations = DeskopsOperations(root)
    path = _create_atom(operations, "atom-kept", "Kept", answer="A failed delete keeps me.")
    before_bytes = path.read_bytes()
    before_check = _store_check(root)
    _fail_sldb_call(monkeypatch, "delete_document", 1)

    with pytest.raises(RuntimeError, match="injected delete_document failure"):
        operations.delete_atom("atom-kept", force=True)

    assert path.read_bytes() == before_bytes
    assert doc_status(root / ".sldb", "atom-kept").status == "ok"
    assert _store_check(root) == before_check


# ------------------------------------------------------------------ closeout
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

    atom_path = _create_atom(operations, "atom-closeout-store-delta-evidence", "Closeout store delta evidence", answer="Evidence.")
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
