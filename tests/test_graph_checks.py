from __future__ import annotations

from pathlib import Path

from deskops.graph.checks import find_missing_graph_references
from deskops.graph.checks import find_missing_snapshot_targets


def test_find_missing_snapshot_targets_reports_dangling_edge() -> None:
    snapshot = {
        "nodes": [{"id": "task:source", "kind": "task", "label": "Source"}],
        "edges": [
            {
                "source": "task:source",
                "target": "atom:missing",
                "role": "references",
                "provenance_path": "desk/tasks/source.md",
                "provenance_locator": "Related Atoms",
            }
        ],
    }

    findings = find_missing_snapshot_targets(snapshot)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "missing_edge_target",
            "source_id": "task:source",
            "target_id": "atom:missing",
            "reason": "edge target was not found among graph nodes",
            "role": "references",
            "provenance_path": "desk/tasks/source.md",
            "provenance_locator": "Related Atoms",
        }
    ]


def test_find_missing_snapshot_targets_accepts_clean_graph_fixture() -> None:
    snapshot = {
        "nodes": [
            {"id": "task:source", "kind": "task", "label": "Source"},
            {"id": "atom:target", "kind": "atom", "label": "Target"},
        ],
        "edges": [{"source": "task:source", "target": "atom:target", "role": "references"}],
    }

    assert find_missing_snapshot_targets(snapshot) == []


def test_find_missing_graph_references_reports_dangling_source_atom(tmp_path: Path) -> None:
    write(
        tmp_path / "docs/guide.md",
        """# Guide

```yaml
source_atoms:
  - atom-missing
```
""",
    )

    findings = find_missing_graph_references(tmp_path)

    assert [finding.to_dict() for finding in findings] == [
        {
            "kind": "dangling_source_atom_reference",
            "source_id": "doc:docs/guide.md",
            "target_id": "atom:atom-missing",
            "reason": "declared target was not found among extracted graph nodes",
            "provenance_path": "docs/guide.md",
            "provenance_locator": "line:3:yaml",
            "extractor": "desk_declared_edges_v1",
        }
    ]


def test_find_missing_graph_references_accepts_task_pill_references(tmp_path: Path) -> None:
    write(
        tmp_path / "desk/tasks/task-template-docs.md",
        """---
id: task-template-docs
references:
- desk/contexts/pill-template-docs.md
---

# Template docs
""",
    )
    write(
        tmp_path / "desk/contexts/pill-template-docs.md",
        """# Template docs pill

ID: pill-template-docs
""",
    )

    assert find_missing_graph_references(tmp_path) == []


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
