"""`deskops graph missing`: a declared target that is an existing file of the repo is not missing
even when the project graph makes no node for it (revisable decision until CC33c)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from deskops.graph import checks
from deskops.graph.checks import declared_target_is_a_file
from deskops.graph.checks import find_missing_graph_references


def _missing(target_id: str) -> SimpleNamespace:
    return SimpleNamespace(
        source_id="task:task-x",
        target_id=target_id,
        provenance_path="desk/tasks/task-x.md",
        provenance_locator="line:1:source-file-reference",
        extractor="test",
        reason="declared target was not found among extracted graph nodes",
        record=None,
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    (tmp_path / "desk" / "drawer" / "plans" / "p").mkdir(parents=True)
    (tmp_path / "desk" / "drawer" / "plans" / "p" / "dag.yaml").write_text("nodes: []\n", encoding="utf-8")
    (tmp_path / "tests" / "fixtures").mkdir(parents=True)
    (tmp_path / "tests" / "fixtures" / "hashes.json").write_text("{}\n", encoding="utf-8")
    (tmp_path.parent / "outside.yaml").write_text("x: 1\n", encoding="utf-8")
    return tmp_path


def test_an_existing_file_the_graph_has_no_node_for_is_not_missing(repo: Path, monkeypatch) -> None:
    targets = ["desk/drawer/plans/p/dag.yaml", "test_file:tests/fixtures/hashes.json"]
    monkeypatch.setattr(checks, "extract_declared_edges", lambda root: SimpleNamespace(missing_targets=[_missing(t) for t in targets]))
    assert find_missing_graph_references(repo) == []


def test_a_target_that_does_not_exist_is_still_missing(repo: Path, monkeypatch) -> None:
    targets = ["source_file:deskops/graph/extract_sources.py", "desk/drawer/plans/p/gone.yaml"]
    monkeypatch.setattr(checks, "extract_declared_edges", lambda root: SimpleNamespace(missing_targets=[_missing(t) for t in targets]))
    found = find_missing_graph_references(repo)
    assert [f.target_id for f in found] == sorted(targets)
    assert {f.kind for f in found} == {"missing_declared_target"}


@pytest.mark.parametrize("target_id", ["../outside.yaml", "spec:../outside.yaml", "/etc/hostname", "atom:atom-x", "desk/drawer/plans/p"])
def test_atoms_paths_leaving_the_root_and_directories_are_not_taken_as_existing_files(repo: Path, target_id: str) -> None:
    assert not declared_target_is_a_file(repo, target_id)
