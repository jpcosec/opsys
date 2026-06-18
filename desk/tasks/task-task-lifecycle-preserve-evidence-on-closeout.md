---
id: task-task-lifecycle-preserve-evidence-on-closeout
status: draft
references: []
depends_on:
- task-task-lifecycle-clean-up-closed-task-artifacts
pills: []
files: []
routine: routine-task-task-lifecycle-preserve-evidence-on-closeout
checklists:
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-execution-ready
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-testing-ready
- checklist-task-task-lifecycle-preserve-evidence-on-closeout-closeout-ready
current_node: checklist-task-task-lifecycle-preserve-evidence-on-closeout-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
---

# Task Lifecycle: Preserve evidence on closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Task knowledge must flow into durable artifacts (atoms, tests, git) before the task is removed.

## Goal

_Describe the concrete result this task must produce._

Integrate knowledge extraction and evidence checking into the closeout gate.

## Scope

_State what is in scope and what is out of scope._

Closeout gate conditions and graph validation.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add a condition to the closeout checklist that queries the graph or git for related evidence before allowing closure.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

A task cannot be closed unless durable evidence (commit, atom, or test) is linked or verified.
