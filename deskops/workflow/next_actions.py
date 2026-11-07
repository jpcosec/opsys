from __future__ import annotations

from typing import Any

from deskops.lifecycle import COMPLETE
from deskops.lifecycle import LifecycleSpec
from deskops.lifecycle import SPEC_PATH
from deskops.lifecycle import Transition


def match_workflow_state(spec: LifecycleSpec, current_node: str) -> dict[str, Any]:
    """The state of ``deskops/spec/workflows/task_lifecycle.yaml`` whose ``current_node``
    is the task's; an empty node matches the first state."""
    node = current_node or ""
    for state in spec.states:
        if state.get("current_node") == node:
            return state
    if not node:
        return _first_state(spec)
    raise ValueError(f"No workflow state in {SPEC_PATH} matches current node '{current_node}'")


def render_workflow_mermaid(spec: LifecycleSpec, transitions: list[Transition]) -> str:
    """Mermaid of the lifecycle graph: one node per state, one arrow per transition of the
    desk's graph, labelled with its relation type and condition."""
    states = list(spec.states)
    by_node = {str(state.get("current_node")): str(state["id"]) for state in states}
    lines = ["flowchart TD"]
    for state in states:
        state_id = str(state["id"])
        label = str(state.get("phase") or state_id).replace('"', "'")
        lines.append(f'    {state_id}["{label}"]')
    for transition in transitions:
        source = by_node.get(transition.source, transition.source)
        target_node = COMPLETE if transition.terminal else transition.target
        target = by_node.get(target_node, target_node)
        label = transition.relation_type
        if transition.condition:
            label += f": {transition.condition}"
        lines.append(f'    {source} -->|"{label.replace(chr(34), chr(39))}"| {target}')
    return "\n".join(lines)


def _first_state(spec: LifecycleSpec) -> dict[str, Any]:
    if not spec.states:
        raise ValueError(f"Workflow spec has no states: {SPEC_PATH}")
    return spec.states[0]
