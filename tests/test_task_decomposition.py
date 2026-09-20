from __future__ import annotations

import pytest

from deskops.models import AcceptanceDoc
from deskops.models import TaskBindingDoc
from deskops.models import TaskIntentDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        TaskIntentDoc,
        {
            "id": "task-intent-template-test",
            "title": "Template Task Intent",
            "status": "active",
            "summary": "How the template task should be implemented.",
            "implementation_path": "Edit the task template.",
            "files": ["deskops/models/task.py", "tests/test_task_decomposition.py"],
            "out_of_scope": "Runtime changes to operations.py.",
            "tags": ["topic:templates"],
        },
    ),
    (
        AcceptanceDoc,
        {
            "id": "acceptance-template-test",
            "title": "Template Acceptance",
            "status": "active",
            "summary": "What closing the template task requires.",
            "validation": ["pytest tests/test_task_decomposition.py"],
            "done_when": ["The task template roundtrips."],
            "evidence": ["Roundtrip assertion passed."],
            "tags": ["topic:templates"],
        },
    ),
    (
        TaskBindingDoc,
        {
            "id": "task-binding-template-test",
            "title": "Template Task Binding",
            "status": "active",
            "summary": "Why the template task is bound to its context.",
            "rationale": "It proves the decomposed task documents roundtrip.",
            "tags": ["topic:templates"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_decomposed_task_models_roundtrip(model, payload) -> None:
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