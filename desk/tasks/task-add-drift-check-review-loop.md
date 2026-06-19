---
id: task-add-drift-check-review-loop
status: active
references:
- desk/drawer/tasks/task-add-drift-check-review-loop.md
depends_on: []
pills: []
files: []
routine: routine-task-add-drift-check-review-loop
checklists:
- checklist-task-add-drift-check-review-loop-execution-ready
- checklist-task-add-drift-check-review-loop-testing-ready
- checklist-task-add-drift-check-review-loop-closeout-ready
current_node: checklist-task-add-drift-check-review-loop-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Add drift check review loop

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Add a review-only drift check that compares atoms, materializations, graph links, tests, diagrams, and implementation surfaces.

## Scope

_State what is in scope and what is out of scope._

- provenance-backed findings
- confidence labels
- dedupe keys
- accepted/rejected decision storage
- promotion paths to tasks, questions, or atoms

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-add-drift-check-review-loop.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
