---
# pill-xxx
id: pill-materialization-contracts-declare-source-intent-and-target
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:materialization
- topic:provenance
---

# Guardrail: materialization contracts declare source, intent, and target

## What

_Define the context or guardrail this pill carries._

Treat materialization as an explicit contract from source atoms to target artifacts, with declared intent, target identity, and validation expectations.

## Why

_Explain why this context matters for safe execution._

Without an explicit contract, docs and projections drift away from their source atoms and become hard to audit or regenerate safely.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task defines materialization models, CLI commands, validation checks, or generated/projection metadata.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to source atom references, target artifact paths, projection metadata, and query surfaces for materialization status.

## How

_Describe the correct way to apply this guidance._

Require declared source references, stable target identity, and validation rules that can prove the target still matches the intended source contract.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat generated or derived docs as self-justifying. Do not leave target paths or source provenance implicit.
