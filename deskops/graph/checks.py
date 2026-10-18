from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import LEGACY_FIELD_VIOLATION
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD
from deskops.atom_references import iter_atom_reference_values
from deskops.atom_references import parse_atom_reference
from deskops.graph.extract_edges import MissingGraphTarget
from deskops.graph.extract_edges import extract_declared_edges
from deskops.graph.snapshot import GraphSnapshot
from deskops.graph.snapshot import GraphSnapshotReadError
from deskops.graph.snapshot import read_graph_snapshot


class GraphMissingCheckError(RuntimeError):
    """Raised when graph missing checks cannot read their input."""


@dataclass(frozen=True)
class GraphMissingFinding:
    kind: str
    source_id: str
    target_id: str
    reason: str
    role: str | None = None
    provenance_path: str | None = None
    provenance_locator: str | None = None
    extractor: str | None = None
    record: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def find_missing_graph_references(root: Path, graph_path: Path | None = None) -> list[GraphMissingFinding]:
    """Return missing graph references from declared source refs and optional snapshot edges."""
    findings = [_finding_from_missing_target(missing) for missing in extract_declared_edges(root).missing_targets]
    if graph_path is not None:
        try:
            snapshot = read_graph_snapshot(graph_path)
        except GraphSnapshotReadError as exc:
            raise GraphMissingCheckError(str(exc)) from exc
        findings.extend(find_missing_snapshot_targets(snapshot))
    return sorted(findings, key=lambda finding: (finding.kind, finding.source_id, finding.target_id))


def find_missing_snapshot_targets(snapshot: GraphSnapshot) -> list[GraphMissingFinding]:
    """Return edges whose target id is absent from a simple or KGDB-style graph snapshot."""
    node_ids = {node.id for node in snapshot.nodes}
    findings: list[GraphMissingFinding] = []
    seen: set[tuple[str, str, str | None]] = set()
    for edge in snapshot.edges:
        if edge.target in node_ids:
            continue
        key = (edge.source, edge.target, edge.role)
        if key in seen:
            continue
        seen.add(key)
        findings.append(
            GraphMissingFinding(
                kind="missing_edge_target",
                source_id=edge.source,
                target_id=edge.target,
                role=edge.role,
                provenance_path=edge.provenance_path,
                provenance_locator=edge.provenance_locator,
                extractor=edge.extractor,
                reason="edge target was not found among graph nodes",
            )
        )
    return sorted(findings, key=lambda finding: (finding.source_id, finding.target_id, finding.role or ""))


def _finding_from_missing_target(missing: MissingGraphTarget) -> GraphMissingFinding:
    kind = "dangling_source_atom_reference" if missing.target_id.startswith("atom:") else "missing_declared_target"
    return GraphMissingFinding(
        kind=kind,
        source_id=missing.source_id,
        target_id=missing.target_id,
        provenance_path=missing.provenance_path,
        provenance_locator=missing.provenance_locator,
        extractor=missing.extractor,
        reason=missing.reason,
        record=missing.record,
    )


@dataclass(frozen=True)
class AtomReferenceFinding:
    kind: str
    path: str
    locator: str
    reason: str
    atom_id: str | None = None
    role: str | None = None
    field_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def find_atom_reference_violations(root: Path) -> list[AtomReferenceFinding]:
    """Report invalid roles and legacy atom reference fields in Markdown frontmatter.

    Only frontmatter under ``desk/`` and ``docs/`` is a declaration. Fenced YAML
    blocks are examples, so they are not scanned.
    """
    project_root = Path(root)
    findings: list[AtomReferenceFinding] = []

    for surface in ("desk", "docs"):
        surface_root = project_root / surface
        if not surface_root.is_dir():
            continue
        for path in sorted(surface_root.rglob("*.md")):
            relative_parts = path.relative_to(project_root).parts
            if any(part.startswith(".") for part in relative_parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            frontmatter = _frontmatter_mapping(text)
            if frontmatter is None:
                continue
            relative_path = path.relative_to(project_root).as_posix()
            findings.extend(_atom_reference_findings(frontmatter, relative_path))

    return sorted(findings, key=lambda finding: (finding.path, finding.locator, finding.kind))


def _frontmatter_mapping(text: str) -> dict[Any, Any] | None:
    if not text.startswith("---\n"):
        return None
    try:
        _, rest = text.split("---\n", 1)
        block, _body = rest.split("\n---", 1)
    except ValueError:
        return None
    try:
        loaded = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return loaded if isinstance(loaded, dict) else None


def _atom_reference_findings(mapping: dict[Any, Any], path: str) -> list[AtomReferenceFinding]:
    findings: list[AtomReferenceFinding] = []
    fields: list[tuple[str, Any]] = []
    for field_name in (CANONICAL_FIELD, MATERIALIZATION_FIELD):
        if field_name in mapping:
            fields.append((field_name, mapping[field_name]))
    materialization = mapping.get("materialization")
    if isinstance(materialization, dict) and MATERIALIZATION_FIELD in materialization:
        fields.append(
            (f"materialization.{MATERIALIZATION_FIELD}", materialization[MATERIALIZATION_FIELD])
        )
    for field_name in LEGACY_FIELDS:
        if field_name in mapping:
            fields.append((field_name, mapping[field_name]))

    for field_name, value in fields:
        if field_name in LEGACY_FIELDS:
            findings.append(
                AtomReferenceFinding(
                    kind=LEGACY_FIELD_VIOLATION,
                    path=path,
                    locator=f"frontmatter:{field_name}",
                    field_name=field_name,
                    reason=(
                        f"uses legacy atom reference field {field_name}; "
                        f"declare atom references in {CANONICAL_FIELD}"
                    ),
                )
            )

        for index, item in enumerate(iter_atom_reference_values(value)):
            parsed = parse_atom_reference(item, field_name)
            if parsed is None or parsed.violation is None:
                continue
            findings.append(
                AtomReferenceFinding(
                    kind=parsed.violation,
                    path=path,
                    locator=f"frontmatter:{field_name}[{index}]",
                    atom_id=parsed.atom_id,
                    role=parsed.role,
                    field_name=field_name,
                    reason=(
                        f"atom {parsed.atom_id} declares invalid role {parsed.role!r}; "
                        f"allowed roles: {', '.join(ALLOWED_ROLES)}"
                    ),
                )
            )

    return findings
