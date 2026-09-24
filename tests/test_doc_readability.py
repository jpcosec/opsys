"""A write must never erase content the reader can still see.

The pill documents in this desk were authored by hand, so they carry their
sections but not the fixed text a model template renders. Extraction therefore
returned empty for every body field, and any edit rendered those empty values
back and blanked the document.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main
from deskops.doc_readability import is_unreadable_by_model
from deskops.doc_readability import unread_section_fields
from deskops.models import PillDoc
from sldb.runtime.validation import render_model_markdown

HAND_WRITTEN_PILL = """---
id: pill-hand-written
tags:
- workspace:desk
---

# Hand written pill

## What

Self-reflection must produce high-signal atoms instead of bulk guesses.

## Why

Noise makes the knowledge base harder to trust.
"""

PILL_PAYLOAD = {
    "id": "pill-rendered",
    "tags": ["workspace:desk"],
    "title": "Rendered pill",
    "what": "Self-reflection must produce high-signal atoms instead of bulk guesses.",
    "why": "Noise makes the knowledge base harder to trust.",
    "when": "When a reflection routine runs.",
    "where": "Desk reflection commands.",
    "how": "Distill findings before writing them.",
    "how_not": "Do not promote low-confidence guesses.",
}


def test_unreadable_fields_are_detected_for_a_hand_written_document() -> None:
    fields = is_unreadable_by_model(PillDoc, HAND_WRITTEN_PILL)

    assert "what" in fields
    assert "why" in fields


def test_a_rendered_document_reports_no_unreadable_fields() -> None:
    rendered = render_model_markdown(PillDoc, PILL_PAYLOAD) + "\n"

    assert is_unreadable_by_model(PillDoc, rendered) == []


def test_unread_section_fields_spots_content_a_rewrite_would_drop() -> None:
    rendered = render_model_markdown(PillDoc, PILL_PAYLOAD) + "\n"
    blanked = render_model_markdown(PillDoc, {**PILL_PAYLOAD, "what": "", "why": ""}) + "\n"

    assert unread_section_fields(PillDoc, HAND_WRITTEN_PILL, blanked) == ["what", "why"]
    assert unread_section_fields(PillDoc, PILL_PAYLOAD and rendered, rendered) == []


def test_editing_an_unreadable_pill_refuses_instead_of_erasing_it(tmp_path: Path, capsys) -> None:
    """The reported bug: `edit pill ... status` blanked the document it edited."""
    assert main(["init", str(tmp_path)]) == 0
    capsys.readouterr()

    pill = tmp_path / "desk" / "contexts" / "pill-hand-written.md"
    pill.write_text(HAND_WRITTEN_PILL, encoding="utf-8")
    before = pill.read_text(encoding="utf-8")

    assert main(["edit", "pill", "pill-hand-written", "status", "active", "--root", str(tmp_path)]) != 0
    out, _err = capsys.readouterr()

    assert "Refusing to rewrite" in out
    assert pill.read_text(encoding="utf-8") == before
