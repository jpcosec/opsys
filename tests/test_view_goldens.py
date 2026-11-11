"""`deskops view board|task|drawer|inbox --format json` against goldens (CC34 a3).

The goldens were captured before the views moved to sldb ViewDocs, on the fixed desk of
``tests/view_desk.py``; only revisions and dates are normalized (c4). Run with
``--update-golden`` to rewrite them.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from deskops.cli.main import main
from tests.view_desk import GOLDEN_TASK
from tests.view_desk import build_view_desk
from tests.view_desk import normalize_view

GOLDEN_DIR = Path(__file__).parent / "fixtures" / "golden" / "output"
VIEWS = {
    "view_board": ["view", "board"],
    "view_task": ["view", "task", GOLDEN_TASK],
    "view_drawer": ["view", "drawer"],
    "view_inbox": ["view", "inbox"],
}


@pytest.fixture
def view_desk(lifecycle_desk: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    build_view_desk(lifecycle_desk, monkeypatch)
    return lifecycle_desk


def _view_json(capsys: pytest.CaptureFixture[str], root: Path, argv: list[str]) -> dict:
    capsys.readouterr()
    assert main([*argv, "--root", str(root), "--format", "json"]) == 0
    return json.loads(capsys.readouterr().out)


def test_view_json_goldens(view_desk: Path, capsys: pytest.CaptureFixture[str], request: pytest.FixtureRequest) -> None:
    update = request.config.getoption("--update-golden")
    for name, argv in VIEWS.items():
        actual = json.dumps(normalize_view(_view_json(capsys, view_desk, argv), view_desk), indent=2, sort_keys=True) + "\n"
        path = GOLDEN_DIR / f"{name}.json"
        if update:
            path.write_text(actual, encoding="utf-8")
            continue
        assert path.exists(), f"missing golden {path}; run pytest --update-golden"
        assert actual == path.read_text(encoding="utf-8"), f"golden mismatch: {name}"
