---
id: pill-006
tags:
- source-atom:atom-001
- system:sldb
- workspace:desk
- pill-type:index
- topic:atoms
- topic:store
---

# Atom: self-described store layout

## What

Treat the `.sldb/` split as one durable concept: shared contracts live in `core/`, rebuildable execution state lives in `runtime/`, and machine-local overrides live in `.config/`.

## Why

This keeps implementation work aligned with the durable atom instead of letting runtime files or local overrides drift back into the shared contract.

## When

Apply this pill during store routing, git-policy work, and any refactor that moves `.sldb` files across layers.

## Where

Applies to `.sldb/README.md`, `.gitignore`, store routing changes, and the store/CLI path-resolution code.

## How

Ask of every `.sldb` file whether it is durable, rebuildable, or local-only. Route it accordingly and keep the implementation consistent with `atom-001`.

## How Not

Do not treat runtime indexes or lock files as durable history, and do not hide shared contract changes in local config.
