---
id: ritual-phase
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:phases
steps:
- 1. Identify the ready dependency layer of tasks whose prerequisites are satisfied and whose planned changes do not overlap operationally.
- 1. Confirm each task has a fresh execution context bundle: the task doc, board-routed instructions, bound pills, linked atoms, linked files, and validation targets.
- 1. Run the execution ritual for each task in the phase before implementation begins.
- 1. Execute phase tasks in parallel when the environment supports it, or in isolated fresh contexts when parallelism is unavailable.
- 1. Require each task to close with its own targeted validation and atomic task commit before considering the phase complete.
- 1. When all phase tasks are closed, run shared integration or end-to-end validation for the combined layer.
- 1. Fix interaction regressions uncovered by the phase-level validation before phase closeout.
- 1. Reconcile the pill set touched by the phase: retire stale pills, merge or delete redundant pills, and promote durable residue into atoms and materializations.
- 1. Capture newly discovered tasks, dependencies, or next-phase pills before advancing.
- 1. Create one descriptive phase-closing commit for the integration and reconciliation pass.
---

# Phase ritual for dependency-layer execution

## Purpose

Run one horizontal dependency layer of tasks as the workflow unit above individual task execution, then close that layer with integration validation, pill reconciliation, and next-phase preparation.

## Trigger

Start when the board has one ready set of tasks whose dependencies are satisfied and whose execution can proceed without overlapping operational changes.

## Preconditions

- The board's active tasks and dependencies are explicit.
- The ready phase has been identified as a non-overlapping layer.
- Each task has a named context bundle and validation target.
- Phase-level validation expectations are known.
- A pill reconciliation pass is planned for phase closeout.

## Validation

- Every task in the phase executed from fresh context.
- Every task closed with its own tests and its own commit.
- Shared phase validation passed after task integration.
- Regressions caused by task interaction were fixed before advancing.
- Pills touched by the phase were reconciled as stale, redundant, durable, or still active.
- Durable residue from pills was promoted into atoms and materializations when needed.
- Newly discovered work for later phases was captured explicitly.
- The phase closeout has its own descriptive commit.

## Failure Modes

- Starting a phase without identifying the actual dependency layer.
- Treating a semantic milestone as a phase even when tasks still depend on one another.
- Letting tasks share one long-lived execution context instead of fresh task-specific bundles.
- Advancing to the next phase after isolated task tests without integration validation.
- Carrying stale or overlapping pills forward because each task closed independently.
- Hiding phase-level regressions inside later task commits instead of closing the layer explicitly.

## Completion

The current dependency layer is integrated, reconciled, and committed, and the board is ready to start the next phase.

## Steps

- Identify the ready dependency layer of tasks whose prerequisites are satisfied and whose planned changes do not overlap operationally.
- Confirm each task has a fresh execution context bundle: the task doc, board-routed instructions, bound pills, linked atoms, linked files, and validation targets.
- Run the execution ritual for each task in the phase before implementation begins.
- Execute phase tasks in parallel when the environment supports it, or in isolated fresh contexts when parallelism is unavailable.
- Require each task to close with its own targeted validation and atomic task commit before considering the phase complete.
- When all phase tasks are closed, run shared integration or end-to-end validation for the combined layer.
- Fix interaction regressions uncovered by the phase-level validation before phase closeout.
- Reconcile the pill set touched by the phase: retire stale pills, merge or delete redundant pills, and promote durable residue into atoms and materializations.
- Capture newly discovered tasks, dependencies, or next-phase pills before advancing.
- Create one descriptive phase-closing commit for the integration and reconciliation pass.
