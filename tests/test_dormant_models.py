from __future__ import annotations

import pytest

import deskops.models as models
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        models.ProtoAtomDoc,
        {
            "id": "proto-atom-template-test",
            "title": "Template Proto Atom",
            "status": "active",
            "content": "Raw capture before typing.",
            "typed_as": "atom",
            "provenance": "https://example.com/source",
            "tags": ["system:deskops"],
        },
    ),
    (
        models.RunDoc,
        {
            "id": "run-template-test",
            "title": "Template Run",
            "kind": "execution",
            "run_dir": "runs/subagents/20260920T000000",
            "herdr_pane_id": "pane-1",
            "session_path": "runs/subagents/20260920T000000/session.json",
            "session_sha256": "0123456789abcdef",
            "started_at": "2026-09-20T00:00:00",
            "ended_at": "2026-09-20T00:01:00",
            "outcome": "success",
            "commit_sha": "0123456789abcdef",
            "move_id": "move-1",
            "model": "deepseek-flash",
            "tokens_in": 1234,
            "tokens_out": 567,
            "cost_usd": 0.25,
            "result_summary": "The run completed.",
            "validation_log": "All checks passed.",
            "tags": ["type:run"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_dormant_models_roundtrip(model, payload) -> None:
    expected = model(**payload).model_dump()
    rendered = render_model_markdown(model, payload)
    extracted = extract_model_data(model, rendered)

    assert extracted == expected
    assert "_." not in rendered
    for value in extracted.values():
        if isinstance(value, str):
            assert "_Describe" not in value