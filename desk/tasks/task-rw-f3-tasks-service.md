---
id: task-rw-f3-tasks-service
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f3-closeout-gates-service
pills:
- desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- deskops/services/tasks.py
- deskops/operations.py
- deskops/cli/commands/operations.py
- deskops/cli/commands/promote.py
- deskops/cli/parse_input.py
- tests/test_taskdoc_read_without_overlay.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f3-tasks-service.md
---

# Task lifecycle moves to a service and reads TaskDoc only through sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S3: for TaskDoc only, `_read_doc` (deskops/operations.py:2366-2377) overlays the regex parser `parse_task_sections` (127-181) on `extract_model_data`, and the regex wins when they disagree. `parse_task_sections` is also used by deskops/cli/commands/promote.py:47 to read free-form inbox notes, which are not TaskDocs. CLI argument parsing (`parse_task_input` and `parse_artifact_input`, 991-1037) also lives in operations.py.

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/tasks.py` owns create/advance/next for tasks; `_read_doc` reads TaskDoc only through `extract_model_data`; `parse_task_sections` remains only as an inbox-note helper used by promote.py; the `parse_*_input` functions move to deskops/cli/.

## Scope

_State what is in scope and what is out of scope._

In scope: the move, removing the overlay, moving the parsers, and editing TaskDoc files under desk/tasks/ and desk/drawer/tasks/ when step 1 finds a divergence. Service methods keep today's signatures (`create_task_bundle(payload) -> TaskBundle`, `advance_task(task_id, target_node=None)`, the `next` report function) and CLI output for create, advance and next stays as pinned by the existing tests (tests/test_cli.py:650 add task, 1440 show/list/advance, 772 next). operations.py keeps no re-export of the moved parsers. Out of scope: the closure path (task-rw-f3-single-closure-path), changing how `list tasks` reports unreadable documents (today a stderr warning naming the file, operations.py:485-488), and TaskDoc contract changes (F6).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. New tests/test_taskdoc_read_without_overlay.py compares overlay output with `extract_model_data` for every TaskDoc under desk/tasks/, desk/drawer/tasks/ (minus Board.md) and tests/fixtures/; fix any divergence by fixing the document, not by keeping the overlay. A document that `extract_model_data` cannot parse at all is listed by the test as a failure, never skipped.
2. Remove the overlay branch from `_read_doc`; move `parse_task_sections` into deskops/cli/commands/promote.py as a private helper; delete `parse_validation_section` (operations.py:184), whose only caller is the overlay. Keep the new test as a regression guard that `_read_doc(TaskDoc)` equals `extract_model_data` for every TaskDoc.
3. Move lifecycle methods into the service and `parse_*_input`, with the helpers only they use (`_load_yaml_mapping`, `_load_json_mapping`), into deskops/cli/parse_input.py; parse_input may import from operations.py (for `ARTIFACT_MODELS`), and operations.py must not import parse_input, so there is no cycle.

## Validation

_List the checks required before this task can close._

- pytest tests
- deskops list tasks --root .
- deskops show task task-write-end-to-end-deskops-operator-manual --root .

## Done When

_Name the observable condition that makes the task complete._

`grep -n 'parse_task_sections\|def parse_.*_input' deskops/operations.py` is empty, deskops/services/tasks.py defines create, advance and next, both CLI checks print the task, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
