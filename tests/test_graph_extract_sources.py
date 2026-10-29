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


def test_extract_source_file_nodes_skips_vendored_tools_and_tmp_trees(tmp_path: Path) -> None:
    write(tmp_path / "deskops/operations.py", "# source\n")
    write(tmp_path / "tools/x/deskops/impl.py", "# vendored source\n")
    write(tmp_path / "tools/x/pyproject.toml", "[project]\nname = \"vendored\"\n")
    write(tmp_path / ".tmp/scratch/deskops/impl.py", "# scratch source\n")

    nodes = extract_source_file_nodes(tmp_path)

    assert [node.id for node in nodes] == ["source_file:deskops/operations.py"]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_materialization(path: Path, target_identity: str) -> None:
    """Write a minimal MaterializationContractDoc with the given target_identity."""
    write(
        path,
        f"""---
id: {path.stem}
title: Test Materialization
source_atoms:
- atom-test
target_kind: source_file
target_identity: {target_identity}
validation:
- pytest
tags: []
---

# Test Materialization

## Intent

Test materialization.
""",
    )


def test_declared_target_src_file_becomes_source_node(tmp_path: Path) -> None:
    """A declared target src/vsm/organs/links.py becomes a source_file node."""
    write(tmp_path / "src/vsm/organs/links.py", "# links\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-links.md",
        "src/vsm/organs/links.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:src/vsm/organs/links.py" in by_id
    node = by_id["source_file:src/vsm/organs/links.py"]
    assert node.kind == "source_file"
    assert node.identity == "src/vsm/organs/links.py"
    assert node.path == "src/vsm/organs/links.py"
    assert node.file_kind == "source"
    assert node.provenance["source_kind"] == "declared_materialization_target"


def test_declared_target_github_workflow_becomes_source_node(tmp_path: Path) -> None:
    """A declared target .github/workflows/pulse.yml becomes a source_file node."""
    write(tmp_path / ".github/workflows/pulse.yml", "name: Pulse\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-pulse.md",
        ".github/workflows/pulse.yml",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:.github/workflows/pulse.yml" in by_id
    node = by_id["source_file:.github/workflows/pulse.yml"]
    assert node.provenance["source_kind"] == "declared_materialization_target"


def test_declared_target_doc_surface_produces_no_source_node(tmp_path: Path) -> None:
    """A declared Markdown target under docs produces no source_file node."""
    write(tmp_path / "docs/guide.md", "# Guide\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-guide.md",
        "docs/guide.md",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # No source_file node for the doc surface
    assert "source_file:docs/guide.md" not in ids


def test_declared_target_already_matched_by_path_rule_not_duplicated(tmp_path: Path) -> None:
    """A target already matched by a path rule is not duplicated."""
    write(tmp_path / "deskops/operations.py", "# operations\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-operations.md",
        "deskops/operations.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # Should appear exactly once, from path_rule
    assert ids.count("source_file:deskops/operations.py") == 1
    node = next(n for n in nodes if n.id == "source_file:deskops/operations.py")
    assert node.provenance["source_kind"] == "path_rule"


def test_declared_target_leading_dotslash_is_stripped(tmp_path: Path) -> None:
    """A leading './' in target_identity is stripped."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-app.md",
        "./src/app.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    assert "source_file:src/app.py" in by_id


def test_declared_target_absolute_path_produces_no_node(tmp_path: Path) -> None:
    """An absolute path target produces no source_file node."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-absolute.md",
        "/etc/passwd",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert not any("passwd" in id_ for id_ in ids)


def test_declared_target_dotdot_path_produces_no_node(tmp_path: Path) -> None:
    """A path with '..' segments produces no source_file node."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-escape.md",
        "../outside/file.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert not any("outside" in id_ for id_ in ids)


def test_declared_target_kind_id_produces_no_node(tmp_path: Path) -> None:
    """A kind:id target produces no source_file node (handled by extract_edges)."""
    write(tmp_path / "src/app.py", "# app\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-kindid.md",
        "source_file:src/app.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    # No source_file node should be created from a kind:id target
    assert "source_file:source_file:src/app.py" not in ids


def test_declared_target_nonexistent_produces_no_node(tmp_path: Path) -> None:
    """A nonexistent target produces no source_file node."""
    write_materialization(
        tmp_path / "desk/materializations/materialization-missing.md",
        "src/missing.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:src/missing.py" not in ids


def test_declared_target_excluded_tmp_produces_no_node(tmp_path: Path) -> None:
    """A target under .tmp/ produces no source_file node."""
    write(tmp_path / ".tmp/scratch.py", "# scratch\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-tmp.md",
        ".tmp/scratch.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:.tmp/scratch.py" not in ids


def test_declared_target_excluded_tools_produces_no_node(tmp_path: Path) -> None:
    """A target under tools/ produces no source_file node."""
    write(tmp_path / "tools/helper.py", "# helper\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-tools.md",
        "tools/helper.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    ids = [node.id for node in nodes]

    assert "source_file:tools/helper.py" not in ids


def test_declared_target_dotslash_github_workflow_yields_correct_node(tmp_path: Path) -> None:
    """'./.github/workflows/pulse.yml' yields node 'source_file:.github/workflows/pulse.yml'.

    Regression test: lstrip("./") was incorrectly stripping every leading '.' and '/',
    so './.github' became 'github'. This verifies removeprefix("./") is used.
    """
    write(tmp_path / ".github/workflows/pulse.yml", "name: Pulse\n")
    write_materialization(
        tmp_path / "desk/materializations/materialization-dotslash-github.md",
        "./.github/workflows/pulse.yml",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    # Must include the leading dot in .github
    assert "source_file:.github/workflows/pulse.yml" in by_id
    # And NOT strip the dot incorrectly
    assert "source_file:github/workflows/pulse.yml" not in by_id

    node = by_id["source_file:.github/workflows/pulse.yml"]
    assert node.identity == ".github/workflows/pulse.yml"
    assert node.path == ".github/workflows/pulse.yml"
    assert node.provenance["path"] == ".github/workflows/pulse.yml"


def test_declared_target_symlink_yields_link_path_not_resolved_target(tmp_path: Path) -> None:
    """A symlink inside root declared as target yields a node for the link path.

    Regression test: the node path was computed from the symlink-resolved path,
    so 'link.py' pointing to 'real.py' would create a node for 'real.py' instead
    of 'link.py'. This verifies the declared normalized path is used.
    """
    # Create the real file
    write(tmp_path / "src/real.py", "# real implementation\n")
    # Create a symlink pointing to it
    link_path = tmp_path / "src/link.py"
    link_path.symlink_to(tmp_path / "src/real.py")

    # Declare the symlink as the materialization target
    write_materialization(
        tmp_path / "desk/materializations/materialization-link.md",
        "src/link.py",
    )

    nodes = extract_source_file_nodes(tmp_path)
    by_id = {node.id: node for node in nodes}

    # Must create a node for the declared link path
    assert "source_file:src/link.py" in by_id
    node = by_id["source_file:src/link.py"]
    assert node.identity == "src/link.py"
    assert node.path == "src/link.py"
    assert node.provenance["path"] == "src/link.py"
    assert node.provenance["source_kind"] == "declared_materialization_target"
