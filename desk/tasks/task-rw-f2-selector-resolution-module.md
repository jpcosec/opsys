---
id: task-rw-f2-selector-resolution-module
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f1-model-contract-snapshot
- task-rw-f1-cli-contract-tests
- task-rw-f1-output-golden-files
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/desk_paths.py
- deskops/operations.py
- tests/test_desk_paths.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f2-selector-resolution-module.md
---

# One module resolves every desk selector

## Rationale

_Explain why this task exists or the business driver behind it._

Four methods in deskops/operations.py resolve selectors: `_resolve_glob` (2077), `_resolve_artifact_selector_multi` (2086), `_resolve_artifact_selector` (2112) and `_one_artifact_match` (2203). After task-rw-f0-reject-ambiguous-selectors they share one rule (exact name or stem first, then a unique prefix, else an ambiguity error), but each keeps its own copy and message.

Plan: phase F2 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

A new `deskops/desk_paths.py` implements that rule once; the four methods become one-line delegations to it.

## Scope

_State what is in scope and what is out of scope._

In scope: selector resolution only (desk layout constants such as `ARTIFACT_PATHS` stay where they are). Behavior is unchanged except two messages, which become one format for all callers: `Ambiguous <what> selector '<selector>': <candidates>` and `No <what> file found for selector '<selector>'`, where <candidates> are the matching paths relative to the desk root, sorted, joined with ', '.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. deskops/desk_paths.py: `resolve_selector(desk_root: Path, directories: list[Path], selector: str, pattern: str, what: str, recursive: bool) -> Path`; `recursive` keeps each caller's current search (`_resolve_glob` uses `glob`, the artifact selectors use `rglob`); `what` is the artifact id for the artifact selectors and the directory kind (`task`, the only one its callers use today) for `_resolve_glob` callers; with two tiers: (1) a file whose `name` or `stem` equals the selector; (2) a unique file whose name or stem starts with it; zero matches raise `FileNotFoundError` and more than one raise `ValueError`, with the messages above. Update any existing test that asserts the old wording, and list each one in the closeout.
2. Make the four methods delegate.
3. tests/test_desk_paths.py covers both tiers, zero matches and ambiguity.

## Validation

_List the checks required before this task can close._

- pytest tests/test_desk_paths.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`grep -n 'glob(\|rglob(' deskops/operations.py` shows no selector-resolution loop outside the delegations, and `pytest tests` (including the F1 contract tests) is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- The F1 CLI contract tests are tests/test_cli_contract.py (created by task-rw-f1-cli-contract-tests); they must pass unchanged.

## Open Ambiguities

None.
