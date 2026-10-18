"""Execute the operator manual's runnable examples against the real CLI.

The manual at ``docs/operator-manual.md`` marks executable blocks with the
``bash runnable`` info string. This test extracts those blocks in document
order and runs them in one sandbox repository created under ``tmp_path``. The
sandbox has its own ``HOME`` (so ``deskops bootstrap`` builds a throwaway
global store), its own git repository, and a ``deskops`` shim that runs this
checkout's package instead of any installed copy.

A failing block fails the test with the block index, command text, stdout and
stderr. That keeps the manual from drifting away from the CLI.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
MANUAL = REPO_ROOT / "docs" / "operator-manual.md"
RUNNABLE_BLOCK = re.compile(
    r"^```bash runnable[ \t]*\n(.*?)^```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
MINIMUM_RUNNABLE_BLOCKS = 15


def _runnable_blocks(text: str) -> list[str]:
    return [match.group(1) for match in RUNNABLE_BLOCK.finditer(text)]


def _git(root: Path, *argv: str, env: dict[str, str] | None = None) -> None:
    subprocess.run(
        ["git", *argv], cwd=root, env=env, check=True, capture_output=True, text=True
    )


def _sandbox(tmp_path: Path) -> tuple[Path, Path, dict[str, str]]:
    root = tmp_path / "repo"
    home = tmp_path / "home"
    bin_dir = tmp_path / "bin"
    root.mkdir(exist_ok=True)
    home.mkdir(exist_ok=True)
    bin_dir.mkdir(exist_ok=True)

    # The shim keeps every manual example spelled `deskops ...` while running
    # this checkout. A bare console script would resolve to an installed copy.
    shim = bin_dir / "deskops"
    shim.write_text(
        "#!/bin/sh\n" f"exec {shlex.quote(sys.executable)} -m deskops \"$@\"\n",
        encoding="utf-8",
    )
    shim.chmod(0o755)

    (home / ".gitconfig").write_text(
        "[user]\n\tname = Operator Manual Test\n\temail = manual@example.invalid\n",
        encoding="utf-8",
    )

    env = dict(os.environ)
    env.update(
        {
            "HOME": str(home),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "PYTHONPATH": str(REPO_ROOT),
            "PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}",
            "GIT_AUTHOR_NAME": "Operator Manual Test",
            "GIT_AUTHOR_EMAIL": "manual@example.invalid",
            "GIT_COMMITTER_NAME": "Operator Manual Test",
            "GIT_COMMITTER_EMAIL": "manual@example.invalid",
        }
    )

    _git(root, "init", "-q", env=env)
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed", env=env)
    return root, home, env


def test_operator_manual_runnable_examples_execute_in_order(tmp_path: Path) -> None:
    if not MANUAL.is_file():
        pytest.fail(f"operator manual is missing: {MANUAL}")

    blocks = _runnable_blocks(MANUAL.read_text(encoding="utf-8"))
    assert len(blocks) >= MINIMUM_RUNNABLE_BLOCKS, (
        f"expected at least {MINIMUM_RUNNABLE_BLOCKS} runnable blocks in {MANUAL}, "
        f"found {len(blocks)}"
    )

    root, _home, env = _sandbox(tmp_path)

    for index, block in enumerate(blocks, start=1):
        result = subprocess.run(
            ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", block],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            timeout=900,
        )
        assert result.returncode == 0, (
            f"runnable block {index} failed (exit {result.returncode})\n"
            f"--- block ---\n{block}\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )
