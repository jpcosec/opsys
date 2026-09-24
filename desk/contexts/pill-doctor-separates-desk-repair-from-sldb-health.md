---
# pill-xxx
id: pill-doctor-separates-desk-repair-from-sldb-health
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:health
- topic:boundary
---

# Guardrail: doctor separates desk repair from sldb health

## What

_Define the context or guardrail this pill carries._

Treat desk health and SLDB/store health as related but distinct layers, with `deskops` repairing desk-owned workflow surfaces and delegating infra checks to SLDB.

## Why

_Explain why this context matters for safe execution._

A single health command is useful only if it is clear which failures belong to desk workflow state and which belong to shared structured-document infrastructure.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task designs `deskops doctor`, recovery flows, invalid desk detection, or store-health delegation.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to desk structure checks, invalid task/pill/atom detection, stale runtime cleanup, and any wrapper around `sldb stores check` or model registration queries.

## How

_Describe the correct way to apply this guidance._

Report desk-owned problems directly, offer non-destructive repair guidance where possible, and call into SLDB for store/infrastructure checks instead of duplicating that logic inside deskops.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not blur desk workflow repair with generic SLDB repair. Do not reimplement store health behavior locally just because the result should appear in one health surface.
