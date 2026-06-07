# Model: source files are graph nodes

ID: pill-009

## What

The deskops knowledge graph must include source files as first-class nodes connected to desk artifacts by explicit roles.

## Why

A graph that only connects desk documents explains knowledge organization but not implementation accountability. Source-file edges make it possible to ask what implements, validates, exposes, configures, or violates an atom or task.

## When

Apply this pill to graph vocabulary, extraction, adapter, CLI, and self-reflection tasks.

## Where

Applies to code under `deskops/`, `desk/`, `docs/`, `spec/`, and `tests/` when those files are represented as graph nodes or edge targets.

## How

Use stable path-based identifiers for source-file nodes first. Add symbol-level nodes only after file-level extraction is validated. Attach provenance metadata to inferred edges.

## How Not

Do not start with symbol-level static analysis unless the task explicitly requires it. Do not infer high-confidence implementation edges from filename similarity alone.

## Tags

- system:deskops
- system:kgdb
- topic:source-code
- topic:traceability
