---
name: sldb
description: Use for StructuredNLDoc models, Markdown roundtrips, store-backed querying, and writing/editing structured Markdown through SLDB rather than ad hoc file edits or desk-local field documents.
---

# SLDB

Use `sldb` for `StructuredNLDoc` models and their Markdown documents.

## When To Use

- Any `StructuredNLDoc`-backed document that should roundtrip as structured data.
- Any structured document change that needs model-level idempotency validation.
- Any field-level inspection, query, update, append, clean, or removal for tracked Markdown documents.
- Any creation, tracking, update, recovery, or composition of structured Markdown documents.
- Any task that touches model templates, `Field(...)` definitions, store indexes, document tracking, sections, or composition.

## Core Rules

- Every `StructuredNLDoc` field must use `Field(description="...")` with a non-empty description.
- The Markdown document is the source surface; the SLDB store indexes, queries, writes, and safely rewrites it through the model contract.
- Fields are first-class through SLDB model payloads, templates, sections, store queries, and field mutation commands.
- Do not create desk-local field instance documents to make fields reusable, queryable, writable, or editable. Use `sldb docs`, `sldb fields`, `sldb sections`, `sldb ast`, and tracked document payloads instead.
- If an SLDB write/edit/query path does not work, add the issue to the `sldb` repo's inbox instead of bypassing SLDB silently.
- For every `StructuredNLDoc` workflow, run `sldb validate` before finishing.

## Useful Commands

- `sldb extract <model-ref> <input-markdown> <output-json-or-yaml>`
- `sldb render <model-ref> <input-data> <output-markdown>`
- `sldb validate <model-ref> --input <markdown>`
- `sldb validate <model-ref> --data <json-or-yaml>`
- `sldb stores init --path .`
- `sldb stores check --store .sldb`
- `sldb stores update --store .sldb --pythonpath .`
- `sldb models add <model-ref> --store .sldb --pythonpath .`
- `sldb models show <ModelName> --store .sldb --pythonpath .`
- `sldb models template edit <ModelName> --input <template.md> --store .sldb --pythonpath .`
- `sldb models fields add <ModelName> <field> --type <type> --description <text> --store .sldb --pythonpath .`
- `sldb models fields remove <ModelName> <field> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --store .sldb --pythonpath .`
- `sldb models validate <ModelName> --promote --store .sldb --pythonpath .`
- `sldb docs create --model <ModelName> -o <path> <payload> --store .sldb --pythonpath .`
- `sldb docs track <path> --model <ModelName> --store .sldb --pythonpath .`
- `sldb docs update <doc> <payload> --store .sldb --pythonpath .`
- `sldb docs recover <doc> --store .sldb --pythonpath .`
- `sldb docs compose <doc> --store .sldb --pythonpath .`
- `sldb fields query <field> --store .sldb --pythonpath .`
- `sldb fields show docs/<doc>/<field> --store .sldb --pythonpath .`
- `sldb fields create docs/<doc>/<field> <value> --store .sldb --pythonpath .`
- `sldb fields update docs/<doc>/<field> <value> --store .sldb --pythonpath .`
- `sldb fields append docs/<doc>/<field> <value> --store .sldb --pythonpath .`
- `sldb fields remove docs/<doc>/<field> --store .sldb --pythonpath .`
- `sldb fields clean docs/<doc>/<field> --dedupe --drop-empty --store .sldb --pythonpath .`
- `sldb sections fields docs/<doc>/<section> --store .sldb --pythonpath .`
- `sldb ast show docs/<doc> --store .sldb --pythonpath .`
- `sldb find <term> --in physical --store .sldb --pythonpath .`
- `sldb find <term> --in semantic --store .sldb --pythonpath .`
- `sldb find <term> --in both --store .sldb --pythonpath .`
- `sldb find <term> --in semantic --global --store .sldb --pythonpath .`

## Model Editing Workflow

Use SLDB model commands when changing a `StructuredNLDoc` contract.

- Register models with `sldb models add` before relying on store-backed operations.
- Inspect contracts with `sldb models show` and `sldb ast show models/<ModelName>`.
- Edit templates with `sldb models template edit`, which writes a draft instead of replacing the active contract immediately.
- Add or remove fields with `sldb models fields add` and `sldb models fields remove`.
- Validate draft model changes with `sldb models validate`.
- Promote only after validation passes with `sldb models validate --promote`.
- Run `sldb stores update` after accepted model/doc changes so semantic, section, and field indexes match the current files.

Do not manually rewrite a model contract and call it done if the same change should be represented through SLDB's draft/validate/promote workflow. If the workflow cannot express the needed change, record that gap in the sibling `sldb` repo's inbox.

## Search Modes

SLDB has two primary search modes.

Use physical search when looking for literal or structural names:

- file paths
- tracked document names
- model names
- section titles and slugs
- field paths such as `title`, `goal`, or `tags`

Example:

- `sldb find desk/atoms --in physical --store .sldb --pythonpath .`
- `sldb find title --in physical --store .sldb --pythonpath .`

Use semantic search when looking for meaning encoded by model semantics, document tags, section context, or semantic indexes:

- `type.knowledge.atom`
- `system:deskops`
- `topic:atoms`
- section about terms

Example:

- `sldb find topic:atoms --in semantic --store .sldb --pythonpath .`
- `sldb find type.knowledge.atom --in semantic --store .sldb --pythonpath .`

Use `--in both` when unsure. Use `--global` when the local store should include linked/federated stores.

## Semantic Store

The `.sldb/` store is not the document source. It is the indexed semantic/query/edit layer over tracked Markdown documents.

It tracks:

- registered model contracts
- tracked document paths and logical names
- extracted field payloads
- semantic tags and model semantics
- section ownership and section context
- integrity hashes for model and document drift
- linked stores for global/federated discovery

Use `sldb stores check` to inspect integrity. Use `sldb stores update` after bulk edits, model changes, document moves, or when search results look stale.

Use semantic search and field queries through the store before inventing deskops-specific query surfaces.

## Boundary With Deskops

`sldb` owns reusable structured-document infrastructure: model contracts, reversible templates, document creation, document updates, field extraction, field mutation, section ownership, store tracking, integrity hashes, recovery, and composition primitives.

`deskops` owns workflow-domain surfaces: tasks, boards, rituals, pills, atoms, routines, hooks, inbox, drawer triage, and operational gates.

If the work is about reading, rendering, validating, creating, tracking, updating, querying, composing, or mutating fields in a structured Markdown document, use SLDB. If the work is about deciding what operational workflow should happen next, use deskops.

If an expected SLDB operation fails or is missing, record it in the sibling `sldb` repo's inbox with the failing command, expected behavior, actual behavior, and any relevant file/model references. Do not build a duplicate deskops-specific workaround before the SLDB gap is captured.

## Python Marker Modes

- Safe mode is the default; `py` markers stay literal and are not evaluated.
- Unsafe mode enables `py` marker evaluation for trusted templates only.
