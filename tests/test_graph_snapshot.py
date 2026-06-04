from __future__ import annotations

import json
from pathlib import Path

from kgdb.contracts.io import GraphSnapshot

from deskops.graph.snapshot import DEFAULT_SNAPSHOT_PATH
from deskops.graph.snapshot import build_graph_snapshot
from deskops.graph.snapshot import write_graph_snapshot


def test_build_graph_snapshot_combines_nodes_and_declared_edges(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/atom-existing.md", "# Existing Atom\n\nID: atom-existing\n")
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
    assert snapshot["metadata"]["runtime_output_path"] == ".sldb/runtime/knowledge_graph.kg.json"
    assert snapshot["metadata"]["node_count"] == 3
    assert snapshot["metadata"]["edge_count"] == 2

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


def test_write_graph_snapshot_uses_ignored_runtime_path(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/atom-existing.md", "# Existing Atom\n\nID: atom-existing\n")

    output_path = write_graph_snapshot(tmp_path)

    assert DEFAULT_SNAPSHOT_PATH.as_posix() == ".sldb/runtime/knowledge_graph.kg.json"
    assert output_path == tmp_path / DEFAULT_SNAPSHOT_PATH
    GraphSnapshot.model_validate(json.loads(output_path.read_text(encoding="utf-8")))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
