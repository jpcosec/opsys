---
# pill-xxx
id: pill-009
# e.g., language:python, library:pydantic
tags:
- system:deskops
- system:kgdb
- pill-type:model
- topic:source-code
- topic:traceability
---

# Model: source files are graph nodes

## What

_Define the context or guardrail this pill carries._

The deskops knowledge graph must include source files as first-class nodes connected to desk artifacts by explicit roles.

## Why

_Explain why this context matters for safe execution._

A graph that only connects desk documents explains knowledge organization but not implementation accountability. Source-file edges make it possible to ask what implements, validates, exposes, configures, or violates an atom or task.

## When

_Describe when an agent should apply this pill._

Apply this pill to graph vocabulary, extraction, adapter, CLI, and self-reflection tasks.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to code under `deskops/`, `desk/`, `docs/`, `spec/`, and `tests/` when those files are represented as graph nodes or edge targets.

## How

_Describe the correct way to apply this guidance._

Use stable path-based identifiers for source-file nodes first. Add symbol-level nodes only after file-level extraction is validated. Attach provenance metadata to inferred edges.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not start with symbol-level static analysis unless the task explicitly requires it. Do not infer high-confidence implementation edges from filename similarity alone.
