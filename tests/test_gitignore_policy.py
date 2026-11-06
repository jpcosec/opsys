from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_sldb_core_and_store_declaration_are_tracked_and_cache_is_ignored() -> None:
    """The `.sldb` layout policy: `.sldb/store.yaml` and `.sldb/core/` are versioned
    whole; the derived cache lives in `.sldb_cache/` and is ignored. Nothing under the
    old `.sldb/runtime/` layout is tracked."""
    assert not _is_ignored(".sldb/store.yaml")
    assert not _is_ignored(".sldb/core/store_index.yaml")
    assert not _is_ignored(".sldb/core/models/AtomDoc.yaml")
    assert not _is_ignored(".sldb/core/documents/AtomDoc.yaml")

    assert _is_tracked(".sldb/store.yaml")
    assert _is_tracked(".sldb/core/store_index.yaml")

    assert _is_ignored(".sldb_cache/semantic_index.yaml")
    assert _is_ignored(".sldb_cache/locks/store.lock")

    assert _tracked_under(".sldb/runtime") == []


def _is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", path],
        cwd=ROOT,
        check=False,
    )
    return result.returncode == 0


def _is_tracked(path: str) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", path],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )
    return result.returncode == 0


def _tracked_under(path: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.split()
