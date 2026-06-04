from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from deskops.graph.checks import GraphMissingFinding
from deskops.graph.checks import find_missing_snapshot_targets


REPORT_SCHEMA = "deskops_self_reflection_report_v1"
DEFAULT_REPORT_PATH = Path(".sldb/runtime/self_reflection_findings.json")

ATOM_REFERENCE_ROLES = {"references", "documents", "specifies", "constrains", "validates"}
SOURCE_LINK_ROLES = {
    "references",
    "documents",
    "specifies",
    "constrains",
    "supports",
    "uses",
    "materializes",
    "implements",
    "validates",
    "tests",
    "violates",
    "invokes",
    "defines",
    "routes",
    "configures",
}
EXCLUDED_SOURCE_PREFIXES = (
    ".sldb/runtime/",
    "tests/fixtures/",
)
EXCLUDED_SOURCE_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
EXCLUDED_SOURCE_SUFFIXES = (
    ".graph.json",
    ".kgdb.json",
    ".snapshot.json",
)


@dataclass(frozen=True)
class SelfReflectionFinding:
    question_id: str
    kind: str
    source_id: str
    target_id: str | None
    role: str | None
    provenance_path: str
    provenance_locator: str
    confidence: str
    reason: str
    later_action: str
    dedupe_key: str
    duplicate_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_self_reflection_report(
    snapshot: dict[str, Any],
    missing_findings: list[GraphMissingFinding] | None = None,
) -> dict[str, Any]:
    """Return review-only self-reflection findings for a graph snapshot."""
    findings = [
        *_missing_atom_reference_findings(snapshot, missing_findings or []),
        *_unlinked_source_file_findings(snapshot),
    ]
    grouped_findings = _group_duplicate_findings(findings)
    return {
        "schema": REPORT_SCHEMA,
        "runtime_only": True,
        "mutation_policy": "review_only_no_source_artifact_mutation",
        "summary": {
            "finding_count": len(grouped_findings),
            "suppressed_duplicate_count": sum(finding.duplicate_count for finding in grouped_findings),
        },
        "findings": [finding.to_dict() for finding in grouped_findings],
    }


def write_self_reflection_report(
    root: Path,
    report: dict[str, Any],
    output_path: Path | None = None,
) -> Path:
    """Write a generated report to runtime storage, not to desk source artifacts."""
    destination = output_path or root / DEFAULT_REPORT_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination


def _missing_atom_reference_findings(
    snapshot: dict[str, Any],
    missing_findings: list[GraphMissingFinding],
) -> list[SelfReflectionFinding]:
    findings = [_missing_atom_finding_from_snapshot(edge) for edge in _missing_atom_edges(snapshot)]
    findings.extend(
        _missing_atom_finding_from_check(finding)
        for finding in missing_findings
        if finding.kind == "dangling_source_atom_reference" and finding.target_id.startswith("atom:")
    )
    return findings


def _missing_atom_edges(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    return [
        edge
        for edge in _snapshot_missing_targets(snapshot)
        if edge.target_id.startswith("atom:") and (edge.role or "") in ATOM_REFERENCE_ROLES
        for edge in [_missing_finding_to_edge(edge)]
    ]


def _snapshot_missing_targets(snapshot: dict[str, Any]) -> list[GraphMissingFinding]:
    return find_missing_snapshot_targets(snapshot)


def _missing_finding_to_edge(finding: GraphMissingFinding) -> dict[str, str]:
    return {
        "source_id": finding.source_id,
        "target_id": finding.target_id,
        "role": finding.role or "references",
        "provenance_path": finding.provenance_path or _path_from_node_id(finding.source_id),
        "provenance_locator": finding.provenance_locator or f"edge:{finding.source_id}:{finding.target_id}",
    }


def _missing_atom_finding_from_snapshot(edge: dict[str, str]) -> SelfReflectionFinding:
    return SelfReflectionFinding(
        question_id="missing-atom-references",
        kind="dangling_source_atom_reference",
        source_id=edge["source_id"],
        target_id=edge["target_id"],
        role=edge.get("role"),
        provenance_path=edge["provenance_path"],
        provenance_locator=edge["provenance_locator"],
        confidence="high",
        reason="declared atom reference target was not found among graph nodes",
        later_action="atom_candidate",
        dedupe_key=_dedupe_key("missing-atom-references", edge["source_id"], edge["target_id"], edge.get("role")),
    )


def _missing_atom_finding_from_check(finding: GraphMissingFinding) -> SelfReflectionFinding:
    role = finding.role or "references"
    return SelfReflectionFinding(
        question_id="missing-atom-references",
        kind="dangling_source_atom_reference",
        source_id=finding.source_id,
        target_id=finding.target_id,
        role=role,
        provenance_path=finding.provenance_path or _path_from_node_id(finding.source_id),
        provenance_locator=finding.provenance_locator or f"missing:{finding.source_id}:{finding.target_id}",
        confidence="high",
        reason="declared atom reference target was not found among graph nodes",
        later_action="atom_candidate",
        dedupe_key=_dedupe_key("missing-atom-references", finding.source_id, finding.target_id, role),
    )


def _unlinked_source_file_findings(snapshot: dict[str, Any]) -> list[SelfReflectionFinding]:
    nodes = _snapshot_nodes(snapshot)
    linked_source_ids = _linked_source_ids(snapshot)
    findings: list[SelfReflectionFinding] = []
    for node in nodes:
        if node.get("kind") != "source_file" or node["id"] in linked_source_ids:
            continue
        path = str(node.get("path") or node.get("identity") or _path_from_node_id(node["id"]))
        if _is_excluded_source_path(path):
            continue
        findings.append(
            SelfReflectionFinding(
                question_id="unlinked-source-files",
                kind="unlinked_source_file",
                source_id=node["id"],
                target_id=None,
                role=None,
                provenance_path=path,
                provenance_locator=f"node:{node['id']}",
                confidence="medium",
                reason="source file has no graph edge connecting it to a desk knowledge surface",
                later_action="issue_candidate",
                dedupe_key=f"unlinked-source-files:{node['id']}",
            )
        )
    return findings


def _linked_source_ids(snapshot: dict[str, Any]) -> set[str]:
    linked: set[str] = set()
    for edge in _snapshot_edges(snapshot):
        if edge.get("role") not in SOURCE_LINK_ROLES:
            continue
        for key in ("source", "target"):
            node_id = edge[key]
            if node_id.startswith("source_file:"):
                linked.add(node_id)
    return linked


def _snapshot_nodes(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    for node in snapshot.get("nodes", []):
        if "id" in node:
            nodes.append(node)
            continue
        identity = node.get("identity", {})
        node_id = identity.get("node_id")
        if not isinstance(node_id, str):
            continue
        semantics = node.get("semantics", {})
        nodes.append(
            {
                "id": node_id,
                "kind": identity.get("node_type"),
                "identity": semantics.get("identity") or _path_from_node_id(node_id),
                "path": semantics.get("path"),
            }
        )
    return nodes


def _snapshot_edges(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    if "edges" in snapshot:
        return [
            {
                "source": edge["source"],
                "target": edge["target"],
                "role": str(edge.get("role") or edge.get("relation_type") or "related"),
            }
            for edge in snapshot.get("edges", [])
        ]

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
                    "source": source_id,
                    "target": target_id,
                    "role": str(edge.get("relation_type") or metadata.get("role") or "related"),
                }
            )
    return edges


def _group_duplicate_findings(findings: list[SelfReflectionFinding]) -> list[SelfReflectionFinding]:
    grouped: dict[str, SelfReflectionFinding] = {}
    duplicate_counts: dict[str, int] = {}
    for finding in sorted(findings, key=lambda item: (item.dedupe_key, item.provenance_path, item.provenance_locator)):
        if finding.dedupe_key not in grouped:
            grouped[finding.dedupe_key] = finding
            duplicate_counts[finding.dedupe_key] = 0
            continue
        duplicate_counts[finding.dedupe_key] += 1
    return [
        SelfReflectionFinding(**{**finding.to_dict(), "duplicate_count": duplicate_counts[finding.dedupe_key]})
        for finding in grouped.values()
    ]


def _dedupe_key(question_id: str, source_id: str, target_id: str | None, role: str | None) -> str:
    return f"{question_id}:{source_id}:{target_id or ''}:{role or ''}"


def _path_from_node_id(node_id: str) -> str:
    return node_id.split(":", 1)[1] if ":" in node_id else node_id


def _is_excluded_source_path(path: str) -> bool:
    parts = Path(path).parts
    if any(part in EXCLUDED_SOURCE_PARTS for part in parts):
        return True
    if any(path.startswith(prefix) for prefix in EXCLUDED_SOURCE_PREFIXES):
        return True
    return any(path.endswith(suffix) for suffix in EXCLUDED_SOURCE_SUFFIXES)
