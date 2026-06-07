from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main
from deskops.graph.snapshot import DEFAULT_SNAPSHOT_PATH
from deskops.graph.snapshot import GraphSnapshotCapabilityError

FIXTURE_GRAPH = Path(__file__).parent / "fixtures/knowledge_graph/static_desk_source_graph.json"


def test_graph_neighbors_shows_fixture_node_neighbors(capsys) -> None:
    result = main(
        [
            "graph",
            "neighbors",
            "atom:atom-documents-point-to-atoms",
            "--graph",
            str(FIXTURE_GRAPH),
        ]
    )

    captured = capsys.readouterr()
    assert result == 0
    assert "Node: atom:atom-documents-point-to-atoms (Documents point to atoms)" in captured.out
    assert "Outgoing:\n- none" in captured.out
    assert "doc:docs/knowledge-graph/desk-source-graph-vocabulary.md" in captured.out
    assert "source_file:desk/materializers/atoms.py" in captured.out
    assert "test_file:tests/test_atom_materialization.py" in captured.out
    assert "references" in captured.out
    assert "implements" in captured.out
    assert "validates" in captured.out


def test_graph_neighbors_reports_missing_graph_file(tmp_path: Path, capsys) -> None:
    graph_path = tmp_path / "missing-graph.json"

    result = main(["graph", "neighbors", "task:any", "--graph", str(graph_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert f"Error: graph snapshot not found: {graph_path}" in captured.out


def test_graph_neighbors_reports_missing_node(capsys) -> None:
    result = main(["graph", "neighbors", "node:missing", "--graph", str(FIXTURE_GRAPH)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Error: graph node not found: node:missing" in captured.out


def test_graph_build_writes_runtime_snapshot(tmp_path: Path, capsys) -> None:
    write(tmp_path / "desk/atoms/atom-existing.md", "# Existing Atom\n\nID: atom-existing\n")

    result = main(["graph", "build", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    output_path = tmp_path / DEFAULT_SNAPSHOT_PATH
    assert result == 0
    assert f"Graph snapshot written: {output_path}" in captured.out
    assert output_path.exists()


def test_graph_build_reports_missing_kgdb_capability(tmp_path: Path, monkeypatch, capsys) -> None:
    def unavailable(_root: Path) -> Path:
        raise GraphSnapshotCapabilityError("KGDB graph snapshot validation is unavailable.")

    monkeypatch.setattr("deskops.graph.snapshot.write_graph_snapshot", unavailable)

    result = main(["graph", "build", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Error: KGDB graph snapshot validation is unavailable." in captured.out
    assert not (tmp_path / DEFAULT_SNAPSHOT_PATH).exists()


def test_graph_build_rejects_missing_root(tmp_path: Path, capsys) -> None:
    missing_root = tmp_path / "missing"

    result = main(["graph", "build", "--root", str(missing_root)])

    captured = capsys.readouterr()
    assert result == 1
    assert f"Error: Provided --root is not a valid directory: {missing_root}" in captured.err


def test_graph_missing_reports_clean_fixture(tmp_path: Path, capsys) -> None:
    result = main(["graph", "missing", "--root", str(tmp_path), "--graph", str(FIXTURE_GRAPH)])

    captured = capsys.readouterr()
    assert result == 0
    assert "No missing graph references found." in captured.out


def test_graph_missing_reports_dangling_source_atom(tmp_path: Path, capsys) -> None:
    write(
        tmp_path / "docs/guide.md",
        """# Guide

```yaml
source_atoms:
  - atom-missing
```
""",
    )

    result = main(["graph", "missing", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "Missing graph references:" in captured.out
    assert "dangling_source_atom_reference: doc:docs/guide.md -> atom:atom-missing" in captured.out
    assert "provenance: docs/guide.md:line:3:yaml" in captured.out


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
