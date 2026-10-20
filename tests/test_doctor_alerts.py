"""`deskops doctor` keeps what breaks the desk apart from what only moved.

An error is damage and fails the command. An alert is the store having moved under an expected
change (a document edited, moved or added by hand, a contract that changed): it is always
printed, with the command that registers it, and alone it exits 0. `--repair` acts on errors
only. See `deskops.doctor_findings`.
"""

from __future__ import annotations

import json
from pathlib import Path

from deskops.cli.main import main

from test_doctor_unmodeled_surfaces import _init_repo, _prepare_current_modeled_surfaces, _write


def _store_check_says(monkeypatch, documents: list[dict], **store: object) -> None:
    # A model deskops does not own, so the placeholder Markdown is not read as a TaskDoc.
    payload = {"models": [{"name": "NoteDoc", "documents": documents}], **store}

    class _Result:
        stdout, stderr, returncode = json.dumps(payload), "", 0

    monkeypatch.setattr("deskops.workspace.subprocess.run", lambda *a, **k: _Result())
    monkeypatch.setattr("deskops.cli.commands.doctor.subprocess.run", lambda *a, **k: _Result())


def _desk(tmp_path: Path, capsys) -> tuple[Path, list[dict]]:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    return root, [{"path": p, "note": "ok"} for p in _prepare_current_modeled_surfaces(root)]


def _doctor(root: Path, capsys, *extra: str) -> tuple[int, str]:
    code = main(["doctor", "--root", str(root), *extra])
    return code, capsys.readouterr().out


def test_an_edited_document_is_an_alert_and_the_desk_stays_healthy(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _write(root / "desk" / "tasks" / "task-a.md")
    _store_check_says(monkeypatch, [*docs, {"path": "desk/tasks/task-a.md", "note": "data_mutation"}])
    code, out = _doctor(root, capsys)
    assert code == 0
    assert "Edited: desk/tasks/task-a.md (edited since the store indexed it)" in out
    assert "register edits, moves and new documents with: deskops desk update --apply" in out
    assert "Errors" not in out
    assert "Desk is healthy, with 1 alert(s)." in out


def test_a_document_moved_by_hand_is_one_move_alert_not_a_broken_desk(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _write(root / "desk" / "tasks" / "task-a.md")
    _store_check_says(monkeypatch, [*docs, {"path": "desk/tasks/old/task-a.md", "note": "missing"}])
    code, out = _doctor(root, capsys)
    assert code == 0
    assert "Moved: desk/tasks/old/task-a.md -> desk/tasks/task-a.md" in out
    assert "Not tracked yet" not in out and "gone" not in out


def test_a_tracked_document_that_is_gone_is_an_error(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _store_check_says(monkeypatch, [*docs, {"path": "desk/tasks/task-a.md", "note": "missing"}])
    code, out = _doctor(root, capsys)
    assert code == 1
    assert "Errors (the desk is broken):" in out
    assert "Tracked document is gone: desk/tasks/task-a.md" in out


def test_repair_leaves_alerts_to_desk_update(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _write(root / "desk" / "tasks" / "task-a.md")
    _store_check_says(monkeypatch, [*docs, {"path": "desk/tasks/task-a.md", "note": "data_mutation"}])
    code, out = _doctor(root, capsys, "--repair")
    assert code == 0
    assert "Repairs applied" not in out
    assert "Edited: desk/tasks/task-a.md" in out


def test_store_level_moves_are_alerts_in_old_and_new_sldb_output(tmp_path: Path, monkeypatch, capsys) -> None:
    root, docs = _desk(tmp_path, capsys)
    _store_check_says(monkeypatch, docs, moved_contracts=["TaskDoc"], roster_only=["PillDoc"])
    code, out = _doctor(root, capsys)
    assert code == 0
    assert "model contract changed: TaskDoc" in out
    assert "document list of PillDoc not reindexed" in out

    alerts = [
        {"code": "store/roster-stale", "subject": "PillDoc", "what": "roster not reindexed", "fix": "sldb stores update"},
        # Already reported from the document's own note: not repeated.
        {"code": "store/data-mutation", "subject": "TaskDoc:task-a", "what": "fields changed", "fix": "", "document": "task-a"},
    ]
    errors = [{"code": "store/unimportable_model", "subject": "StepDoc", "what": "model does not import", "fix": ""}]
    _store_check_says(monkeypatch, docs, alerts=alerts, errors=errors)
    code, out = _doctor(root, capsys)
    assert code == 1
    assert "PillDoc: roster not reindexed" in out.split("Alerts")[1]
    assert "StepDoc: model does not import" in out.split("Alerts")[0]
    assert "fields changed" not in out
