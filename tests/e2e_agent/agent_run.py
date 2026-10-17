"""Run one cheap pi agent on a scenario and read what it did from its JSON event stream."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tests.e2e_agent.sandbox import REPO_ROOT, Sandbox
from tests.e2e_agent.scenario import Scenario

DEFAULT_PROVIDER, DEFAULT_MODEL = "deepseek", "deepseek-flash"
FRICTION_KINDS = (
    "naming mismatch", "missing discovery surface", "scope ambiguity", "hidden state dependency",
    "misleading help", "recoverability failure", "documentation/runtime divergence",
)

PROMPT = """You are a developer using the `deskops` CLI for the first time. It is already installed
and on PATH (and so is `sldb`, which deskops builds on). Your working directory is a git repo:
{root}

What you want to get done:
{intent}

Rules:
- Learn deskops ONLY from the documents attached to this message, the files deskops creates in
  this repo, and the CLI's own output (including --help). Do NOT read deskops or sldb source code
  or their installed package files; if the docs are not enough, say so in your report instead.
- Work only inside {root}. Do not ask questions: decide, act, and note what was unclear.
- When you are done (or stuck), end your LAST message with exactly one fenced ```json block:
{{
  "completed": true or false,
  "summary": "one or two sentences",
  "steps": [{{"goal": "...", "command": "...", "doc": "file and section you followed, or 'help' or 'guess'", "worked": true}}],
  "friction": [{{"doc": "file", "section": "heading", "problem": "what was missing, wrong or unclear",
                "kind": one of {kinds}, "severity": "blocker" | "major" | "minor",
                "how_resolved": "what you did instead, or 'not resolved'"}}]
}}
Report every place where the docs and the CLI disagreed, or where you had to guess.
"""

_FENCE = re.compile(r"```json\s*(\{.*?\})\s*```", re.S)
_HELP = re.compile(r"(^|\s)(--help|-h)(\s|$)")


@dataclass
class AgentRun:
    events: list[dict[str, Any]] = field(default_factory=list)
    stopped: str = ""   # "", "timeout" or "budget"
    seconds: float = 0.0

    def tool_calls(self) -> list[dict[str, Any]]:
        calls: dict[str, dict[str, Any]] = {}
        for e in self.events:
            if e.get("type") == "tool_execution_start":
                calls[e["toolCallId"]] = {"tool": e["toolName"], "args": e.get("args", {}), "error": False, "output": ""}
            elif e.get("type") == "tool_execution_end" and e["toolCallId"] in calls:
                result = e.get("result") or {}
                text = "".join(c.get("text", "") for c in result.get("content", []) if isinstance(c, dict))
                calls[e["toolCallId"]].update(error=bool(e.get("isError")), output=text[-600:])
        return list(calls.values())

    def cost(self) -> float:
        return sum(((e["message"].get("usage") or {}).get("cost") or {}).get("total", 0.0)
                   for e in self.events if e.get("type") == "message_end" and e["message"].get("role") == "assistant")

    def final_text(self) -> str:
        for e in reversed(self.events):
            if e.get("type") == "message_end" and e["message"].get("role") == "assistant":
                texts = [c.get("text", "") for c in e["message"].get("content", []) if c.get("type") == "text"]
                if any(texts):
                    return "\n".join(texts)
        return ""

    def report(self) -> dict[str, Any] | None:
        found = _FENCE.findall(self.final_text())
        if not found:
            return None
        try:
            return json.loads(found[-1])
        except json.JSONDecodeError:
            return None


def run_agent(scenario: Scenario, box: Sandbox, events_path: Path, provider: str = DEFAULT_PROVIDER, model: str = DEFAULT_MODEL) -> AgentRun:
    """Run pi headless; stop it when it overruns the scenario's time or cost budget."""
    if shutil.which("pi") is None:
        raise RuntimeError("pi is not on PATH")
    prompt = PROMPT.format(root=box.root, intent=scenario.intent.strip(), kinds=" | ".join(f'"{k}"' for k in FRICTION_KINDS))
    docs = [f"@{REPO_ROOT / d}" for d in scenario.docs]
    argv = ["pi", "-p", "--mode", "json", "--no-session", "--provider", provider, "--model", model,
            "--no-skills", "--no-context-files", "--no-extensions", "--tools", "bash,read,write,edit,ls,grep,find",
            *docs, prompt]
    run, start = AgentRun(), time.monotonic()
    with events_path.open("w", encoding="utf-8") as sink:
        proc = subprocess.Popen(argv, cwd=box.root, env=box.env(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        for line in proc.stdout:
            event = _parse(line)
            if event is None or event.get("type") == "message_update":
                continue  # streaming deltas: the matching message_end carries the whole message
            run.events.append(event)
            sink.write(json.dumps(event, ensure_ascii=False) + "\n")
            run.stopped = _overrun(run, scenario, start)
            if run.stopped:
                proc.kill()
                break
        proc.wait()
    run.seconds = time.monotonic() - start
    return run


def _parse(line: str) -> dict[str, Any] | None:
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def _overrun(run: AgentRun, scenario: Scenario, start: float) -> str:
    if time.monotonic() - start > scenario.timeout_s:
        return "timeout"
    return "budget" if run.cost() > scenario.max_cost_usd else ""


def source_reads(calls: list[dict[str, Any]], forbidden: list[str]) -> list[str]:
    """Tool calls that read deskops or sldb code: the docs were not enough to go on."""
    hits = []
    for call in calls:
        text = json.dumps(call["args"], ensure_ascii=False)
        if any(f in text for f in forbidden) or re.search(r"import (deskops|sldb)|site-packages|inspect\.getsource", text):
            hits.append(text[:200])
    return hits


def help_probes(calls: list[dict[str, Any]]) -> int:
    return sum(1 for c in calls if c["tool"] == "bash" and _HELP.search(c["args"].get("command", "")))
