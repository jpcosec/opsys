# Migrate the flat store implementation into core/runtime/.config routing

ID: feature-005
Status: promoted

## Goal

Refactor SLDB commands and store internals so they understand the new .sldb/core, .sldb/runtime, and .config layout instead of assuming a flat runtime-only store.

## Why

A conceptual layout is not enough; the runtime code must stop assuming that all store files live side by side. Without this migration, the new store structure remains only a design note.

## Scope

In scope: command path resolution, runtime indexes, lock files, model registration paths, temp drafts, and store rebuild behavior under the new layout. Out of scope: atom materialization by itself.

## Proposed Shape

Move durable model and plugin references under .sldb/core, keep active indexes and temp artifacts under .sldb/runtime, and teach CLI/store code to resolve the correct layer by responsibility. Preserve a single .sldb root while splitting the internals by role.

## Adoption Path

Promoted into active execution and now represented by the store layout helpers, migration code, and rebuilt `.sldb/` structure.

## Validation

- Core and runtime paths are resolved correctly by the CLI.
- Temp model drafts and locks live under runtime.
- Durable artifacts can be versioned independently of runtime noise.
- Existing store workflows continue to pass after migration.

## Tags

- system:sldb
- workspace:drawer
- topic:store
- topic:migration
- topic:runtime
