"""Introspect Pydantic models to extract CLI-ready field metadata.

Replaces YAML-spec-driven CLI arg generation. The Pydantic model is the
single source of truth for field names, types, defaults, help text, and
validation rules.
"""
from __future__ import annotations

import typing
from dataclasses import dataclass, field as dataclass_field
from typing import Any, Collection

from pydantic import BaseModel, TypeAdapter
from pydantic.fields import FieldInfo, PydanticUndefined


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class CliFieldMeta:
    """Metadata for one CLI-exposed model field."""

    name: str  # Python field name (e.g. "five_wh_one_plus")
    cli_name: str  # CLI flag without dashes (e.g. "five-wh-one-plus")
    help: str  # argparse help text
    is_required: bool  # True when the model has no default
    is_list: bool  # True when the field is a list type
    choices: tuple[str, ...] | None  # Enum choices, if applicable
    default: Any  # Resolved default value or sentinel
    pattern: str | None  # Regex pattern from JSON schema, if any

    @property
    def cli_option(self) -> str:
        """The --flag name for argparse."""
        return f"--{self.cli_name.replace('_', '-')}"


DEFAULT_FACTORY = object()  # sentinel for fields with default_factory=list
REQUIRED = object()  # sentinel for fields with no default at all

# Mirror a small set of field defaults that are part of the operator-facing CLI
# contract for selected models. This keeps argparse metadata aligned with the
# model contract when these fields are intentionally optional/backward-compatible.
_MODEL_FIELD_DEFAULT_OVERRIDES: dict[tuple[str, str], Any] = {
    ("InboxNoteDoc", "target_project"): None,
    ("InboxNoteDoc", "acknowledged_by"): None,
    ("InboxNoteDoc", "acknowledged_at"): None,
}


# ---------------------------------------------------------------------------
# List detection
# ---------------------------------------------------------------------------


def _is_list_annotation(annotation: Any) -> bool:
    """Return True if annotation is list[...] or typing.List[...].
    
    Handles:
      - list[str]
      - typing.List[str]
      - Annotated[..., ...] wrapping a list
    """
    # Direct list origin
    origin = getattr(annotation, "__origin__", None)
    if origin is list or origin is typing.List:
        return True

    # Check Annotated[list[str], ...]
    if hasattr(annotation, "__metadata__"):
        # Walk the Annotated args looking for a list type
        args = getattr(annotation, "__args__", ())
        if args and _is_list_annotation(args[0]):
            return True

    return False


# ---------------------------------------------------------------------------
# Default resolution
# ---------------------------------------------------------------------------


def _resolve_field_default(field: FieldInfo) -> Any:
    """Return the resolved default for a Pydantic field.

    Returns DEFAULT_FACTORY when the field uses default_factory.
    Returns the actual default value when set explicitly (including None).
    Returns REQUIRED when there is no default (required field).
    """
    default = field.default
    if default is PydanticUndefined:
        factory = getattr(field, "default_factory", None)
        if factory is not None:
            return DEFAULT_FACTORY
        return REQUIRED
    return default


# ---------------------------------------------------------------------------
# Enum choice extraction
# ---------------------------------------------------------------------------


def _extract_enum_choices(
    model: type[BaseModel], field_name: str
) -> tuple[str, ...] | None:
    """Extract enum member values from a string enum field via JSON schema.

    Returns None when the field is not a string enum.
    """
    try:
        schema = TypeAdapter(model).json_schema()
    except Exception:
        return None

    props = schema.get("properties", {})
    field_schema = props.get(field_name, {})

    # Follow $ref if present
    ref = field_schema.get("$ref", "")
    if ref:
        defs = schema.get("$defs", {})
        key = ref.split("/")[-1]
        enum_def = defs.get(key, {})
        members = enum_def.get("enum")
        if members is not None and all(isinstance(v, str) for v in members):
            return tuple(str(v) for v in members)
        return None

    # Inline enum (rare)
    enum = field_schema.get("enum")
    if enum is not None:
        return tuple(str(v) for v in enum)

    return None


# ---------------------------------------------------------------------------
# Pattern extraction
# ---------------------------------------------------------------------------


def _extract_pattern(
    model: type[BaseModel], field_name: str
) -> str | None:
    """Extract the first regex pattern found in a field's JSON schema.

    Useful for Annotated fields like AtomTag that carry a pattern.
    """
    try:
        schema = TypeAdapter(model).json_schema()
    except Exception:
        return None

    props = schema.get("properties", {})
    field_schema = props.get(field_name, {})

    # Check top-level pattern
    pat = field_schema.get("pattern")
    if pat:
        return str(pat)

    # Check items level (for list types)
    items = field_schema.get("items", {})
    if isinstance(items, dict):
        pat = items.get("pattern")
        if pat:
            return str(pat)

    return None


# ---------------------------------------------------------------------------
# Core introspection
# ---------------------------------------------------------------------------

# Fields that are operational state or internal — never exposed as CLI args.
# These are managed by the runtime, not set by users at creation time.
_INTERNAL_FIELDS: frozenset[str] = frozenset({
    "id",
    "current_node",
    "history",
})

# Fields managed via a dedicated CLI flag rather than a generic --field option.


def introspect_model(model: type[BaseModel]) -> list[CliFieldMeta]:
    """Return CLI-ready metadata for every user-facing field in a Pydantic model.

    Fields are ordered as they appear in the model definition.

    Skipped fields:
    - ``id`` — generated by slugification
    - ``current_node``, ``history`` — managed by the lifecycle graph (deskops/lifecycle.py)
    - ``status`` — managed by lifecycle transitions on operational artifacts
    """
    results: list[CliFieldMeta] = []
    for name, fInfo in model.model_fields.items():
        if name in _INTERNAL_FIELDS:
            continue
        # status is internal for operational artifacts (TaskDoc, PillDoc, BoardDoc, etc.)
        # but a normal user-settable field for simple artifacts (RepositoryDoc).
        if name == "status":
            from deskops.models.base import OperationalArtifactDoc
            if issubclass(model, OperationalArtifactDoc):
                continue

        is_list = _is_list_annotation(fInfo.annotation)
        choices = _extract_enum_choices(model, name)
        pattern = _extract_pattern(model, name)
        default = _MODEL_FIELD_DEFAULT_OVERRIDES.get(
            (model.__name__, name),
            _resolve_field_default(fInfo),
        )
        is_required = default is REQUIRED

        # Use field description as help text
        help_text = fInfo.description or f"{name.replace('_', ' ').capitalize()}."

        results.append(
            CliFieldMeta(
                name=name,
                cli_name=name,
                help=help_text,
                is_required=is_required,
                is_list=is_list,
                choices=choices,
                default=default,
                pattern=pattern,
            )
        )

    return results


def model_cli_fields(
    model: type[BaseModel],
    *,
    include_special: bool = False,
) -> list[CliFieldMeta]:
    """Return CLI fields for a given model.

    The `include_special` flag controls exclusion of fields that have dedicated
    hardcoded CLI flags on the task subcommand (--depends-on, --validation).
    For non-task artifacts, these fields are normal user-settable fields and
    are always included.
    """
    metas = introspect_model(model)
    if include_special:
        # Task subcommand has hardcoded --depends-on and --validation flags.
        # Exclude them from generated args to avoid duplication.
        return [m for m in metas if m.name not in frozenset({"depends_on", "validation"})]
    return metas


def artifact_model_fields() -> dict[str, type[BaseModel]]:
    """Map artifact_id -> Pydantic model class for all artifact subjects.

    This is the authoritative mapping used by CLI arg generation.
    """
    from deskops.models import (
        AtomDoc,
        BoardDoc,
        DeskFAQDoc,
        InboxNoteDoc,
        MaterializationContractDoc,
        PillDoc,
        RepositoryDoc,
        RitualDoc,
        StepDoc,
    )

    return {
        "artifact.atom": AtomDoc,
        "artifact.board": BoardDoc,
        "artifact.faq": DeskFAQDoc,
        "artifact.inbox_note": InboxNoteDoc,
        "artifact.materialization": MaterializationContractDoc,
        "artifact.pill": PillDoc,
        "artifact.repository": RepositoryDoc,
        "artifact.ritual": RitualDoc,
        "artifact.step": StepDoc,
        # artifact.task uses a separate bundle creation path (not this path)
    }


# ---------------------------------------------------------------------------
# Artifact-level defaults
# ---------------------------------------------------------------------------

# id_pattern, status_default and tags are not field-level schema: each artifact model
# declares them as its ``__artifact__`` class attribute (a dict with those three keys).


def _artifact_defaults(artifact_id: str) -> dict[str, Any]:
    from deskops.doc_access import ARTIFACT_MODELS

    model = ARTIFACT_MODELS.get(artifact_id)
    if model is None:
        return {}
    return dict(getattr(model, "__artifact__", {}))


def artifact_id_pattern(artifact_id: str) -> str:
    """Return the id_pattern for an artifact. E.g. 'atom-{slug}'."""
    return _artifact_defaults(artifact_id).get("id_pattern", "{slug}")


def artifact_status_default(artifact_id: str) -> str | None:
    """Return the status_default for an artifact, or None if status is not managed."""
    return _artifact_defaults(artifact_id).get("status_default")


def artifact_tags_default(artifact_id: str) -> list[str]:
    """Return the default tags for an artifact when none are provided."""
    return list(_artifact_defaults(artifact_id).get("tags", []))
