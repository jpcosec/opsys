---
id: pill-doctor-separates-desk-repair-from-sldb-health
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:health
- topic:boundary
---

# Guardrail: doctor separates desk repair from sldb health

## What

Treat desk health and SLDB/store health as related but distinct layers, with `deskops` repairing desk-owned workflow surfaces and delegating infra checks to SLDB.

## Why

A single health command is useful only if it is clear which failures belong to desk workflow state and which belong to shared structured-document infrastructure.

## When

Apply this pill whenever a task designs `deskops doctor`, recovery flows, invalid desk detection, or store-health delegation.

## Where

Applies to desk structure checks, invalid task/pill/atom detection, stale runtime cleanup, and any wrapper around `sldb stores check` or model registration queries.

## How

Report desk-owned problems directly, offer non-destructive repair guidance where possible, and call into SLDB for store/infrastructure checks instead of duplicating that logic inside deskops.

## How Not

Do not blur desk workflow repair with generic SLDB repair. Do not reimplement store health behavior locally just because the result should appear in one health surface.
