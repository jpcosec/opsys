# Extract declared graph edges

ID: task-007-extract-declared-graph-edges

## Goal

Extract graph edges that are explicitly declared in desk docs or metadata, without heuristic inference.

## Scope

- Source atoms lists.
- Related task/issue references.
- Diagram source references.
- Explicit source file references in task or issue text.
- Heuristic code ownership inference is out of scope.

## Output

- Add `deskops/graph/extract_edges.py` or equivalent focused module.
- Add `tests/test_graph_extract_edges.py`.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`

## Done When

- A unit test proves declared references become edges with provenance.
- Missing targets are reported rather than silently ignored.

## Validation

- Focused edge extractor test.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:traceability
