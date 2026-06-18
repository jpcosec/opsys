---
id: task-task-lifecycle-clean-up-closed-task-artifacts
status: draft
references: []
depends_on:
- task-task-lifecycle-enforce-phase-gates-during-advancement
pills: []
files: []
routine: routine-task-task-lifecycle-clean-up-closed-task-artifacts
checklists:
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-execution-ready
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-testing-ready
- checklist-task-task-lifecycle-clean-up-closed-task-artifacts-closeout-ready
current_node: checklist-task-task-lifecycle-clean-up-closed-task-artifacts-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Task Lifecycle: Clean up closed task artifacts

## Rationale

_Explain why this task exists or the business driver behind it._

The active workspace desk/ should not be cluttered with closed task artifacts.

## Goal

_Describe the concrete result this task must produce._

Automatically remove or move task artifacts when a task reaches the closed state.

## Scope

_State what is in scope and what is out of scope._

Close operator primitive and task closeout logic.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add file deletion or archive logic to the task close operator in deskops/runtime/.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Closing a task automatically removes its markdown files from desk/tasks/ and desk/routines/.
