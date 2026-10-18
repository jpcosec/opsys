---
id: task-next-why-explanation
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
- deskops/cli/registry.py
- deskops/services/tasks.py
- deskops/cli/commands/operations.py
- tests/test_cli.py
- tests/fixtures/golden/help/deskops_next.txt
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Add --why to deskops next

## Rationale

_Explain why this task exists or the business driver behind it._

`next` reports what to do but not why that task and those actions were selected. Users and agents
must infer the board route, lifecycle state, and source paths from separate commands.

## Goal

_Describe the concrete result this task must produce._

`deskops next --why` prints a `Why:` section that names the selection route, the matched workflow
state, the merged pill sources, and the source files, without mutating the desk.

## Scope

_State what is in scope and what is out of scope._

In scope: one `--why` flag, report fields, printer output, tests, and the help golden. Out of
scope: new workflow states, changes to the lifecycle spec, and changes to `advance`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Add `A("--why", action="store_true", help="Explain why this task and these actions were selected.")`
   to the `("next",)` command in `deskops/cli/registry.py`.
2. In `next_action_report`, add a `"why"` list to the task report:
   - `task selected by explicit selector` or `task selected from the single board route`;
   - `current_node <node> matched workflow state <state id> in deskops/spec/workflows/task_lifecycle.yaml`;
   - `pills merged from desk/tasks/Board.md and the task`;
   - the existing task, board, and workflow source paths.
3. In `_print_next_action_report`, when the flag is set, print a `Why:` heading followed by `- `
   lines before `Next actions:`.
4. Update `tests/fixtures/golden/help/deskops_next.txt` from the actual `python -m deskops next
   --help` output; do not hand-edit the usage line.
5. Add a test in `tests/test_cli.py` that runs `next <task> --why` and asserts the `Why:` heading,
   the workflow state path, and the board path appear, and the task file is unchanged.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py -q
- python -m pytest tests/test_command_registry.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

`deskops next --why` prints the selection route, matched state, pill sources, and source paths;
the help golden matches; and all listed tests pass.
