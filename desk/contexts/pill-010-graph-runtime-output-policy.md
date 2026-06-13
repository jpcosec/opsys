---
id: pill-010
tags:
- system:deskops
- system:kgdb
- topic:runtime
- topic:drift-control
---

# Guardrail: generated graph output is runtime state

## What

Generated graph snapshots and query indexes are runtime artifacts unless a task explicitly promotes a fixture or contract example into versioned test data.

## Why

Graph outputs can become large, noisy, and stale. Keeping generated outputs in runtime prevents the repository from confusing source knowledge with derived graph projections.

## When

Apply this pill whenever a task writes KGDB graph JSON, generated indexes, query results, or self-reflection reports.

## Where

Generated outputs should prefer `.sldb/runtime/` or another agreed ignored runtime location. Versioned fixtures belong under tests or contracts only when they prove behavior.

## How

Separate source specs/adapters from generated graph outputs. Add or update ignore rules when a new runtime path is introduced. Keep small golden fixtures only for tests.

## How Not

Do not commit full generated graph snapshots as documentation. Do not use generated graph output as the only source of relation truth.
