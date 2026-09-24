---
# pill-xxx
id: pill-atom-lifecycle-preserves-provenance-and-materialization-links
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:atoms
- topic:provenance
---

# Guardrail: atom lifecycle preserves provenance and materialization links

## What

_Define the context or guardrail this pill carries._

Treat atom create, split, merge, and deletion operations as provenance-sensitive changes that must preserve or deliberately reroute references, materializations, and traceability.

## Why

_Explain why this context matters for safe execution._

Atoms are the durable knowledge source. Lifecycle operations that ignore downstream links create stale docs, orphaned references, and duplicate knowledge.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task changes atom lifecycle commands, tag validation, atom extraction, or any workflow that creates atoms from pills, findings, or diagrams.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to atom models, lifecycle CLI surfaces, materialization contracts, graph links, and validation flows for atom references.

## How

_Describe the correct way to apply this guidance._

Require explicit handling of references before split, merge, or delete; validate namespaces; and keep downstream materializations queryable through stable provenance.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat atoms like disposable notes. Do not allow split/merge/delete operations to leave silent orphan references behind.
