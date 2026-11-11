"""Reproducción (coord2, 2026-11-11): closeout resolved-by de una tarea que el modelo rechaza
(draft con history [task_activates, task_hands_to_closeout]), el mismo armado que el test de supersede."""
from pathlib import Path
import pytest
from deskops.cli.main import main
from tests.test_closeout import _make_repo, _write_lifecycle_task, _write_board, _git


def test_resolved_by_of_a_task_the_model_rejects(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _make_repo(tmp_path)
    _write_lifecycle_task(root)
    path = root / "desk" / "tasks" / "task-x.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("status: active\n", "status: draft\n").replace("current_node: ritual-testing\n", "current_node: ritual-closeout\n")
    text = text.replace("history:\n- task_activates\n", "history:\n- task_activates\n- task_hands_to_closeout\n")
    path.write_text(text, encoding="utf-8")
    (root / "tests").mkdir()
    (root / "tests" / "test_x.py").write_text("def test_x():\n    pass\n", encoding="utf-8")
    _write_board(root, "task-x")
    _git(root, "add", "desk/tasks", "tests")
    _git(root, "commit", "-q", "-m", "add incoherent task, board and test")
    ref = _git(root, "rev-parse", "HEAD")
    rc = main(["closeout", "resolved-by", "--root", str(root), "--task", "task-x", "--reason", "work entered", "--ref", ref, "--test", "tests/test_x.py"])
    out = capsys.readouterr()
    print("RC", rc, "\nOUT", out.out, "\nERR", out.err)
    assert rc == 0, out.out + out.err
