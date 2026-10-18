from __future__ import annotations

from pathlib import Path

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import DEFAULT_ROLE
from deskops.atom_references import LEGACY_FIELD_VIOLATION
from deskops.atom_references import parse_atom_reference
from deskops.graph.checks import find_atom_reference_violations


def test_valid_roles_pass(tmp_path: Path) -> None:
    roles = "".join(f"  - {{id: atom-{role}, role: {role}}}\n" for role in ALLOWED_ROLES)
    write(
        tmp_path / "docs/guide.md",
        f"""---
{CANONICAL_FIELD}:
{roles}  - atom-bare
---
# Guide
""",
    )

    assert find_atom_reference_violations(tmp_path) == []


def test_unknown_role_produces_one_finding(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """---
atoms:
  - id: atom-known
    role: documents
  - id: atom-unknown
    role: explains
---
# Guide
""",
    )

    findings = find_atom_reference_violations(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "invalid_atom_reference_role",
            "path": "docs/guide.md",
            "locator": "frontmatter:atoms[1]",
            "reason": "atom atom-unknown declares invalid role 'explains'; allowed roles: references, documents, specifies, constrains, validates",
            "atom_id": "atom-unknown",
            "role": "explains",
            "field_name": "atoms",
        }
    ]


def test_related_atoms_produces_one_legacy_finding(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/atoms/atom-source.md",
        """---
id: atom-source
related_atoms:
  - atom-first
  - atom-second
---
# Source
""",
    )

    findings = find_atom_reference_violations(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": LEGACY_FIELD_VIOLATION,
            "path": "desk/atoms/atom-source.md",
            "locator": "frontmatter:related_atoms",
            "reason": "uses legacy atom reference field related_atoms; declare atom references in atoms",
            "field_name": "related_atoms",
        }
    ]


def test_bare_string_maps_to_references() -> None:
    parsed = parse_atom_reference("atom-bare")

    assert parsed is not None
    assert parsed.as_tuple() == ("atom-bare", DEFAULT_ROLE, CANONICAL_FIELD)
    assert parsed.violation is None


def test_mapping_without_role_maps_to_references() -> None:
    parsed = parse_atom_reference({"id": "atom-bare"})

    assert parsed is not None
    assert parsed.as_tuple() == ("atom-bare", DEFAULT_ROLE, CANONICAL_FIELD)
    assert parsed.violation is None


def test_fenced_yaml_examples_are_not_scanned(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """---
title: Guide
---
# Guide

```yaml
atoms:
  - id: atom-example
    role: explains
related_atoms:
  - atom-example
```
""",
    )

    assert find_atom_reference_violations(tmp_path) == []


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
