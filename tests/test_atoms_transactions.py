from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops import doc_io
from deskops.operations import DeskopsOperations
from sldb.api import check_store


def _store_check(root: Path) -> dict:
    return check_store(root / ".sldb", root, pythonpath=str(ROOT))


def _fail_on_call(monkeypatch: pytest.MonkeyPatch, name: str, fail_at: int) -> dict[str, int]:
    calls = {"count": 0}
    original = getattr(doc_io, name)

    def flaky(*args, **kwargs):
        calls["count"] += 1
        if calls["count"] == fail_at:
            raise RuntimeError(f"injected {name} failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(doc_io, name, flaky)
    return calls


def _create_atom(
    operations: DeskopsOperations,
    atom_id: str,
    title: str,
    *,
    question: str = "how",
    answer: str,
) -> Path:
    record = operations.create_artifact(
        "artifact.atom",
        {
            "id": atom_id,
            "title": title,
            "five_wh_one_plus": question,
            "answer": answer,
            "tags": [],
        },
    )
    return record.path


def test_merge_restores_referrers_and_atoms_when_target_track_fails(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    source_path = _create_atom(
        operations,
        "atom-source-guidance",
        "Source Guidance",
        answer="Prefer explicit redirects during knowledge refactors.",
    )
    target_path = _create_atom(
        operations,
        "atom-target-guidance",
        "Target Guidance",
        answer="Keep canonical guidance on the surviving atom.",
    )
    referrer_path = lifecycle_desk / "desk" / "tasks" / "task-ref.md"
    referrer_path.write_text(
        "# Ref\n\nDepends on atom:atom-source-guidance today.\n",
        encoding="utf-8",
    )

    originals = {
        path: path.read_bytes()
        for path in (source_path, target_path, referrer_path)
    }
    before_check = _store_check(lifecycle_desk)
    calls = _fail_on_call(monkeypatch, "track_document_file", 1)

    with pytest.raises(RuntimeError, match="injected track_document_file failure"):
        operations.merge_atom("atom-source-guidance", into_selector="atom-target-guidance")

    assert calls["count"] >= 1
    for path, original in originals.items():
        assert path.read_bytes() == original, f"{path} was not restored"
    assert "atom:atom-source-guidance" in referrer_path.read_text(encoding="utf-8")
    assert _store_check(lifecycle_desk) == before_check


def test_split_restores_source_and_store_when_second_atom_track_fails(
    lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    operations = DeskopsOperations(lifecycle_desk)
    source_path = _create_atom(
        operations,
        "atom-splittable-guidance",
        "Splittable Guidance",
        answer=(
            "### Rerouting\n\n"
            "Preserve downstream resolution by keeping a redirect stub.\n\n"
            "### Validation\n\n"
            "Block mutation when inbound references are still present.\n"
        ),
    )
    created_paths = [
        lifecycle_desk / "desk" / "atoms" / "atom-rerouting-guidance.md",
        lifecycle_desk / "desk" / "atoms" / "atom-validation-guidance.md",
    ]
    for path in created_paths:
        assert not path.exists()

    original_source = source_path.read_bytes()
    before_check = _store_check(lifecycle_desk)
    calls = _fail_on_call(monkeypatch, "track_document_file", 2)

    with pytest.raises(RuntimeError, match="injected track_document_file failure"):
        operations.split_atom(
            "atom-splittable-guidance",
            into_ids=["atom-rerouting-guidance", "atom-validation-guidance"],
        )

    assert calls["count"] == 2
    assert source_path.read_bytes() == original_source
    for path in created_paths:
        assert not path.exists(), f"{path} survived the failed split"
    assert _store_check(lifecycle_desk) == before_check
