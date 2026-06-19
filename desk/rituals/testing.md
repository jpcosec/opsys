---
id: ritual-testing
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:testing
steps:
- 1. Confirm the incoming handoff names the intended contract, touched surfaces, and
  pill guardrails to prove.
- 1. Check whether existing tests are stale or encode obsolete behavior.
- 1. Translate the bound pills into concrete assertions, especially the failure cases
  implied by `how_not`.
- 1. Add or update tests for the intended contract.
- 1. Run the smallest relevant test scope first.
- 1. Run broader validation when the task changes shared behavior.
- 1. Do not proceed to closeout while relevant tests fail.
- 1. Exit testing only by opening a closeout handoff that confirms passing evidence
  for the contract and the bound pills.
---

# Testing ritual for desk task closure

## Purpose

Verify the intended task behavior with the right test scope before a task can close, while leaving shared integration or end-to-end proof for phase closeout.

## Trigger

Run after implementation changes and before closeout.

## Preconditions

- The intended behavior is clear.
- Relevant tests or test locations are known.
- Bound pills and their guardrails are known.
- The execution-to-testing handoff gate is explicit.

## Validation

- The intended behavior is covered.
- Bound pill guardrails are covered directly by tests or by an explicit validation step.
- The relevant tests pass.
- No known failure was ignored to force completion.
- Closeout receives an explicit green handoff rather than an informal claim that the task is done.

## Failure Modes

- Treating stale tests as truth.
- Skipping tests to move faster.
- Closing with failing relevant tests.
- Passing contract tests while leaving a bound pill's `how_not` path unchecked.
- Letting work skip from execution to closeout without a testing gate.

## Completion

The task has trustworthy test evidence and can proceed to closeout, with any broader cross-task validation obligations handed forward to the phase ritual.

## Steps

- Confirm the incoming handoff names the intended contract, touched surfaces, and pill guardrails to prove.
- Check whether existing tests are stale or encode obsolete behavior.
- Translate the bound pills into concrete assertions, especially the failure cases implied by `how_not`.
- Add or update tests for the intended contract.
- Run the smallest relevant test scope first.
- Run broader validation when the task changes shared behavior.
- Do not proceed to closeout while relevant tests fail.
- Exit testing only by opening a closeout handoff that confirms passing evidence for the contract and the bound pills.

