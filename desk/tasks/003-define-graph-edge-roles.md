# Define graph edge roles

ID: task-003-define-graph-edge-roles

## Goal

Define the first allowed deskops graph edge roles and their direction before any extractor emits graph data.

## Scope

- Roles for document materialization, atom references, source implementation, validation, CLI invocation, generated projections, routing, and violations.
- Direction, required metadata, and confidence/provenance expectations for each role.

## Output

- Create or update `docs/knowledge-graph/desk-source-graph-vocabulary.md` with an `Edge Roles` section.
- Add examples for declared roles and inferred roles, and mark which are allowed in the first extractor.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`

## Done When

- A role vocabulary exists and does not conflict with atom reference roles.
- Each role has an example source and target node kind.
- Low-confidence inferred roles are distinguished from declared roles.

## Validation

- Review against `desk/drawer/issues/issue-formalize-atom-reference-role-vocabulary.md`.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:knowledge-graph
