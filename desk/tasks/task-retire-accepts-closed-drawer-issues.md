---
id: task-retire-accepts-closed-drawer-issues
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
- deskops/services/retire.py
- tests/test_retire_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops retire` also retires closed drawer issues, with their reason and refs

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-19 the coordinator asked to retire the closed inbox notes and the closed drawer issues with `deskops retire`, citing the commit that resolved each one, as sldb and graph_ui did. retire refuses every file under desk/drawer/ and points at `drawer remove`, which records no reason or ref. The 28 closed or resolved issues and the archived diagnosis record in desk/drawer/issues/ have no retire path that keeps the reason.

## Goal

_Describe the concrete result this task must produce._

`deskops retire desk/drawer/issues/<file>.md --reason ... --ref ...` works when the issue's status is closed or resolved, or when the issue is an archived record (`record: true`). Open drawer issues and other drawer entries keep pointing at `drawer remove` (or `issue close` for open issues). The drawer Board's bullets for the retired issue are removed in the same transaction, as drawer remove does.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/services/retire.py (an exception to the drawer refusal for closed or record issues, reusing issue_status from deskops/services/issues.py and the Board-bullet removal from DrawerService), and tests in tests/test_retire_cli.py. Out of scope: open issues.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Before the dedicated-verb refusal, allow desk/drawer/issues/*.md when issue_status(text) is closed or resolved, or the frontmatter has `record: true`. 2. Remove its `- `<stem>` ` bullets from desk/drawer/tasks/Board.md in the same DocTransaction, and do not count the drawer Board as an inbound reference for that file. 3. Tests: a closed issue is retired and its Board bullet removed; an open issue is refused with a pointer to issue close; a record issue is retired.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_retire_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The tests pass and `pytest tests` is green.
