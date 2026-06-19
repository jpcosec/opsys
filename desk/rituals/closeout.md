---
id: ritual-closeout
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:closeout
steps:
- 1. Confirm the incoming handoff includes passing evidence for the contract, validations,
  and bound pills.
- 1. Invalidate or fix stale tests if they no longer prove the intended behavior.
- 1. Run the required validation commands and confirm they pass.
- 1. Confirm the task satisfied each bound pill and that no matching board-routed
  pill was missed during execution.
- 1. Remove stale context docs that are no longer needed.
- 1. Untrack the task document from the local store if it is tracked.
- 1. Delete the resolved task file and remove it from the board.
- 1. Create one atomic closing commit for the task as the mandatory final gate.
---

# Closeout ritual for tracked desk tasks

## Purpose

Close a desk task only after tests, board cleanup, store cleanup when needed, and a dedicated closing commit, while leaving shared integration, pill reconciliation, and next-phase preparation to the phase ritual.

## Trigger

Start when the implementation work for a task is complete.

## Preconditions

- Relevant tests pass.
- Bound pill obligations were checked during testing.
- The testing-to-closeout handoff gate is explicit.
- Board updates are prepared.
- Any stale context docs are ready to be removed.
- The closing change is ready to commit.

## Validation

- The task is gone from desk/tasks.
- The board no longer routes the task.
- No bound pill is left unmet or unverified.
- The local store stays consistent after untracking.
- A dedicated closing commit exists in git.
- The task was not treated as closed before the final commit gate.

## Failure Modes

- Deleting the task before the closing commit exists.
- Leaving a stale tracked document in the store.
- Calling a task closed while tests still fail.
- Closing from green tests alone without checking pill coverage.
- Treating board cleanup or task deletion as equivalent to the final commit gate.

## Completion

The task has left the active workspace and its closure is recorded by its own git commit. If it was the last open task in the current phase, the board must still pass through phase closeout before the next phase begins.

## Steps

- Confirm the incoming handoff includes passing evidence for the contract, validations, and bound pills.
- Invalidate or fix stale tests if they no longer prove the intended behavior.
- Run the required validation commands and confirm they pass.
- Confirm the task satisfied each bound pill and that no matching board-routed pill was missed during execution.
- Remove stale context docs that are no longer needed.
- Untrack the task document from the local store if it is tracked.
- Delete the resolved task file and remove it from the board.
- Create one atomic closing commit for the task as the mandatory final gate.

