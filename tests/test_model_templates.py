from __future__ import annotations

import pytest

from deskops.models import AtomDoc
from deskops.models import BoardDoc
from deskops.models import ChecklistDoc
from deskops.models import ConditionDoc
from deskops.models import EdgeDoc
from deskops.models import FAQDoc
from deskops.models import HookDoc
from deskops.models import InboxNoteDoc
from deskops.models import OperatorDoc
from deskops.models import PillDoc
from deskops.models import RepositoryDoc
from deskops.models import RitualDoc
from deskops.models import RoutineDoc
from deskops.models import StepDoc
from deskops.models import TaskDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        AtomDoc,
        {
            "id": "atom-template-test",
            "title": "Template Test",
            "five_wh_one_plus": "what",
            "answer": "A template test proves instructions stay fixed.",
            "tags": ["system:deskops"],
        },
    ),
    (
        BoardDoc,
        {
            "id": "board-template-test",
            "title": "Template Board",
            "scope": "desk",
            "purpose": "Route template validation.",
            "tasks": [],
            "pills": ["desk/contexts/pill-template.md"],
            "rituals": ["desk/rituals/testing.md"],
            "notes": "No extra notes.",
            "tags": ["workspace:desk"],
        },
    ),
    (
        ChecklistDoc,
        {
            "id": "checklist-template-test",
            "title": "Template Checklist",
            "status": "active",
            "summary": "Checks template behavior.",
            "items": ["Render", "Extract"],
            "condition_refs": ["condition-template-test"],
            "mode": "all",
            "tags": ["topic:templates"],
        },
    ),
    (
        ConditionDoc,
        {
            "id": "condition-template-test",
            "title": "Template Condition",
            "status": "active",
            "summary": "Checks a field value.",
            "subject": "status",
            "predicate": "equals",
            "expected": "active",
            "tags": ["topic:templates"],
        },
    ),
    (
        EdgeDoc,
        {
            "id": "edge-template-test",
            "title": "Template Edge",
            "status": "active",
            "summary": "Connects two nodes.",
            "source": "node-a",
            "target": "node-b",
            "condition_ref": "condition-template-test",
            "tags": ["topic:templates"],
        },
    ),
    (
        FAQDoc,
        {
            "title": "Template FAQ",
            "body": "How does it work?\n\nIt roundtrips fixed text safely.",
        },
    ),
    (
        HookDoc,
        {
            "id": "hook-template-test",
            "title": "Template Hook",
            "status": "active",
            "summary": "Invokes an operator.",
            "event": "task.closed",
            "target": "operator-template-test",
            "condition_ref": "condition-template-test",
            "tags": ["topic:templates"],
        },
    ),
    (
        InboxNoteDoc,
        {
            "kind": "suggestion",
            "sender_project": "test-project",
            "created_at": "2026-06-13T00:00:00",
            "status": "open",
            "title": "Template Inbox Note",
            "body": "Capture enough evidence to triage this note.",
        },
    ),
    (
        OperatorDoc,
        {
            "id": "operator-template-test",
            "title": "Template Operator",
            "status": "active",
            "summary": "Sets the task status.",
            "action": "set_field",
            "target": "status",
            "value": "closed",
            "tags": ["topic:templates"],
        },
    ),
    (
        PillDoc,
        {
            "id": "pill-template-test",
            "title": "Template Pill",
            "what": "A context capsule.",
            "why": "It prevents ambiguity.",
            "when": "Before editing templates.",
            "where": "deskops/models.",
            "how": "Follow fixed text rules.",
            "how_not": "Do not put comments in frontmatter.",
            "tags": ["topic:templates"],
        },
    ),
    (
        RepositoryDoc,
        {
            "id": "repo-template-test",
            "name": "template-repo",
            "path": ".",
            "status": "active",
            "description": "Repository used to validate template roundtrips.",
            "tags": ["type:tool"],
        },
    ),
    (
        RitualDoc,
        {
            "id": "ritual-template-test",
            "title": "Template Ritual",
            "purpose": "Validate fixed instructions.",
            "trigger": "A template changes.",
            "preconditions": ["A model exists."],
            "steps": [],
            "validation": ["Roundtrip passes."],
            "failure_modes": ["Instruction text is extracted as data."],
            "completion": "All templates roundtrip.",
            "tags": ["topic:templates"],
        },
    ),
    (
        RoutineDoc,
        {
            "id": "routine-template-test",
            "title": "Template Routine",
            "status": "active",
            "summary": "Coordinates template checks.",
            "entrypoint": "checklist-template-test",
            "decomposition": ["checklist-template-test"],
            "edges": ["edge-template-test"],
            "terminal_nodes": ["done"],
            "tags": ["topic:templates"],
        },
    ),
    (
        StepDoc,
        {
            "id": "step-template-test",
            "title": "Template Step",
            "action": "Render the document.",
            "outcome": "Markdown with fixed instructions.",
            "tags": ["topic:templates"],
        },
    ),
    (
        TaskDoc,
        {
            "id": "task-template-test",
            "title": "Template Task",
            "status": "active",
            "goal": "Render helpful task docs.",
            "scope": "Task template only.",
            "references": [],
            "depends_on": [],
            "pills": ["pill-template-test"],
            "files": ["deskops/models/task.py"],
            "routine": "routine-template-test",
            "checklists": ["checklist-template-test"],
            "current_node": "checklist-template-test",
            "history": [],
            "implementation_path": "Edit the task template.",
            "validation": ["pytest tests/test_model_templates.py"],
            "done_when": "The task template roundtrips.",
            "tags": ["topic:templates"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_model_templates_roundtrip_with_instructional_text(model, payload) -> None:
    expected = model(**payload).model_dump()
    rendered = render_model_markdown(model, payload)
    extracted = extract_model_data(model, rendered)

    assert extracted == expected
    assert "_." not in rendered
    assert "_" in rendered
    assert "Describe" in rendered or "List" in rendered or "Answer" in rendered or "Generated" in rendered or "Write" in rendered or "Summarize" in rendered
    for value in extracted.values():
        if isinstance(value, str):
            assert "_Describe" not in value
            assert "_List" not in value
            assert "_Summarize" not in value
