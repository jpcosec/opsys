from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from collections.abc import Collection

from pydantic.fields import PydanticUndefined

from deskops.cli.model_introspection import artifact_id_pattern
from deskops.cli.model_introspection import artifact_tags_default
from deskops.cli.model_introspection import DEFAULT_FACTORY
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
        "why": str(raw_payload.get("why") or "Not provided."),
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
        "task_type": str(raw_payload.get("task_type") or ""),
        "inherits_from": _coerce_list(raw_payload.get("inherits_from") or []),
        "inherit_acceptance_context": bool(raw_payload.get("inherit_acceptance_context") or False),
        "atoms": _coerce_list(raw_payload.get("atoms") or []),
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
    """Compile a raw payload into an artifact payload using the Pydantic model.

    The Pydantic model is the single source of truth for which fields exist and
    their defaults. The YAML spec (via registry) is consulted only for artifact-
    level config: id_pattern and status_default.
    """
    from deskops.operations import ARTIFACT_MODELS

    artifact = registry.artifacts[artifact_id]
    display_value = raw_payload.get("title") or raw_payload.get("name") or raw_payload.get("id")
    if display_value is None:
        raise KeyError(f"Payload for {artifact_id} must include 'title', 'name', or 'id'")
    title = str(display_value).strip()
    if not title:
        raise ValueError(f"Payload for {artifact_id} has empty title/name/id after stripping whitespace")
    slug = _slugify(title)

    # id_pattern from model_introspection (was in YAML doc section)
    id_pattern = artifact_id_pattern(artifact_id)
    doc_id = str(raw_payload.get("id") or id_pattern.format(slug=slug))

    supported = set(model_fields or [])
    payload: dict[str, Any] = {"id": doc_id}
    if "title" in supported:
        payload["title"] = title

    model = ARTIFACT_MODELS.get(artifact_id)
    if model is not None:
        for field_name, field_info in model.model_fields.items():
            if field_name == "id":
                continue  # already handled

            # Value from raw_payload overrides everything
            if field_name in raw_payload and raw_payload[field_name] is not None:
                payload[field_name] = raw_payload[field_name]
                continue

            # Apply defaults from the Pydantic model
            default = field_info.default
            if default is PydanticUndefined:
                factory = getattr(field_info, "default_factory", None)
                if factory is not None:
                    payload[field_name] = []  # default_factory=list
                # else: required field, leave as None (model validation handles it)
            elif isinstance(default, str):
                payload[field_name] = default
            elif isinstance(default, (list, tuple)):
                payload[field_name] = list(default)
            # else: other default types — leave for model validation

    # Handle status_default from artifact config (not in model)
    if "status" in supported and "status" not in payload:
        status_default = str(artifact["data"]["doc"].get("status_default", "active"))
        payload["status"] = status_default

    # Handle tags default — prefer model factory, fall back to artifact config
    if "tags" in supported and "tags" not in payload:
        # Check if model has default_factory for tags
        if model is not None and "tags" in model.model_fields:
            field_info = model.model_fields["tags"]
            factory = getattr(field_info, "default_factory", None)
            if factory is not None:
                payload["tags"] = []
            else:
                payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))
        else:
            payload["tags"] = _coerce_list(artifact_tags_default(artifact_id))

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
