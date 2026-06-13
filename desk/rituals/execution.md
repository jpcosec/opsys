---
id: ritual-execution
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
steps:
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- 1. Send one fresh subagent with no prior task context to review the task, board-routed
  pills, and planned file touches only for ambiguity, missing guardrails, and likely
  missed pills.
- 1. Resolve or record the cold-review findings before implementation starts.
- 1. Sweep the board-routed pills and any task-local pills against the task scope,
  touched files, implementation path, and planned validation.
- 1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part
  of the task.
- 1. If a risky ambiguity is still uncovered, create or update a pill before implementation
  instead of proceeding on implicit assumptions.
- 1. Do not start implementation until the initialization gate confirms atomization,
  cold review, and pill coverage.
- 1. Implement only the changes required for the active task.
- 1. Keep scope tight and avoid unrelated fixes.
- 1. Prepare validation before calling the work complete.
- 1. Exit execution only by opening a handoff to testing that names the intended contract,
  relevant tests, and pill guardrails that must be proven.
---

# Execution ritual for active desk tasks

## Purpose

Carry one active desk task through scoped implementation with explicit task and pill binding, including a coverage check strong enough to catch missing guardrails before implementation starts.

## Trigger

Start when a desk task becomes the current execution target.

## Preconditions

- The task exists in desk/tasks.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.
- The active board pills are visible to the executor.
- The initialization gate is still open.

## Validation

- The active task is explicit.
- A fresh-context subagent reviewed the task before implementation.
- Required pills are named in the task.
- Cold-review ambiguities were resolved, tracked, or converted into pill updates before code changes.
- Each changed surface is either covered by a named pill or explicitly judged to need no pill.
- No active board pill was skipped just because it looked generic or already familiar.
- Implementation did not start before the initialization gate was satisfied.
- Changes stay within task scope.
- The work is ready for testing and has an explicit testing handoff.

## Failure Modes

- Working without an active task doc.
- Mixing unrelated concerns into one task.
- Skipping the fresh-context subagent review and relying only on the primary executor's familiarity.
- Skipping pill binding when ambiguity still exists.
- Treating the task's `## Pills` list as a formality instead of a coverage checklist.
- Binding only the most obvious pill while ignoring pills implied by `when`, `where`, or `how_not`.
- Starting code changes before the initialization gate is closed.
- Handing work to closeout directly from execution without a testing gate.

## Completion

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.

## Steps

- Open the initialization gate by making the active task, task scope, touched files, and validation targets explicit.
- Atomize the work into one coherent deliverable.
- Audit code, docs, tests, and git state before changing anything.
- Send one fresh subagent with no prior task context to review the task, board-routed pills, and planned file touches only for ambiguity, missing guardrails, and likely missed pills.
- Resolve or record the cold-review findings before implementation starts.
- Sweep the board-routed pills and any task-local pills against the task scope, touched files, implementation path, and planned validation.
- Bind every pill whose `when`, `where`, or `how_not` matches a plausible part of the task.
- If a risky ambiguity is still uncovered, create or update a pill before implementation instead of proceeding on implicit assumptions.
- Do not start implementation until the initialization gate confirms atomization, cold review, and pill coverage.
- Implement only the changes required for the active task.
- Keep scope tight and avoid unrelated fixes.
- Prepare validation before calling the work complete.
- Exit execution only by opening a handoff to testing that names the intended contract, relevant tests, and pill guardrails that must be proven.

