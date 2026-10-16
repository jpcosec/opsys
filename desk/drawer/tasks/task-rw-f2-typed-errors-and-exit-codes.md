---
id: task-rw-f2-typed-errors-and-exit-codes
status: deferred
references: []
depends_on:
- task-rw-f2-selector-resolution-module
pills:
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
files:
- deskops/errors.py
- deskops/cli/main.py
- deskops/cli/parser.py
- deskops/cli/commands/desk.py
- deskops/operations.py
- tests/test_cli.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f2
- topic:errors
- topic:cli
---

# Typed errors, a fixed exit-code table, and no swallowed tracebacks

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory findings X2 and X3. `deskops.cli.main.main` (deskops/cli/main.py:370-392) maps a few built-in exceptions to exit 1, classifies others by `exc.__class__.__name__`, and turns everything else into `SystemExit("Unexpected: ...")` with no traceback; that hid both the doctor crash and the Governance CI SyntaxError. deskops/cli/commands/desk.py:149-171 ignores a failing `stores check` and prints 'Desk is up to date.' with exit 0.

Plan: phase F2 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

deskops raises typed errors from one module; the CLI maps them to exit codes 0 ok, 1 domain error, 2 usage error (argparse already uses 2), 3 environment error; an unexpected exception prints `Unexpected error: <type>: <message> (rerun with --debug for the traceback)` on stderr and exits 3; with `--debug` it prints the full traceback to stderr and still exits 3.

## Scope

_State what is in scope and what is out of scope._

In scope: new deskops/errors.py, the handler in cli/main.py, a global `--debug` flag added to the root parser in `build_parser` (deskops/cli/parser.py:25) that also sets logging to DEBUG, and the `desk update` swallow. `--debug` is a root-only option parsed by argparse; `CLI.run` stores it on the CLI instance and `main()` (which handles exceptions outside `CLI.run`) reads it from that instance. Logging is unchanged (already DEBUG to a file); only delete the first `_setup_logging` definition (operations.py:350, dead and self-recursive) and keep the second (362). Typed errors print their message and exit with their code, with no traceback, with or without `--debug`, on stderr as today's exit-1 mappings do. `<type>` in the unexpected-error line is `type(exc).__name__`; with `--debug` the traceback prints first, then that line. `UsageError` replaces the hand-written `return 2` at cli/main.py:153 and :227 and cli/commands/drift.py:14; the handler prints the same text to the same stream those sites use today (stdout). Existing exit-1 mappings (FileNotFoundError, KeyError, ValueError, pydantic ValidationError, SLDBStoreError) stay exit 1. Out of scope: the JSON error envelope (task-rw-f5-output-renderer).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. errors.py: `DeskopsError(Exception)` with `exit_code`, subclasses `DomainError` (1), `UsageError` (2), `DeskopsEnvironmentError` (3).
2. main.py: `isinstance` checks instead of class-name strings (import pydantic's ValidationError and sldb's SLDBStoreError); unexpected exceptions exit 3 as described.
3. desk.py: a failing `stores check` or unparseable JSON raises `DeskopsEnvironmentError`.
4. Tests in tests/test_cli.py: an injected unexpected exception exits 3 and prints the one-line message without `--debug`, and exits 3 and prints a traceback with `--debug`; `desk update` with a broken store exits 3. List every exit code that changes in the closeout.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli.py tests/test_desk_sync.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

No path prints `Unexpected:` without the `--debug` hint, the new tests pass, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
