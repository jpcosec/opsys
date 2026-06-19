---
id: pill-materialization-contracts-declare-source-intent-and-target
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:materialization
- topic:provenance
---

# Guardrail: materialization contracts declare source, intent, and target

## What

Treat materialization as an explicit contract from source atoms to target artifacts, with declared intent, target identity, and validation expectations.

## Why

Without an explicit contract, docs and projections drift away from their source atoms and become hard to audit or regenerate safely.

## When

Apply this pill whenever a task defines materialization models, CLI commands, validation checks, or generated/projection metadata.

## Where

Applies to source atom references, target artifact paths, projection metadata, and query surfaces for materialization status.

## How

Require declared source references, stable target identity, and validation rules that can prove the target still matches the intended source contract.

## How Not

Do not treat generated or derived docs as self-justifying. Do not leave target paths or source provenance implicit.
