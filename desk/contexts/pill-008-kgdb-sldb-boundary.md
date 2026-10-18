---
# pill-xxx
id: pill-008
# e.g., language:python, library:pydantic
tags:
- system:deskops
- system:sldb
- pill-type:decision
- topic:knowledge-graph
---

# Decision: sldb owns the graph layer

## What

_Define the context or guardrail this pill carries._

sldb owns graph persistence, traversal, and the graph contracts. deskops builds its workflow-specific snapshot and validates and writes it through the sldb graph API (`sldb.api.graph`, `sldb.store.graph.graph_io`); there is no separate kgdb dependency.

## Why

_Explain why this context matters for safe execution._

If deskops reimplemented graph contracts or persisted graphs on its own, the ecosystem would gain a competing graph runtime and two sources of truth for graph semantics. sldb already owns document semantics and the graph layer, so duplicating either boundary splits ownership.

## When

_Describe when an agent should apply this pill._

Apply this pill to every task that emits, imports, queries, or documents graph data involving SLDB documents or semantic tags.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/tasks/*graph*.md`, deskops graph modules, SLDB semantic export payloads, and graph ingest/query integration.

## How

_Describe the correct way to apply this guidance._

Treat SLDB semantic tags, indexes, DAG nodes, sections, and document payloads as graph inputs. Validate snapshots with `sldb.api.graph.snapshot.GraphSnapshot` and load/save them with `sldb.api.graph.snapshot.snapshot_load` and `sldb.store.graph.graph_io.save_graph`. Keep workflow-specific relation extraction in deskops.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not add SLDB document parsing or semantic tag derivation to deskops. Do not reintroduce a kgdb dependency or a deskops-owned graph runtime. Do not treat OWL or ontology reasoning as the first runtime dependency.
