"""Classify the top-level CLI grammar by workflow noun.

The parser is generated from ``deskops.cli.registry``; this test states which
top-level nouns are intentional public surfaces so new commands cannot drift
into the namespace just because they exist. It classifies existing nouns only;
it does not change parsing or command behavior.
"""

from __future__ import annotations

from deskops.cli.registry import command_for_path
from deskops.cli.registry import command_registry


TOP_LEVEL_GRAMMAR: dict[str, frozenset[str]] = {
    "operational": frozenset(
        {
            "next",
            "advance",
            "closeout",
            "promote",
            "bind",
            "message",
            "inbox",
            "graph",
            "drift",
            "runtime",
            "drawer",
            "issue",
            "retire",
        }
    ),
    "model_crud": frozenset({"add", "edit", "list", "show"}),
    "admin": frozenset(
        {
            "about",
            "doctor",
            "status",
            "faq",
            "bootstrap",
            "init",
            "repo",
            "desk",
        }
    ),
    "mixed": frozenset({"atoms"}),
    "transitional": frozenset({"materialize"}),
}


def test_top_level_nouns_are_classified_exactly_once() -> None:
    classified = [noun for nouns in TOP_LEVEL_GRAMMAR.values() for noun in nouns]

    assert len(classified) == len(set(classified))
    assert set(classified) == {command.path[0] for command in command_registry()}


def test_operational_mutates_guards() -> None:
    assert command_for_path(("next",)).mutates is False
    assert command_for_path(("show",)).mutates is False
    assert command_for_path(("advance",)).mutates is True
    assert command_for_path(("closeout",)).mutates is True
