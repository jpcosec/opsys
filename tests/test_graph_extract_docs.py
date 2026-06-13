from __future__ import annotations

from pathlib import Path

from deskops.graph.extract_docs import extract_doc_nodes


def test_extract_doc_nodes_reads_only_desk_document_surfaces(tmp_path: Path) -> None:
    write(tmp_path / "desk/atoms/workflow/atom-documents-point-to-atoms.md", """---
id: atom-documents-point-to-atoms
five_wh_one_plus: what
tags:
- system:deskops
---

# Documents point to atoms
""")
    write(tmp_path / "desk/tasks/005-extract-desk-doc-graph-nodes.md", """# Extract desk doc graph nodes

ID: task-005-extract-desk-doc-graph-nodes
""")
    write(tmp_path / "desk/tasks/Board.md", "# Tasks Board\n")
    write(tmp_path / "desk/drawer/issues/issue-integrate-kgdb.md", "# Integrate KGDB\n")
    write(tmp_path / "docs/knowledge-graph/desk-source-graph-vocabulary.md", """# Desk Source Graph Vocabulary

ID: desk-source-graph-vocabulary
""")
    write(tmp_path / "docs/diagrams/codebase/codebase-knowledge-surfaces.md", "# Codebase Knowledge Surfaces\n")
    write(tmp_path / "docs/diagrams/codebase/codebase-knowledge-surfaces.mmd", "flowchart TB\n")
    write(tmp_path / "spec/artifacts/atom.yaml", """id: artifact.atom
title: Atom Artifact
type: artifact
""")
    write(tmp_path / "deskops/operations.py", "# source file must not become a node\n")
    write(tmp_path / "tests/test_atom_materialization.py", "# test file must not become a node\n")

    nodes = extract_doc_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert set(by_id) == {
        "atom:atom-documents-point-to-atoms",
        "task:task-005-extract-desk-doc-graph-nodes",
        "issue:integrate-kgdb",
        "doc:docs/knowledge-graph/desk-source-graph-vocabulary.md",
        "diagram:docs/diagrams/codebase/codebase-knowledge-surfaces.md",
        "diagram:docs/diagrams/codebase/codebase-knowledge-surfaces.mmd",
        "spec:spec/artifacts/atom.yaml",
    }
    assert by_id["atom:atom-documents-point-to-atoms"].kind == "atom"
    assert by_id["atom:atom-documents-point-to-atoms"].path == "desk/atoms/workflow/atom-documents-point-to-atoms.md"
    assert by_id["atom:atom-documents-point-to-atoms"].label == "Documents point to atoms"
    assert by_id["atom:atom-documents-point-to-atoms"].document_id == "atom-documents-point-to-atoms"
    assert by_id["doc:docs/knowledge-graph/desk-source-graph-vocabulary.md"].document_id == "desk-source-graph-vocabulary"
    assert by_id["spec:spec/artifacts/atom.yaml"].document_id == "artifact.atom"
    assert by_id["spec:spec/artifacts/atom.yaml"].label == "Atom Artifact"
    assert by_id["diagram:docs/diagrams/codebase/codebase-knowledge-surfaces.mmd"].label == "Codebase Knowledge Surfaces"
    assert by_id["task:task-005-extract-desk-doc-graph-nodes"].provenance == {
        "path": "desk/tasks/005-extract-desk-doc-graph-nodes.md",
        "source_kind": "file_metadata",
        "extractor": "desk_doc_nodes_v1",
    }


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
