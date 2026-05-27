from __future__ import annotations

from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from desk.cli.main import main


def test_cli_help_uses_deskops_name(capsys) -> None:
    result = main(["--help"])

    captured = capsys.readouterr()
    assert result == 0
    assert "usage: deskops" in captured.out
    assert "{inbox,faq,repo,desk}" in captured.out


def test_faq_lists_deskops_questions(capsys) -> None:
    result = main(["faq"])

    captured = capsys.readouterr()
    assert result == 0
    assert "deskops FAQ questions:" in captured.out
    assert "How do I run the CLI correctly?" in captured.out


def test_desk_install_scaffolds_expected_surface(tmp_path: Path, capsys) -> None:
    result = main(["desk", "install", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 0
    assert "Scaffold complete." in captured.out
    assert "Register the repo separately" in captured.out

    expected_paths = [
        tmp_path / "desk" / "tasks" / "Board.md",
        tmp_path / "desk" / "contexts" / "pills.md",
        tmp_path / "desk" / "rituals" / "execution.md",
        tmp_path / "desk" / "rituals" / "testing.md",
        tmp_path / "desk" / "rituals" / "closeout.md",
        tmp_path / "desk" / "inbox",
        tmp_path / "desk" / "drawer" / "README.md",
        tmp_path / "desk" / "drawer" / "atoms",
    ]
    for path in expected_paths:
        assert path.exists()

    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "## Rituals" in board_text
    assert "desk/contexts/pills.md" in board_text


def test_desk_install_is_idempotent(tmp_path: Path, capsys) -> None:
    first = main(["desk", "install", str(tmp_path)])
    first_output = capsys.readouterr()

    second = main(["desk", "install", str(tmp_path)])
    second_output = capsys.readouterr()

    assert first == 0
    assert second == 0
    assert "Wrote" in first_output.out
    assert "Wrote" not in second_output.out


def test_desk_install_rejects_non_directory_target(tmp_path: Path, capsys) -> None:
    target = tmp_path / "not-a-directory.txt"
    target.write_text("placeholder", encoding="utf-8")

    result = main(["desk", "install", str(target)])

    captured = capsys.readouterr()
    assert result == 1
    assert "is not a directory" in captured.out


def test_repo_register_fails_without_store(tmp_path: Path, monkeypatch, capsys) -> None:
    """repo register should fail preflight when no store is available."""
    monkeypatch.chdir(tmp_path)
    result = main(["repo", "register", "test-repo", str(tmp_path)])
    captured = capsys.readouterr()
    assert result == 1
    assert "Error:" in captured.out


def test_repo_register_fails_with_nonexistent_store(tmp_path: Path, capsys) -> None:
    """repo register should fail preflight when --store points nowhere."""
    bad_store = str(tmp_path / "nonexistent" / "store")
    result = main(["repo", "register", "test-repo", str(tmp_path), "--store", bad_store])
    captured = capsys.readouterr()
    assert result == 1
    assert "Error:" in captured.out
