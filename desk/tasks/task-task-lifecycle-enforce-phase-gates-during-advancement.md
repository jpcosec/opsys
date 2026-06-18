---
id: task-task-lifecycle-enforce-phase-gates-during-advancement
status: draft
references: []
depends_on:
- task-task-lifecycle-implement-pill-binding-command
pills: []
files: []
routine: routine-task-task-lifecycle-enforce-phase-gates-during-advancement
checklists:
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-execution-ready
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-testing-ready
- checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-closeout-ready
current_node: checklist-task-task-lifecycle-enforce-phase-gates-during-advancement-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Task Lifecycle: Enforce phase gates during advancement

## Rationale

_Explain why this task exists or the business driver behind it._

Tasks should not skip from implementation to closeout without passing testing and validation.

## Goal

_Describe the concrete result this task must produce._

Ensure deskops advance task respects strict phase gates (execution -> testing -> closeout).

## Scope

_State what is in scope and what is out of scope._

deskops/operations.py and advancement primitives (checklists, operators).

## Implementation Path

_Outline the expected implementation route or affected surface._

Update the checklist and condition evaluation in advance command to halt if evidence/validation is missing.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

deskops advance refuses to transition to closeout if testing or validation is incomplete.
