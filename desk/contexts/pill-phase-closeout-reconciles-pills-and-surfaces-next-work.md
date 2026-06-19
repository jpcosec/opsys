---
id: pill-phase-closeout-reconciles-pills-and-surfaces-next-work
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:phases
- topic:pills
- topic:closeout
---

# Guardrail: phase closeout reconciles pills and surfaces next work

## What

After all tasks in a dependency layer close, run one explicit phase closeout pass that checks integration behavior, reconciles the pill set, and captures newly discovered work before the next phase begins.

## Why

Task closeout proves each deliverable in isolation, but it does not by itself clean up overlapping pills, catch interaction regressions, or prepare the next execution layer. Without a phase pass, stale context and cross-task breakage accumulate between waves.

## When

Apply this pill whenever a board is executed through dependency layers and a full phase of non-overlapping tasks has finished task-level closeout.

## Where

Applies to `desk/rituals/phase.md`, `desk/tasks/Board.md`, board-level execution planning, pill audits, and end-of-phase validation.

## How

Treat phase closeout as mandatory: run integration or end-to-end validation, fix regressions, classify pills as stale, redundant, durable, or still needed, promote durable knowledge into atoms and materializations, and draft or bind the pills needed for the next ready phase.

## How Not

Do not treat a stack of closed task commits as sufficient to start the next phase. Do not carry stale or overlapping pills forward just because each individual task passed its own tests.
