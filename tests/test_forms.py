"""F4 T4.1-T4.3: the forms layer over the world (create/edit/read a task)."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops import forms
from deskops.derived_conditions import UnknownTaskError


@pytest.fixture(scope="module")
def root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One bootstrapped root for the module: `bootstrap_world` costs seconds."""
    return tmp_path_factory.mktemp("forms")


def test_create_task_lands_in_the_drawer_with_a_drawer_status(root: Path) -> None:
    view = forms.create_task(
        root,
        title="Drawer work",
        goal="Stay unrouted.",
        scope="Drawer only.",
        implementation_path="Write the file.",
        done_when="The task exists.",
    )

    assert view.id == "task-drawer-work"
    assert view.path == root / "desk" / "drawer" / "tasks" / "task-drawer-work.md"
    assert view.status == "drawer"
    assert "## Implementation Path" in view.path.read_text(encoding="utf-8")


def test_create_task_routed_lands_in_the_active_folder(root: Path) -> None:
    view = forms.create_task(
        root, title="Routed work", goal="g", scope="s", drawer=False
    )

    assert view.path == root / "desk" / "tasks" / "task-routed-work.md"


def test_read_task_returns_the_stored_payload_and_derived_status(root: Path) -> None:
    forms.create_task(root, title="Readable", goal="Read me.", scope="s")

    view = forms.read_task(root, "task-readable")

    assert view.payload["goal"] == "Read me."
    assert view.status == "drawer"


def test_read_unknown_task_raises(root: Path) -> None:
    with pytest.raises(UnknownTaskError):
        forms.read_task(root, "task-not-there")


def test_list_tasks_reports_every_tracked_task_with_its_status(root: Path) -> None:
    forms.create_task(root, title="Listed one", goal="g", scope="s")
    forms.create_task(root, title="Listed two", goal="g", scope="s")

    listed = {view.id: view.status for view in forms.list_tasks(root)}

    assert listed["task-listed-one"] == "drawer"
    assert listed["task-listed-two"] == "drawer"


def test_edit_task_field_rewrites_only_that_field(root: Path) -> None:
    forms.create_task(
        root,
        title="Edit me",
        goal="Original goal.",
        scope="Original scope.",
        implementation_path="Original path.",
        done_when="Original done when.",
    )

    view = forms.edit_task_field(root, "task-edit-me", "implementation_path", "New path.")

    text = view.path.read_text(encoding="utf-8")
    assert view.payload["implementation_path"] == "New path."
    assert "New path." in text
    assert "Original goal." in text
    assert "Original done when." in text


def test_edit_task_field_parses_json_lists_for_list_fields(root: Path) -> None:
    forms.create_task(root, title="Edit lists", goal="g", scope="s")

    view = forms.edit_task_field(root, "task-edit-lists", "validation", '["pytest", "ruff"]')

    assert view.payload["validation"] == ["pytest", "ruff"]


def test_edit_task_field_rejects_immutable_and_unknown_fields(root: Path) -> None:
    forms.create_task(root, title="Refuse edits", goal="g", scope="s")

    with pytest.raises(forms.FormsError, match="immutable"):
        forms.edit_task_field(root, "task-refuse-edits", "id", "task-other")
    with pytest.raises(forms.FormsError, match="Unknown field"):
        forms.edit_task_field(root, "task-refuse-edits", "nonesuch", "x")


def test_edit_task_field_rejects_a_bad_list_value(root: Path) -> None:
    forms.create_task(root, title="Bad list", goal="g", scope="s")

    with pytest.raises(forms.FormsError, match="JSON list"):
        forms.edit_task_field(root, "task-bad-list", "validation", "pytest")


def test_resolve_task_id_accepts_exact_id_and_unique_fragment(root: Path) -> None:
    forms.create_task(root, title="Fragment one", goal="g", scope="s")
    forms.create_task(root, title="Fragment two", goal="g", scope="s")

    assert forms.resolve_task_id(root, "task-fragment-one") == "task-fragment-one"
    assert forms.resolve_task_id(root, "fragment-two") == "task-fragment-two"


def test_resolve_task_id_reports_ambiguity_and_absence(root: Path) -> None:
    forms.create_task(root, title="Shared alpha", goal="g", scope="s")
    forms.create_task(root, title="Shared beta", goal="g", scope="s")

    with pytest.raises(forms.FormsError, match="Ambiguous"):
        forms.resolve_task_id(root, "task-shared")
    with pytest.raises(FileNotFoundError):
        forms.resolve_task_id(root, "task-nothing-like-this")


def test_edit_adopts_an_authored_task_file_into_the_store(root: Path) -> None:
    folder = root / "desk" / "tasks"
    folder.mkdir(parents=True, exist_ok=True)
    authored = folder / "task-authored-by-hand.md"
    authored.write_text(
        "---\nid: task-authored-by-hand\nstatus: active\ntags: []\n---\n\n"
        "# Authored by hand\n\n## Rationale\n\nWhy.\n\n## Goal\n\nGoal.\n\n## Scope\n\nScope.\n\n"
        "## Implementation Path\n\n_Outline the expected implementation route or affected surface._\n\n"
        "Old path.\n\n## Validation\n\n_List the checks required before this task can close._\n\n"
        "- pytest\n\n## Done When\n\n_Name the observable condition that makes the task complete._\n\nDone.\n",
        encoding="utf-8",
    )

    view = forms.edit_task_field(root, "task-authored-by-hand", "goal", "Edited goal.")

    assert view.payload["goal"] == "Edited goal."
    assert "Edited goal." in authored.read_text(encoding="utf-8")
    assert forms.read_task(root, "task-authored-by-hand").id == "task-authored-by-hand"
