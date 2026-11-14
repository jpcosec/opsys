"""The closeout graph skips the `runs/` walk unless a materialization declares a target there.

`runs/` is evidence, not a graph surface: no document surface or file rule reads it. A
materialization can still declare a file there, and then the full graph (the fallback) keeps
the node, so the optimization changes no answer of the graph.
"""

from __future__ import annotations

from pathlib import Path

from deskops.graph.desk_graph import desk_graph


def _materialization(root: Path, target: str) -> None:
    path = root / "desk" / "materializations" / "materialization-run-output.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        "id: materialization-run-output\n"
        "title: run output\n"
        f"target_identity: {target}\n"
        "---\n\n"
        "# run output\n",
        encoding="utf-8",
    )


def test_a_materialization_target_under_runs_is_still_a_graph_node(tmp_path: Path) -> None:
    run_file = tmp_path / "runs" / "subagents" / "r" / "out.py"
    run_file.parent.mkdir(parents=True)
    run_file.write_text("x = 1\n", encoding="utf-8")
    _materialization(tmp_path, "runs/subagents/r/out.py")

    graph = desk_graph(tmp_path)

    assert graph.nodes.lookup.by_path["runs/subagents/r/out.py"].id == "source_file:runs/subagents/r/out.py"


def test_runs_without_a_declared_target_adds_no_node(tmp_path: Path) -> None:
    run_file = tmp_path / "runs" / "subagents" / "r" / "out.py"
    run_file.parent.mkdir(parents=True)
    run_file.write_text("x = 1\n", encoding="utf-8")
    _materialization(tmp_path, "deskops/out.py")
    (tmp_path / "deskops").mkdir()
    (tmp_path / "deskops" / "out.py").write_text("x = 1\n", encoding="utf-8")

    graph = desk_graph(tmp_path)

    assert not [path for path in graph.nodes.lookup.by_path if path.startswith("runs/")]
    assert graph.nodes.lookup.by_path["deskops/out.py"].id == "source_file:deskops/out.py"
