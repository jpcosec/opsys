from __future__ import annotations

import json
from pathlib import Path

from deskops.graph.checks import GraphMissingFinding
from deskops.graph.self_reflection import DEFAULT_REPORT_PATH
from deskops.graph.self_reflection import build_self_reflection_report
from deskops.graph.self_reflection import write_self_reflection_report


FIXTURE_GRAPH = Path(__file__).parent / "fixtures/knowledge_graph/static_desk_source_graph.json"


def test_self_reflection_report_generates_findings_and_writes_runtime_report(tmp_path: Path) -> None:
    snapshot = json.loads(FIXTURE_GRAPH.read_text(encoding="utf-8"))
    snapshot["nodes"].append(
        {
            "id": "source_file:deskops/unlinked.py",
            "kind": "source_file",
            "label": "Unlinked source",
            "identity": "deskops/unlinked.py",
            "path": "deskops/unlinked.py",
        }
    )
    snapshot["edges"].append(
        {
            "source": "task:task-004-create-static-graph-fixture",
            "target": "atom:atom-missing-reflection",
            "role": "references",
            "provenance_path": "desk/tasks/004-create-static-graph-fixture.md",
            "provenance_locator": "Related Atoms",
        }
    )

    report = build_self_reflection_report(snapshot)
    report_path = write_self_reflection_report(tmp_path, report)

    assert report_path == tmp_path / DEFAULT_REPORT_PATH
    assert report_path.exists()
    assert not (tmp_path / "desk").exists()
    assert report["runtime_only"] is True
    assert report["mutation_policy"] == "review_only_no_source_artifact_mutation"
    assert report["summary"] == {"finding_count": 2, "suppressed_duplicate_count": 0}
    assert report["findings"] == [
        {
            "question_id": "missing-atom-references",
            "kind": "dangling_source_atom_reference",
            "source_id": "task:task-004-create-static-graph-fixture",
            "target_id": "atom:atom-missing-reflection",
            "role": "references",
            "provenance_path": "desk/tasks/004-create-static-graph-fixture.md",
            "provenance_locator": "Related Atoms",
            "confidence": "high",
            "reason": "declared atom reference target was not found among graph nodes",
            "later_action": "atom_candidate",
            "dedupe_key": "missing-atom-references:task:task-004-create-static-graph-fixture:atom:atom-missing-reflection:references",
            "duplicate_count": 0,
        },
        {
            "question_id": "unlinked-source-files",
            "kind": "unlinked_source_file",
            "source_id": "source_file:deskops/unlinked.py",
            "target_id": None,
            "role": None,
            "provenance_path": "deskops/unlinked.py",
            "provenance_locator": "node:source_file:deskops/unlinked.py",
            "confidence": "medium",
            "reason": "source file has no graph edge connecting it to a desk knowledge surface",
            "later_action": "issue_candidate",
            "dedupe_key": "unlinked-source-files:source_file:deskops/unlinked.py",
            "duplicate_count": 0,
        },
    ]


def test_self_reflection_report_suppresses_duplicate_findings() -> None:
    snapshot = {
        "nodes": [{"id": "task:source", "kind": "task", "label": "Source"}],
        "edges": [
            {
                "source": "task:source",
                "target": "atom:missing",
                "role": "references",
                "provenance_path": "desk/tasks/source.md",
                "provenance_locator": "Related Atoms",
            },
            {
                "source": "task:source",
                "target": "atom:missing",
                "role": "references",
                "provenance_path": "desk/tasks/source.md",
                "provenance_locator": "YAML metadata",
            },
        ],
    }
    missing_findings = [
        GraphMissingFinding(
            kind="dangling_source_atom_reference",
            source_id="task:source",
            target_id="atom:missing",
            reason="declared target was not found among extracted graph nodes",
            role="references",
            provenance_path="desk/tasks/source.md",
            provenance_locator="line:3:yaml",
        )
    ]

    report = build_self_reflection_report(snapshot, missing_findings)

    assert report["summary"] == {"finding_count": 1, "suppressed_duplicate_count": 1}
    assert report["findings"][0]["dedupe_key"] == "missing-atom-references:task:source:atom:missing:references"
    assert report["findings"][0]["duplicate_count"] == 1
