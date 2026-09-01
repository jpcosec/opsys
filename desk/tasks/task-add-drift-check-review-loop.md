---
id: task-add-drift-check-review-loop
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-add-drift-check-review-loop
current_node: checklist-task-add-drift-check-review-loop-closeout-ready
history:
- operator-task-add-drift-check-review-loop-activate
- operator-task-add-drift-check-review-loop-ready-for-testing
references: []
depends_on: []
pills:
- desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md
- desk/contexts/pill-011-self-reflection-noise-control.md
- desk/contexts/pill-009-source-file-graph-traceability.md
files: []
checklists:
- checklist-task-add-drift-check-review-loop-execution-ready
- checklist-task-add-drift-check-review-loop-testing-ready
- checklist-task-add-drift-check-review-loop-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: false
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
