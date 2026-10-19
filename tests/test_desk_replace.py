from __future__ import annotations

import subprocess
from pathlib import Path

from deskops import doc_io
from deskops.cli.main import main
from deskops.models import RoleDoc
from sldb.runtime.validation import render_model_markdown


def _git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=True).stdout.strip()


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "T")
    _git(root, "add", "-A")
    _git(root, "commit", "-q", "-m", "seed")
    return root


def _replace(root: Path, path: str, old: str, new: str, *extra: str) -> int:
    return main(["desk", "replace", path, "--root", str(root), "--old", old, "--new", new, *extra])


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_replace_edits_an_unmodeled_drawer_file(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    note = _write(root, "desk/drawer/features/note.md", "# Feature\n\nOld wording.\n")
    capsys.readouterr()

    assert _replace(root, "desk/drawer/features/note.md", "Old wording.", "New wording.") == 0
    out = capsys.readouterr().out

    assert "Replaced 1 occurrence(s) in desk/drawer/features/note.md" in out
    assert note.read_text(encoding="utf-8") == "# Feature\n\nNew wording.\n"


def test_replace_refuses_when_the_old_text_is_missing(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    _write(root, "desk/drawer/features/note.md", "# Feature\n")
    capsys.readouterr()

    assert _replace(root, "desk/drawer/features/note.md", "absent", "new") == 1
    captured = capsys.readouterr()
    assert "found 0 occurrence(s)" in captured.out + captured.err
    assert (root / "desk/drawer/features/note.md").read_text(encoding="utf-8") == "# Feature\n"


def test_replace_requires_an_exact_count(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    note = _write(root, "desk/drawer/features/note.md", "same same\n")
    capsys.readouterr()

    assert _replace(root, "desk/drawer/features/note.md", "same", "other") == 1
    captured = capsys.readouterr()
    assert "found 2 occurrence(s)" in captured.out + captured.err
    assert note.read_text(encoding="utf-8") == "same same\n"

    assert _replace(root, "desk/drawer/features/note.md", "same", "other", "--count", "2") == 0
    assert note.read_text(encoding="utf-8") == "other other\n"


def test_replace_retracks_a_role_doc_and_keeps_the_store_pass(tmp_path: Path, capsys) -> None:
    from sldb.api import check_store, doc_status

    root = _repo(tmp_path)
    role_path = _write(
        root,
        "desk/roles/deskops-supervisor.md",
        render_model_markdown(
            RoleDoc,
            {
                "id": "role-deskops-supervisor",
                "name": "deskops-supervisor",
                "description": "Use when acting as the desk workflow supervisor.",
                "kind": "pi",
                "model": "anthropic/claude-opus-4-8",
                "fallback_models": [],
                "tools": ["read", "bash"],
                "system_prompt_mode": "replace",
                "inherit_project_context": True,
                "inherit_skills": True,
                "default_context": "fresh",
                "body": "# Workflow Supervisor\n\nOld body.",
            },
        )
        + "\n",
    )
    doc_io.track(root, role_path, "RoleDoc")
    capsys.readouterr()

    assert _replace(root, "desk/roles/deskops-supervisor.md", "# Workflow Supervisor", "# Workflow Lead") == 0

    assert "New body" not in role_path.read_text(encoding="utf-8")
    assert "# Workflow Lead" in role_path.read_text(encoding="utf-8")
    assert doc_status(root / ".sldb", "desk/roles/deskops-supervisor.md").exists
    check = check_store(root / ".sldb", root, pythonpath=str(Path(__file__).resolve().parents[1]))
    assert check["ok"] is True


def test_replace_refuses_a_modeled_pill(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    pill = _write(root, "desk/contexts/pill-old.md", "# Old pill\n\nOld wording.\n")
    capsys.readouterr()

    assert _replace(root, "desk/contexts/pill-old.md", "Old wording.", "New wording.") == 1
    captured = capsys.readouterr()
    assert "deskops edit pill" in captured.out + captured.err
    assert pill.read_text(encoding="utf-8") == "# Old pill\n\nOld wording.\n"


def test_replace_edits_an_issue_body(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    issue = _write(root, "desk/issues/issue-old.md", "ID: issue-old\nStatus: open\n\nOld wording.\n")
    capsys.readouterr()

    assert _replace(root, "desk/issues/issue-old.md", "Old wording.", "New wording.") == 0

    assert issue.read_text(encoding="utf-8") == "ID: issue-old\nStatus: open\n\nNew wording.\n"


def test_replace_edits_legacy_drawer_tasks_but_refuses_a_valid_task_doc(tmp_path: Path, capsys) -> None:
    root = _repo(tmp_path)
    legacy = _write(
        root,
        "desk/drawer/tasks/task-legacy.md",
        "# Legacy drawer task\n\nStatus: draft\n\nOld wording.\n",
    )
    capsys.readouterr()

    assert _replace(root, "desk/drawer/tasks/task-legacy.md", "Old wording.", "New wording.") == 0
    assert "New wording." in legacy.read_text(encoding="utf-8")

    assert main(
        [
            "add",
            "task",
            "--root",
            str(root),
            "--title",
            "Modeled task",
            "--goal",
            "g",
            "--scope",
            "s",
            "--validation",
            "pytest",
        ]
    ) == 0
    task = next((root / "desk" / "tasks").glob("task-modeled-task*.md"))
    drawer_task = root / "desk" / "drawer" / "tasks" / task.name
    drawer_task.parent.mkdir(parents=True, exist_ok=True)
    drawer_task.write_bytes(task.read_bytes())
    capsys.readouterr()

    assert _replace(root, drawer_task.relative_to(root).as_posix(), "# Modeled task", "# Renamed") == 1
    captured = capsys.readouterr()
    assert "deskops edit task" in captured.out + captured.err
    assert "# Modeled task" in drawer_task.read_text(encoding="utf-8")
