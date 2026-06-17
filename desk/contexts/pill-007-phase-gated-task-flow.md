---
id: pill-007
tags:
- system:sldb
- workspace:desk
- pill-type:guardrail
- topic:workflow
- topic:phase-gates
---

# Guardrail: force every task through explicit phase gates

## What

Every desk task must pass through explicit entry, handoff, testing, and closeout gates instead of flowing directly from implementation intent to completion.

## Why

Agents keep skipping atomization, test review, test execution, or the closing commit when those obligations live only as background expectations. Phase gates turn those obligations into mandatory stop points.

## When

Apply this pill whenever a desk task is initialized, handed from execution to testing, or handed from testing to closeout.

## Where

Applies to `desk/rituals/execution.md`, `desk/rituals/testing.md`, `desk/rituals/closeout.md`, and any task that changes code, docs, or workflow state.

## How

Open each task with an initialization gate that confirms task clarity, file scope, validation targets, and atomization. Require an execution exit gate before testing, a testing exit gate before closeout, and a final closeout gate that ends in the dedicated commit.

## How Not

Do not treat implementation as the default starting point. Do not jump from “code looks done” to task deletion or board cleanup without a testing handoff and a dedicated closing commit.
