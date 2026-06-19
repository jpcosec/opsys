---
id: task-conciliate-active-pills-for-reuse-and-next-phase
status: active
references:
- desk/drawer/tasks/task-conciliate-active-pills-for-reuse-and-next-phase.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
files:
- AGENTS.md
- desk/atoms/workflow-model/atom-pills-are-transient.md
- desk/atoms/workflow-model/atom-pills-index-existing-and-bound-future-context.md
- desk/atoms/workflow-model/atom-pills-carry-transitional-task-knowledge.md
- desk/atoms/workflow-model/atom-pills-end-as-atoms-docs-or-deletion.md
- desk/atoms/workflow-model/atom-pills-are-reusable-across-tasks.md
- desk/contexts/README.md
- desk/contexts/pills.md
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
- desk/tasks/Board.md
- docs/workflow-policy-reference.md
routine: routine-task-conciliate-active-pills-for-reuse-and-next-phase
checklists:
- checklist-task-conciliate-active-pills-for-reuse-and-next-phase-execution-ready
- checklist-task-conciliate-active-pills-for-reuse-and-next-phase-testing-ready
- checklist-task-conciliate-active-pills-for-reuse-and-next-phase-closeout-ready
current_node: checklist-task-conciliate-active-pills-for-reuse-and-next-phase-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Conciliate active pills for reuse and next phase

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Audit the current active context pills, remove overfit or stale pills, make the reusable many-to-many pill model explicit, and leave the board with a smaller reconciled pill set for the next phase.

## Scope

_State what is in scope and what is out of scope._

- classify current pills as reusable, stale, redundant, or misfiled
- promote durable pill-governance truth into atoms and durable docs
- remove or retire pills that are incomplete, obsolete, or too task-specific
- add any missing reusable phase/pill-governance pills needed for the next phase
- update board routing and pill reference docs to match the reconciled set

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-conciliate-active-pills-for-reuse-and-next-phase.md.

Distill reusable pill-governance truth into atoms and durable docs, delete stale or overfit pills from the active context surface, add the missing reusable phase-routing guardrails, and leave the board with a smaller reusable baseline for the next phase.

## Validation

_List the checks required before this task can close._

- python -m deskops list pills --root .
- python -m deskops list tasks --root .
- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
