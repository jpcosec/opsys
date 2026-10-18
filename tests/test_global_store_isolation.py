from __future__ import annotations

import hashlib
import os
from pathlib import Path
import pwd
import subprocess
import sys

REAL_HOME = Path(pwd.getpwuid(os.getuid()).pw_dir)


def _store_index_hash() -> str | None:
    index = REAL_HOME / ".sldb" / "core" / "store_index.yaml"
    if not index.exists():
        return None
    return hashlib.sha256(index.read_bytes()).hexdigest()


def test_home_is_isolated_from_the_real_home() -> None:
    assert Path.home() != REAL_HOME
    assert Path.home().is_dir()
    assert (Path.home() / ".gitconfig").exists()


def test_deskops_init_does_not_touch_the_real_global_store(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    before = _store_index_hash()

    result = subprocess.run(
        [sys.executable, "-m", "deskops", "init", str(root)],
        cwd=root,
        capture_output=True,
        text=True,
        env={**os.environ},
    )

    assert result.returncode == 0, result.stderr or result.stdout
    assert _store_index_hash() == before
    assert (Path.home() / ".sldb" / "core" / "store_index.yaml").exists()
