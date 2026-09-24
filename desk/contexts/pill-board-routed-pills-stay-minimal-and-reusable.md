---
# pill-xxx
id: pill-board-routed-pills-stay-minimal-and-reusable
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:pills
- topic:boards
- topic:routing
---

# Guardrail: board-routed pills stay minimal and reusable

## What

_Define the context or guardrail this pill carries._

Treat the board-routed pill set as the smallest reusable baseline that most active tasks should see, not as a dumping ground for every historical or domain-specific pill in the workspace.

## Why

_Explain why this context matters for safe execution._

If the board routes too many pills, fresh subagents inherit stale or irrelevant context and start treating pills like task mirrors instead of reusable atomic truths.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever the board pill list is updated, a new phase is prepared, or a pill audit asks whether a rule belongs in the board baseline or only on selected tasks.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/tasks/Board.md`, `desk/contexts/pills.md`, pill conciliation passes, and future phase-preparation workflows.

## How

_Describe the correct way to apply this guidance._

Keep only cross-cutting reusable pills on the board. Bind domain-specific, risky, or file-specific pills directly on the tasks that need them. During phase closeout, remove board pills that no longer serve as reusable baseline guidance.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not route old tranche pills board-wide just because they still exist in `desk/contexts/`. Do not confuse "relevant to one active task" with "baseline context for most board work."
