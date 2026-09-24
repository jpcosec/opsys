---
# pill-xxx
id: pill-zero-context-preflight-precedes-executor
# e.g., language:python, library:pydantic
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

_Define the context or guardrail this pill carries._

Before any Executor is dispatched, run one fresh-context subagent against only the TaskDoc and require a step-by-step reformulation of the intended work plus any ambiguity it detects.

## Why

_Explain why this context matters for safe execution._

This cheap comprehension gate proves whether the TaskDoc itself is sufficient. If the subagent cannot restate the intent correctly from the task alone, the real execution bundle is still relying on hidden context or coordinator memory.

## When

_Describe when an agent should apply this pill._

Apply this whenever an active desk task enters execution and before the real Executor launch.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/execution.md` preparation work and evidence stored under `runs/subagents/<run-dir>/preflight.md`.

## How

_Describe the correct way to apply this guidance._

Pass only when the reformulation reproduces the task intent closely enough to execute without guesswork. If the subagent reports any ambiguity, or misses the intended step sequence, fix the TaskDoc first and rerun the preflight.

## How Not

_Describe the shortcut or failure mode to avoid._
