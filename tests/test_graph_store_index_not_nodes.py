"""The store's derived files are not graph nodes (fix(graph) ec296bf8 and 53951d08).

The `config_file` rule of `desk_graph.py` makes a node of any data file whose stem contains
`config`, `namespace` or `registry`. The `.yaml` files sldb derives under `.sldb/core/documents/`
and `.sldb_cache/` are named after the tracked documents, so a receipt of a task named
"...namespaces..." became a node. That node inherited the store index's unresolved
references, and closing the task made `deskops graph missing` report the receipt's subject as
missing (CC35d, 2026-11-10). Both directories are excluded; a real config file elsewhere keeps
its node.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops.graph.checks import find_missing_graph_references
from deskops.graph.desk_graph import desk_graph_config
from sldb.api.edges.project_graph.project_graph import ProjectGraph

DERIVED = (
    ".sldb/core/documents/ReviewDoc/review-task-x-reemplazo-namespaces-preflight-1.yaml",
    ".sldb/core/documents/PillDoc/pill-local-config-policy.yaml",
    ".sldb/core/documents/AtomDoc/atom-shared-registry-resolver.yaml",
    ".sldb_cache/edges/ReviewDoc/review-task-x-reemplazo-namespaces-bundle-1.yaml",
    ".sldb_cache/edges/AtomDoc/atom-project-config.yaml",
)
KEPT = "desk/tag-namespaces.yaml"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    for relative in (*DERIVED, KEPT):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("name: x\nsubject: doc:TaskCodeDoc:task-x\n", encoding="utf-8")
    return tmp_path


def _node_paths(root: Path) -> set[str]:
    graph = ProjectGraph(root, desk_graph_config())
    return set(graph.nodes.lookup.by_path)


def test_the_store_derived_yaml_files_are_not_graph_nodes(repo: Path) -> None:
    nodes = _node_paths(repo)
    assert not nodes & set(DERIVED)


def test_a_config_file_outside_the_store_keeps_its_node(repo: Path) -> None:
    assert KEPT in _node_paths(repo)


def test_graph_missing_reports_nothing_from_the_store_derived_files(repo: Path) -> None:
    found = find_missing_graph_references(repo)
    assert not [f for f in found if (f.provenance_path or "").startswith((".sldb/", ".sldb_cache/"))]
