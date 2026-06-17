---
id: pill-005
tags:
- system:sldb
- workspace:desk
- pill-type:pattern
- topic:subagents
- topic:execution
---

# Pattern: execute opsys migration work through subagents

## What

Use specialized subagents as the normal execution surface for the opsys migration tasks, with the primary session acting as coordinator, integrator, and final verifier.

## Why

The remaining tasks span architecture, store migration, AtomDoc design, semantic mapping, and workflow materialization. Subagents reduce context overload and make it easier to keep each line of work coherent while preserving a single coordinated plan.

## When

Apply this pill whenever task-013 through task-020 are executed or decomposed.

## Where

Applies to opsys-boundary work, .sldb redesign, AtomDoc modeling, materialization routines, and proof-slice execution.

## How

Split work into focused subproblems, assign them to specialized subagents, collect their outputs back into the active task flow, and only close tasks after the main session integrates results, runs validations, and records the final commit.

## How Not

Do not try to carry the entire opsys migration as one monolithic thread in a single context. Do not let subagent outputs bypass the main validation, board, and commit workflow.
