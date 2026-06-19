---
id: task-formalize-phase-layer-workflow
status: active
references:
- desk/drawer/tasks/task-formalize-phase-layer-workflow.md
depends_on: []
pills:
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
files:
- AGENTS.md
- desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md
- desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/rituals/execution.md
- desk/rituals/testing.md
- desk/rituals/closeout.md
- desk/rituals/phase.md
- desk/tasks/Board.md
- docs/workflow-policy-reference.md
routine: routine-task-formalize-phase-layer-workflow
checklists:
- checklist-task-formalize-phase-layer-workflow-execution-ready
- checklist-task-formalize-phase-layer-workflow-testing-ready
- checklist-task-formalize-phase-layer-workflow-closeout-ready
current_node: checklist-task-formalize-phase-layer-workflow-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Formalize phase-layer workflow

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Define the missing phase-level workflow layer so deskops explicitly models task execution as a dependency graph with horizontal execution phases, per-task fresh-subagent execution, per-task unit-test-plus-commit closeout, and per-phase integration plus pill-reconciliation closeout.

## Scope

_State what is in scope and what is out of scope._

- add durable atoms for the phase-layer model
- add or update rituals so phase start, task execution, phase closeout, and next-phase preparation are explicit
- clarify that the old "cycle" intuition maps to the phase layer instead of a separate durable concept
- update operator-facing docs and onboarding guidance to use the phase model consistently
- seed the next-cycle / next-phase pill-generation expectation in the ritual layer

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-formalize-phase-layer-workflow.md.

Refine the workflow model so phase becomes the named dependency-layer execution unit above tasks, add a dedicated phase ritual, update task rituals to hand off into and out of phase work explicitly, and align operator-facing docs and board routing with the new model.

## Validation

_List the checks required before this task can close._

- pytest
- python -m deskops --help

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
