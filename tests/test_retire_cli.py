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
    pill = _add_pill(root)
    relative = pill.relative_to(root).as_posix()
    # A mention in prose (the path, read by the desk graph's SOURCE_PATH pattern) is never rewritten.
    guide = root / "desk" / "tasks" / "task-guide.md"
    guide.write_text(f"# Guide\n\nSee {relative} for the old guardrail.\n", encoding="utf-8")
    capsys.readouterr()

    assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD")) == 1
    captured = capsys.readouterr()
    assert "still referenced by desk/tasks/task-guide.md" in captured.out + captured.err
    assert pill.exists()

    assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD"), "--force") == 0
    assert not pill.exists()
    assert relative in guide.read_text(encoding="utf-8")


def _pill_routed_by_board_and_two_tasks(root: Path) -> tuple[str, list[Path]]:
    pill = _add_pill(root)
    relative = pill.relative_to(root).as_posix()
    assert main(["edit", "board", "Board", "pills", json.dumps([relative]), "--root", str(root)]) == 0
    tasks = []
    for name in ("one", "two"):
        assert main(["add", "task", "--root", str(root), "--title", f"Pill user {name}", "--task-type", "task.docs"]) == 0
        task = root / "desk" / "tasks" / f"task-pill-user-{name}.md"
        assert main(["edit", "task", task.stem, "pills", json.dumps([relative]), "--root", str(root)]) == 0
        assert relative in task.read_text(encoding="utf-8")
        tasks.append(task)
    return relative, tasks


def _desk_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for base in (root / "desk", root / ".sldb")
        for path in sorted(base.rglob("*"))
        if path.is_file()
    }


def test_retire_removes_a_pill_from_the_board_and_two_tasks_in_one_transaction(tmp_path: Path, capsys, monkeypatch) -> None:
    from contextlib import contextmanager

    from deskops import doc_access

    root = _repo(tmp_path)
    relative, tasks = _pill_routed_by_board_and_two_tasks(root)
    board = root / "desk" / "tasks" / "Board.md"
    capsys.readouterr()

    original = doc_access.desk_transaction
    depth = [0]
    opened: list[Path] = []

    @contextmanager
    def counting(block_root: Path):
        if depth[0] == 0:
            opened.append(block_root)
        depth[0] += 1
        try:
            with original(block_root) as tx:
                yield tx
        finally:
            depth[0] -= 1

    monkeypatch.setattr(doc_access, "desk_transaction", counting)
    assert _retire(root, relative, "--ref", _git(root, "rev-parse", "HEAD")) == 0
    out = capsys.readouterr().out

    assert len(opened) == 1
    for path in (board, *tasks):
        assert f"Unrouted from {path.relative_to(root).as_posix()}" in out
        text = path.read_text(encoding="utf-8")
        assert relative not in text
        assert "pill-old-guardrail" not in text
    assert not (root / relative).exists()
    monkeypatch.undo()
    check = _store_check(root)
    assert check.returncode == 0, check.stdout + check.stderr


def test_retire_failing_midway_leaves_the_desk_and_store_unchanged(tmp_path: Path, monkeypatch) -> None:
    import pytest

    from deskops import doc_access
    from deskops.services.retire import retire_document

    root = _repo(tmp_path)
    relative, _ = _pill_routed_by_board_and_two_tasks(root)
    before = _desk_bytes(root)

    def failing_delete(*_args, **_kwargs):
        raise RuntimeError("forced failure after the Board and the tasks were rewritten")

    monkeypatch.setattr(doc_access, "delete_doc", failing_delete)
    with pytest.raises(RuntimeError, match="forced failure"):
        retire_document(root, relative, "Describes a retired surface", [_git(root, "rev-parse", "HEAD")])

    assert _desk_bytes(root) == before


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
