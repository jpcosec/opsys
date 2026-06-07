# Integrate KGDB for desk source knowledge graph

## Kind

feature

## Status

open

## Problem

Deskops knowledge relations currently live as prose, atom references, diagram edges, and scattered file paths. There is no generated graph that connects desk artifacts to source files and lets users query neighborhoods such as "which source files implement this atom?" or "which tasks touched this CLI command?".

## Desired Outcome

Build a deskops adapter that emits a KGDB `GraphSnapshot` from desk docs, specs, diagrams, tests, models, CLI modules, primitives, and source files, then uses KGDB/NetworkX for traversal and query.

## Initial Scope

- Nodes: atoms, tasks, issues, docs, diagrams, specs, primitives, models, CLI commands, source files, tests.
- Edges: materializes, references, validates, implements, invokes, defines, routes, configures, tests, generated_from, source_for.
- Output: `.sldb/runtime/knowledge_graph.kg.json` or equivalent generated runtime file.
- CLI: `deskops graph build`, `deskops graph neighbors <id>`, `deskops graph trace <id>`, `deskops graph missing`.

## Questions

- Should graph build output live under `.sldb/runtime`, `.kgdb/`, or a deskops runtime directory?
- Should source-file nodes come from static file scanning, SLDB tracked docs, git history, or all three?
- Which relations are authoritative versus inferred heuristically?
- Should deskops depend directly on `kgdb`, or shell out to the `kgdb` CLI?

## Related Atoms

- atom-knowledge-graph-connects-desk-and-source-files
- atom-kgdb-is-graph-substrate-not-reasoner
- atom-networkx-is-first-graph-runtime
- atom-source-file-relations-make-knowledge-actionable
