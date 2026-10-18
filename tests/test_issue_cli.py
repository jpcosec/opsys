"""`deskops issue close` and `deskops issue list` across the three status formats."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from deskops.cli.main import main


FRONTMATTER_ISSUE = """---
id: issue-frontmatter
status: open
tags:
- system:demo
---

# Frontmatter issue

Body stays.

## Problem

Details stay.
"""

SECTION_ISSUE = """# Section issue

## Status

open (blocked upstream)

## Problem

Details stay.
"""

STATUS_LINE_ISSUE = """# Line issue

ID: issue-line
Status: open

## What

Details stay.
"""


def _write_issue(root: Path, name: str, text: str) -> Path:
    path = root / "desk" / "drawer" / "issues" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _run(capsys: pytest.CaptureFixture[str], *argv: str) -> tuple[int, str, str]:
    code = main(list(argv))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


@pytest.mark.parametrize(
    ("name", "text", "expected_prefix", "issue_id"),
    [
        (
            "issue-frontmatter",
            FRONTMATTER_ISSUE,
            FRONTMATTER_ISSUE.replace("status: open", "status: closed"),
            "issue-frontmatter",
        ),
        (
            "issue-section",
            SECTION_ISSUE,
            SECTION_ISSUE.replace("open (blocked upstream)", "closed"),
            "issue-section",
        ),
        (
            "issue-line",
            STATUS_LINE_ISSUE,
            STATUS_LINE_ISSUE.replace("Status: open", "Status: closed"),
            "issue-line",
        ),
    ],
    ids=("frontmatter", "status-section", "status-line"),
)
def test_close_each_status_format_then_list(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    name: str,
    text: str,
    expected_prefix: str,
    issue_id: str,
) -> None:
    path = _write_issue(tmp_path, name, text)

    code, out, err = _run(
        capsys,
        "issue",
        "close",
        name,
        "--root",
        str(tmp_path),
        "--reason",
        "Fixed by the CLI",
        "--ref",
        "abc1234",
        "--ref",
        "deskops/cli",
    )

    assert code == 0, err
    assert f"Path: {path}" in out
    updated = path.read_text(encoding="utf-8")
    assert path.exists()
    assert updated.split("## Resolution", 1)[0].rstrip() == expected_prefix.rstrip()
    assert f"Closed: {date.today().isoformat()}" in updated
    assert "Reason: Fixed by the CLI" in updated
    assert "Refs: abc1234, deskops/cli" in updated

    code, out, err = _run(capsys, "issue", "list", "--root", str(tmp_path))
    assert code == 0, err
    assert f"{issue_id} | closed |" in out


def test_list_reports_id_status_and_title(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_issue(tmp_path, "issue-open", SECTION_ISSUE.replace("Section issue", "Open issue"))
    _write_issue(
        tmp_path,
        "issue-closed",
        STATUS_LINE_ISSUE.replace("Line issue", "Closed issue").replace(
            "ID: issue-line", "ID: issue-closed"
        ).replace("Status: open", "Status: closed"),
    )

    code, out, err = _run(capsys, "issue", "list", "--root", str(tmp_path), "--status", "open")

    assert code == 0, err
    assert "issue-open | open | Open issue" in out
    assert "issue-closed" not in out

    code, out, err = _run(capsys, "issue", "list", "--root", str(tmp_path), "--status", "closed")
    assert code == 0, err
    assert "issue-closed | closed | Closed issue" in out
    assert "issue-open" not in out

    code, out, err = _run(capsys, "issue", "list", "--root", str(tmp_path), "--status", "all")
    assert code == 0, err
    assert "issue-open" in out
    assert "issue-closed" in out


def test_close_refuses_already_closed_issue_unless_forced(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    text = SECTION_ISSUE.replace("open (blocked upstream)", "closed")
    path = _write_issue(tmp_path, "issue-already-closed", text)

    code, _out, err = _run(
        capsys, "issue", "close", "issue-already-closed", "--root", str(tmp_path), "--reason", "Again"
    )

    assert code == 1
    assert "already closed" in err
    assert path.read_text(encoding="utf-8") == text

    code, _out, err = _run(
        capsys,
        "issue",
        "close",
        "issue-already-closed",
        "--root",
        str(tmp_path),
        "--reason",
        "Closing again",
        "--force",
    )

    assert code == 0, err
    updated = path.read_text(encoding="utf-8")
    assert "Reason: Closing again" in updated
    assert "## Resolution" in updated


def test_close_unknown_selector_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_issue(tmp_path, "issue-known", SECTION_ISSUE)

    code, _out, err = _run(
        capsys, "issue", "close", "issue-missing", "--root", str(tmp_path), "--reason", "Nope"
    )

    assert code == 1
    assert "issue-missing" in err


def test_close_unreadable_status_names_the_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = _write_issue(tmp_path, "issue-no-status", "# No status\n\n## Status\n\nnarrative text\n")

    code, _out, err = _run(
        capsys, "issue", "close", "issue-no-status", "--root", str(tmp_path), "--reason", "Nope"
    )

    assert code == 1
    assert "No recognizable status" in err
    assert path.name in err
    assert "## Resolution" not in path.read_text(encoding="utf-8")


def test_close_rejects_empty_reason(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = _write_issue(tmp_path, "issue-reason", SECTION_ISSUE)

    code, _out, err = _run(
        capsys, "issue", "close", "issue-reason", "--root", str(tmp_path), "--reason", "   "
    )

    assert code == 1
    assert "non-empty --reason" in err
    assert "## Resolution" not in path.read_text(encoding="utf-8")


def test_close_finds_issue_under_desk_issues(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "desk" / "issues" / "issue-active.md"
    path.parent.mkdir(parents=True)
    path.write_text(STATUS_LINE_ISSUE, encoding="utf-8")

    code, out, err = _run(
        capsys, "issue", "close", "issue-active", "--root", str(tmp_path), "--reason", "Done"
    )

    assert code == 0, err
    assert f"Path: {path}" in out
    assert "Status: closed" in path.read_text(encoding="utf-8")
