"""The fixed desk the `deskops view` goldens are captured on (CC34 a3, b6, c3).

Three board tasks, one per lifecycle node (`ritual-execution`, `ritual-testing`,
`ritual-closeout`), one drawer task and one inbox note, all written through deskops (the
inbox clock is fixed, so note ids and dates are stable). What still varies between runs
(the root path, revisions, the timestamps sldb and the receipts stamp) is normalized by
``normalize_view`` to fixed markers before comparing with the goldens.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from deskops.cli.main import main
from deskops.operations import DeskopsOperations
from tests.activation_receipts import accept_receipts

#: The seed ViewDocs of the package (DA4: they live only there).
VIEWS_DIR = Path(__file__).resolve().parents[1] / "deskops" / "data" / "views"

#: The task `deskops view task <id>` is captured on (c3).
GOLDEN_TASK = "task-view-golden-execution"
NOTE_CLOCK = (datetime(2026, 11, 4, 10, 15, 0), datetime(2026, 11, 4, 10, 16, 0))

_ISO = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?")
_REVISION_KEYS = {"revision"}
_DATE_KEYS = {"date", "acknowledged_at", "created_at", "at"}


def _task(ops: DeskopsOperations, title: str, **extra: Any) -> str:
    payload = {
        "title": title,
        "goal": f"goal of {title}",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest -q tests/test_x.py"],
        "task_type": "code",
        **extra,
    }
    return ops.create_task_bundle(payload).task_id


def _fixed_clock(monkeypatch: pytest.MonkeyPatch, moment: datetime) -> None:
    import deskops.cli.commands.message as message

    class _Clock(datetime):
        @classmethod
        def now(cls, tz: Any = None) -> datetime:  # noqa: ARG003 - same signature
            return moment

    monkeypatch.setattr(message, "datetime", _Clock)


def build_view_desk(root: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Fill the initialized desk at ``root`` (a ``lifecycle_desk``) with the golden content."""
    monkeypatch.chdir(root)
    ops = DeskopsOperations(root)
    pill = ops.create_artifact(
        "artifact.pill",
        {
            "title": "Guardrail: view pill",
            "what": "what text",
            "why": "why text",
            "when": "when text",
            "where": "where text",
            "how": "how text",
            "how_not": "how not text",
            "tags": ["topic:view"],
        },
    ).doc_id
    atom = ops.create_artifact(
        "artifact.atom",
        {"title": "Atom for the view", "five_wh_one_plus": "what", "answer": "the answer", "tags": ["topic:view"]},
    ).doc_id
    execution = _task(ops, "View golden execution", pills=[pill], atoms=[atom])
    testing = _task(ops, "View golden testing", pills=["pill-does-not-exist"], atoms=["atom-does-not-exist"])
    closeout = _task(ops, "View golden closeout", references=["tests/test_x.py"])
    for task in (testing, closeout):
        accept_receipts(root, task)
        ops.advance_task(task)
    ops.advance_task(closeout)

    _fixed_clock(monkeypatch, NOTE_CLOCK[0])
    assert main(["message", "send", "--root", str(root), "--title", "Deferred idea", "--kind", "suggestion", "Body of the idea"]) == 0
    deferred = next((root / "desk" / "inbox").glob("*-deferred-idea.md"))
    assert main(["promote", "inbox-to-drawer-task", deferred.stem, "--root", str(root)]) == 0
    _fixed_clock(monkeypatch, NOTE_CLOCK[1])
    assert main(["message", "send", "--root", str(root), "--title", "Open question", "--kind", "unclear", "Question body"]) == 0
    monkeypatch.setattr("deskops.cli.commands.message.datetime", datetime)
    install_views(root)
    assert execution == GOLDEN_TASK
    return {"execution": execution, "testing": testing, "closeout": closeout, "pill": pill, "atom": atom}


def install_views(root: Path) -> list[str]:
    """Track the package's seed ViewDocs in the test desk's own store, under ``views/``.

    The real desks reach them through a link to the deskops store (b2); sldb's ``run_view``
    does not resolve a ViewDoc of a linked store yet (H9), so the tests track a copy locally.
    The copy is made through sldb (``add_model`` + ``create_document``), never by hand."""
    from sldb import api
    from sldb.core.exceptions import SLDBModelError
    from sldb.models.notation.view_doc import ViewDoc
    from sldb.runtime.validation import extract_model_data

    store = root / ".sldb"
    try:
        api.add_model(store, "sldb.models.notation_models:ViewDoc", "")
    except SLDBModelError:  # already registered
        pass
    (root / "views").mkdir(exist_ok=True)
    names = []
    for seed in sorted(VIEWS_DIR.glob("*.md")):
        payload = ViewDoc.model_validate(extract_model_data(ViewDoc, seed.read_text(encoding="utf-8"))).model_dump()
        api.create_document(store, "ViewDoc", root / "views" / seed.name, payload, payload["name"], "")
        names.append(payload["name"])
    return names


def normalize_view(value: Any, root: Path) -> Any:
    """The view with the root path, every revision and every date replaced by fixed markers (c4)."""
    if isinstance(value, dict):
        return {
            key: "<revision>" if key in _REVISION_KEYS and isinstance(item, str)
            else "<date>" if key in _DATE_KEYS and isinstance(item, str)
            else normalize_view(item, root)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [normalize_view(item, root) for item in value]
    if isinstance(value, str):
        return _ISO.sub("<date>", value.replace(str(root), "<root>"))
    return value
