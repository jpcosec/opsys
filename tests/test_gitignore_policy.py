from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_sldb_core_is_trackable_and_runtime_is_ignored() -> None:
    assert not _is_ignored(".sldb/core/store_index.yaml")
    assert not _is_ignored(".sldb/core/models/AtomDoc.yaml")
    assert not _is_ignored(".sldb/core/documents/AtomDoc.yaml")
    assert _is_ignored(".sldb/runtime/semantic_index.yaml")
    assert _is_ignored(".sldb/runtime/locks/store.lock")


def _is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", path],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0
