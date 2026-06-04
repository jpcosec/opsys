# Extract source file graph nodes

ID: task-006-extract-source-file-graph-nodes

## Goal

Implement file-level source node extraction for selected source, test, config, and spec files.

## Scope

- File-level nodes only.
- Include project-root-relative path, file kind, and provenance metadata.
- Exclude generated/runtime files unless explicitly selected as fixtures.

## Output

- Add `deskops/graph/extract_sources.py` or equivalent focused module.
- Add `tests/test_graph_extract_sources.py`.

## Pills

- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`

## Done When

- A unit test proves representative source/test/config files become graph nodes.
- Generated graph/runtime files are excluded by default.

## Validation

- Focused extractor test.
- Atom tests still pass.

## Tags

- system:deskops
- system:kgdb
- topic:source-code
