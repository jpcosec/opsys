from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
