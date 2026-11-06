"""The lifecycle gates have no CLI escape hatch (D2, DC4).

`deskops advance` only fires a transition whose condition holds, and the
`status`, `current_node`, `history`, `task_type` and `closeout_evidence`
fields are written by the workflow commands, not by `edit task`.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops.cli.main import main


TASK_ID = "task-escape-hatch"


def _add_task(root: Path, capsys) -> None:
    result = main(
        [
            "add",
            "task",
            "--root",
            str(root),
            "--title",
            "Escape hatch",
            "--task-type",
            "task.code",
            "--goal",
            "Exercise the lifecycle gates.",
            "--scope",
            "One task in a sandbox desk.",
            "--implementation-path",
            "None.",
            "--done-when",
            "The gate refuses the shortcut.",
            "--validation",
            "pytest",
        ]
    )
    capsys.readouterr()
    assert result == 0


def _task_path(root: Path) -> Path:
    return root / "desk" / "tasks" / f"{TASK_ID}.md"


def test_advance_to_is_a_usage_error(lifecycle_desk: Path, capsys) -> None:
    _add_task(lifecycle_desk, capsys)

    result = main(
        ["advance", "task", TASK_ID, "--to", "ritual-testing", "--root", str(lifecycle_desk)]
    )

    captured = capsys.readouterr()
    assert result == 2
    assert "unrecognized arguments: --to ritual-testing" in captured.err
    assert "Status: draft" not in captured.out


def test_advance_help_does_not_mention_to(capsys) -> None:
    result = main(["advance", "task", "--help"])

    output = capsys.readouterr().out
    assert result == 0
    assert "--to" not in output


@pytest.mark.parametrize(
    ("field", "value", "writer"),
    [
        (
            "status",
            "closed",
            "deskops advance (transition effects) and deskops closeout commit",
        ),
        ("current_node", "ritual-testing", "deskops advance"),
        ("history", "[]", "deskops advance and deskops closeout (append-only)"),
        (
            "task_type",
            "task.docs",
            "deskops add task --task-type (create a new task to change the type)",
        ),
        (
            "closeout_evidence",
            "[]",
            "the task type, and deskops add task --evidence at creation",
        ),
    ],
)
def test_edit_task_refuses_lifecycle_fields(
    lifecycle_desk: Path,
    capsys,
    field: str,
    value: str,
    writer: str,
) -> None:
    _add_task(lifecycle_desk, capsys)

    result = main(
        ["edit", "task", TASK_ID, field, value, "--root", str(lifecycle_desk)]
    )

    output = capsys.readouterr().out
    assert result == 1
    assert f"Error: {field} is not editable with edit task; it is written by {writer}." in output


def test_edit_task_status_names_closeout_commit(lifecycle_desk: Path, capsys) -> None:
    _add_task(lifecycle_desk, capsys)

    result = main(
        ["edit", "task", TASK_ID, "status", "closed", "--root", str(lifecycle_desk)]
    )

    output = capsys.readouterr().out
    assert result == 1
    assert "closeout commit" in output


def test_edit_task_keeps_ordinary_fields_editable(lifecycle_desk: Path, capsys) -> None:
    _add_task(lifecycle_desk, capsys)

    result = main(
        ["edit", "task", TASK_ID, "goal", "Updated goal.", "--root", str(lifecycle_desk)]
    )

    assert result == 0
    assert "Updated goal." in _task_path(lifecycle_desk).read_text(encoding="utf-8")
