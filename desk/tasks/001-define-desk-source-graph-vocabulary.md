# Define desk source graph vocabulary

ID: task-001-define-desk-source-graph-vocabulary

## Goal

Define the deskops-specific node kinds, edge roles, identifier formats, and provenance fields needed to connect desk artifacts with source files through KGDB.

## Scope

- Atoms, tasks, issues, docs, diagrams, specs, primitives, models, CLI commands, source files, tests, and config files.
- Relations such as materializes, references, validates, implements, invokes, defines, routes, configures, tests, generated_from, source_for, and violates.

## Output

- Create `docs/knowledge-graph/desk-source-graph-vocabulary.md`.
- Include node kinds, edge role families, relation direction policy, confidence/provenance policy, and explicit non-goals.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`

## Done When

- A small vocabulary spec exists.
- It is aligned with KGDB's extensibility decision.
- It references existing atom relation vocabulary instead of creating a conflicting one.

## Validation

- Review against `desk/drawer/issues/issue-define-desk-source-graph-vocabulary.md`.
- Run a cold ambiguity review before implementation.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:knowledge-graph
