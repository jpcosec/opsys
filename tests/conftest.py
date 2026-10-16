from __future__ import annotations

import contextlib
import io
import shutil
import subprocess
from pathlib import Path

import pytest


def _git(root: Path, *argv: str) -> None:
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True)


@pytest.fixture(scope="session")
def _lifecycle_desk_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One initialized desk (store, scaffold, lifecycle graph), built once per session."""
    from deskops.bootstrap import SLDBBootstrap
    from deskops.lifecycle import ensure_lifecycle_graph
    from deskops.workspace import scaffold_desk

    root = tmp_path_factory.mktemp("lifecycle-desk-template") / "repo"
    root.mkdir()
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(root) == 0
    scaffold_desk(root)
    ensure_lifecycle_graph(root)
    return root


@pytest.fixture
def lifecycle_desk(tmp_path: Path, _lifecycle_desk_template: Path) -> Path:
    """A git repo (one empty seed commit; the desk itself is not committed) whose store
    carries the lifecycle graph, as `deskops init` leaves it."""
    root = tmp_path / "repo"
    shutil.copytree(_lifecycle_desk_template, root)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "test@example.com")
    _git(root, "config", "user.name", "Test")
    _git(root, "commit", "--allow-empty", "-q", "-m", "seed")
    return root
