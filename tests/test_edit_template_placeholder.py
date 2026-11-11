"""`deskops edit` does not store the template's placeholder paragraph as content.

The template writes a literal italic paragraph before each section field (the anchor that
extract consumes). A value that already carried it, such as the raw section text plus a new
paragraph, was written after the anchor and read back as content: one more copy per edit
(CC33c, 4305c7d9; reproduction [1, 2, 3]). The edit path now drops paragraphs that are exactly
the field's placeholder, read from the model's own template.
"""

from __future__ import annotations

from pathlib import Path

from sldb.runtime.validation import extract_model_data

from deskops.cli.main import main
from deskops.doc_access import strip_template_placeholders
from deskops.doc_access import template_placeholders
from deskops.models import InboxNoteDoc
from deskops.models import TaskDoc
from deskops.operations import DeskopsOperations

PLACEHOLDER = "_Outline the expected implementation route or affected surface._"
INBOX_PLACEHOLDER = "_Describe the incoming message with enough evidence to triage._"


def _task(root: Path, title: str, implementation_path: str = "base") -> Path:
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": title, "why": "w", "goal": "g", "scope": "s", "implementation_path": implementation_path,
         "done_when": "d", "validation": ["v"], "task_type": "task.code"}
    ).task_id
    return root / "desk" / "tasks" / f"{task_id}.md"


def _section(path: Path, heading: str) -> str:
    return path.read_text(encoding="utf-8").split(f"## {heading}", 1)[1].split("\n## ", 1)[0].strip()


def _edit(root: Path, subject: str, selector: str, field: str, value: str) -> None:
    assert main(["edit", subject, selector, field, value, "--root", str(root)]) == 0


def test_the_placeholders_come_from_the_template() -> None:
    assert template_placeholders(TaskDoc)["implementation_path"] == PLACEHOLDER
    assert template_placeholders(InboxNoteDoc) == {"body": INBOX_PLACEHOLDER}


def test_editing_with_the_raw_section_text_keeps_one_placeholder(lifecycle_desk: Path, capsys) -> None:
    """Case 3 of the reproduction: [1, 2, 3] before, [1, 1, 1] now."""
    root = lifecycle_desk
    path = _task(root, "Placeholder raw section")
    counts = [path.read_text(encoding="utf-8").count(PLACEHOLDER)]
    for extra in ("b9", "b10"):
        _edit(root, "task", path.stem, "implementation_path", _section(path, "Implementation Path") + "\n\n" + extra)
        counts.append(path.read_text(encoding="utf-8").count(PLACEHOLDER))
    capsys.readouterr()
    assert counts == [1, 1, 1]
    payload = extract_model_data(TaskDoc, path.read_text(encoding="utf-8"))
    assert payload["implementation_path"] == "base\n\nb9\n\nb10"


def test_the_same_value_twice_leaves_the_same_file(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    path = _task(root, "Placeholder idempotent")
    value = PLACEHOLDER + "\n\nnuevo texto"
    _edit(root, "task", path.stem, "implementation_path", value)
    first = path.read_text(encoding="utf-8")
    _edit(root, "task", path.stem, "implementation_path", value)
    capsys.readouterr()
    assert path.read_text(encoding="utf-8") == first
    assert first.count(PLACEHOLDER) == 1


def test_a_value_that_is_only_the_placeholder_empties_the_field(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    path = _task(root, "Placeholder only")
    _edit(root, "task", path.stem, "implementation_path", PLACEHOLDER)
    capsys.readouterr()
    text = path.read_text(encoding="utf-8")
    assert text.count(PLACEHOLDER) == 1
    assert extract_model_data(TaskDoc, text)["implementation_path"] == ""


def test_the_phrase_inside_a_longer_paragraph_is_kept(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    path = _task(root, "Placeholder inside prose")
    value = f"La plantilla dice {PLACEHOLDER} y aquí se cita."
    _edit(root, "task", path.stem, "implementation_path", value)
    capsys.readouterr()
    text = path.read_text(encoding="utf-8")
    assert text.count(PLACEHOLDER) == 2
    assert extract_model_data(TaskDoc, text)["implementation_path"] == value


def test_inbox_note_body_keeps_one_placeholder(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    assert main(["add", "inbox-note", "--root", str(root), "--kind", "suggestion", "--title",
                 "Placeholder inbox probe", "--body", "Primer párrafo con evidencia."]) == 0
    capsys.readouterr()
    [path] = (root / "desk" / "inbox").glob("*placeholder-inbox-probe*.md")
    assert path.read_text(encoding="utf-8").count(INBOX_PLACEHOLDER) == 1
    raw_body = path.read_text(encoding="utf-8").split("# Placeholder inbox probe", 1)[1].strip()
    _edit(root, "inbox-note", path.stem, "body", raw_body + "\n\nSegundo párrafo.")
    first = path.read_text(encoding="utf-8")
    _edit(root, "inbox-note", path.stem, "body", raw_body + "\n\nSegundo párrafo.")
    capsys.readouterr()
    assert path.read_text(encoding="utf-8") == first
    assert first.count(INBOX_PLACEHOLDER) == 1
    assert extract_model_data(InboxNoteDoc, first)["body"] == "Primer párrafo con evidencia.\n\nSegundo párrafo."
    _edit(root, "inbox-note", path.stem, "body", INBOX_PLACEHOLDER)
    capsys.readouterr()
    assert extract_model_data(InboxNoteDoc, path.read_text(encoding="utf-8"))["body"] == ""


def test_only_text_fields_and_only_whole_top_level_paragraphs_are_normalized() -> None:
    assert strip_template_placeholders(TaskDoc, "validation", [PLACEHOLDER]) == [PLACEHOLDER]
    for kept in (f"> {PLACEHOLDER}", f"- {PLACEHOLDER}", f"```\n{PLACEHOLDER}\n```"):
        assert strip_template_placeholders(TaskDoc, "implementation_path", kept) == kept
    piled = f"{PLACEHOLDER}\n\n{PLACEHOLDER}\n\nbase\n\n{PLACEHOLDER}\n\nb9"
    assert strip_template_placeholders(TaskDoc, "implementation_path", piled) == "base\n\nb9"
    # another field's placeholder is that field's content
    assert strip_template_placeholders(TaskDoc, "goal", PLACEHOLDER) == PLACEHOLDER
