"""The declared command registry must match the frozen CLI surface.

The help goldens were captured from the hand-built parser by
task-rw-f1-output-golden-files, so comparing registry paths against that
directory catches both dropped commands and accidental new ones.
"""

from __future__ import annotations

from pathlib import Path

from deskops.cli.registry import command_registry


HELP_GOLDENS = Path(__file__).resolve().parent / "fixtures" / "golden" / "help"


def _golden_command_paths() -> set[tuple[str, ...]]:
    paths: set[tuple[str, ...]] = set()
    for path in HELP_GOLDENS.glob("deskops_*.txt"):
        if path.name == "deskops.txt":
            continue
        paths.add(tuple(path.stem.split("_")[1:]))
    return paths


def test_registry_paths_match_help_goldens() -> None:
    declared = {command.path for command in command_registry()}

    assert declared == _golden_command_paths()


def test_registry_paths_are_unique_and_have_parents() -> None:
    commands = command_registry()
    paths = [command.path for command in commands]

    assert len(paths) == len(set(paths))
    declared = set(paths)
    for path in paths:
        assert path
        if len(path) > 1:
            assert path[:-1] in declared
