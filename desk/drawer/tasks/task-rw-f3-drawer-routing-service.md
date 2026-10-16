---
id: task-rw-f3-drawer-routing-service
status: deferred
references: []
depends_on:
- task-rw-f2-transactional-doc-io
pills:
- desk/contexts/pill-cli-gaps-become-tracked-work.md
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
files:
- deskops/services/__init__.py
- deskops/services/drawer.py
- deskops/operations.py
- deskops/cli/commands/promote.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f3
- topic:refactor
- topic:drawer
---

# Drawer lookup moves to its own service

## Rationale

_Explain why this task exists or the business driver behind it._

deskops/operations.py mixes 15 domains. Its drawer members are `DRAWER_INDEX_FILES` (549), `resolve_drawer_source` (551) and `attach_drawer_source` (583); inbox-to-drawer promotion lives in deskops/cli/commands/promote.py (`PromoteCLI`).

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/drawer.py` owns drawer lookup and promotion logic; `DeskopsOperations` and `PromoteCLI` delegate to it.

## Scope

_State what is in scope and what is out of scope._

In scope: moving those members and `PromoteCLI`'s helpers (`_inbox_to_drawer_task` minus its printing, `_untrack_note`, `_resolve_unique`, `_read_markdown`, `_render_drawer_task`, `_slug`) with unchanged behavior; `PromoteCLI.run` stays in the CLI and prints what the service returns. This task creates the `deskops/services/` package and sets its pattern: each service is a class constructed with `root: Path` that uses `deskops.desk_paths` and `deskops.doc_io` as modules; `DeskopsOperations.__init__` builds it lazily and its old methods become one-line wrappers. Out of scope: any new verb (task-rw-f3-drawer-entry-removal-verb).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create deskops/services/__init__.py and deskops/services/drawer.py with `DrawerService(root)`.
2. Move the members; leave wrappers in operations.py and promote.py.
3. Run the named tests and the F1 contract tests unmodified.

## Validation

_List the checks required before this task can close._

- pytest tests/test_inbox_promote_cli_gaps.py tests/test_promotion_nesting.py tests/test_cli_contract.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`def resolve_drawer_source` in deskops/operations.py is a one-line wrapper, `grep -n DrawerService deskops/cli/commands/promote.py` matches, and the named tests pass unmodified.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- The F1 CLI contract tests are tests/test_cli_contract.py (created by task-rw-f1-cli-contract-tests).

## Open Ambiguities

None.
