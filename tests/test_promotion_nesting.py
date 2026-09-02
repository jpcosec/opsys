from __future__ import annotations

import re
from pathlib import Path

from sldb.runtime.validation import render_model_markdown

from deskops.cli.main import main
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations


def _section(body: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", body, flags=re.MULTILINE | re.DOTALL)
    assert match is not None, f"missing section {heading}"
    return match.group(1).strip()


def test_inbox_promotion_keeps_structured_sections_flat_in_drawer(tmp_path: Path) -> None:
    assert main(["desk", "install", str(tmp_path)]) == 0

    note = tmp_path / "desk" / "inbox" / "20260902-010101-suggestion-structured-intake.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\n"
        "kind: suggestion\n"
        "status: open\n"
        "---\n\n"
        "# Structured Intake\n\n"
        "## Goal\n\n"
        "Keep authored goal text.\n\n"
        "## Scope\n\n"
        "Keep authored scope text.\n\n"
        "## Validation\n\n"
        "- pytest tests/test_promotion_nesting.py -q\n\n"
        "## Done When\n\n"
        "Nested sections stay flat after promotion.\n",
        encoding="utf-8",
    )

    assert main(["promote", "inbox-to-drawer-task", "structured-intake", "--root", str(tmp_path)]) == 0

    drawer_task = tmp_path / "desk" / "drawer" / "tasks" / "task-structured-intake.md"
    text = drawer_task.read_text(encoding="utf-8")

    assert text.count("## Goal") == 1
    assert text.count("## Scope") == 1
    assert text.count("## Validation") == 1
    assert text.count("## Done When") == 1
    assert _section(text, "Goal") == "Keep authored goal text."
    assert _section(text, "Scope") == "Keep authored scope text."
    assert _section(text, "Validation") == "- pytest tests/test_promotion_nesting.py -q"
    assert "## Validation" not in _section(text, "Scope")
    assert "## Done When" not in _section(text, "Scope")



def test_drawer_promotion_flattens_nested_structured_sections_into_active_task_fields(tmp_path: Path) -> None:
    assert main(["desk", "install", str(tmp_path)]) == 0

    drawer_task = tmp_path / "desk" / "drawer" / "tasks" / "task-nested-drawer.md"
    drawer_task.parent.mkdir(parents=True, exist_ok=True)
    drawer_task.write_text(
        "# Nested Drawer\n\n"
        "ID: task-nested-drawer\n"
        "Status: deferred\n"
        "Priority: medium\n\n"
        "## Goal\n\n"
        "Promote authored sections without nesting.\n\n"
        "## Scope\n\n"
        "Keep this body in scope.\n\n"
        "## Implementation Path\n\n"
        "Use the promote normalization path.\n\n"
        "## Validation\n\n"
        "- pytest tests/test_promotion_nesting.py -q\n\n"
        "## Done When\n\n"
        "Every active task field is flat.\n",
        encoding="utf-8",
    )

    assert main(["promote", "drawer-task-to-active-task", "nested-drawer", "--root", str(tmp_path)]) == 0

    active_task = tmp_path / "desk" / "tasks" / "task-nested-drawer.md"
    text = active_task.read_text(encoding="utf-8")
    operations = DeskopsOperations(tmp_path)
    task, _statuses = operations.show_task("task-nested-drawer")

    assert task is not None
    assert task.goal == "Promote authored sections without nesting."
    assert task.scope == "Keep this body in scope."
    assert task.implementation_path == "Use the promote normalization path."
    assert task.validation == ["pytest tests/test_promotion_nesting.py -q"]
    assert task.done_when == "Every active task field is flat."
    assert text.count("## Goal") == 1
    assert text.count("## Scope") == 1
    assert text.count("## Implementation Path") == 1
    assert text.count("## Validation") == 1
    assert text.count("## Done When") == 1
    assert "## Validation" not in _section(text, "Scope")
    assert "## Done When" not in _section(text, "Implementation Path")



def test_advance_task_reads_nested_task_sections_from_first_occurrence(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.ensure_workspace()

    payload = {
        "id": "task-nested-active",
        "title": "Nested Active",
        "status": "active",
        "why": "Why.",
        "goal": "Goal text.",
        "scope": (
            "Keep this intro in scope.\n\n"
            "## Implementation Path\n\n"
            "Nested implementation path.\n\n"
            "## Validation\n\n"
            "- pytest tests/test_promotion_nesting.py -q\n\n"
            "## Done When\n\n"
            "Nested done-when text."
        ),
        "implementation_path": "Generated implementation path.",
        "validation": ["pytest"],
        "done_when": "Generated done-when text.",
        "references": [],
        "depends_on": [],
        "pills": [],
        "files": [],
        "checklists": [],
        "tags": ["workspace:desk", "artifact:task"],
        "task_type": "",
        "inherits_from": [],
        "inherit_acceptance_context": False,
        "atoms": [],
        "routine": "",
        "current_node": "",
        "history": [],
    }
    task_path = tmp_path / "desk" / "tasks" / "task-nested-active.md"
    task_path.write_text(render_model_markdown(TaskDoc, payload) + "\n", encoding="utf-8")

    task, result = operations.advance_task("task-nested-active")

    assert result is None
    assert task is not None
    assert task.scope == "Keep this intro in scope."
    assert task.implementation_path == "Nested implementation path."
    assert task.validation == ["pytest tests/test_promotion_nesting.py -q"]
    assert task.done_when == "Nested done-when text."
