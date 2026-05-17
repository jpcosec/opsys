# Guardrail: keep sldb, specyaml, and opsys separated

ID: pill-004

## What

Treat sldb as infra, specyaml as canonical semantic contract, and opsys as the workflow-domain instance that owns desk, drawer, atoms, routines, edges, and materializers.

## Why

The current implementation work will sprawl and become hard to migrate if workflow-specific logic keeps leaking back into sldb or if canonical semantic concerns blur with operational documents.

## When

Apply this pill whenever a task changes models, folders, routines, materializers, or store contracts related to the opsys split.

## Where

Applies to task-013 through task-020, especially boundary, migration, AtomDoc, and materialization work.

## How

When adding or moving a model, ask first whether it belongs to infra, semantic contract, or workflow instance. Keep infra reusable, keep semantics canonical, and move workflow-specific behavior into opsys-owned surfaces.

## How Not

Do not add desk or drawer domain logic as if it were generic sldb infrastructure. Do not treat specyaml as the place for operational workflow documents.

## Tags

- system:sldb
- workspace:desk
- topic:opsys
- topic:separation
