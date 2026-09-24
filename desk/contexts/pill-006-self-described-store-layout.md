---
# pill-xxx
id: pill-006
# e.g., language:python, library:pydantic
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

_Define the context or guardrail this pill carries._

Treat the `.sldb/` split as one durable concept: shared contracts live in `core/`, rebuildable execution state lives in `runtime/`, and machine-local overrides live in `.config/`.

## Why

_Explain why this context matters for safe execution._

This keeps implementation work aligned with the durable atom instead of letting runtime files or local overrides drift back into the shared contract.

## When

_Describe when an agent should apply this pill._

Apply this pill during store routing, git-policy work, and any refactor that moves `.sldb` files across layers.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `.sldb/README.md`, `.gitignore`, store routing changes, and the store/CLI path-resolution code.

## How

_Describe the correct way to apply this guidance._

Ask of every `.sldb` file whether it is durable, rebuildable, or local-only. Route it accordingly and keep the implementation consistent with `atom-001`.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat runtime indexes or lock files as durable history, and do not hide shared contract changes in local config.
