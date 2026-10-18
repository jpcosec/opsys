"""Build the argparse tree by walking :mod:`deskops.cli.registry`.

No command is declared here: the registry is the single source of truth for
paths, help text, arguments, and epilogs.
"""

from __future__ import annotations

import argparse
from typing import Any

from deskops.cli.registry import ROOT_DESCRIPTION
from deskops.cli.registry import ROOT_EPILOG
from deskops.cli.registry import Arg
from deskops.cli.registry import Command
from deskops.cli.registry import command_registry


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deskops",
        description=ROOT_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=ROOT_EPILOG,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print a full traceback for unexpected errors.",
    )
    _add_command_level(parser, command_registry(), (), "command")
    return parser


def _add_command_level(
    parser: argparse.ArgumentParser,
    commands: tuple[Command, ...],
    parent_path: tuple[str, ...],
    dest: str | None,
) -> None:
    children = [command for command in commands if command.path[:-1] == parent_path]
    if not children:
        return
    if dest is None:
        raise RuntimeError(f"Command {parent_path!r} declares children without a subcommand dest")
    subparsers = parser.add_subparsers(dest=dest, required=True)
    for command in children:
        command_parser = _add_command_parser(subparsers, command)
        _add_arguments(command_parser, command.args)
        _add_command_level(command_parser, commands, command.path, command.subcommand_dest)


def _add_command_parser(
    subparsers: argparse._SubParsersAction[argparse.ArgumentParser],
    command: Command,
) -> argparse.ArgumentParser:
    kwargs: dict[str, Any] = {}
    if command.raw_text:
        kwargs["formatter_class"] = argparse.RawTextHelpFormatter
    if command.description is not None:
        kwargs["description"] = command.description
    if command.epilog is not None:
        kwargs["epilog"] = command.epilog
    parser = subparsers.add_parser(command.path[-1], help=command.help, **kwargs)
    parser.set_defaults(_deskops_command_path=command.path)
    return parser


def _add_arguments(parser: argparse.ArgumentParser, args: tuple[Arg, ...]) -> None:
    groups: dict[str, argparse._MutuallyExclusiveGroup] = {}
    for arg in args:
        target: Any = parser
        if arg.group is not None:
            group = groups.get(arg.group)
            if group is None:
                group = parser.add_mutually_exclusive_group(required=arg.group_required)
                groups[arg.group] = group
            target = group
        target.add_argument(*arg.flags, **arg.kwargs)
