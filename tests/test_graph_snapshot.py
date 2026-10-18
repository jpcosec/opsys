from __future__ import annotations

import json
from pathlib import Path

import pytest
from sldb.api.graph.snapshot import GraphSnapshot

from deskops.graph.snapshot import DEFAULT_SNAPSHOT_PATH
from deskops.graph.snapshot import LEGACY_SNAPSHOT_PATH
from deskops.graph.snapshot import GraphSnapshotReadError
from deskops.graph.snapshot import build_graph_snapshot
from deskops.graph.snapshot import default_snapshot_read_path
from deskops.graph.snapshot import networkx_path_for_snapshot
from deskops.graph.snapshot import read_graph_snapshot
from deskops.graph.snapshot import write_graph_snapshot


def test_build_graph_snapshot_combines_nodes_and_declared_edges(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")
    write(tmp_path / "deskops/operations.py", "def run() -> None:\n    pass\n")
    write(
        tmp_path / "desk/tasks/008-write-kgdb-graph-snapshot.md",
        """# Write KGDB graph snapshot

ID: task-008-write-kgdb-graph-snapshot

## Related Atoms

- atom-existing

## Notes

Explicit source file reference: `deskops/operations.py`.
""",
    )

    snapshot = build_graph_snapshot(tmp_path)
    validated = GraphSnapshot.model_validate(snapshot)
    nodes_by_id = {node.identity.node_id: node for node in validated.nodes}

    assert snapshot["metadata"]["schema"] == "deskops_kgdb_graph_snapshot_v1"
    assert snapshot["metadata"]["runtime_output_path"] == ".sldb/runtime/graphs/deskops.kg.json"
    assert snapshot["metadata"]["node_count"] >= 3
    assert snapshot["metadata"]["edge_count"] > 2
    assert "desk_kgdb_coverage_v1" in snapshot["metadata"]["source_extractors"]

    task_node = nodes_by_id["task:task-008-write-kgdb-graph-snapshot"]
    assert task_node.identity.node_type == "task"
    assert [(edge.target_id, edge.relation_type) for edge in task_node.edges] == [
        ("atom:atom-existing", "references"),
        ("source_file:deskops/operations.py", "references"),
    ]
    assert task_node.edges[0].metadata == {
        "role": "references",
        "source_kind": "declared",
        "confidence": "high",
        "provenance_path": "desk/tasks/008-write-kgdb-graph-snapshot.md",
        "provenance_locator": "line:7:related atoms",
        "extractor": "desk_declared_edges_v1",
    }
    assert any(node.identity.node_type == "facet" for node in validated.nodes)
    assert any(edge.relation_type == "answers" for node in validated.nodes for edge in node.edges)


def test_write_graph_snapshot_uses_ignored_runtime_path(tmp_path: Path) -> None:
    write_atom(tmp_path / "desk/atoms/atom-existing.md", "atom-existing", "Existing Atom")

    output_path = write_graph_snapshot(tmp_path)

    assert DEFAULT_SNAPSHOT_PATH.as_posix() == ".sldb/runtime/graphs/deskops.kg.json"
    assert output_path == tmp_path / DEFAULT_SNAPSHOT_PATH
    GraphSnapshot.model_validate(json.loads(output_path.read_text(encoding="utf-8")))


def test_snapshot_path_helpers_keep_projections_separate(tmp_path: Path) -> None:
    preferred = tmp_path / DEFAULT_SNAPSHOT_PATH
    legacy = tmp_path / LEGACY_SNAPSHOT_PATH

    assert networkx_path_for_snapshot(preferred) == (
        tmp_path / ".sldb/runtime/graphs/deskops.nx.json"
    )
    assert default_snapshot_read_path(tmp_path) == preferred

    write(legacy, "legacy")
    assert default_snapshot_read_path(tmp_path) == legacy

    write(preferred, "deskops")
    assert default_snapshot_read_path(tmp_path) == preferred


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_atom(path: Path, atom_id: str, title: str) -> None:
    write(
        path,
        f"""---
id: {atom_id}
title: {title}
five_wh_one_plus: what
tags: []
---

# {title}

## Answer

Existing knowledge.
""",
    )


def test_read_graph_snapshot_flattens_nested_edges() -> None:
    path = Path(__file__).parent / "fixtures/golden/graph_snapshot.kg.json"

    snapshot = read_graph_snapshot(path)

    atom = next(node for node in snapshot.nodes if node.id == "atom:atom-golden-one")
    assert atom.kind == "atom"
    assert atom.path == "desk/atoms/atom-golden-one.md"
    assert isinstance(atom.identity, dict)
    assert atom.identity["node_id"] == "atom:atom-golden-one"
    assert atom.label == "Golden atom one"

    edge = next(edge for edge in snapshot.edges if edge.source == "atom:atom-golden-one")
    assert edge.target == "facet:what"
    assert edge.role == "answers"
    assert edge.provenance_path == "desk/atoms/atom-golden-one.md"
    assert edge.provenance_locator == "frontmatter:five_wh_one_plus"
    assert edge.extractor == "desk_kgdb_coverage_v1"


def test_read_graph_snapshot_accepts_top_level_edges_and_id_identity(tmp_path: Path) -> None:
    snapshot = {
        "nodes": [{"identity": {"node_id": "task:source", "node_type": "task"}, "semantics": {"title": "Source"}}],
        "edges": [{"source": "task:source", "target": "atom:missing", "role": "references"}],
    }
    path = _write(tmp_path, json.dumps(snapshot))

    result = read_graph_snapshot(path)

    assert [(node.id, node.kind, node.label) for node in result.nodes] == [("task:source", "task", "Source")]
    assert [(edge.source, edge.target, edge.role) for edge in result.edges] == [
        ("task:source", "atom:missing", "references")
    ]


def test_read_graph_snapshot_rejects_missing_file(tmp_path: Path) -> None:
    path = tmp_path / "missing.json"

    with pytest.raises(GraphSnapshotReadError, match="graph snapshot not found"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_invalid_json(tmp_path: Path) -> None:
    path = _write(tmp_path, "{not json")

    with pytest.raises(GraphSnapshotReadError, match="not valid JSON"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_missing_key(tmp_path: Path) -> None:
    path = _write(tmp_path, json.dumps({"version": "1.0"}))

    with pytest.raises(GraphSnapshotReadError, match="missing the nodes list"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": [{"kind": "atom"}]}))

    with pytest.raises(GraphSnapshotReadError, match="missing its id"):
        read_graph_snapshot(path)


def test_read_graph_snapshot_rejects_malformed_shape(tmp_path: Path) -> None:
    path = _write(tmp_path, json.dumps({"nodes": {}}))

    with pytest.raises(GraphSnapshotReadError, match="missing the nodes list"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": ["node"]}))

    with pytest.raises(GraphSnapshotReadError, match="non-object node"):
        read_graph_snapshot(path)

    path = _write(tmp_path, json.dumps({"nodes": [{"id": "task:source", "edges": {}}]}))

    with pytest.raises(GraphSnapshotReadError, match="node edges must be a list"):
        read_graph_snapshot(path)


def _write(path: Path, content: str) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    target = path / "snapshot.json"
    target.write_text(content, encoding="utf-8")
    return target
