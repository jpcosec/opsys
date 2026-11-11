"""Reproducción (coord2, 2026-11-11): deskops edit task <id> implementation_path, dos veces, sobre una
tarea recién creada; se cuenta el placeholder '_Outline the expected implementation route…_'."""
from pathlib import Path

from deskops.cli.main import main
from deskops.operations import DeskopsOperations

PLACEHOLDER = "_Outline the expected implementation route or affected surface._"


def test_edit_task_does_not_pile_up_the_placeholder(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": "Placeholder probe", "why": "w", "goal": "g", "scope": "s",
         "implementation_path": "primer texto", "done_when": "d", "validation": ["v"], "task_type": "task.code"}
    ).task_id
    path = root / "desk" / "tasks" / f"{task_id}.md"
    counts = [path.read_text(encoding="utf-8").count(PLACEHOLDER)]
    for value in ("segundo texto", "tercer texto"):
        assert main(["edit", "task", task_id, "implementation_path", value, "--root", str(root)]) == 0
        counts.append(path.read_text(encoding="utf-8").count(PLACEHOLDER))
    capsys.readouterr()
    section = path.read_text(encoding="utf-8").split("## Implementation Path", 1)[1].split("\n## ", 1)[0]
    print("COUNTS", counts, "\nSECTION", repr(section))
    assert counts == [counts[0]] * 3, counts
    assert "tercer texto" in section and "segundo texto" not in section


def test_extract_then_edit_round_trip(lifecycle_desk: Path, capsys) -> None:
    from sldb.runtime.validation import extract_model_data
    from deskops.models import TaskCodeDoc

    root = lifecycle_desk
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": "Placeholder probe two", "why": "w", "goal": "g", "scope": "s",
         "implementation_path": "uno\n\ndos", "done_when": "d", "validation": ["v"], "task_type": "task.code"}
    ).task_id
    path = root / "desk" / "tasks" / f"{task_id}.md"
    counts, values = [path.read_text(encoding="utf-8").count(PLACEHOLDER)], []
    for _ in range(2):
        value = extract_model_data(TaskCodeDoc, path.read_text(encoding="utf-8"))["implementation_path"]
        values.append(value)
        assert main(["edit", "task", task_id, "implementation_path", value + "\n\nmás", "--root", str(root)]) == 0
        counts.append(path.read_text(encoding="utf-8").count(PLACEHOLDER))
    capsys.readouterr()
    print("COUNTS2", counts, "\nVALUES", [repr(v) for v in values])
    assert counts == [counts[0]] * 3, counts


def test_edit_with_the_raw_section_text_piles_up(lifecycle_desk: Path, capsys) -> None:
    root = lifecycle_desk
    task_id = DeskopsOperations(root).create_task_bundle(
        {"title": "Placeholder probe three", "why": "w", "goal": "g", "scope": "s",
         "implementation_path": "base", "done_when": "d", "validation": ["v"], "task_type": "task.code"}
    ).task_id
    path = root / "desk" / "tasks" / f"{task_id}.md"
    counts = [path.read_text(encoding="utf-8").count(PLACEHOLDER)]
    for extra in ("b9", "b10"):
        raw = path.read_text(encoding="utf-8").split("## Implementation Path", 1)[1].split("\n## ", 1)[0].strip()
        assert main(["edit", "task", task_id, "implementation_path", raw + "\n\n" + extra, "--root", str(root)]) == 0
        counts.append(path.read_text(encoding="utf-8").count(PLACEHOLDER))
    capsys.readouterr()
    print("COUNTS3", counts)
    assert counts == [counts[0]] * 3, counts
