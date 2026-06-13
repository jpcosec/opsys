from __future__ import annotations

from pathlib import Path

from deskops.graph.extract_sources import extract_source_file_nodes


def test_extract_source_file_nodes_reads_file_level_source_surfaces(tmp_path: Path) -> None:
    write(tmp_path / "deskops/operations.py", "def run() -> None:\n    pass\n")
    write(tmp_path / "deskops/cli/commands/atoms.py", "def main() -> None:\n    pass\n")
    write(tmp_path / "tests/test_atom_materialization.py", "def test_atom() -> None:\n    pass\n")
    write(tmp_path / "pyproject.toml", "[project]\nname = \"deskops\"\n")
    write(tmp_path / "desk/atoms/tag-namespaces.yaml", "namespaces: []\n")
    write(tmp_path / "spec/artifacts/atom.yaml", "id: artifact.atom\n")
    write(tmp_path / "spec/contracts/source-node.md", "# Source Node Contract\n")
    write(tmp_path / "desk/tasks/006-extract-source-file-graph-nodes.md", "# Task doc\n")
    write(tmp_path / "docs/knowledge-graph/desk-source-graph-vocabulary.md", "# Vocabulary doc\n")

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert set(by_id) == {
        "config_file:desk/atoms/tag-namespaces.yaml",
        "config_file:pyproject.toml",
        "source_file:deskops/cli/commands/atoms.py",
        "source_file:deskops/operations.py",
        "spec:spec/artifacts/atom.yaml",
        "spec:spec/contracts/source-node.md",
        "test_file:tests/test_atom_materialization.py",
    }
    assert by_id["source_file:deskops/operations.py"].kind == "source_file"
    assert by_id["source_file:deskops/operations.py"].identity == "deskops/operations.py"
    assert by_id["source_file:deskops/operations.py"].path == "deskops/operations.py"
    assert by_id["source_file:deskops/operations.py"].file_kind == "source"
    assert by_id["test_file:tests/test_atom_materialization.py"].file_kind == "test"
    assert by_id["config_file:pyproject.toml"].file_kind == "config"
    assert by_id["spec:spec/artifacts/atom.yaml"].file_kind == "spec"
    assert by_id["config_file:desk/atoms/tag-namespaces.yaml"].provenance == {
        "path": "desk/atoms/tag-namespaces.yaml",
        "source_kind": "path_rule",
        "extractor": "desk_source_file_nodes_v1",
    }


def test_extract_source_file_nodes_excludes_generated_runtime_outputs_by_default(
    tmp_path: Path,
) -> None:
    write(tmp_path / "deskops/operations.py", "# source\n")
    write(tmp_path / "deskops/__pycache__/operations.cpython-313.pyc", "compiled\n")
    write(tmp_path / ".sldb/runtime/source-graph.json", "{}\n")
    write(tmp_path / "tests/fixtures/knowledge_graph/static_desk_source_graph.json", "{}\n")
    write(tmp_path / "runtime.snapshot.json", "{}\n")

    nodes = extract_source_file_nodes(tmp_path)

    assert [node.id for node in nodes] == ["source_file:deskops/operations.py"]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
