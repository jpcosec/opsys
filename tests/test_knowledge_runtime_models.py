from __future__ import annotations

import pytest

import deskops.models as models
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        models.CrossroadDoc,
        {
            "id": "crossroad-pizzeria",
            "title": "Pizzeria",
            "path": "pizzeria.carta",
            "content": "Menu and reservations for the pizzeria.",
            "tags": ["domain:pizzeria"],
        },
    ),
    (
        models.RuntimeProfileDoc,
        {
            "id": "runtime-pi",
            "title": "Pi runtime",
            "kind": "pi",
            "binary": "pi",
            "model_flag": "--model",
            "fallback_models_flag": "--fallback-models",
            "tools_flag": "--tools",
            "system_prompt_flag": "--system-prompt",
            "system_prompt_delivery": "inline",
            "session_flag": "--session",
            "extra_args": ["--quiet"],
            "unsupported_role_fields": ["fallback_models"],
            "notes": "Needs authentication.",
            "tags": ["system:deskops"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_knowledge_and_runtime_models_roundtrip(model, payload) -> None:
    expected = model(**payload).model_dump()
    rendered = render_model_markdown(model, payload)
    extracted = extract_model_data(model, rendered)

    assert extracted == expected
    assert "_." not in rendered