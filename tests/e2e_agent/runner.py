"""One scenario end to end: sandbox, agent, checks, verdict, and the run directory it leaves."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import sldb

from tests.e2e_agent.agent_run import DEFAULT_MODEL, DEFAULT_PROVIDER, help_probes, run_agent, source_reads
from tests.e2e_agent.sandbox import REPO_ROOT, make_sandbox, run_checks, run_steps
from tests.e2e_agent.scenario import Scenario

RUNS_DIR = REPO_ROOT / "runs" / "e2e"


def run_reference(scenario: Scenario) -> list[dict]:
    """Setup, the scenario's known-good commands, then its checks: no LLM involved."""
    box = make_sandbox()
    try:
        run_steps(box, scenario.setup, "setup")
        run_steps(box, scenario.reference, "reference")
        return run_checks(box, scenario.checks)
    finally:
        shutil.rmtree(box.root.parent, ignore_errors=True)


def run_scenario(scenario: Scenario, provider: str = DEFAULT_PROVIDER, model: str = DEFAULT_MODEL, keep: bool = False) -> dict[str, Any]:
    """The agent attempts the scenario from its docs; the harness judges and writes runs/e2e/<run>/."""
    out = RUNS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}-{scenario.id}"
    out.mkdir(parents=True)
    box = make_sandbox()
    try:
        run_steps(box, scenario.setup, "setup")
        agent = run_agent(scenario, box, out / "events.jsonl", provider, model)
        result = _judge(scenario, agent, run_checks(box, scenario.checks), f"{provider}/{model}", box.root)
    finally:
        if not keep:
            shutil.rmtree(box.root.parent, ignore_errors=True)
    (out / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "summary.md").write_text(_summary(result), encoding="utf-8")
    result["run_dir"] = str(out)
    return result


def _judge(scenario: Scenario, agent, checks: list[dict], model: str, root: Path) -> dict[str, Any]:
    calls = agent.tool_calls()
    report = agent.report()
    friction = (report or {}).get("friction") or []
    peeks = source_reads(calls, [str(REPO_ROOT), str(Path(sldb.__file__).resolve().parents[1])])
    works = all(c["ok"] for c in checks)
    severities = [f.get("severity") for f in friction]
    docs_ok = report is not None and bool(report.get("completed")) and not agent.stopped \
        and len(peeks) <= scenario.max_source_reads and "blocker" not in severities \
        and severities.count("major") <= scenario.max_major_friction
    return {
        "scenario": scenario.id, "model": model, "sandbox": str(root),
        "verdict": {"works": works, "docs_ok": docs_ok, "pass": works and docs_ok},
        "metrics": {
            "cost_usd": round(agent.cost(), 4), "seconds": round(agent.seconds, 1), "stopped": agent.stopped,
            "tool_calls": len(calls), "failed_commands": sum(c["error"] for c in calls),
            "help_probes": help_probes(calls), "source_reads": len(peeks),
            "friction": {s: severities.count(s) for s in ("blocker", "major", "minor")},
        },
        "checks": checks,
        "source_reads": peeks,
        "agent_report": report,
        "commands": [c["args"].get("command", c["args"].get("path", "")) for c in calls],
        "failed": [{"command": c["args"].get("command", c["args"].get("path", "")), "output": c["output"]} for c in calls if c["error"]],
    }


def _summary(r: dict[str, Any]) -> str:
    v, m, report = r["verdict"], r["metrics"], r["agent_report"] or {}
    lines = [
        f"# e2e: {r['scenario']} ({r['model']})", "",
        f"- works (harness checks): {'yes' if v['works'] else 'NO'}",
        f"- docs ok (agent got there from the docs): {'yes' if v['docs_ok'] else 'NO'}",
        f"- cost ${m['cost_usd']}, {m['seconds']}s, {m['tool_calls']} tool calls, {m['failed_commands']} failed, "
        f"{m['help_probes']} --help, {m['source_reads']} source reads{', stopped: ' + m['stopped'] if m['stopped'] else ''}",
        "", "## Checks", "",
        *[f"- [{'x' if c['ok'] else ' '}] {c['name']}" for c in r["checks"]],
        "", "## Agent", "", report.get("summary", "(no report: the agent did not end with the JSON block)"),
        "", "## Friction", "",
        *_or_none([f"- **{f.get('severity', '?')}** ({f.get('kind', '?')}) {f.get('doc', '')} § {f.get('section', '')}: "
                   f"{f.get('problem', '')} — {f.get('how_resolved', '')}" for f in report.get("friction") or []]),
        "", "## Failed commands", "",
        *_or_none([f"- `{f['command'][:160]}`" for f in r["failed"]]),
        "", "## Source reads (docs were not enough)", "",
        *_or_none([f"- `{s}`" for s in r["source_reads"]]), "",
    ]
    return "\n".join(lines)


def _or_none(items: list[str]) -> list[str]:
    return items or ["- none"]
