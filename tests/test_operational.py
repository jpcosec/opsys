from __future__ import annotations

import json
from pathlib import Path

import pytest

from deskops.models.task import TaskDoc
from deskops.operations import DeskopsOperations
from tests.test_lifecycle_end_to_end import _cli, _make_repo


def test_create_artifact_rolls_back_file_when_tracking_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)

    def fail_tracking(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("tracking failed")

    monkeypatch.setattr(operations, "_track_created_artifact", fail_tracking)

    with pytest.raises(RuntimeError, match="tracking failed"):
        operations.create_artifact(
            "artifact.atom",
            {
                "title": "Rollback atom",
                "five_wh_one_plus": "what",
                "answer": "Created files must disappear if tracking fails.",
            },
        )

    assert not list((tmp_path / "desk" / "atoms").glob("atom-rollback-atom.md"))


def test_create_task_bundle_rolls_back_the_task_when_tracking_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)

    def fail_tracking(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("tracking failed")

    monkeypatch.setattr(operations, "_track_created_document", fail_tracking)

    with pytest.raises(RuntimeError, match="tracking failed"):
        operations.create_task_bundle(
            {
                "title": "Rollback bundle",
                "goal": "Prove rollback.",
                "scope": "Task creation.",
                "implementation_path": "deskops/operations.py",
                "done_when": "No orphan files remain.",
            }
        )

    assert not (tmp_path / "desk" / "tasks" / "task-rollback-bundle.md").exists()
    board_text = (tmp_path / "desk" / "tasks" / "Board.md").read_text(encoding="utf-8")
    assert "desk/tasks/task-rollback-bundle.md" not in board_text


def test_create_task_bundle_writes_only_the_task(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    bundle = operations.create_task_bundle(
        {
            "title": "Only the task",
            "goal": "One document per task.",
            "scope": "Task creation.",
            "implementation_path": "deskops/operations.py",
            "done_when": "Nothing but the task and its Board line is written.",
        }
    )

    assert bundle.task_path == tmp_path / "desk" / "tasks" / "task-only-the-task.md"
    payload = operations._read_doc(bundle.task_path, TaskDoc)
    assert payload["current_node"] == "ritual-execution"
    assert "routine" not in payload and "checklists" not in payload
    assert not (tmp_path / "desk" / "routines").exists()
    assert not (tmp_path / "desk" / "primitives").exists()


def test_create_task_bundle_restores_board_when_append_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.ensure_workspace()
    board_path = tmp_path / "desk" / "tasks" / "Board.md"
    original_board_text = board_path.read_text(encoding="utf-8")
    original_append = operations._append_task_to_board

    def fail_after_append(task_id: str) -> None:
        original_append(task_id)
        raise RuntimeError("board append failed")

    monkeypatch.setattr(operations, "_append_task_to_board", fail_after_append)

    with pytest.raises(RuntimeError, match="board append failed"):
        operations.create_task_bundle(
            {
                "title": "Rollback board",
                "goal": "Prove board rollback.",
                "scope": "Board mutation.",
                "implementation_path": "deskops/operations.py",
                "done_when": "Board is restored.",
            }
        )

    assert board_path.read_text(encoding="utf-8") == original_board_text
    assert not list((tmp_path / "desk" / "tasks").glob("task-rollback-board.md"))
    assert not list((tmp_path / "desk").rglob("*task-rollback-board*.md"))


def test_pill_graduation_is_verified_when_bound_pills_have_an_atom_reference(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)
    operations.create_artifact(
        "artifact.atom",
        {
            "title": "Graduated knowledge",
            "five_wh_one_plus": "what",
            "answer": "Atom references satisfy pill knowledge graduation.",
        },
    )

    assert operations._has_verified_task_pill_graduation(
        {"pills": ["desk/contexts/pill-example.md"], "references": ["desk/atoms/atom-graduated-knowledge.md"]}
    )


def test_pill_graduation_is_not_verified_when_bound_pills_lack_an_atom_reference(tmp_path: Path) -> None:
    operations = DeskopsOperations(tmp_path)

    assert not operations._has_verified_task_pill_graduation(
        {"pills": ["desk/contexts/pill-example.md"], "references": ["tests/test_runtime.py::test_runtime"]}
    )


def test_pill_graduation_is_trivially_verified_without_bound_pills(tmp_path: Path) -> None:
    assert DeskopsOperations(tmp_path)._has_verified_task_pill_graduation({"pills": [], "references": []})


def test_advance_task_does_not_persist_computed_gate_facts(lifecycle_desk: Path) -> None:
    """Older versions wrote closeout_evidence_verified / pill_graduation_verified into the task."""
    operations = DeskopsOperations(lifecycle_desk)
    operations.create_task_bundle(
        {
            "title": "No leaked facts",
            "goal": "Keep the task frontmatter clean.",
            "scope": "advance only.",
            "implementation_path": "deskops/operations.py",
            "validation": ["pytest"],
            "done_when": "The task file holds only its own fields.",
        }
    )

    task, result = operations.advance_task("task-no-leaked-facts")

    assert result is not None and result.progressed
    text = (lifecycle_desk / "desk" / "tasks" / "task-no-leaked-facts.md").read_text(encoding="utf-8")
    assert "closeout_evidence_verified" not in text
    assert "pill_graduation_verified" not in text


def _seed_task(root: Path, task_id: str, title: str) -> None:
    payload = {
        "id": task_id,
        "title": title,
        "goal": "g",
        "scope": "s",
        "implementation_path": "i",
        "done_when": "d",
        "validation": ["pytest"],
    }
    _cli(root, "add", "task", "--root", str(root), json.dumps(payload))


def test_advance_task_prefix_selector_rejects_ambiguity(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _cli(root, "init", str(root))
    _seed_task(root, "task-foo-bar", "Foo Bar")
    _seed_task(root, "task-foo-baz", "Foo Baz")
    bar = root / "desk" / "tasks" / "task-foo-bar.md"
    baz = root / "desk" / "tasks" / "task-foo-baz.md"
    before = (bar.read_text(encoding="utf-8"), baz.read_text(encoding="utf-8"))

    result = _cli(root, "advance", "task", "task-foo", check=False)

    assert result.returncode == 1
    assert "task-foo-bar" in result.stderr
    assert "task-foo-baz" in result.stderr
    assert (bar.read_text(encoding="utf-8"), baz.read_text(encoding="utf-8")) == before


def test_advance_task_exact_selector_wins_over_prefix(tmp_path: Path) -> None:
    root = _make_repo(tmp_path)
    _cli(root, "init", str(root))
    _seed_task(root, "task-foo", "Foo")
    _seed_task(root, "task-foo-bar", "Foo Bar")
    bar = root / "desk" / "tasks" / "task-foo-bar.md"
    before = bar.read_text(encoding="utf-8")

    result = _cli(root, "advance", "task", "task-foo")

    assert "Task: task-foo" in result.stdout
    assert bar.read_text(encoding="utf-8") == before
