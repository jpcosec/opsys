from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deskops.graph.extract_edges import MissingGraphTarget
from deskops.graph.extract_edges import extract_declared_edges


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

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def find_missing_graph_references(root: Path, graph_path: Path | None = None) -> list[GraphMissingFinding]:
    """Return missing graph references from declared source refs and optional snapshot edges."""
    findings = [_finding_from_missing_target(missing) for missing in extract_declared_edges(root).missing_targets]
    if graph_path is not None:
        findings.extend(find_missing_snapshot_targets(read_graph_snapshot(graph_path)))
    return sorted(findings, key=lambda finding: (finding.kind, finding.source_id, finding.target_id))


def read_graph_snapshot(snapshot_path: Path) -> dict[str, Any]:
    if not snapshot_path.exists() or not snapshot_path.is_file():
        raise GraphMissingCheckError(f"graph snapshot not found: {snapshot_path}")
    return json.loads(snapshot_path.read_text(encoding="utf-8"))


def find_missing_snapshot_targets(snapshot: dict[str, Any]) -> list[GraphMissingFinding]:
    """Return edges whose target id is absent from a simple or KGDB-style graph snapshot."""
    node_ids = _snapshot_node_ids(snapshot)
    findings: list[GraphMissingFinding] = []
    seen: set[tuple[str, str, str | None]] = set()
    for edge in _snapshot_edges(snapshot):
        if edge["target_id"] in node_ids:
            continue
        key = (edge["source_id"], edge["target_id"], edge.get("role"))
        if key in seen:
            continue
        seen.add(key)
        findings.append(
            GraphMissingFinding(
                kind="missing_edge_target",
                source_id=edge["source_id"],
                target_id=edge["target_id"],
                role=edge.get("role"),
                provenance_path=edge.get("provenance_path"),
                provenance_locator=edge.get("provenance_locator"),
                extractor=edge.get("extractor"),
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
    )


def _snapshot_node_ids(snapshot: dict[str, Any]) -> set[str]:
    node_ids: set[str] = set()
    for node in snapshot.get("nodes", []):
        if isinstance(node.get("id"), str):
            node_ids.add(node["id"])
            continue
        identity = node.get("identity")
        if isinstance(identity, dict) and isinstance(identity.get("node_id"), str):
            node_ids.add(identity["node_id"])
    return node_ids


def _snapshot_edges(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    if "edges" in snapshot:
        return [_simple_snapshot_edge(edge) for edge in snapshot.get("edges", [])]

    edges: list[dict[str, str]] = []
    for node in snapshot.get("nodes", []):
        identity = node.get("identity", {})
        source_id = identity.get("node_id")
        if not isinstance(source_id, str):
            continue
        for edge in node.get("edges", []):
            target_id = edge.get("target_id")
            if not isinstance(target_id, str):
                continue
            metadata = edge.get("metadata", {})
            edges.append(
                {
                    "source_id": source_id,
                    "target_id": target_id,
                    "role": str(edge.get("relation_type") or metadata.get("role") or "related"),
                    **_edge_metadata(metadata),
                }
            )
    return edges


def _simple_snapshot_edge(edge: dict[str, Any]) -> dict[str, str]:
    metadata = edge.get("metadata", {})
    return {
        "source_id": edge["source"],
        "target_id": edge["target"],
        "role": str(edge.get("role") or edge.get("relation_type") or metadata.get("role") or "related"),
        **_edge_metadata(edge),
        **_edge_metadata(metadata),
    }


def _edge_metadata(edge: dict[str, Any]) -> dict[str, str]:
    return {
        key: value
        for key in ("provenance_path", "provenance_locator", "extractor")
        if isinstance((value := edge.get(key)), str)
    }
