---
id: task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout
status: active
references:
- desk/drawer/tasks/task-enforce-pill-to-atom-knowledge-graduation.md
depends_on: []
pills:
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files: []
routine: routine-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout
checklists:
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-execution-ready
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-testing-ready
- checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-closeout-ready
current_node: checklist-task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Enforce pill-to-atom knowledge graduation during task closeout

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make task closeout verify that durable knowledge discovered through pills is promoted into atoms before transient execution context is deleted.

## Scope

_State what is in scope and what is out of scope._

- define how closeout distinguishes transitional pill context from durable residue
- require pill audit during closeout for bugfix, feature, and migration tasks
- record or verify atom updates when a task refined project rulings or reusable patterns
- avoid forcing atom updates when a pill only routed already-existing knowledge
- integrate the rule with task deletion, pill cleanup, and closeout evidence

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-enforce-pill-to-atom-knowledge-graduation.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
