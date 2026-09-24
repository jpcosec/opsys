---
# pill-xxx
id: pill-legacy-desk-formats-need-explicit-adaptation
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:migration
- topic:legacy
---

# Guardrail: legacy desk formats need explicit adaptation

## What

_Define the context or guardrail this pill carries._

Treat a hand-written or older desk layout as a distinct workspace format that must be detected and adapted explicitly before current deskops modeled commands can manage it safely.

## Why

_Explain why this context matters for safe execution._

A legacy desk can contain real project workflow history while still failing current `BoardDoc`, `TaskDoc`, or pill model validation. If deskops treats that state as merely empty or malformed, operators lose visibility and cannot migrate confidently.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes desk initialization, health checks, board/task loading, migration logic, or per-project desk version detection.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `deskops` workspace detection, `deskops list/show/add task`, future doctor or migrate commands, and any repo whose `desk/` predates the current modeled contract.

## How

_Describe the correct way to apply this guidance._

Detect legacy markers explicitly, report the mismatch clearly, and offer a preservation-first migration path that upgrades the workspace contract without silently rewriting authored content.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat a legacy desk as a fresh empty desk. Do not overwrite hand-written operational history just to satisfy the current model validator.
