---
id: task-next-guidance-without-active-task
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
- deskops/services/tasks.py
- deskops/cli/commands/operations.py
- tests/test_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Make deskops next guide the user when no board task is routable

## Rationale

_Explain why this task exists or the business driver behind it._

`deskops next` without a selector raises `FileNotFoundError` when the board routes no tasks and
`ValueError` when it routes more than one. Both are dead ends for a first-use user who needs to
know what to do next.

## Goal

_Describe the concrete result this task must produce._

`deskops next` returns a structured, non-mutating guidance report for zero or multiple board
tasks and exits 0, while preserving the current report for a single task or an explicit selector.

## Scope

_State what is in scope and what is out of scope._

In scope: `next_action_report`, the CLI printer, and tests. Out of scope: changing `advance`,
changing board routing, adding new task fields, and treating the guidance state as an error.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In `deskops/services/tasks.py::next_action_report`, when `task_selector` is empty, read the
   board task refs before calling `_next_task_path`.
2. If there are zero refs, return
   `{"kind": "no_board_task", "board": "desk/tasks/Board.md", "suggested_commands": [...]}`.
   Suggestions, in order: `deskops list tasks --root .`, `deskops promote inbox-to-drawer-task
   <selector> --root .`, `deskops add task --root . --title "..." ...`.
3. If there is more than one ref, return
   `{"kind": "multiple_board_tasks", "board": "desk/tasks/Board.md", "tasks": [{"id", "status",
   "title"}], "suggested_commands": ["deskops next <task-id> --root .", "deskops list tasks
   --root ."]}`.
4. In `deskops/cli/commands/operations.py`, branch on `report["kind"]` and print a `Next:` heading,
   the explanation, and the suggested commands one per line. Return exit code 0.
5. Keep the existing task report path unchanged.
6. Add tests in `tests/test_cli.py`: empty board prints the guidance and exits 0; two routed tasks
   list both ids and ask for a selector; the board and task files are unchanged.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py -q
- python -m pytest tests/test_closeout.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Zero and multiple board-task states both print actionable guidance, exit 0, and leave desk files
byte-identical; the existing single-task `next` test still passes.
