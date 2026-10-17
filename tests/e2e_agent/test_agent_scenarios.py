"""The agent e2e scenarios as tests.

`test_reference_solutions` and `test_checks_need_the_work` run in the normal suite (no LLM):
every scenario must be solvable with the documented commands, and its checks must not already
hold after setup alone. `test_agent_scenarios` runs a pi agent per scenario and only runs with
`DESKOPS_AGENT_E2E=1` (it costs money and minutes).
"""

from __future__ import annotations

import os
import shutil

import pytest

from tests.e2e_agent.runner import run_reference, run_scenario
from tests.e2e_agent.sandbox import make_sandbox, run_checks, run_steps
from tests.e2e_agent.scenario import all_scenarios

SCENARIOS = all_scenarios()
IDS = [s.id for s in SCENARIOS]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=IDS)
def test_reference_solutions(scenario):
    failed = [c for c in run_reference(scenario) if not c["ok"]]
    assert not failed, "\n".join(f"{c['name']}: {c['output']}" for c in failed)


@pytest.mark.parametrize("scenario", SCENARIOS, ids=IDS)
def test_checks_need_the_work(scenario):
    box = make_sandbox()
    try:
        run_steps(box, scenario.setup, "setup")
        assert not all(c["ok"] for c in run_checks(box, scenario.checks)), "the checks already hold before anyone works"
    finally:
        shutil.rmtree(box.root.parent, ignore_errors=True)


@pytest.mark.skipif(os.environ.get("DESKOPS_AGENT_E2E") != "1" or shutil.which("pi") is None, reason="set DESKOPS_AGENT_E2E=1 (needs pi and a DeepSeek key)")
@pytest.mark.parametrize("scenario", SCENARIOS, ids=IDS)
def test_agent_scenarios(scenario):
    model = os.environ.get("DESKOPS_AGENT_E2E_MODEL", "deepseek/deepseek-flash")
    result = run_scenario(scenario, *model.split("/", 1))
    assert result["verdict"]["works"], f"harness checks failed; see {result['run_dir']}/summary.md"
    assert result["verdict"]["docs_ok"], f"the agent could not get there from the docs; see {result['run_dir']}/summary.md"
