---
id: pill-zero-context-preflight-precedes-executor
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:subagents
- topic:preflight
- topic:execution
---

# Guardrail: zero-context preflight precedes executor

## What

Before any Executor is dispatched, run one fresh-context subagent against only the TaskDoc and require a step-by-step reformulation of the intended work plus any ambiguity it detects.

## Why

This cheap comprehension gate proves whether the TaskDoc itself is sufficient. If the subagent cannot restate the intent correctly from the task alone, the real execution bundle is still relying on hidden context or coordinator memory.

## When

Apply this whenever an active desk task enters execution and before the real Executor launch.

## Where

Applies to `desk/rituals/execution.md` preparation work and evidence stored under `runs/subagents/<run-dir>/preflight.md`.

## How

Pass only when the reformulation reproduces the task intent closely enough to execute without guesswork. If the subagent reports any ambiguity, or misses the intended step sequence, fix the TaskDoc first and rerun the preflight.
