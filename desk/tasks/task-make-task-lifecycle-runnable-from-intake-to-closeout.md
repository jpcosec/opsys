---
id: task-make-task-lifecycle-runnable-from-intake-to-closeout
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files: []
routine: routine-task-make-task-lifecycle-runnable-from-intake-to-closeout
checklists:
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-testing-ready
- checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-closeout-ready
current_node: checklist-task-make-task-lifecycle-runnable-from-intake-to-closeout-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Make task lifecycle runnable from intake to closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Turn the documented task lifecycle into an executable deskops path.

## Scope

_State what is in scope and what is out of scope._

- promote drawer or inbox item into task candidate
- create routed task bundle
- bind pills
- advance through execution, testing, and closeout gates
- delete closed active task artifacts
- preserve durable evidence in atoms, docs, graph relations, tests, and git

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-make-task-lifecycle-runnable-end-to-end.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
