"""Declared model metadata is a graph input.

TaskDoc declares its routine, checklists, pills and atoms as containment and
its references, depends_on, inherits_from and from_drawer as references.
BoardDoc declares tasks, pills and rituals. Those declarations only reach the
snapshot as prose unless the declared fields are read from the model, which is
what these tests pin down.
"""

from __future__ import annotations

from pathlib import Path

from deskops.graph.extract_edges import extract_declared_edges


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


TASK = """---
id: task-do-the-thing
status: active
routine: routine-task-do-the-thing
checklists:
- checklist-task-do-the-thing-execution-ready
pills:
- desk/contexts/pill-guardrail.md
atoms:
- atom-do-the-thing
references:
- task-something-else
depends_on: []
inherits_from: []
from_drawer: desk/drawer/tasks/task-do-the-thing.md
---

# Do the thing
"""


def _build_desk(root: Path) -> None:
    write(root / "desk/tasks/task-do-the-thing.md", TASK)
    write(
        root / "desk/routines/routine-task-do-the-thing.md",
        "---\nid: routine-task-do-the-thing\n---\n\n# Routine\n",
    )
    write(
        root / "desk/primitives/checklists/checklist-task-do-the-thing-execution-ready.md",
        "---\nid: checklist-task-do-the-thing-execution-ready\n---\n\n# Checklist\n",
    )
    write(
        root / "desk/contexts/pill-guardrail.md",
        "---\nid: pill-guardrail\n---\n\n# Pill\n",
    )
    write(
        root / "desk/atoms/atom-do-the-thing.md",
        "---\nid: atom-do-the-thing\nfive_wh_one_plus: what\n---\n\n# Atom\n",
    )
    write(
        root / "desk/tasks/task-something-else.md",
        "---\nid: task-something-else\n---\n\n# Other\n",
    )
    write(
        root / "desk/tasks/Board.md",
        "---\nid: board-001\ntasks:\n- desk/tasks/task-do-the-thing.md\n---\n\n# Board\n",
    )


def test_declared_containment_becomes_edges_with_the_field_as_role(tmp_path: Path) -> None:
    _build_desk(tmp_path)

    extraction = extract_declared_edges(tmp_path)
    task_edges = {
        (edge.role, edge.target_id)
        for edge in extraction.edges
        if edge.source_id == "task:task-do-the-thing"
    }

    assert ("routine", "routine:routine-task-do-the-thing") in task_edges
    assert (
        "checklists",
        "checklist:checklist-task-do-the-thing-execution-ready",
    ) in task_edges
    assert ("pills", "pill:pill-guardrail") in task_edges
    assert ("atoms", "atom:atom-do-the-thing") in task_edges
    assert ("references", "task:task-something-else") in task_edges


def test_board_task_reference_resolves_to_the_task_node(tmp_path: Path) -> None:
    _build_desk(tmp_path)

    extraction = extract_declared_edges(tmp_path)

    assert any(
        edge.source_id == "board:board-001"
        and edge.role == "tasks"
        and edge.target_id == "task:task-do-the-thing"
        for edge in extraction.edges
    )


def test_a_declared_field_holding_prose_is_not_an_unresolved_reference(tmp_path: Path) -> None:
    """Ritual steps are instruction text; edge targets are workflow node names."""
    write(
        tmp_path / "desk/rituals/ritual-phase.md",
        "---\n"
        "id: ritual-phase\n"
        "steps:\n"
        "- Identify the ready dependency layer of tasks whose prerequisites are satisfied.\n"
        "---\n\n# Phase\n",
    )
    write(
        tmp_path / "desk/primitives/edges/edge-task-x-close-to-complete.md",
        "---\n"
        "id: edge-task-x-close-to-complete\n"
        "source: task-x\n"
        "target: complete\n"
        "---\n\n# Edge\n",
    )

    extraction = extract_declared_edges(tmp_path)

    assert extraction.missing_targets == []
    assert all(
        "prerequisites" not in edge.target_id for edge in extraction.edges
    )
