from __future__ import annotations

import subprocess
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


def test_retire_removes_a_tracked_pill_and_its_store_record(tmp_path: Path, capsys) -> None:
    from sldb.api import doc_status

    root = _repo(tmp_path)
    assert main(["add", "pill", "--root", str(root), "--title", "Old guardrail", "--what", "w", "--why", "y", "--when", "n", "--where", "e", "--how", "h", "--how-not", "x"]) == 0
    main(["desk", "update", "--root", str(root), "--apply"])
    pill = next((root / "desk" / "contexts").glob("pill-old-guardrail*.md"))
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


def test_retire_refuses_an_unresolvable_ref_and_keeps_the_file(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    leftover = root / "desk" / "models" / "__init__.py"
    leftover.parent.mkdir(parents=True, exist_ok=True)
    leftover.write_text("", encoding="utf-8")

    assert _retire(root, "desk/models/__init__.py", "--ref", "deadbeef") == 1
    assert leftover.exists()
    assert _retire(root, "desk/models/__init__.py", "--ref", _git(root, "rev-parse", "HEAD")) == 0
    assert not leftover.exists()
