RESTATEMENT:

1. Confirm prerequisites: the four `depends_on` tasks (`task-rw-f4-request-sldb-unresolved-references`, `task-rw-f3-atoms-service`, `task-rw-f0-graph-missing-ignores-archived-records`, `task-rw-f1-output-golden-files`) are closed, and the task is active in `desk/tasks/` (promotion done by supervisor).
2. Read pills `desk/contexts/pill-008-kgdb-sldb-boundary.md`, `pill-009-source-file-graph-traceability.md`, `pill-010-graph-runtime-output-policy.md`.
3. Read `deskops/graph/extract_edges.py`, `extract_docs.py` (lines 59–115), `extract_sources.py` (108–112), `snapshot.py`, `deskops/services/closeout_gates.py` graph context.
4. Capture baseline before any edit: `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`.
5. In `extract_edges.py`: delete the regex frontmatter declared-field edge parsing; source those edges from sldb's public edge index (API from `task-rw-f4-request-sldb-unresolved-references`). Keep local edges: `_diagram_source_declarations`, `_section_declarations`, per-line path scanner.
6. In `extract_docs.py`: replace the multiple id schemes with a single `<kind>:<id>` scheme; fold `drawer_task:<path>` into `task`; leave `source_file:<path>`/`test_file:<path>` in `extract_sources.py` unchanged.
7. Update `snapshot.py` node/edge assembly for the renamed ids.
8. Update the graph context in `deskops/services/closeout_gates.py` for the new ids.
9. Change `graph missing` to use sldb's unresolved-reference report.
10. Update `tests/fixtures/golden/graph_snapshot.kg.json`, `tests/test_graph_cli.py`, `tests/test_graph_declared_edges.py`, `tests/test_graph_extract_edges.py` for the id change only.
11. Verify baseline parity: run `deskops graph missing --root .`, map old ids to new, diff against `runs/planning/graph-missing-baseline.txt`, require identical dangling-reference set.
12. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, then `pytest tests`.
13. Record the full old→new id mapping in the closeout; do not commit (supervisor commits via `deskops closeout commit`).

AMBIGUITIES:

1. Task `status: deferred` and `source: drawer` contradict the Resolved Decision that it is promoted to `desk/tasks/` and dispatched; no instruction on who flips status or where the doc file currently lives.
2. The sldb public edge index API is not given here and `task-rw-f4-request-sldb-unresolved-references` is unreadable from this task document: no module, function, CLI, or return shape to call.
3. The exact node-id mapping is unspecified: what `<id>` is for atoms, pills, docs, board, and drawer tasks (filename vs frontmatter id), and whether `drawer_task:<path>` becomes `task:<path>` or `task:<task-id>`.
4. Whether other consumers of the old id prefixes (queries, kgdb graph validation, docs, other deskops services) must be updated is not stated; scope lists only five files.
5. "Compared after mapping old ids to new ones" has no concrete procedure or mapping table; ordering/format tolerance of the `graph missing` output for the comparison is undefined.
6. Whether `runs/planning/graph-missing-baseline.txt` is a committed artifact that must be regenerated in this diff, or only a scratch comparison, is unclear.
7. Boundary between "edges declared by model fields" (sldb-provided) and `_section_declarations` (local) is not defined; section-declared atom refs may also be model-field derived.
8. The "coverage extractor" declared out of scope is not identified by file or function.
9. Golden fixture update method is unspecified (regenerate via CLI vs hand-edit) and no golden-update command is named.
10. "List every id mapping in the closeout" does not say whether that goes in the commit message, the task doc, or a run-dir artifact.
11. No requirement stated on backwards compatibility/aliasing of old ids after the rename, so behavior for existing consumers is undefined.
12. Dependency closure is asserted only in `depends_on`; no instruction verifies those tasks are complete before this work starts.
