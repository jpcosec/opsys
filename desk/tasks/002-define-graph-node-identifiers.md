# Define graph node identifiers

ID: task-002-define-graph-node-identifiers

## Goal

Define stable identifier formats for deskops graph nodes before any extractor emits graph data.

## Scope

- Atoms, tasks, issues, docs, diagrams, specs, primitives, SLDB models, CLI commands, source files, tests, and config files.
- File-level identifiers only; symbol-level identifiers are explicitly out of scope for this task.

## Output

- Create or update `docs/knowledge-graph/desk-source-graph-vocabulary.md` with a `Node Identifiers` section.
- Add examples for `atom:`, `task:`, `issue:`, `doc:`, `diagram:`, `spec:`, `primitive:`, `sldb_model:`, `cli_command:`, `source_file:`, `test_file:`, and `config_file:` identifiers.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`

## Done When

- A small identifier spec exists.
- The spec states how ids remain stable across file moves or when they intentionally change.
- Source-file ids are path-based with project-root-relative provenance.

## Validation

- Add or update a fixture/example showing ids for at least one atom, task, source file, test file, and CLI command.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:knowledge-graph
