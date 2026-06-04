# Create static graph fixture

ID: task-004-create-static-graph-fixture

## Goal

Create one small hand-authored fixture that demonstrates the desk/source graph vocabulary before implementing extraction.

## Scope

- Include at least one atom, task, doc, source file, test file, and CLI command node.
- Include at least one materializes/references, implements, validates, and invokes edge.
- Keep the fixture small enough to review manually.

## Output

- Create `tests/fixtures/knowledge_graph/static_desk_source_graph.json`.
- Create `tests/fixtures/knowledge_graph/static_desk_source_graph.notes.md` if explanation is needed.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`

## Done When

- The fixture is versioned as a test/contract fixture, not as generated runtime output.
- KGDB can ingest it once the KGDB vocabulary task supports the needed terms, or the blocker is recorded.

## Validation

- Validate the fixture against the chosen KGDB graph shape.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:fixtures
