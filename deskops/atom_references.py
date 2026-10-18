"""Canonical atom reference metadata.

One artifact field carries structured atom references: ``atoms``. A reference is
either a bare atom id or a mapping with an ``id`` and an optional ``role``. The
role vocabulary is deliberately small; ``related_atoms`` is a legacy alias that
``deskops drift check`` reports, and ``source_atoms`` remains the
``MaterializationContractDoc`` field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


CANONICAL_FIELD = "atoms"
LEGACY_FIELDS = ("related_atoms",)
MATERIALIZATION_FIELD = "source_atoms"
ALLOWED_ROLES = ("references", "documents", "specifies", "constrains", "validates")
DEFAULT_ROLE = "references"

INVALID_ROLE_VIOLATION = "invalid_atom_reference_role"
LEGACY_FIELD_VIOLATION = "legacy_atom_reference_field"


@dataclass(frozen=True)
class ParsedAtomReference:
    """One declared atom reference.

    ``role`` keeps the declared value even when it is invalid; ``violation``
    names the problem so extractors can fall back to ``DEFAULT_ROLE`` while the
    drift validator reports the declaration instead of hiding it.
    """

    atom_id: str
    role: str
    field_name: str
    violation: str | None = None

    def as_tuple(self) -> tuple[str, str, str]:
        return (self.atom_id, self.role, self.field_name)


def parse_atom_reference(
    value: Any,
    field_name: str = CANONICAL_FIELD,
) -> ParsedAtomReference | None:
    """Parse a string or ``{id, role}`` mapping into an atom reference.

    Returns ``None`` when the value is not a reference shape. An unknown role is
    returned as an explicit ``invalid_atom_reference_role`` violation; it is
    never silently rewritten here.
    """
    if isinstance(value, str):
        atom_id = value.strip()
        if not atom_id:
            return None
        return ParsedAtomReference(atom_id=atom_id, role=DEFAULT_ROLE, field_name=field_name)

    if not isinstance(value, dict):
        return None

    atom_id = value.get("id")
    if not isinstance(atom_id, str) or not atom_id.strip():
        return None

    role = value.get("role")
    if not isinstance(role, str) or not role.strip():
        return ParsedAtomReference(
            atom_id=atom_id.strip(),
            role=DEFAULT_ROLE,
            field_name=field_name,
        )

    role = role.strip()
    violation = None if role in ALLOWED_ROLES else INVALID_ROLE_VIOLATION
    return ParsedAtomReference(
        atom_id=atom_id.strip(),
        role=role,
        field_name=field_name,
        violation=violation,
    )


def iter_atom_reference_values(value: Any) -> list[Any]:
    """Normalize a declared field value to the reference shapes to parse."""
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]
