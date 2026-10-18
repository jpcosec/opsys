"""Selector resolution: one rule for every desk artifact lookup."""

from __future__ import annotations

from pathlib import Path

import pytest

from deskops.desk_paths import resolve_selector


def _write(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {path.stem}\n", encoding="utf-8")
    return path


def test_exact_name_tier_wins_over_prefix(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    exact = _write(directory / "atom-example.md")
    _write(directory / "atom-example-extra.md")

    resolved = resolve_selector(desk_root, [directory], "atom-example.md", "atom-*.md", "artifact.atom", True)

    assert resolved == exact


def test_exact_stem_tier_wins_over_prefix(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    exact = _write(directory / "atom-example.md")
    _write(directory / "atom-example-extra.md")

    resolved = resolve_selector(desk_root, [directory], "atom-example", "atom-*.md", "artifact.atom", True)

    assert resolved == exact


def test_unique_prefix_falls_back_to_the_only_match(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    only = _write(directory / "nested" / "atom-trackable.md")

    resolved = resolve_selector(desk_root, [directory], "atom-track", "atom-*.md", "artifact.atom", True)

    assert resolved == only


def test_recursive_search_is_opt_in(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "tasks"
    root = _write(directory / "task-one.md")
    _write(directory / "archive" / "task-one.md")

    assert resolve_selector(desk_root, [directory], "task-one", "task-*.md", "task", False) == root

    with pytest.raises(ValueError, match="Ambiguous task selector 'task-one'"):
        resolve_selector(desk_root, [directory], "task-one", "task-*.md", "task", True)


def test_zero_matches_raises_the_shared_not_found_message(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "atom-other.md")

    with pytest.raises(FileNotFoundError, match=r"No artifact.atom file found for selector 'atom-missing'"):
        resolve_selector(desk_root, [directory], "atom-missing", "atom-*.md", "artifact.atom", True)


def test_exact_ambiguity_lists_sorted_paths_relative_to_the_desk_root(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "b" / "atom-shared.md")
    _write(directory / "a" / "atom-shared.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [directory], "atom-shared", "atom-*.md", "artifact.atom", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.atom selector 'atom-shared': atoms/a/atom-shared.md, atoms/b/atom-shared.md"
    )


def test_prefix_ambiguity_lists_matches(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "atoms"
    _write(directory / "atom-shared-alpha.md")
    _write(directory / "atom-shared-beta.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [directory], "atom-shared", "atom-*.md", "artifact.atom", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.atom selector 'atom-shared': atoms/atom-shared-alpha.md, atoms/atom-shared-beta.md"
    )


def test_multiple_directories_share_one_candidate_set(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    contexts = desk_root / "contexts"
    drawer = desk_root / "drawer" / "pills"
    _write(contexts / "pill-shared.md")
    _write(drawer / "pill-shared.md")

    with pytest.raises(ValueError) as excinfo:
        resolve_selector(desk_root, [contexts, drawer], "pill-shared", "pill-*.md", "artifact.pill", True)

    assert str(excinfo.value) == (
        "Ambiguous artifact.pill selector 'pill-shared': "
        "contexts/pill-shared.md, drawer/pills/pill-shared.md"
    )


def test_missing_directories_are_skipped(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    present = desk_root / "contexts"
    _write(present / "pill-present.md")

    resolved = resolve_selector(
        desk_root,
        [desk_root / "missing", present],
        "pill-present",
        "pill-*.md",
        "artifact.pill",
        True,
    )

    assert resolved == present / "pill-present.md"


def test_empty_selector_is_rejected_before_any_lookup(tmp_path: Path) -> None:
    desk_root = tmp_path / "desk"
    directory = desk_root / "tasks"
    _write(directory / "task-one.md")

    with pytest.raises(ValueError, match="Empty or whitespace-only"):
        resolve_selector(desk_root, [directory], "   ", "task-*.md", "artifact.task", True)
