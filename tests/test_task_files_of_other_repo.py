"""``deskops add task`` and ``deskops doctor`` point at task.external when a task's files are another repo's.

Two repositories registered with ``deskops repo register`` in tmp_path (never the real ecosystem
registry): the desk (governance) and the repository its code would live in (infra). Only the
``files`` of a task count; the warning never blocks and never changes the exit code.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from deskops.cli.main import main
from deskops.foreign_files import task_warning

from test_doctor_alerts import _doctor, _store_check_says
from test_doctor_unmodeled_surfaces import _init_repo, _prepare_current_modeled_surfaces, _write

OTHER = "infra"


@pytest.fixture
def eco(tmp_path: Path, capsys) -> dict[str, Path]:
    desk, other = tmp_path / "governance", tmp_path / "infra"
    _init_repo(desk, capsys)
    other.mkdir()
    config = desk / "desk" / "config.json"
    config.write_text(json.dumps({**json.loads(config.read_text()), "project_identity": "governance"}) + "\n")
    store = str(desk / ".sldb")
    assert main(["repo", "register", OTHER, "--path", str(other), "--id", OTHER, "--store", store]) == 0
    assert main(["repo", "register", "governance", "--path", str(desk), "--id", "governance", "--store", store]) == 0
    capsys.readouterr()
    return {"desk": desk, "other": other}


def _add(desk: Path, capsys, task_id: str, files: list[str], task_type: str = "task.code") -> str:
    payload = desk / f"{task_id}.json"
    payload.write_text(
        json.dumps({"id": task_id, "title": task_id, "goal": "g", "scope": "s", "validation": "pytest",
                    "task_type": task_type, "files": files}),
        encoding="utf-8",
    )
    assert main(["add", "task", "--root", str(desk), str(payload.read_text())]) == 0
    return capsys.readouterr().out


def _warns(out: str, task_id: str) -> bool:
    return task_warning(task_id, OTHER) in out


def test_the_warning_has_the_agreed_text() -> None:
    assert task_warning("task-x", "infra") == (
        "Files of task-x belong to repository infra; "
        "if the work lives there consider task_type task.external or a mirror task in its desk."
    )


def test_a_qualified_file_warns(eco, capsys) -> None:
    out = _add(eco["desk"], capsys, "task-q", [f"{OTHER}:src/app.py"])
    assert "Created task bundle task-q" in out and "Files of task-q belong to repository infra; " in out


def test_an_absolute_file_under_the_other_root_warns(eco, capsys) -> None:
    out = _add(eco["desk"], capsys, "task-a", [str(eco["other"] / "src" / "app.py")])
    assert _warns(out, "task-a")


def test_a_parent_relative_file_under_the_other_root_warns(eco, capsys) -> None:
    out = _add(eco["desk"], capsys, "task-p", ["../infra/src/app.py"])
    assert _warns(out, "task-p")


def test_local_files_do_not_warn(eco, capsys) -> None:
    desk = eco["desk"]
    files = ["src/app.py", "governance:src/own.py", str(desk / "src" / "abs.py"), "../elsewhere/x.py", "unknown:x.py"]
    out = _add(desk, capsys, "task-l", files)
    assert "Created task bundle task-l" in out and "belong to repository" not in out


def test_task_external_does_not_warn(eco, capsys) -> None:
    out = _add(eco["desk"], capsys, "task-e", [f"{OTHER}:src/app.py"], task_type="task.external")
    assert "Created task bundle task-e" in out and "belong to repository" not in out


def test_the_doctor_alerts_for_an_open_task_without_changing_its_exit_code(eco, monkeypatch, capsys) -> None:
    desk = eco["desk"]
    docs = [{"path": p, "note": "ok"} for p in _prepare_current_modeled_surfaces(desk)]
    _store_check_says(monkeypatch, docs)
    code_before, out_before = _doctor(desk, capsys)
    _add(desk, capsys, "task-code", [f"{OTHER}:src/app.py"])
    _add(desk, capsys, "task-ext", [f"{OTHER}:src/app.py"], task_type="task.external")
    _add(desk, capsys, "task-own", ["src/app.py"])
    code, out = _doctor(desk, capsys)
    assert code == code_before == 0, out
    assert "belong to repository" not in out_before
    assert f"- {task_warning('task-code', OTHER)}" in out
    assert "task-ext belong" not in out and "task-own belong" not in out
