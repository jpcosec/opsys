from __future__ import annotations

import pytest

from deskops.models import PlanDoc
from deskops.models import PlanIterationDoc
from deskops.models import PlanTargetDoc
from deskops.models import SymbolContractDoc
from sldb.runtime.validation import extract_model_data
from sldb.runtime.validation import render_model_markdown


MODEL_PAYLOADS = [
    (
        PlanDoc,
        {
            "id": "plan-template-test",
            "title": "Template Plan",
            "goal": "Render helpful plan docs.",
            "context_findings": "A template already exists for tasks.",
            "interpretation": "The plan models the planner output.",
            "risks": "The roundtrip may drop nested sections.",
            "ambiguities": ["Where iteration rounds live."],
            "tags": ["topic:planning"],
        },
    ),
    (
        PlanTargetDoc,
        {
            "id": "plan-target-template-test",
            "title": "Template Plan Target",
            "surface": "deskops/models/plan_target.py",
            "symbol": "deskops.models:PlanTargetDoc",
            "change_kind": "modify",
            "rationale": "It bridges the plan to the AST.",
            "acceptance": "The target roundtrips.",
            "tags": ["topic:planning"],
        },
    ),
    (
        PlanIterationDoc,
        {
            "id": "plan-iteration-template-test",
            "title": "Template Plan Iteration",
            "round": 2,
            "trigger": "The previous plan changed.",
            "findings": "The roundtrip is stable.",
            "plan_delta": "No structural changes.",
            "outcome": "Iteration recorded.",
            "tags": ["topic:planning"],
        },
    ),
    (
        SymbolContractDoc,
        {
            "id": "symbol-contract-template-test",
            "title": "Template Symbol Contract",
            "qualname": "deskops.models:SymbolContractDoc",
            "kind": "class",
            "signature": "class SymbolContractDoc",
            "docstring": "A contract declared before implementation.",
            "purpose": "Gate implementation against a declared contract.",
            "architecture": "Planning layer bridging the AST.",
            "invariants": ["docstring is non-empty"],
            "lint_rules": ["complexity <= 10"],
            "test_plan": ["roundtrip preserves payload"],
            "test_qualname": "tests.test_planning_models::test_contract_roundtrip",
            "tags": ["topic:planning"],
        },
    ),
]


@pytest.mark.parametrize(("model", "payload"), MODEL_PAYLOADS)
def test_planning_models_roundtrip(model, payload) -> None:
    expected = model(**payload).model_dump()
    rendered = render_model_markdown(model, payload)
    extracted = extract_model_data(model, rendered)

    assert extracted == expected
    assert "_." not in rendered
    assert "_" in rendered
    assert "Describe" in rendered or "List" in rendered or "Explain" in rendered or "Record" in rendered or "Summarize" in rendered
    for value in extracted.values():
        if isinstance(value, str):
            assert "_Describe" not in value
            assert "_Explain" not in value
            assert "_Record" not in value