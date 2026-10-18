---
id: task-task-selectors-resolve-tracked-legacy-filenames
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/desk_paths.py
- deskops/operations.py
- tests/test_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Task selectors also resolve tracked tasks whose file name predates `task-*`

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. graph_ui desk/tasks/001-define-graph-ui-data-contract.md .. 006-*.md are tracked TaskDocs, but `deskops edit task` and `advance task` resolve through `_artifact_glob_pattern("artifact.task")` = `task-*.md`, so every selector returns "No artifact.task file found". `show task` resolves with `<selector>*.md` and finds them. graph_ui needs `edit` to rewrite 8 unresolved `depends_on` refs.

## Goal

_Describe the concrete result this task must produce._

When the `task-*.md` pattern finds nothing, task selectors fall back to the TaskDoc files tracked in the repo's `.sldb` under desk/tasks, with the same exact-then-unique-prefix rule.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/desk_paths.py (optional filter for candidates), deskops/operations.py (fallback for artifact.task), a regression test. Out of scope: renaming legacy task files or migrating their ids.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `resolve_selector` takes an optional `keep` predicate over candidate paths. 2. `_resolve_artifact_selector` for artifact.task: on FileNotFoundError, retry with pattern `*.md` keeping only paths tracked as TaskDoc in `.sldb/core/documents/TaskDoc/*.yaml`. 3. Test: a sandbox desk with a tracked task file `001-legacy.md`; `edit task 001-legacy` succeeds.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`deskops edit task 001-legacy ...` works on a tracked legacy task file, untracked `*.md` files in desk/tasks are still ignored, and `pytest tests` is green.
