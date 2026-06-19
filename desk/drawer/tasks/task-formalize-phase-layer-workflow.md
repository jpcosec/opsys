# Formalize phase-layer workflow

ID: task-formalize-phase-layer-workflow
Status: deferred
Priority: high

## Goal

Define the missing phase-level workflow layer so deskops explicitly models task execution as a dependency graph with horizontal execution phases, per-task fresh-subagent execution, per-task unit-test-plus-commit closeout, and per-phase integration plus pill-reconciliation closeout.

## Scope

- add durable atoms for the phase-layer model
- add or update rituals so phase start, task execution, phase closeout, and next-phase preparation are explicit
- clarify that the old "cycle" intuition maps to the phase layer instead of a separate durable concept
- update operator-facing docs and onboarding guidance to use the phase model consistently
- seed the next-cycle / next-phase pill-generation expectation in the ritual layer

## Suggested Pills

- `desk/contexts/pill-001-task-closure-commit.md`
- `desk/contexts/pill-005-subagent-execution.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`

## Done When

- the repo has an explicit phase ritual
- atoms define tasks, phases, and their reconciliation responsibilities clearly
- onboarding and workflow docs stop implying that only task-level rituals exist
- the relationship between phase and cycle is resolved in favor of one clear operational term
