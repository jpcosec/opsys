"""A scenario: what the user wants, which docs the agent gets, the starting state, and how the
harness decides it worked."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

SCENARIOS_DIR = Path(__file__).parent / "scenarios"


@dataclass(frozen=True)
class Check:
    """One shell command run in the sandbox after the agent; it holds when it exits 0."""

    name: str
    run: str


@dataclass(frozen=True)
class Scenario:
    id: str
    intent: str
    docs: list[str]
    setup: list[str]
    reference: list[str]
    checks: list[Check]
    max_cost_usd: float = 0.25
    timeout_s: int = 900
    max_source_reads: int = 0
    max_major_friction: int = 0   # "major" friction points the docs may still have and pass
    notes: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


def load_scenario(path: Path) -> Scenario:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    checks = [Check(name=c["name"], run=c["run"]) for c in data.pop("checks")]
    known = {k: data.pop(k) for k in list(data) if k in Scenario.__dataclass_fields__}
    return Scenario(checks=checks, extra=data, **known)


def all_scenarios() -> list[Scenario]:
    return [load_scenario(p) for p in sorted(SCENARIOS_DIR.glob("*.yaml"))]
