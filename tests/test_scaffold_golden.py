"""Golden of the desk scaffold (CC36).

Two captures taken with the code before the scaffold moved to declared seeds, kept so the move
cannot change what a desk looks like:

- ``init.json``: every file ``deskops init`` writes under ``desk/`` for a desk named
  ``golden-desk`` (project-relative path and sha256).
- ``update.json``: the report of ``deskops desk update --apply`` over a copy of the old test
  desk ``tests/fixtures/golden_desk`` (its lines, normalized and sorted, because the order of the
  tracking lines follows a set) and the tree it leaves under ``desk/``.

Run ``pytest tests/test_scaffold_golden.py --update-golden`` only to capture a change the
acceptance of a task names; the fixture desk itself is never modified.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import shutil
from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.paths import package_pythonpath

ROOT = Path(__file__).resolve().parents[1]
GOLDEN_DIR = ROOT / "tests" / "fixtures" / "golden" / "scaffold"
FIXTURE_DESK = ROOT / "tests" / "fixtures" / "golden_desk"
INIT_DESK_NAME = "golden-desk"
UPDATE_DESK_NAME = FIXTURE_DESK.name

_UNTRACKED_LINE = re.compile(r"^(- Untracked desk documents: )(.*)$")


def _run(argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


def _tree(root: Path) -> dict[str, str]:
    """``{project-relative path: sha256}`` of every file under ``root/desk``."""
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted((root / "desk").rglob("*"))
        if path.is_file()
    }


def _normalize_report(out: str, root: Path) -> list[str]:
    owner_store = str(Path(package_pythonpath()) / ".sldb")
    lines: list[str] = []
    for line in out.splitlines():
        line = line.replace(str(root), "<root>").replace(owner_store, "<owner-store>")
        match = _UNTRACKED_LINE.match(line)
        if match:
            line = match.group(1) + ", ".join(sorted(match.group(2).split(", ")))
        if line.strip():
            lines.append(line)
    return sorted(lines)


def capture_init(tmp_path: Path) -> dict:
    root = tmp_path / INIT_DESK_NAME
    root.mkdir()
    code, out = _run(["init", str(root)])
    assert code == 0, out
    return {"desk_name": INIT_DESK_NAME, "files": _tree(root)}


def capture_update(tmp_path: Path) -> tuple[dict, Path]:
    root = tmp_path / UPDATE_DESK_NAME
    shutil.copytree(FIXTURE_DESK, root)
    code, out = _run(["desk", "update", "--root", str(root), "--apply"])
    assert code == 0, out
    return {"desk_name": UPDATE_DESK_NAME, "report": _normalize_report(out, root), "files": _tree(root)}, root


def _check_golden(request: pytest.FixtureRequest, name: str, actual: dict) -> None:
    path = GOLDEN_DIR / name
    rendered = json.dumps(actual, indent=2, sort_keys=True) + "\n"
    if request.config.getoption("--update-golden"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
        return
    assert path.exists(), f"missing golden {path}; run pytest tests/test_scaffold_golden.py --update-golden"
    assert json.loads(path.read_text(encoding="utf-8")) == actual


def test_init_writes_the_golden_desk(tmp_path: Path, request: pytest.FixtureRequest) -> None:
    _check_golden(request, "init.json", capture_init(tmp_path))


def test_desk_update_apply_on_the_old_desk_matches_the_golden(tmp_path: Path, request: pytest.FixtureRequest) -> None:
    actual, _root = capture_update(tmp_path)
    _check_golden(request, "update.json", actual)


def test_a_second_desk_update_apply_changes_nothing(tmp_path: Path) -> None:
    actual, root = capture_update(tmp_path)
    code, out = _run(["desk", "update", "--root", str(root), "--apply"])
    assert code == 0, out
    assert out.strip() == "Desk is up to date."
    assert _tree(root) == actual["files"]
