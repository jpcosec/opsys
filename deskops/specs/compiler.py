from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from collections.abc import Collection

from .loader import SpecRegistry


@dataclass(slots=True)
class CompiledTaskBundleSpec:
    task_payload: dict[str, Any]
    condition_payloads: list[dict[str, Any]]
    checklist_payloads: list[dict[str, Any]]
    operator_payloads: list[dict[str, Any]]
    edge_payloads: list[dict[str, Any]]
    routine_payload: dict[str, Any]


@dataclass(slots=True)
class CompiledArtifactSpec:
    artifact_payload: dict[str, Any]


def compile_task_bundle_spec(
    registry: SpecRegistry,
    raw_payload: dict[str, Any],
) -> CompiledTaskBundleSpec:
    artifact = registry.artifacts["artifact.task"]
    title = str(raw_payload["title"]).strip()
    slug = _slugify(title)
    task_id = str(raw_payload.get("id") or artifact["data"]["doc"]["id_pattern"].format(slug=slug))
    context = {
        "title": title,
        "slug": slug,
        "task_id": task_id,
    }

    task_payload = {
        "title": title,
        "id": task_id,
        "status": str(raw_payload.get("status") or artifact["data"]["doc"].get("status_default", "draft")),
        "why": str(raw_payload.get("why") or ""),
        "goal": str(raw_payload.get("goal") or ""),
        "scope": str(raw_payload.get("scope") or ""),
        "references": _coerce_list(raw_payload.get("references") or []),
        "depends_on": _coerce_list(raw_payload.get("depends_on") or []),
        "pills": _coerce_list(raw_payload.get("pills") or []),
        "files": _coerce_list(raw_payload.get("files") or []),
        "implementation_path": str(raw_payload.get("implementation_path") or ""),
        "validation": _coerce_list(raw_payload.get("validation") or []),
        "done_when": str(raw_payload.get("done_when") or ""),
        "history": _coerce_list(raw_payload.get("history") or []),
        "tags": _coerce_list(raw_payload.get("tags") or artifact["data"]["doc"].get("tags", [])),
    }
    context["status"] = task_payload["status"]

    condition_payloads = _compile_primitives(registry, artifact["data"]["operational"]["conditions"], context)
    checklist_payloads = _compile_primitives(registry, artifact["data"]["operational"]["checklists"], context)
    operator_payloads = _compile_primitives(registry, artifact["data"]["operational"]["operators"], context)
    edge_payloads = _compile_edge_sets(registry, artifact["data"]["operational"]["edges"], context)
    routine_payload = _compile_mapping(artifact["data"]["operational"]["routine"], context)
    routine_payload["edges"] = [item["id"] for item in edge_payloads]
    routine_payload["tags"] = ["workspace:desk", "primitive:routine"]

    task_payload["routine"] = routine_payload["id"]
    task_payload["checklists"] = [item["id"] for item in checklist_payloads]
    task_payload["current_node"] = routine_payload["entrypoint"]
    context["current_node"] = task_payload["current_node"]

    return CompiledTaskBundleSpec(
        task_payload=task_payload,
        condition_payloads=condition_payloads,
        checklist_payloads=checklist_payloads,
        operator_payloads=operator_payloads,
        edge_payloads=edge_payloads,
        routine_payload=routine_payload,
    )


def compile_artifact_spec(
    registry: SpecRegistry,
    artifact_id: str,
    raw_payload: dict[str, Any],
    *,
    model_fields: Collection[str] | None = None,
) -> CompiledArtifactSpec:
    artifact = registry.artifacts[artifact_id]
    display_value = raw_payload.get("title") or raw_payload.get("name") or raw_payload.get("id")
    if display_value is None:
        raise KeyError(f"Payload for {artifact_id} must include 'title', 'name', or 'id'")
    title = str(display_value).strip()
    if not title:
        raise ValueError(f"Payload for {artifact_id} has empty title/name/id after stripping whitespace")
    slug = _slugify(title)
    artifact_doc = artifact["data"]["doc"]
    doc_id = str(raw_payload.get("id") or artifact_doc["id_pattern"].format(slug=slug))

    supported = set(model_fields or [])
    payload: dict[str, Any] = {"id": doc_id}
    if "title" in supported:
        payload["title"] = title

    for field_id in artifact["data"].get("fields", []):
        field_spec = registry.fields[field_id]
        field_key = str(field_spec["data"]["key"])
        value = raw_payload.get(field_key, field_spec["data"].get("default"))
        payload[field_key] = value

    if "status" in supported and "status" not in raw_payload:
        payload["status"] = str(artifact_doc.get("status_default", "active"))
    if "tags" in supported and "tags" not in raw_payload:
        payload["tags"] = _coerce_list(artifact_doc.get("tags", []))
    if "routine" in supported and "routine" not in raw_payload:
        payload["routine"] = ""
    if "current_node" in supported and "current_node" not in raw_payload:
        payload["current_node"] = ""
    if "history" in supported and "history" not in raw_payload:
        payload["history"] = _coerce_list(raw_payload.get("history") or [])

    return CompiledArtifactSpec(artifact_payload=payload)


def _compile_primitives(
    registry: SpecRegistry,
    primitive_ids: list[str],
    context: dict[str, str],
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for primitive_id in primitive_ids:
        spec = registry.primitives[primitive_id]
        payloads.append(_compile_mapping(spec["data"]["template"], context))
    return payloads


def _compile_edge_sets(
    registry: SpecRegistry,
    primitive_ids: list[str],
    context: dict[str, str],
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for primitive_id in primitive_ids:
        spec = registry.primitives[primitive_id]
        template = spec["data"]["template"]
        if isinstance(template, list):
            for item in template:
                payloads.append(_compile_mapping(item, context))
    return payloads


def _compile_mapping(value: Any, context: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: _compile_mapping(item, context) for key, item in value.items()}
    if isinstance(value, list):
        return [_compile_mapping(item, context) for item in value]
    if isinstance(value, str):
        return value.format(**context)
    return value


def _coerce_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value in (None, ""):
        return []
    return [str(value)]


def _slugify(text: str) -> str:
    lowered = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    parts = [part for part in lowered.split("-") if part]
    return "-".join(parts) or "item"
