---
id: task-desk-update-apply-writes-the-lifecycle-graph
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/cli/commands/desk.py
- tests/test_desk_sync.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-desk-update-apply-writes-the-lifecycle-graph.md
---

# `desk update --apply` on a fresh repo also writes the lifecycle graph

## Rationale

_Explain why this task exists or the business driver behind it._

Found by the supervisor on 2026-10-18 while reviewing task-rw-f2-typed-errors-and-exit-codes. The same behavior exists before that change. In a fresh `git init` repo with no desk and no store:
- `deskops desk update --root . --apply` exits 0 and `sldb stores check` passes;
- a second `deskops desk update --root .` still reports `- Legacy task lifecycle: 0 routine/primitive documents to delete, 0 tasks to rewrite, lifecycle graph missing, retired models still registered: none` and asks for `--apply` again.

So the first apply scaffolds the desk and the store but does not write the lifecycle graph, and the report sends an operator in a loop. `deskops init` does write it (`ensure_lifecycle_graph`, called from deskops/cli/main.py).

## Goal

_Describe the concrete result this task must produce._

One `desk update --apply` on a fresh repo leaves a desk for which a second `desk update` prints `Desk is up to date.`

## Scope

_State what is in scope and what is out of scope._

In scope: the apply path of `DeskCLI.update` and one test. Out of scope: `deskops init`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce with the commands in Rationale.
2. When the report includes `lifecycle graph missing` and the desk has the lifecycle rituals (after scaffolding), `--apply` calls `ensure_lifecycle_graph(root)` after the store is registered. Find why the current legacy-migration branch skips it on a desk with no legacy documents.
3. Test in tests/test_desk_sync.py: fresh repo, `desk update --apply` exit 0, then `desk update` prints `Desk is up to date.` and exits 0.

## Validation

_List the checks required before this task can close._

- pytest tests/test_desk_sync.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new test passes and fails on the current code; `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` and drive the real CLI. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
