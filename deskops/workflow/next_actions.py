from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_task_lifecycle_spec(spec_root: Path) -> dict[str, Any]:
    path = spec_root / "workflows" / "task_lifecycle.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Workflow spec must be a mapping: {path}")
    payload["_path"] = path
    return payload


def match_workflow_state(spec: dict[str, Any], current_node: str) -> dict[str, Any]:
    node = current_node or ""
    for state in spec.get("states") or []:
        if not isinstance(state, dict):
            continue
        if state.get("current_node") == node:
            return state
        suffix = state.get("current_node_suffix")
        if suffix and node.endswith(str(suffix)):
            return state
    if not node:
        return _first_state(spec)
    raise ValueError(f"No workflow state in {spec.get('_path')} matches current node '{current_node}'")


def render_workflow_mermaid(spec: dict[str, Any]) -> str:
    states = [state for state in spec.get("states") or [] if isinstance(state, dict)]
    lines = ["flowchart TD"]
    for state in states:
        state_id = str(state["id"])
        label = str(state.get("phase") or state_id).replace('"', "'")
        lines.append(f'    {state_id}["{label}"]')
    for source, target in zip(states, states[1:]):
        lines.append(f"    {source['id']} --> {target['id']}")
    return "\n".join(lines)


def _first_state(spec: dict[str, Any]) -> dict[str, Any]:
    states = [state for state in spec.get("states") or [] if isinstance(state, dict)]
    if not states:
        raise ValueError(f"Workflow spec has no states: {spec.get('_path')}")
    return states[0]
