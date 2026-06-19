---
id: pill-atom-lifecycle-preserves-provenance-and-materialization-links
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:atoms
- topic:provenance
---

# Guardrail: atom lifecycle preserves provenance and materialization links

## What

Treat atom create, split, merge, and deletion operations as provenance-sensitive changes that must preserve or deliberately reroute references, materializations, and traceability.

## Why

Atoms are the durable knowledge source. Lifecycle operations that ignore downstream links create stale docs, orphaned references, and duplicate knowledge.

## When

Apply this pill whenever a task changes atom lifecycle commands, tag validation, atom extraction, or any workflow that creates atoms from pills, findings, or diagrams.

## Where

Applies to atom models, lifecycle CLI surfaces, materialization contracts, graph links, and validation flows for atom references.

## How

Require explicit handling of references before split, merge, or delete; validate namespaces; and keep downstream materializations queryable through stable provenance.

## How Not

Do not treat atoms like disposable notes. Do not allow split/merge/delete operations to leave silent orphan references behind.
