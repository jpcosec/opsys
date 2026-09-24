---
# pill-xxx
id: pill-008
# e.g., language:python, library:pydantic
tags:
- system:deskops
- system:sldb
- system:kgdb
- pill-type:decision
- topic:knowledge-graph
---

# Decision: keep KGDB parallel to SLDB

## What

_Define the context or guardrail this pill carries._

Deskops graph work must use KGDB as graph persistence and traversal while preserving SLDB as the owner of modeled Markdown and semantic document truth.

## Why

_Explain why this context matters for safe execution._

If KGDB starts recreating SLDB semantics, the ecosystem gains two competing sources of truth for document meaning. If deskops bypasses KGDB, graph traversal becomes another workflow-local implementation.

## When

_Describe when an agent should apply this pill._

Apply this pill to every task that emits, imports, queries, or documents graph data involving SLDB documents or semantic tags.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/tasks/*graph*.md`, future graph adapter modules, SLDB semantic export payloads, and KGDB ingest/query integration.

## How

_Describe the correct way to apply this guidance._

Treat SLDB semantic tags, indexes, DAG nodes, sections, and document payloads as graph inputs. Treat KGDB graph snapshots and NetworkX traversal as graph runtime. Keep workflow-specific relation extraction in deskops.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not add SLDB document parsing or semantic tag derivation to KGDB. Do not make deskops own general graph persistence. Do not treat OWL or ontology reasoning as the first runtime dependency.
