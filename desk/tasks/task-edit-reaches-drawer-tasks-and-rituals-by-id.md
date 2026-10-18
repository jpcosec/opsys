---
id: task-edit-reaches-drawer-tasks-and-rituals-by-id
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
- deskops/operations.py
- tests/test_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops edit` reaches drawer tasks, and finds rituals by their id

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 while bringing the desk to zero through the CLI only. (1) `deskops edit task <drawer-task> ...` answers "No artifact.task file found": edit only looks in desk/tasks/. To change the release drawer task, the supervisor had to remove it and recreate it through message send plus promote. (2) `deskops edit ritual ritual-closeout ...` answers "No artifact.ritual file found for selector ritual-closeout". The ritual id is ritual-closeout, but only the file stem `closeout` resolves.

## Goal

_Describe the concrete result this task must produce._

`deskops edit task <id>` edits a task in desk/drawer/tasks/ when no active task matches, and `deskops edit ritual <id>` accepts the ritual's frontmatter id as well as its file stem.

## Scope

_State what is in scope and what is out of scope._

In scope: the edit path in deskops/operations.py (`_editable_artifact` and selector resolution for artifact.task and artifact.ritual), and tests. Out of scope: other subjects.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. For artifact.task, after desk/tasks/ finds nothing, search desk/drawer/tasks/ with the same exact-then-prefix rule. Active tasks win when both match. 2. For artifact.ritual, add a candidate filter that matches the frontmatter id (for example `ritual-<stem>`), or map `ritual-` prefixed selectors onto the stem. 3. Tests for a drawer task edit, a ritual edited by id, and an active task shadowing a drawer task with the same id.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The three cases pass in tests, and `pytest tests` is green.
