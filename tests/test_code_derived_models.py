from __future__ import annotations

import pytest

import deskops.models as models
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        models.CommitDoc,
        {
            "id": "commit-template-test",
            "title": "Template Commit",
            "sha": "0123456789abcdef",
            "author": "agent <agent@example.com>",
            "committed_at": "2026-09-20T00:00:00",
            "message": "Split TaskDoc into intent, acceptance and binding.",
            "trailers": {"co-authored-by": "x <x@example.com>"},
            "tags": ["type:commit"],
        },
    ),
    (
        models.ChangeDoc,
        {
            "id": "change-template-test",
            "title": "Template Change",
            "path": "deskops/models/task.py",
            "line_start": 1,
            "line_end": 10,
            "added": 7,
            "removed": 3,
            "symbol": "deskops.models:TaskDoc",
            "tags": ["type:change"],
        },
    ),
    (
        models.TestCoverageDoc,
        {
            "id": "test-coverage-template-test",
            "title": "Template Test Coverage",
            "test_qualname": "tests.test_model_templates::test_roundtrip",
            "covers_symbol": "deskops.models:TaskDoc",
            "granularity": "module",
            "source": "import_decl",
            "tags": ["type:test-coverage"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_code_derived_models_roundtrip(model, payload) -> None:
    expected = model(**payload).model_dump()
    rendered = render_model_markdown(model, payload)
    extracted = extract_model_data(model, rendered)

    assert extracted == expected
    assert "_." not in rendered
    for value in extracted.values():
        if isinstance(value, str):
            assert "_Describe" not in value