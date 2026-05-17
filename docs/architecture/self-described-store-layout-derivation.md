# Self-described Store Layout Derivation

Derived from `atom-001`.

The atom states that `.sldb/` must separate durable shared state from runtime state and local machine overrides. This document stabilizes that concept as durable guidance outside the active desk surface.

## Why this matters

When the store shape is explicit, contributors can commit durable contracts confidently, regenerate runtime indexes safely, and avoid dragging local machine state into shared history.

## Operational application

Treat `.sldb/core/` as the durable contract layer, `.sldb/runtime/` as rebuildable execution state, and `.sldb/.config/` as local override state. Use the same atom lineage to explain the feature, task, and pill that operationalize the concept.

## Workflow lineage

- `desk/drawer/features/feature-001-sldb-core-runtime-layout.md`
- `desk/contexts/pill-006-self-described-store-layout.md`
- `.sldb/README.md`
