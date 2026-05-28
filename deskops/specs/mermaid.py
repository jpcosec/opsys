from __future__ import annotations

from .loader import SpecRegistry


def render_artifact_structure_mermaid(registry: SpecRegistry, artifact_id: str) -> str:
    artifact = registry.artifacts[artifact_id]
    lines = ["flowchart TD"]
    lines.append(f"  {artifact_id}[{artifact['title']}]")
    for field_id in artifact["data"].get("fields", []):
        lines.append(f"  {field_id}[{field_id}]")
        lines.append(f"  {artifact_id} --> {field_id}")
    return "\n".join(lines)


def render_task_routine_mermaid(registry: SpecRegistry, artifact_id: str) -> str:
    artifact = registry.artifacts[artifact_id]
    routine = artifact["data"]["operational"]["routine"]
    lines = ["flowchart TD"]
    decomposition = list(routine.get("decomposition", []))
    for node in decomposition:
        lines.append(f"  {node}[{_label_for_node(node)}]")
    for current, nxt in zip(decomposition, decomposition[1:]):
        lines.append(f"  {current} --> {nxt}")
    lines.append("  operator-task-id-close --> complete[complete]")
    return "\n".join(lines)


def _label_for_node(node: str) -> str:
    if "execution-ready" in node:
        return "Execution Ready"
    if "testing-ready" in node:
        return "Testing Ready"
    if "closeout-ready" in node:
        return "Closeout Ready"
    if node.endswith("activate"):
        return "Activate Task"
    if node.endswith("ready-for-testing"):
        return "Ready For Testing"
    if node.endswith("close"):
        return "Close Task"
    return node
