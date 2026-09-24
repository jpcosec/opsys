"""Regression tests for the CLI gaps reported in desk/inbox/.

Covers the two inbox notes:
  - 20260827-160657 "CLI gaps: inbox --root, promote deja notas tracked
    huerfanas, sin listado de drawer"
  - 20260827-164846 "edit/extractor corre secciones vacias y advance --to no
    toca status" (the advance half; the extractor half is a sldb-level fix
    covered by sldb's tests/test_section_body_extraction.py)

Drawer -> active task promotion was removed rather than repaired: the drawer
is loose by design and an active task is a compiled, fully authored bundle,
so a drawer item becomes a task only through `deskops add task`.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.main import main
from deskops.operations import DeskopsOperations


def _install_desk(tmp_path: Path) -> None:
    assert main(["desk", "install", str(tmp_path)]) == 0


def _write_note(tmp_path: Path, stem: str, body: str) -> Path:
    note = tmp_path / "desk" / "inbox" / f"{stem}.md"
    note.parent.mkdir(parents=True, exist_ok=True)
    note.write_text(
        "---\nkind: suggestion\nstatus: open\n---\n\n" + body,
        encoding="utf-8",
    )
    return note


# ── inbox --root ──────────────────────────────────────────────────────────────


def test_inbox_accepts_root_like_every_other_subcommand(tmp_path: Path, capsys) -> None:
    """The epilog documented `deskops inbox --list --root .` while the parser
    only accepted --desk-root, so the documented invocation failed outright."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-hello", "# Hello\n\nBody.\n")
    capsys.readouterr()

    assert main(["inbox", "--list", "--root", str(tmp_path)]) == 0

    assert "Hello" in capsys.readouterr().out


def test_inbox_desk_root_wins_over_root(tmp_path: Path, capsys) -> None:
    """--desk-root is the more specific flag and must keep precedence."""
    _install_desk(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    _install_desk(other)
    _write_note(tmp_path, "20260101-000000-suggestion-in-root", "# InRoot\n\nBody.\n")
    _write_note(other, "20260101-000001-suggestion-in-desk-root", "# InDeskRoot\n\nBody.\n")
    capsys.readouterr()

    assert main(["inbox", "--list", "--root", str(tmp_path), "--desk-root", str(other / "desk")]) == 0

    out = capsys.readouterr().out
    assert "InDeskRoot" in out
    assert "InRoot" not in out


# ── inbox -> drawer stays loose ──────────────────────────────────────────────


def test_inbox_to_drawer_keeps_the_note_body_loose(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-plain", "# Plain\n\nRaw dump of context.\n")

    assert main(["promote", "inbox-to-drawer-task", "plain", "--root", str(tmp_path)]) == 0

    text = (tmp_path / "desk" / "drawer" / "tasks" / "task-plain.md").read_text(encoding="utf-8")
    assert "Raw dump of context." in text
    assert not (tmp_path / "desk" / "tasks" / "task-plain.md").exists()


def test_inbox_to_drawer_rejects_task_structure_flags(tmp_path: Path) -> None:
    """Goal/scope/validation are authored when a task is created, not injected
    while a note is still a loose drawer candidate."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-shaped", "# Shaped\n\nBody.\n")

    assert main(["promote", "inbox-to-drawer-task", "shaped", "--root", str(tmp_path), "--goal", "X"]) != 0


def test_drawer_to_active_task_promotion_no_longer_exists(tmp_path: Path) -> None:
    """Drawer content is loose; a task is a compiled bundle. The old direct
    promotion filled every required field with generic placeholders, so it was
    removed: a drawer item becomes a task only via `deskops add task`."""
    _install_desk(tmp_path)
    drawer = tmp_path / "desk" / "drawer" / "tasks"
    drawer.mkdir(parents=True, exist_ok=True)
    (drawer / "task-loose.md").write_text("# Loose\n\nID: task-loose\nStatus: deferred\n", encoding="utf-8")

    assert main(["promote", "drawer-task-to-active-task", "loose", "--root", str(tmp_path)]) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-loose.md").exists()


def test_list_tasks_does_not_surface_drawer_items(tmp_path: Path, capsys) -> None:
    """An available task is board-routed work, not a drawer item."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-candidate", "# Candidate\n\nBody.\n")
    assert main(["promote", "inbox-to-drawer-task", "candidate", "--root", str(tmp_path)]) == 0
    capsys.readouterr()

    assert main(["list", "tasks", "--root", str(tmp_path)]) == 0

    assert "task-candidate" not in capsys.readouterr().out


# ── promote untracks the note ────────────────────────────────────────────────


def test_promote_untracks_the_note_from_the_store(tmp_path: Path) -> None:
    """Regression: promote unlinked the inbox file but left the tracked
    InboxNoteDoc entry behind, so `deskops status` reported it as an invalid
    missing document forever after."""
    from sldb.cli import main as sldb_main

    _install_desk(tmp_path)
    note = _write_note(tmp_path, "20260101-000000-suggestion-tracked", "# Tracked\n\nBody.\n")

    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(["models", "add", "deskops.models:InboxNoteDoc", "--store", str(tmp_path / ".sldb")]) == 0
    assert sldb_main([
        "docs", "track", str(note), "--model", "InboxNoteDoc",
        "--name", note.stem, "--store", str(tmp_path / ".sldb"), "--force",
    ]) == 0
    assert _tracked_names(tmp_path) == [note.stem]

    assert main(["promote", "inbox-to-drawer-task", "tracked", "--root", str(tmp_path)]) == 0

    assert not note.exists()
    assert _tracked_names(tmp_path) == []


def _tracked_names(tmp_path: Path) -> list[str]:
    from sldb.store.io import load_documents_index, load_models_index, load_store_index

    names: list[str] = []
    for entry in load_store_index(tmp_path / ".sldb").models:
        models_idx = load_models_index(tmp_path / entry.models_index)
        names.extend(d.name for d in load_documents_index(tmp_path / models_idx.documents_index).documents)
    return sorted(names)


def test_promote_still_succeeds_without_a_store(tmp_path: Path) -> None:
    """A desk with no .sldb must still promote; untracking is best effort."""
    _install_desk(tmp_path)
    _write_note(tmp_path, "20260101-000000-suggestion-nostore", "# NoStore\n\nBody.\n")

    assert main(["promote", "inbox-to-drawer-task", "nostore", "--root", str(tmp_path)]) == 0

    assert (tmp_path / "desk" / "drawer" / "tasks" / "task-nostore.md").exists()


# ── advance --to complete closes the status ──────────────────────────────────


def _make_task(tmp_path: Path, task_id: str) -> DeskopsOperations:
    operations = DeskopsOperations(tmp_path)
    operations.create_task_bundle({
        "id": task_id,
        "title": "Forced Transition",
        "status": "active",
        "why": "Because.",
        "goal": "Reach the terminal node.",
        "scope": "Just this task.",
        "implementation_path": "None.",
        "validation": ["pytest"],
        "done_when": "It is complete.",
        "references": [],
        "tags": ["workspace:desk", "artifact:task"],
    })
    return operations


def test_forced_advance_to_complete_also_closes_status(tmp_path: Path) -> None:
    """Regression: `advance --to complete` moved current_node only, leaving
    status at 'active'. The gated path pairs current_node == 'complete' with
    status == 'closed', so the forced path left the two disagreeing and the
    task read as terminal but never as closed."""
    _install_desk(tmp_path)
    operations = _make_task(tmp_path, "task-forced-complete")

    task, result = operations.advance_task("task-forced-complete", target_node="complete")

    assert result is not None
    assert task.current_node == "complete"
    assert task.status == "closed"


def test_forced_advance_to_a_normal_node_leaves_status_alone(tmp_path: Path) -> None:
    """Only the terminal node closes the task; ordinary forced moves must not
    silently change status."""
    _install_desk(tmp_path)
    operations = _make_task(tmp_path, "task-forced-mid")

    task, _ = operations.advance_task("task-forced-mid", target_node="some-checklist-node")

    assert task.current_node == "some-checklist-node"
    assert task.status == "active"


def test_forced_advance_to_a_status_value_still_sets_status(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    operations = _make_task(tmp_path, "task-forced-blocked")

    task, _ = operations.advance_task("task-forced-blocked", target_node="blocked")

    assert task.status == "blocked"


# ── add task --from-drawer ───────────────────────────────────────────────────


def _drawer_file(tmp_path: Path, relative: str, body: str = "# Loose idea\n\nUnstructured notes.\n") -> Path:
    path = tmp_path / "desk" / "drawer" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def _authored_task_argv(tmp_path: Path, *extra: str) -> list[str]:
    # --validation takes nargs="+", so it has to stay last.
    return [
        "add", "task", "--root", str(tmp_path),
        "--title", "Authored From Drawer",
        "--goal", "G.", "--scope", "S.", "--implementation-path", "I.", "--done-when", "D.",
        *extra,
        "--validation", "pytest",
    ]


def _task_doc(tmp_path: Path, task_id: str) -> dict:
    from sldb.runtime.validation import extract_model_data

    from deskops.models import TaskDoc

    return extract_model_data(TaskDoc, (tmp_path / "desk" / "tasks" / f"{task_id}.md").read_text(encoding="utf-8"))


def test_add_task_from_drawer_records_source_and_keeps_the_file(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    source = _drawer_file(tmp_path, "tasks/task-loose-idea.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0

    doc = _task_doc(tmp_path, "task-authored-from-drawer")
    assert doc["from_drawer"] == "desk/drawer/tasks/task-loose-idea.md"
    assert source.exists(), "the drawer file is kept for manual cleanup"


def test_add_task_from_drawer_resolves_any_drawer_subfolder(tmp_path: Path) -> None:
    """The drawer holds features, issues and questions, not only tasks."""
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "features/feature-shiny.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "feature-shiny")) == 0

    assert _task_doc(tmp_path, "task-authored-from-drawer")["from_drawer"] == "desk/drawer/features/feature-shiny.md"


def test_add_task_from_drawer_rejects_an_unknown_selector(tmp_path: Path) -> None:
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "nothing-like-this")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_add_task_from_drawer_rejects_an_ambiguous_selector(tmp_path: Path) -> None:
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-idea-one.md")
    _drawer_file(tmp_path, "features/feature-idea-two.md")

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "idea")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_add_task_from_drawer_rejects_paths_outside_the_drawer(tmp_path: Path) -> None:
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path, "--from-drawer", "desk/tasks/Board.md")) != 0
    assert not (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").exists()


def test_from_drawer_survives_replacing_references(tmp_path: Path) -> None:
    """Why the origin is its own field: closeout replaces the whole
    references list via `deskops edit task <id> references ...`."""
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0

    assert main([
        "edit", "task", "task-authored-from-drawer", "references", '["pytest tests/x.py"]',
        "--root", str(tmp_path),
    ]) == 0

    doc = _task_doc(tmp_path, "task-authored-from-drawer")
    assert doc["references"] == ["pytest tests/x.py"]
    assert doc["from_drawer"] == "desk/drawer/tasks/task-loose-idea.md"


def test_tasks_not_from_the_drawer_do_not_carry_the_field(tmp_path: Path) -> None:
    """from_drawer is written only when set, so every task already tracked in
    every desk keeps byte-identical content and an unchanged hash."""
    _install_desk(tmp_path)

    assert main(_authored_task_argv(tmp_path)) == 0

    text = (tmp_path / "desk" / "tasks" / "task-authored-from-drawer.md").read_text(encoding="utf-8")
    assert "from_drawer" not in text


def test_show_task_reports_the_drawer_origin(tmp_path: Path, capsys) -> None:
    _install_desk(tmp_path)
    _drawer_file(tmp_path, "tasks/task-loose-idea.md")
    assert main(_authored_task_argv(tmp_path, "--from-drawer", "loose-idea")) == 0
    capsys.readouterr()

    assert main(["show", "task", "task-authored-from-drawer", "--root", str(tmp_path)]) == 0

    assert "From drawer: desk/drawer/tasks/task-loose-idea.md" in capsys.readouterr().out
