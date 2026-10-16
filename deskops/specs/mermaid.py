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
