---
id: task-rw-f5-command-registry
status: deferred
references: []
depends_on:
- task-rw-f3-atoms-service
- task-rw-f4-single-snapshot-reader
- task-rw-f1-cli-contract-tests
- task-rw-f1-output-golden-files
pills:
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/cli/parser.py
- deskops/cli/main.py
- deskops/cli/registry.py
- tests/test_command_registry.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f5
- topic:cli
- topic:refactor
---

# The CLI is built from a declarative command registry

## Rationale

_Explain why this task exists or the business driver behind it._

deskops/cli/parser.py is about 1,000 lines of hand-built argparse in which shared arguments (`--root`, selectors, `--format`) are redefined per command.

Plan: phase F5 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

deskops/cli/registry.py declares every command once (path, help, args, handler, `mutates: bool`); shared args are defined once; parser.py only walks the registry; every command's `--help` text stays byte-identical to the F1 help goldens, and exit codes stay as pinned by the F1 contract tests.

## Scope

_State what is in scope and what is out of scope._

In scope: parser and dispatch. `--format` is two shared argument groups, not one: `text|json` (`_add_output_format_argument`, parser.py:839-845, and runtime workers) and `text|json|yaml` (inbox, message, faq); each command keeps its variant. Do not edit tests/test_cli*.py, tests/test_output_goldens.py, tests/conftest.py or anything under tests/fixtures/golden/, and do not run `--update-golden`. Out of scope: renaming commands or flags.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Define the registry types as frozen dataclasses: `Arg(flags: tuple[str, ...], kwargs: dict, group: str | None = None, group_required: bool = False)` (args sharing a `group` go into one mutually exclusive group; required at parser.py:161 and 185, optional at 988) and `Command(path: tuple[str, ...], help: str, args: tuple[Arg, ...], handler: str, mutates: bool, epilog: str | None = None)`, where `handler` is a dotted `module:Class` path such as `deskops.cli.commands.runtime:RuntimeCLI`; commands generated from data today (the loops at parser.py:715, 780, 874 and 918, including the model-generated args) become factory functions that return `Command`s.
2. Port commands group by group; after each group run the F1 contract tests and the `help/` goldens.
3. Delete the per-command builder functions from parser.py; the walker's own `add_parser` call is the only one left.
4. Add tests/test_command_registry.py asserting that the set of command paths declared in the registry equals the set of command paths that have a file in tests/fixtures/golden/help/ (written from the old parser by task-rw-f1-output-golden-files), so a dropped or extra command fails.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli.py tests/test_cli_contract.py tests/test_output_goldens.py
- python -m deskops --help
- deskops faq
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

registry.py exists, parser.py has no per-command builder functions, the registry-equality test passes, and the contract and golden tests pass with their files unmodified.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- The F1 CLI contract tests are tests/test_cli_contract.py (created by task-rw-f1-cli-contract-tests); the help goldens are tests/fixtures/golden/help/ (task-rw-f1-output-golden-files).

## Open Ambiguities

None.
