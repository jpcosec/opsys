from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from sldb.api.edges.project_graph import MissingProjectTarget as MissingGraphTarget

from deskops.atom_references import ALLOWED_ROLES
from deskops.atom_references import CANONICAL_FIELD
from deskops.atom_references import LEGACY_FIELD_VIOLATION
from deskops.atom_references import LEGACY_FIELDS
from deskops.atom_references import MATERIALIZATION_FIELD
from deskops.atom_references import iter_atom_reference_values
from deskops.atom_references import parse_atom_reference


from deskops.graph.desk_graph import extract_declared_edges
from deskops.graph.desk_graph import extract_doc_nodes
from deskops.graph.view import GraphReadError
from deskops.graph.view import GraphView
from deskops.graph.view import read_graph_file


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
    """Missing references of sldb's project graph (GD21), plus the dangling edges of a ``--graph`` file."""
    findings = [
        _finding_from_missing_target(missing)
        for missing in extract_declared_edges(root).missing_targets
        if not declared_target_is_a_file(root, missing.target_id)
    ]
    if graph_path is not None:
        try:
            snapshot = read_graph_file(graph_path)
        except GraphReadError as exc:
            raise GraphMissingCheckError(str(exc)) from exc
        findings.extend(find_missing_snapshot_targets(snapshot))
    return sorted(findings, key=lambda finding: (finding.kind, finding.source_id, finding.target_id))


def declared_target_is_a_file(root: Path, target_id: str) -> bool:
    """Whether a declared target the graph has no node for is still an existing file of the repo.

    The project graph makes nodes only for the files its surfaces extract, so an existing
    ``.yaml`` or ``.json`` (the plan's ``dag.yaml`` in the drawer, a test fixture) is reported as
    a missing target although it is there. CC33c read ``graph`` from sldb's project graph (GD21)
    and found it still makes no node for them, so the exception stays: such a target is not
    missing when, without its ``kind:`` prefix, it names a file inside ``root``. An atom reference, a path that does not exist, and a
    path that leaves ``root`` (absolute, or through ``..``) are still reported.
    """
    if target_id.startswith("atom:"):
        return False
    prefix, sep, rest = target_id.partition(":")
    relative = rest if sep and "/" not in prefix else target_id
    if not relative or Path(relative).is_absolute():
        return False
    base = Path(root).resolve()
    candidate = (base / relative).resolve()
    return candidate.is_relative_to(base) and candidate.is_file()


def find_missing_snapshot_targets(snapshot: GraphView) -> list[GraphMissingFinding]:
    """Return edges whose target id is absent from the graph's nodes."""
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

    The documents are the project graph's (sldb, GD21) under ``desk/`` and ``docs/``; only
    their frontmatter is a declaration. Fenced YAML blocks are examples, so they are not read.
    """
    project_root = Path(root)
    findings: list[AtomReferenceFinding] = []
    paths = {node.path for node in extract_doc_nodes(project_root) if node.path.endswith(".md") and node.path.split("/", 1)[0] in ("desk", "docs")}
    for relative_path in sorted(paths):
        if any(part.startswith(".") for part in Path(relative_path).parts):
            continue
        try:
            text = (project_root / relative_path).read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter = _frontmatter_mapping(text)
        if frontmatter is not None:
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
