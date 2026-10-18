"""Turn CLI arguments into artifact payloads.

This module is CLI-only: it translates argparse namespaces into the dicts the
operations/service layer consumes. It may import from ``deskops.operations``
(for the artifact model registry); ``deskops.operations`` must not import it,
so the dependency stays one-way.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from deskops.operations import ARTIFACT_MODELS


def parse_task_input(args: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    if getattr(args, "from_yaml", None):
        payload.update(_load_yaml_mapping(Path(args.from_yaml)))
    elif getattr(args, "payload", None):
        payload.update(_load_json_mapping(args.payload))

    if getattr(args, "title", None): payload["title"] = args.title
    if getattr(args, "why", None): payload["why"] = args.why
    if getattr(args, "goal", None): payload["goal"] = args.goal
    if getattr(args, "scope", None): payload["scope"] = args.scope
    if getattr(args, "implementation_path", None): payload["implementation_path"] = args.implementation_path
    if getattr(args, "done_when", None): payload["done_when"] = args.done_when
    if getattr(args, "validation", None): payload["validation"] = args.validation
    if getattr(args, "depends_on", None): payload["depends_on"] = args.depends_on
    if getattr(args, "task_type", None): payload["task_type"] = args.task_type
    if getattr(args, "inherits_from", None): payload["inherits_from"] = args.inherits_from
    if getattr(args, "atom", None): payload["atoms"] = args.atom
    if getattr(args, "inherit_acceptance_context", False): payload["inherit_acceptance_context"] = True

    return payload


def parse_artifact_input(artifact_id: str, args: Any) -> dict[str, Any]:
    """Parse a raw payload for artifact creation.

    YAML payload (--from-yaml) is loaded first, then CLI args override it.
    Field names come from the Pydantic model (the single source of truth),
    not from the YAML spec's fields list.
    """
    payload: dict[str, Any] = {}
    if getattr(args, "from_yaml", None):
        payload.update(_load_yaml_mapping(Path(args.from_yaml)))

    model = ARTIFACT_MODELS.get(artifact_id)
    if model is not None:
        # Iterate over model fields, not YAML spec fields
        for field_name in model.model_fields:
            if field_name == "id":
                continue  # id is generated from slug
            value = getattr(args, field_name, None)
            if isinstance(value, list) and value:
                payload[field_name] = list(value)
            elif value is not None and not isinstance(value, list):
                payload[field_name] = value

    return payload


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML payload in {path}: {exc}") from exc
    return _ensure_mapping_payload(payload, f"YAML payload in {path}")


def _load_json_mapping(raw: str) -> dict[str, Any]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON payload: {exc.msg}") from exc
    return _ensure_mapping_payload(payload, "JSON payload")


def _ensure_mapping_payload(payload: Any, label: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        kind = type(payload).__name__
        raise ValueError(f"{label} must be a mapping/object, got {kind}")
    return dict(payload)
