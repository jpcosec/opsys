"""Selectors of tracked desk surfaces resolve through ``sldb.api.select_documents`` (CC35b).

The rule is the disk rule's (exact name before a unique prefix) and so are the messages;
a file whose name differs from its tracked document's resolves by both (TaskDoc a6).
"""

from __future__ import annotations

from pathlib import Path

import pytest
from sldb.runtime.validation import render_model_markdown

from deskops import doc_access
from deskops.models import AtomDoc
from deskops.models import RitualDoc


def _ritual(root: Path, file_name: str, ritual_id: str) -> Path:
    path = root / "desk" / "rituals" / file_name
    payload = RitualDoc(
        id=ritual_id,
        title=f"Ritual {ritual_id}",
        purpose="Purpose.",
        trigger="Trigger.",
        completion="Done.",
    ).render_payload()
    doc_access.create_doc(root, path, RitualDoc, payload, ritual_id)
    return path


def _atom(root: Path, atom_id: str, folder: str = "") -> Path:
    path = root / "desk" / "atoms" / folder / f"{atom_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = AtomDoc(id=atom_id, title=f"Atom {atom_id}", five_wh_one_plus="what", answer="An answer.").render_payload()
    doc_access.create_doc(root, path, AtomDoc, payload, atom_id)
    return path


def test_ritual_resolves_by_its_tracked_name_and_by_its_file_stem(lifecycle_desk: Path) -> None:
    path = _ritual(lifecycle_desk, "handoff.md", "ritual-handoff")

    assert doc_access.resolve_ritual_selector(lifecycle_desk, "ritual-handoff") == path
    assert doc_access.resolve_ritual_selector(lifecycle_desk, "handoff") == path


def test_ritual_execution_resolves_by_name_and_by_stem(lifecycle_desk: Path) -> None:
    path = lifecycle_desk / "desk" / "rituals" / "execution.md"
    if path.exists():
        doc_access.delete_doc(lifecycle_desk, path)
    _ritual(lifecycle_desk, "execution.md", "ritual-execution")

    assert doc_access.resolve_ritual_selector(lifecycle_desk, "ritual-execution") == path
    assert doc_access.resolve_ritual_selector(lifecycle_desk, "execution") == path


def test_exact_name_wins_over_a_longer_name_with_the_same_prefix(lifecycle_desk: Path) -> None:
    exact = _atom(lifecycle_desk, "atom-cc35b-sample")
    _atom(lifecycle_desk, "atom-cc35b-sample-extra")

    resolved = doc_access.resolve_artifact_selector(
        lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "atom-cc35b-sample"
    )

    assert resolved == exact


def test_unique_prefix_resolves_in_a_subfolder(lifecycle_desk: Path) -> None:
    only = _atom(lifecycle_desk, "atom-cc35b-nested", folder="nested")

    resolved = doc_access.resolve_artifact_selector(
        lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "atom-cc35b-nes"
    )

    assert resolved == only


def test_not_found_keeps_the_disk_rule_message(lifecycle_desk: Path) -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        doc_access.resolve_artifact_selector(
            lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "atom-cc35b-missing"
        )

    assert str(excinfo.value) == "No artifact.atom file found for selector 'atom-cc35b-missing'"


def test_prefix_ambiguity_lists_sorted_paths_relative_to_the_desk(lifecycle_desk: Path) -> None:
    _atom(lifecycle_desk, "atom-cc35b-shared-beta", folder="b")
    _atom(lifecycle_desk, "atom-cc35b-shared-alpha")

    with pytest.raises(ValueError) as excinfo:
        doc_access.resolve_artifact_selector(
            lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "atom-cc35b-shared"
        )

    assert str(excinfo.value) == (
        "Ambiguous artifact.atom selector 'atom-cc35b-shared': "
        "atoms/atom-cc35b-shared-alpha.md, atoms/b/atom-cc35b-shared-beta.md"
    )


def test_file_stem_ambiguity_keeps_the_disk_rule_message(lifecycle_desk: Path) -> None:
    _ritual(lifecycle_desk, "cc35b-gate.md", "ritual-cc35b-gate-one")
    _ritual(lifecycle_desk, "cc35b-gate-two.md", "ritual-cc35b-gate-two")

    with pytest.raises(ValueError) as excinfo:
        doc_access.resolve_ritual_selector(lifecycle_desk, "cc35b-gate")

    assert str(excinfo.value) == (
        "Ambiguous artifact.ritual selector 'cc35b-gate': rituals/cc35b-gate-two.md, rituals/cc35b-gate.md"
    )


def test_an_untracked_file_on_a_tracked_surface_does_not_resolve(lifecycle_desk: Path) -> None:
    stray = lifecycle_desk / "desk" / "atoms" / "atom-cc35b-stray.md"
    stray.write_text("# atom-cc35b-stray\n", encoding="utf-8")

    with pytest.raises(FileNotFoundError, match="No artifact.atom file found for selector 'atom-cc35b-stray'"):
        doc_access.resolve_artifact_selector(
            lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "atom-cc35b-stray"
        )


def test_the_drawer_still_resolves_on_disk(lifecycle_desk: Path) -> None:
    drawer_task = lifecycle_desk / "desk" / "drawer" / "tasks" / "task-cc35b-drawer-only.md"
    drawer_task.parent.mkdir(parents=True, exist_ok=True)
    drawer_task.write_text("# task-cc35b-drawer-only\n", encoding="utf-8")

    resolved = doc_access.resolve_artifact_selector(
        lifecycle_desk, "artifact.task", lifecycle_desk / "desk" / "drawer" / "tasks", "task-cc35b-drawer"
    )

    assert resolved == drawer_task


def test_empty_selector_is_rejected_before_any_query(lifecycle_desk: Path) -> None:
    with pytest.raises(ValueError, match="Empty or whitespace-only selector provided for artifact.atom"):
        doc_access.resolve_artifact_selector(lifecycle_desk, "artifact.atom", lifecycle_desk / "desk" / "atoms", "  ")
