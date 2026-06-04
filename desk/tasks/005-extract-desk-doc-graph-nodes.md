# Extract desk doc graph nodes

ID: task-005-extract-desk-doc-graph-nodes

## Goal

Implement the first extractor for desk document nodes only.

## Scope

- Read atoms, task files, drawer issues, docs, diagram docs, and specs.
- Emit nodes only; edge extraction is out of scope.
- Preserve path, kind, title/id when available, and provenance metadata.

## Output

- Add `deskops/graph/__init__.py` if the package does not exist.
- Add `deskops/graph/extract_docs.py` or equivalent focused module.
- Add `tests/test_graph_extract_docs.py`.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-008-kgdb-sldb-boundary.md`

## Done When

- A unit test proves known desk files become graph nodes.
- The extractor does not parse source code or infer edges.

## Validation

- Focused extractor test.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:knowledge-graph
