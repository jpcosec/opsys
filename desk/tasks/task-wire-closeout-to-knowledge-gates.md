---
id: task-wire-closeout-to-knowledge-gates
status: active
references:
- desk/drawer/tasks/task-wire-closeout-knowledge-gates.md
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files: []
routine: routine-task-wire-closeout-to-knowledge-gates
checklists:
- checklist-task-wire-closeout-to-knowledge-gates-execution-ready
- checklist-task-wire-closeout-to-knowledge-gates-testing-ready
- checklist-task-wire-closeout-to-knowledge-gates-closeout-ready
current_node: checklist-task-wire-closeout-to-knowledge-gates-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Wire closeout to knowledge gates

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make closeout check tests, atoms, graph links, materialization status, cleanup, and commit evidence before work leaves the active desk.

## Scope

_State what is in scope and what is out of scope._

- relevant tests pass
- changed files have atom/materialization links or routed follow-up work
- generated artifacts declare sources
- stale tasks/pills are deleted or promoted
- dedicated commit exists

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-wire-closeout-knowledge-gates.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
