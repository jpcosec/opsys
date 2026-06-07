# Add SLDB primitives docs CLI component diagram

## Kind

feature

## Status

open

## Problem

The repository had diagrams for documents/primitives and workflow surfaces, but no end-to-end component diagram showing how SLDB, models, docs, fields, primitives, materializers, specs, and CLI interact.

## Desired Outcome

Review and stabilize `docs/diagrams/codebase/sldb-primitives-docs-cli-components.md`, then migrate it to structured spec2viz source when that workflow is ready.

## Questions

- Are materializers correctly placed between desk surfaces and modeled SLDB docs?
- Should primitives belong only to deskops, or should some primitive abstractions move to SLDB or another reusable tool?
- Which arrows represent implemented behavior today versus target architecture?

## Related Atoms

- atom-cli-is-thin-over-primitives-and-sldb
- atom-primitives-encode-operational-rules
- atom-deskops-owns-workflow-not-document-infrastructure
