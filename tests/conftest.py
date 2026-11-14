from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# Where the sibling sldb lives for the tests. ``SLDB_SRC`` (the ``src`` directory of an sldb
# checkout) wins and must exist; without it the sibling checkout ``../sldb/src`` is used when it
# exists. The path goes first on ``sys.path`` here, once: conftest loads before any test module,
# also when a single file is run (``python -m pytest tests/<file>``), so no test repeats it.
# Run against another sldb: ``SLDB_SRC=/path/to/sldb/src python -m pytest -q tests/<file>``.
_SIBLING_SLDB_SRC = Path(__file__).resolve().parents[2] / "sldb" / "src"


def resolve_sldb_src() -> Path | None:
    """The sldb ``src`` the tests import: ``$SLDB_SRC``, else the sibling checkout if present."""
    declared = os.environ.get("SLDB_SRC")
    if declared:
        path = Path(declared).expanduser()
        if not path.is_dir():
            raise pytest.UsageError(f"SLDB_SRC={declared} does not exist")
        return path.resolve()
    return _SIBLING_SLDB_SRC if _SIBLING_SLDB_SRC.is_dir() else None


SLDB_SRC = resolve_sldb_src()
if SLDB_SRC is not None and str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--update-golden",
        action="store_true",
        default=False,
        help="Rewrite the committed golden output fixtures from the current behavior.",
    )


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point HOME at a throwaway directory so no test writes the real ~/.sldb.

    Subprocesses inherit the patched environment, so `python -m deskops` also
    builds its global store under the fake home. Git gets a user identity from
    the fake home's .gitconfig; the real one is not consulted.
    """
    home = tmp_path / "home"
    home.mkdir()
    (home / ".gitconfig").write_text(
        "[user]\n\tname = Deskops Test\n\temail = test@example.com\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("HOME", str(home))
    assert Path.home() == home
    return home


def _git(root: Path, *argv: str) -> None:
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True, text=True)


@pytest.fixture(params=["warm", "cold"])
def sldb_cache(request, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Prepare a desk's sldb cache for the run: warm keeps it, cold starts from nothing.

    Cold is the clean-clone case (H1-H3 reproduction): the store's `.sldb_cache/` is gone and
    `XDG_CACHE_HOME` points at an empty directory. Call the fixture with the desk root after it
    exists; it returns whether the run is cold.
    """
    cache_home = tmp_path / "xdg-cache"
    cache_home.mkdir()
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache_home))

    def prepare(root: Path) -> bool:
        cold = request.param == "cold"
        if cold:
            shutil.rmtree(Path(root) / ".sldb_cache", ignore_errors=True)
            shutil.rmtree(cache_home, ignore_errors=True)
            cache_home.mkdir()
        return cold

    return prepare


@pytest.fixture(scope="session")
def _lifecycle_desk_template(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One initialized desk (store, scaffold, lifecycle graph), built once per session."""
    from deskops.atom_tags import sync_tag_declaration
    from deskops.bootstrap import SLDBBootstrap
    from deskops.lifecycle import write_lifecycle_graph
    from deskops.workspace import seed_desk

    root = tmp_path_factory.mktemp("lifecycle-desk-template") / "repo"
    root.mkdir()
    with contextlib.redirect_stdout(io.StringIO()):
        assert SLDBBootstrap().init_local_store(root) == 0
    seed_desk(root)
    write_lifecycle_graph(root)
    # `deskops init` also declares the seeded tag namespaces in .sldb/store.yaml (CC35d resto);
    # without this step the template is not "as deskops init leaves it" and desk update repairs it.
    sync_tag_declaration(root)
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
