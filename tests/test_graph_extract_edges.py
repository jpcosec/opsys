from __future__ import annotations

from pathlib import Path

from deskops.graph.extract_edges import extract_declared_edges


def test_extract_declared_edges_returns_explicit_references_with_provenance(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/atom-source.md", "# Source Atom\n\nID: atom-source\n")
    write(tmp_path / "desk/atoms/atom-related.md", "# Related Atom\n\nID: atom-related\n")
    write(tmp_path / "desk/tasks/001-target.md", "# Target Task\n\nID: task-target\n")
    write(tmp_path / "desk/drawer/issues/issue-target.md", "# Target Issue\n\nID: issue-target\n")
    write(tmp_path / "deskops/operations.py", "def run() -> None:\n    pass\n")
    write(tmp_path / "docs/diagrams/example/source.mmd", "flowchart TB\n")
    write(
        tmp_path / "docs/guide.md",
        """# Guide

```yaml
source_atoms:
  - atom-source
```

## Related Atoms

- atom-related
""",
    )
    write(
        tmp_path / "desk/tasks/002-current.md",
        """# Current Task

ID: task-current

## Related Tasks

- task-target

## Related Issues

- issue-target

## Notes

Explicit source file reference: `deskops/operations.py`.
""",
    )
    write(
        tmp_path / "docs/diagrams/example/rendered.md",
        """# Rendered Diagram

## Diagram Sources

- docs/diagrams/example/source.mmd
""",
    )

    result = extract_declared_edges(tmp_path)
    edge_lookup = {(edge.source_id, edge.target_id, edge.role) for edge in result.edges}

    assert edge_lookup == {
        ("doc:docs/guide.md", "atom:atom-source", "references"),
        ("doc:docs/guide.md", "atom:atom-related", "references"),
        ("task:task-current", "task:task-target", "references"),
        ("task:task-current", "issue:issue-target", "references"),
        ("task:task-current", "source_file:deskops/operations.py", "references"),
        (
            "diagram:docs/diagrams/example/rendered.md",
            "diagram:docs/diagrams/example/source.mmd",
            "references",
        ),
    }
    assert result.missing_targets == []
    guide_edge = next(edge for edge in result.edges if edge.target_id == "atom:atom-source")
    assert guide_edge.source_kind == "declared"
    assert guide_edge.confidence == "high"
    assert guide_edge.provenance_path == "docs/guide.md"
    assert guide_edge.provenance_locator == "line:3:yaml"


def test_extract_declared_edges_reports_missing_targets(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/atom-existing.md", "# Existing\n\nID: atom-existing\n")
    write(
        tmp_path / "desk/drawer/issues/issue-missing-references.md",
        """# Missing References

ID: issue-missing-references

## Related Atoms

- atom-existing
- atom-missing

This explicitly names `deskops/missing.py`.
""",
    )

    result = extract_declared_edges(tmp_path)

    assert [(edge.source_id, edge.target_id) for edge in result.edges] == [
        ("issue:issue-missing-references", "atom:atom-existing")
    ]
    assert [missing.to_dict() for missing in result.missing_targets] == [
        {
            "source_id": "issue:issue-missing-references",
            "target_id": "atom:atom-missing",
            "provenance_path": "desk/drawer/issues/issue-missing-references.md",
            "provenance_locator": "line:8:related atoms",
            "reason": "declared target was not found among extracted graph nodes",
            "extractor": "desk_declared_edges_v1",
        },
        {
            "source_id": "issue:issue-missing-references",
            "target_id": "source_file:deskops/missing.py",
            "provenance_path": "desk/drawer/issues/issue-missing-references.md",
            "provenance_locator": "line:10:source-file-reference",
            "reason": "declared target was not found among extracted graph nodes",
            "extractor": "desk_declared_edges_v1",
        },
    ]


def test_extract_declared_edges_reads_drawer_question_maps(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/atom-workflow.md", "# Workflow\n\nID: atom-workflow\n")
    write(
        tmp_path / "desk/drawer/questions/workflow-question-map.md",
        """# Workflow Question Map

## Related Atoms

- atom-workflow
""",
    )

    result = extract_declared_edges(tmp_path)

    assert [(edge.source_id, edge.target_id, edge.role) for edge in result.edges] == [
        (
            "question:desk/drawer/questions/workflow-question-map.md",
            "atom:atom-workflow",
            "references",
        )
    ]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
