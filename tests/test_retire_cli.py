from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from deskops.cli.main import main


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")
    return root


def _retire(root: Path, path: str, *extra: str) -> int:
    return main(["retire", path, "--root", str(root), "--reason", "Describes a retired surface", *extra])


def _store_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "sldb", "stores", "check", "--store", str(root / ".sldb")],
        capture_output=True,
        text=True,
    )


def _add_pill(root: Path, title: str = "Old guardrail") -> Path:
    assert main(["add", "pill", "--root", str(root), "--title", title, "--what", "w", "--why", "y", "--when", "n", "--where", "e", "--how", "h", "--how-not", "x"]) == 0
    return next((root / "desk" / "contexts").glob(f"pill-{title.lower().replace(' ', '-')}*.md"))


def test_add_pill_tracks_the_created_document(tmp_path: Path, capsys) -> None:
    from sldb.api import doc_status

    root = _repo(tmp_path)
    pill = _add_pill(root)
    relative = pill.relative_to(root).as_posix()
    capsys.readouterr()

    assert doc_status(root / ".sldb", relative).exists
    assert main(["doctor", "--root", str(root)]) == 0
    assert "Desk is healthy" in capsys.readouterr().out


def test_add_pill_from_yaml_needs_no_field_flags(tmp_path: Path) -> None:
    from sldb.api import doc_status

    root = _repo(tmp_path)
    payload = tmp_path / "pill.yaml"
    payload.write_text(
        "title: YAML pill\nwhat: w\nwhy: y\nwhen: n\nwhere: e\nhow: h\nhow_not: x\n",
        encoding="utf-8",
    )

    assert main(["add", "pill", "--from-yaml", str(payload), "--root", str(root)]) == 0

    pill = root / "desk" / "contexts" / "pill-yaml-pill.md"
    assert pill.exists()
    assert doc_status(root / ".sldb", "desk/contexts/pill-yaml-pill.md").exists


def test_retire_unroutes_a_board_routed_pill_and_keeps_the_store_green(tmp_path: Path, capsys) -> None:
    from sldb.api import doc_status

    root = _repo(tmp_path)
    pill = _add_pill(root)
    relative = pill.relative_to(root).as_posix()
    assert main(["edit", "board", "Board", "pills", json.dumps([relative]), "--root", str(root)]) == 0
    board = root / "desk" / "tasks" / "Board.md"
    assert relative in board.read_text(encoding="utf-8")
    capsys.readouterr()

    assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD")) == 0
    out = capsys.readouterr().out

    assert "Unrouted from desk/tasks/Board.md" in out
    assert not pill.exists()
    assert relative not in board.read_text(encoding="utf-8")
    assert not doc_status(root / ".sldb", relative).exists
    assert main(["doctor", "--root", str(root)]) == 0
    check = _store_check(root)
    assert check.returncode == 0
    assert "PASS" in check.stdout


def test_retire_removes_a_tracked_pill_and_its_store_record(tmp_path: Path, capsys) -> None:
    from sldb.api import doc_status

    root = _repo(tmp_path)
    pill = _add_pill(root)
    relative = pill.relative_to(root).as_posix()
    assert doc_status(root / ".sldb", relative).exists
    capsys.readouterr()

    assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD")) == 0
    out = capsys.readouterr().out

    assert f"Retired {relative}" in out
    assert "Reason: Describes a retired surface" in out
    assert not pill.exists()
    assert not doc_status(root / ".sldb", relative).exists


def test_retire_refuses_while_referenced_unless_forced(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    note = root / "desk" / "logbook" / "old-note.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text("# Old note\n", encoding="utf-8")
    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "guide.md").write_text("See desk/logbook/old-note.md.\n", encoding="utf-8")
    capsys.readouterr()

    assert _retire(root, "desk/logbook/old-note.md", "--ref", "docs/guide.md") == 1
    captured = capsys.readouterr()
    assert "docs/guide.md" in captured.out + captured.err
    assert note.exists()

    assert _retire(root, "desk/logbook/old-note.md", "--ref", "docs/guide.md", "--force") == 0
    assert not note.exists()


def test_retire_points_tasks_and_drawer_entries_at_their_own_verbs(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    assert _retire(root, "desk/tasks/Board.md", "--ref", _git(root, "rev-parse", "HEAD")) == 1
    captured = capsys.readouterr()
    assert "closeout" in captured.out + captured.err


def test_retire_refuses_required_desk_structure(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    for relative in ("desk/rituals/phase.md", "desk/config.json"):
        assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD")) == 1
        captured = capsys.readouterr()
        assert "required desk structure" in captured.out + captured.err
        assert (root / relative).exists()


def test_retire_refuses_an_unresolvable_ref_and_keeps_the_file(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    leftover = root / "desk" / "models" / "__init__.py"
    leftover.parent.mkdir(parents=True, exist_ok=True)
    leftover.write_text("", encoding="utf-8")

    assert _retire(root, "desk/models/__init__.py", "--ref", "deadbeef") == 1
    assert leftover.exists()
    assert _retire(root, "desk/models/__init__.py", "--ref", _git(root, "rev-parse", "HEAD")) == 0
    assert not leftover.exists()


def _drawer_issue(root: Path, stem: str, status: str) -> Path:
    issue = root / "desk" / "drawer" / "issues" / f"{stem}.md"
    issue.parent.mkdir(parents=True, exist_ok=True)
    issue.write_text(f"# {stem}\n\n## Status\n\n{status}\n", encoding="utf-8")
    board = root / "desk" / "drawer" / "tasks" / "Board.md"
    board.parent.mkdir(parents=True, exist_ok=True)
    existing = board.read_text(encoding="utf-8") if board.exists() else "# Drawer\n\n"
    board.write_text(existing + f"- `{stem}` — an issue\n", encoding="utf-8")
    return issue


def test_retire_takes_a_closed_drawer_issue_and_its_board_bullet(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    issue = _drawer_issue(root, "issue-done", "closed")
    capsys.readouterr()

    assert _retire(root, "desk/drawer/issues/issue-done.md", "--ref", _git(root, "rev-parse", "HEAD")) == 0
    out = capsys.readouterr().out

    assert not issue.exists()
    assert "issue-done" not in (root / "desk" / "drawer" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/drawer/tasks/Board.md" in out


def test_retire_refuses_an_open_drawer_issue(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    issue = _drawer_issue(root, "issue-live", "open")
    capsys.readouterr()

    assert _retire(root, "desk/drawer/issues/issue-live.md", "--ref", _git(root, "rev-parse", "HEAD")) == 1
    captured = capsys.readouterr()
    assert "issue close" in captured.out + captured.err
    assert issue.exists()


def test_retire_takes_an_archived_record_issue(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    record = root / "desk" / "drawer" / "issues" / "diagnosis-archive.md"
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text("---\nrecord: true\n---\n\n# Archive\n", encoding="utf-8")

    assert _retire(root, "desk/drawer/issues/diagnosis-archive.md", "--ref", _git(root, "rev-parse", "HEAD")) == 0
    assert not record.exists()
