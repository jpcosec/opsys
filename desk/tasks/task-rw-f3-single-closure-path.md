---
id: task-rw-f3-single-closure-path
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f3-atoms-service
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- deskops/services/closure.py
- deskops/operations.py
- deskops/cli/commands/closeout.py
- desk/rituals/closeout.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f3-single-closure-path.md
---

# One closure service behind every way of closing a task

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S1: three ways to close a task. `deskops advance` at the closeout node runs gates and commits through `_auto_commit_task_closure`; `deskops advance task <id> --to complete` skips gates, does not commit and leaves the task on the Board; `deskops closeout commit` (deskops/cli/commands/closeout.py) makes the commit but runs no gates and does not touch the Board. Issue 2 is decided (owner, 2026-10-16): option A, shipped in 819a8b8 as `deskops closeout commit --no-run --reason <text>` (trailers `Closeout-Mode: manual` and `Closeout-Reason`, index entry with `run_dir: null` and `mode: manual`). Tasks closed before that use a fabricated run dir such as runs/subagents/20260901-manual-task-fix-sldb-deskops-cli-drift-breaking-11-tests; it stays as history.

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/closure.py` performs every closure: gates (closeout_gates), Board update, bundle removal, exactly one commit with the route's trailers, and the index entry. `closeout commit` (both routes) uses it with its CLI unchanged.

## Scope

_State what is in scope and what is out of scope._

In scope: closure.py, rewiring `closeout commit`, rewiring `advance` per the decision (option A), and updating desk/rituals/closeout.md so it names `deskops closeout commit` as the one entry point. Out of scope: the `--run-dir`/`--no-run` CLI contract, which is fixed.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Implement closure.py on closeout_gates and doc_io, with both routes.
2. Point `closeout commit` at it; its existing tests in tests/test_closeout.py pass unmodified. tests/test_lifecycle_end_to_end.py may change only where the decision changes what `advance` does.
3. Rewire `advance` and `advance --to complete` per the decision.
4. 'Same closure result' means: exit 0, task file gone, task removed from desk/tasks/Board.md, one new commit with the route's trailers, one new index line.

## Validation

_List the checks required before this task can close._

- pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Every closing entry point produces the result defined in step 4, and desk/rituals/closeout.md names one entry point.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): option A. `advance` at the closeout node and `advance --to complete` stop closing: they exit 1 without changing anything and print that the task closes with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. `closeout commit` is the one entry point; tests/test_lifecycle_end_to_end.py and any other test that closes through `advance` switch to `closeout commit`.

## Open Ambiguities

None.
