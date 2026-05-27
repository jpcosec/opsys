from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deskops",
        description="deskops: Workflow-domain layer for the hum-ecosystem.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    _add_inbox_commands(subparsers)
    _add_faq_commands(subparsers)
    _add_repo_commands(subparsers)
    _add_desk_commands(subparsers)

    return parser


def _add_desk_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("desk", help="Desk workspace management.")
    s = p.add_subparsers(dest="desk_command", required=True)

    ins = s.add_parser("install", help="Scaffold a standard desk/ surface in a repo.")
    ins.add_argument("path", help="Target repository path")
    ins.add_argument("--name", help="Repo name for the registry")
    ins.add_argument("--id", help="Repo ID for the registry")
    ins.add_argument("--store", help="Ecosystem store to update")
    ins.add_argument("--pythonpath", help="Python path for model resolution")


def _add_repo_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("repo", help="Repository registration and discovery.")
    s = p.add_subparsers(dest="repo_command", required=True)

    reg = s.add_parser("register", help="Register a repository in the ecosystem.")
    reg.add_argument("name", help="Human-readable name")
    reg.add_argument("path", help="Relative path to repo root")
    reg.add_argument("--id", help="Stable unique ID, defaults to slugified name")
    reg.add_argument("--description", help="Markdown description")
    reg.add_argument("--tags", help="Comma-separated tags")
    reg.add_argument("--store", help="Store path to anchor the registry")
    reg.add_argument("--pythonpath", help="Python path for model resolution")


def _add_inbox_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser(
        "inbox", help="Log unclear points or suggestions into the repo desk."
    )
    p.add_argument("message", nargs="?", help="Inbox note body")
    p.add_argument(
        "--kind",
        choices=("unclear", "suggestion"),
        default="unclear",
        help="Type of desk note to write",
    )
    p.add_argument("--title", help="Short title for the note")
    p.add_argument(
        "--desk-root",
        help="Desk root directory override; defaults to the active project desk",
    )
    p.add_argument(
        "--store",
        help="Store path used to resolve the target project root for the default desk",
    )
    p.add_argument(
        "--repo",
        help="Target a registered repository name in the ecosystem",
    )
    p.add_argument(
        "--pythonpath",
        help="Project path used when auto-tracking inbox notes through a registered InboxNoteDoc model",
    )
    p.add_argument("--author", default="cli", help="Source label for the inbox note")
    p.add_argument("--list", action="store_true", help="List desk inbox notes")
    p.add_argument("--show", help="Show one inbox note by filename, stem, or slug fragment")
    p.add_argument("--limit", type=int, default=20, help="Limit listed notes")
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")


def _add_faq_commands(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
) -> None:
    p = subparsers.add_parser("faq", help="Browse the first-use FAQ by question.")
    p.add_argument(
        "question",
        nargs="?",
        help="Question index, slug, or text fragment. Omit to list available questions.",
    )
    p.add_argument("--format", choices=("text", "json", "yaml"), default="text")
    p.add_argument("--faq-path", default="docs/faq.md", help="FAQ markdown path")
