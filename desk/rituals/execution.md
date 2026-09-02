---
id: ritual-execution
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
steps:
- 1. Confirm the current phase is explicit and that this task belongs to the ready dependency layer being executed.
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- 1. Run a zero-context preflight comprehension gate: give one fresh subagent only the
  TaskDoc and require it to restate the intended work step by step plus every ambiguity
  it sees, then store that reformulation at `runs/subagents/<run-dir>/preflight.md`.
- 1. Pass the preflight only when that reformulation reproduces the task intent closely
  enough to execute without guesswork; if the subagent reports any ambiguity or misses
  the intended work, fix the TaskDoc before dispatching any Executor.
- 1. Send one fresh subagent with no prior task context to review the full task bundle,
  board-routed instructions, bound pills, linked atoms, linked files, and planned
  validation only for ambiguity, missing guardrails, and likely missed pills.
- 1. Resolve or record the cold-review findings before implementation starts.
- 1. Sweep the board-routed pills and any task-local pills against the task scope,
  touched files, implementation path, and planned validation.
- 1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part
  of the task.
- 1. If a risky ambiguity is still uncovered, create or update a pill before implementation
  instead of proceeding on implicit assumptions.
- 1. Do not start implementation until the initialization gate confirms atomization,
  preflight comprehension, cold review, and pill coverage.
- 1. Implement only the changes required for the active task.
- 1. Keep scope tight and avoid unrelated fixes.
- 1. Prepare validation before calling the work complete.
- 1. Exit execution only by opening a handoff to testing that names the intended contract,
  relevant tests, and pill guardrails that must be proven.
---

# Execution ritual for active desk tasks

## Purpose

Carry one active desk task through scoped implementation inside an explicit phase with task and pill binding, including a zero-context TaskDoc comprehension gate and a fresh-context coverage check strong enough to catch missing guardrails before implementation starts.

## Trigger

Start when a desk task becomes the current execution target.

## Preconditions

- The task exists in desk/tasks.
- The current phase or ready dependency layer is explicit.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.
- The active board pills are visible to the executor.
- The initialization gate is still open.
- The TaskDoc is specific enough for a fresh-context subagent to restate the work without guessing.

## Validation

- The active task is explicit.
- A fresh-context subagent ran the TaskDoc-only preflight comprehension gate before any Executor was dispatched.
- The preflight reformulation was stored at `runs/subagents/<run-dir>/preflight.md`.
- The preflight passed only because the subagent's reformulation reproduced the intended work and surfaced no unresolved ambiguity.
- A fresh-context subagent reviewed the task bundle before implementation.
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
- Skipping the zero-context TaskDoc comprehension gate and dispatching an Executor anyway.
- Letting the preflight pass even though the reformulation missed intent or reported ambiguity.
- Skipping the fresh-context subagent review and relying only on the primary executor's familiarity.
- Skipping pill binding when ambiguity still exists.
- Treating the task's `## Pills` list as a formality instead of a coverage checklist.
- Binding only the most obvious pill while ignoring pills implied by `when`, `where`, or `how_not`.
- Starting code changes before the initialization gate is closed.
- Handing work to closeout directly from execution without a testing gate.

## Completion

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.

## Steps

- Confirm the current phase is explicit and that this task belongs to the ready dependency layer being executed.
- Open the initialization gate by making the active task, task scope, touched files, and validation targets explicit.
- Atomize the work into one coherent deliverable.
- Audit code, docs, tests, and git state before changing anything.
- Run a zero-context preflight comprehension gate: give one fresh subagent only the TaskDoc and require it to restate the intended work step by step plus every ambiguity it sees.
- Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
- Pass the preflight only when the reformulation reproduces the task intent closely enough to execute without guesswork; if the subagent reports any ambiguity or misses the intended work, fix the TaskDoc before dispatching any Executor.
- Send one fresh subagent with no prior task context to review the task, board-routed instructions, bound pills, linked atoms, linked files, and planned validation only for ambiguity, missing guardrails, and likely missed pills.
- Resolve or record the cold-review findings before implementation starts.
- Sweep the board-routed pills and any task-local pills against the task scope, touched files, implementation path, and planned validation.
- Bind every pill whose `when`, `where`, or `how_not` matches a plausible part of the task.
- If a risky ambiguity is still uncovered, create or update a pill before implementation instead of proceeding on implicit assumptions.
- Do not start implementation until the initialization gate confirms atomization, preflight comprehension, cold review, and pill coverage.
- Implement only the changes required for the active task.
- Keep scope tight and avoid unrelated fixes.
- Prepare validation before calling the work complete.
- Exit execution only by opening a handoff to testing that names the intended contract, relevant tests, and pill guardrails that must be proven.

