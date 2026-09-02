from __future__ import annotations

import json
from pathlib import Path

from deskops.cli.main import main
from deskops.workspace import desk_doc_is_modeled_by_sldb


def _init_repo(root: Path, capsys) -> None:
    root.mkdir()
    assert main(["init", str(root)]) == 0
    capsys.readouterr()


def _write(path: Path, content: str = "# Note\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _seed_unmodeled_docs(root: Path) -> None:
    _write(root / "desk" / "drawer" / "features" / "future-work.md")
    _write(root / "desk" / "drawer" / "issues" / "issue-loose-problem.md")
    _write(root / "desk" / "drawer" / "stress-tests" / "st-01.md")
    _write(root / "desk" / "inbox" / "20260902-000000-suggestion-ignore-me.md")
    _write(root / "desk" / "issues" / "issue-non-modeled.md")
    _write(root / "desk" / "features" / "future-surface.md")
    _write(root / "desk" / "logbook" / "README.md")
    _write(root / "desk" / "METHODOLOGY.md")


def _mock_store_check(monkeypatch, tracked_docs: list[str]) -> None:
    payload = {
        "models": [
            {
                "documents": [{"path": path, "note": "ok"} for path in tracked_docs],
            }
        ]
    }

    class _Result:
        def __init__(self) -> None:
            self.stdout = json.dumps(payload)
            self.stderr = ""
            self.returncode = 0

    def _fake_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        return _Result()

    monkeypatch.setattr("deskops.workspace.subprocess.run", _fake_run)
    monkeypatch.setattr("deskops.cli.commands.doctor.subprocess.run", _fake_run)


def _prepare_current_modeled_surfaces(root: Path) -> list[str]:
    _write(root / "desk" / "rituals" / "phase.md", "# Phase\n")
    return [
        "desk/tasks/Board.md",
        "desk/contexts/pills.md",
        "desk/rituals/execution.md",
        "desk/rituals/testing.md",
        "desk/rituals/closeout.md",
        "desk/rituals/phase.md",
    ]


def test_workspace_classifies_unmodeled_and_modeled_desk_docs(tmp_path: Path) -> None:
    root = tmp_path / "project"
    desk_dir = root / "desk"

    unmodeled_paths = [
        desk_dir / "drawer" / "features" / "future-work.md",
        desk_dir / "drawer" / "issues" / "issue-loose-problem.md",
        desk_dir / "drawer" / "stress-tests" / "st-01.md",
        desk_dir / "inbox" / "20260902-000000-suggestion-ignore-me.md",
        desk_dir / "issues" / "issue-non-modeled.md",
        desk_dir / "features" / "future-surface.md",
        desk_dir / "logbook" / "README.md",
        desk_dir / "METHODOLOGY.md",
    ]
    modeled_paths = [
        desk_dir / "tasks" / "task-real.md",
        desk_dir / "contexts" / "pill-real.md",
        desk_dir / "rituals" / "phase.md",
    ]

    for path in unmodeled_paths:
        assert desk_doc_is_modeled_by_sldb(root, path) is False
    for path in modeled_paths:
        assert desk_doc_is_modeled_by_sldb(root, path) is True


def test_doctor_ignores_intentionally_unmodeled_surfaces(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    tracked_docs = _prepare_current_modeled_surfaces(root)
    _mock_store_check(monkeypatch, tracked_docs)
    _seed_unmodeled_docs(root)

    assert main(["doctor", "--root", str(root)]) == 0
    out, _ = capsys.readouterr()
    assert "Desk is healthy. No issues found." in out
    assert "Untracked" not in out


def test_doctor_reports_only_untracked_sldb_modeled_surfaces(tmp_path: Path, monkeypatch, capsys) -> None:
    root = tmp_path / "project"
    _init_repo(root, capsys)
    tracked_docs = _prepare_current_modeled_surfaces(root)
    _mock_store_check(monkeypatch, tracked_docs)
    _seed_unmodeled_docs(root)
    _write(root / "desk" / "tasks" / "untracked-task.md", "# Untracked\n")

    assert main(["doctor", "--root", str(root)]) == 1
    out, _ = capsys.readouterr()

    assert "Untracked desk documents: desk/tasks/untracked-task.md" in out
    assert "These are SLDB-modeled surfaces with broken tracking/state, not intentionally unmodeled desk notes." in out
    assert "Ignored by design:" in out
    assert "desk/drawer/** is intentionally not SLDB-modeled" in out
    assert "desk/inbox/** is intentionally not SLDB-modeled" in out
    assert "desk/issues/** is intentionally not SLDB-modeled" in out
    assert "desk/features/** is intentionally not SLDB-modeled" in out
    assert "desk/logbook/** is intentionally not SLDB-modeled" in out
    assert "desk/METHODOLOGY.md is a top-level desk note intentionally not SLDB-modeled" in out
    assert "desk/drawer/features/future-work.md" not in out
    assert "desk/inbox/20260902-000000-suggestion-ignore-me.md" not in out
    assert "desk/issues/issue-non-modeled.md" not in out
    assert "desk/features/future-surface.md" not in out
    assert "desk/logbook/README.md" not in out
