"""Typed deskops errors and their CLI exit codes.

Exit-code contract:
    0  success
    1  domain error
    2  usage error (argparse also uses 2)
    3  environment error
"""

from __future__ import annotations


class DeskopsError(Exception):
    """Base class for errors the CLI knows how to report."""

    exit_code = 1


class DomainError(DeskopsError):
    """The request was understood but the workflow domain rejected it."""

    exit_code = 1


class UsageError(DeskopsError):
    """The invocation itself is wrong; reported on stdout like argparse help."""

    exit_code = 2


class DeskopsEnvironmentError(DeskopsError):
    """The local environment (tooling, store, external process) is unusable."""

    exit_code = 3
