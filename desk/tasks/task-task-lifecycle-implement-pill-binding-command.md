---
id: task-task-lifecycle-implement-pill-binding-command
status: draft
references: []
depends_on: []
pills: []
files: []
routine: routine-task-task-lifecycle-implement-pill-binding-command
checklists:
- checklist-task-task-lifecycle-implement-pill-binding-command-execution-ready
- checklist-task-task-lifecycle-implement-pill-binding-command-testing-ready
- checklist-task-task-lifecycle-implement-pill-binding-command-closeout-ready
current_node: checklist-task-task-lifecycle-implement-pill-binding-command-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Task Lifecycle: Implement pill binding command

## Rationale

_Explain why this task exists or the business driver behind it._

Binding pills to tasks ensures execution happens with clear context and guardrails.

## Goal

_Describe the concrete result this task must produce._

Provide a CLI command or safe field append operation to bind a pill to a task.

## Scope

_State what is in scope and what is out of scope._

CLI parsing for binding pills to task artifacts.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add a 'deskops bind pill <task-id> <pill-id>' command or modify 'deskops edit' to support list appending.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

A user can bind an existing pill to an active task using the deskops CLI.
