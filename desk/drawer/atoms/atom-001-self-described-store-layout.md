# Self-described store layout

ID: atom-001
Status: stable
Category: store-contract

## What

The `.sldb/` workspace separates durable shared state under `core/`, rebuildable execution-time state under `runtime/`, and machine-local overrides under `.config/`.

## Why

Without this boundary, contributors cannot tell what belongs in git, what can be regenerated, or what should remain local to one machine.

## How

Version model and document contracts under `core/`. Rebuild semantic, section, and lock state under `runtime/`. Keep operator-specific overrides in `.config/`. Materialize the same concept into durable docs, deferred planning, active tasks, and temporary pills without rewriting the core idea each time.

## When

Apply this atom whenever store layout, tracking behavior, or git policy is being changed or explained.

## Where

It applies to `.sldb/`, `src/sldb/store/`, `src/sldb/cli/`, `.gitignore`, and the desk workflow that governs store evolution.

## For Whom

Maintainers changing SLDB store behavior and operators using desk to route that work.

## Related Atoms

- atom:none

## Materializes Into

- docs/architecture/self-described-store-layout-derivation.md
- desk/drawer/features/feature-001-sldb-core-runtime-layout.md
- desk/contexts/pill-006-self-described-store-layout.md

## Stabilized In

- .sldb/README.md
- docs/workspaces.md

## Distinct From

Pills are temporary execution guidance for one working set. This atom is the durable concept those pills should point back to.

## Tags

- system:sldb
- workspace:drawer
- topic:atoms
- topic:store
- topic:runtime
