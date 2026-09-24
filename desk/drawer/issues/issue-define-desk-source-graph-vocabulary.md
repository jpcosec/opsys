# Define desk source graph vocabulary

## Kind

feature

## Status

open

## Problem

The graph needs a typed vocabulary for desk artifacts and source files before KGDB can be used safely. Without a small controlled vocabulary, graph edges become inconsistent prose labels.

## Desired Outcome

Define the first node kinds, edge roles, identifier formats, and provenance metadata for the desk/source knowledge graph.

## Candidate Node Kinds

- atom
- task
- issue
- doc
- diagram
- spec
- primitive
- sldb_model
- cli_command
- source_file
- test_file
- config_file

## Candidate Edge Roles

- materializes
- references
- validates
- implements
- invokes
- defines
- routes
- configures
- tests
- generated_from
- source_for
- violates

## Questions

- Which names must match KGDB contracts exactly?
- Which relation roles overlap with existing atom reference roles?
- Should ontology/OWL mapping be stored now as metadata, or deferred until after the property graph is useful?

## Related Atoms

- atom-knowledge-graph-connects-desk-and-source-files
- atom-atom-references-carry-roles
- atom-extensibility-is-a-contract

---

## Merged item: `integrate-kgdb-for-desk-source-knowledge-graph`

#### Kind

feature

#### Status

open

#### Problem

Deskops knowledge relations currently live as prose, atom references, diagram edges, and scattered file paths. There is no generated graph that connects desk artifacts to source files and lets users query neighborhoods such as "which source files implement this atom?" or "which tasks touched this CLI command?".

#### Desired Outcome

Build a deskops adapter that emits a KGDB `GraphSnapshot` from desk docs, specs, diagrams, tests, models, CLI modules, primitives, and source files, then uses KGDB/NetworkX for traversal and query.

#### Initial Scope

- Nodes: atoms, tasks, issues, docs, diagrams, specs, primitives, models, CLI commands, source files, tests.
- Edges: materializes, references, validates, implements, invokes, defines, routes, configures, tests, generated_from, source_for.
- Output: `.sldb/runtime/knowledge_graph.kg.json` or equivalent generated runtime file.
- CLI: `deskops graph build`, `deskops graph neighbors <id>`, `deskops graph trace <id>`, `deskops graph missing`.

#### Questions

- Should graph build output live under `.sldb/runtime`, `.kgdb/`, or a deskops runtime directory?
- Should source-file nodes come from static file scanning, SLDB tracked docs, git history, or all three?
- Which relations are authoritative versus inferred heuristically?
- Should deskops depend directly on `kgdb`, or shell out to the `kgdb` CLI?

#### Related Atoms

- atom-knowledge-graph-connects-desk-and-source-files
- atom-kgdb-is-graph-substrate-not-reasoner
- atom-networkx-is-first-graph-runtime
- atom-source-file-relations-make-knowledge-actionable
