RESTATEMENT:

1. Read the sldb edge-index API from dependency `task-rw-f4-request-sldb-unresolved-references` (entry point and return shape for declared-field edges and for unresolved-reference reports).
2. Before any edit, capture the baseline: `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`.
3. In `deskops/graph/extract_docs.py:59-115,183-193` change node-id construction: frontmatter-`id` kinds (atom, task, pill, board, rest) → `<kind>:<frontmatter id>`; `drawer_task:<path>` → `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) → `<kind>:<path>`; file nodes keep `source_file:<path>`/`test_file:<path>` (`extract_sources.py:108-112`). No aliases for old ids.
4. In `deskops/graph/extract_edges.py` remove the regex frontmatter reference-field parsing and source declared-field edges from sldb; keep local: `_diagram_source_declarations`, `_section_declarations`, `_atom_declarations` (`extract_edges.py:244`), the per-line path scanner, and `_declarations_from_mapping` for models without `__references__`/`__containment__` (MaterializationContractDoc `source_atoms`, `target_identity`; pinned by `tests/test_materialization_contract.py:163`).
5. Convert each sldb edge to role = its `field` metadata so roles stay the declaring field names (`depends_on`, `pills`, ...; pinned by `tests/test_graph_declared_edges.py:78-92`).
6. Update `deskops/graph/snapshot.py` and the closeout graph context in `deskops/services/closeout_gates.py` for the new edge source and ids.
7. Update hard-coded old ids: `deskops/graph/self_reflection.py:164,173,450`; `deskops/operations.py:1728,2287` (or moved copies); `deskops/cli/parser.py:323`; `tests/fixtures/knowledge_graph/static_desk_source_graph.json`; `tests/test_graph_extract_docs.py:48-53`.
8. Update `tests/fixtures/golden/graph_snapshot.kg.json` and the graph tests for the id change only; any other diff is a regression to fix.
9. Write the old→new id table to `runs/planning/graph-id-mapping.md`.
10. Make `graph missing` use sldb's unresolved-reference report; verify its dangling set equals the baseline after id mapping — equal sets of `(kind, mapped source id, mapped target id)`, order ignored.
11. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`; run `deskops graph missing --root .`; run `pytest tests`.
12. Do not commit; hand the diff to the supervisor for review/closeout.

AMBIGUITIES:

1. The sldb edge-index API is not in this document (only "per the API agreed in task-rw-f4-request-sldb-unresolved-references"): no module path, function signature, or edge record shape — cannot write the call.
2. Metadata key name for the edge field is asserted as "its `field`" but not shown; the exact sldb metadata schema is unknown.
3. Which models declare `__references__`/`__containment__` (the set to route through sldb vs. `_declarations_from_mapping`) is not enumerated.
4. Whether sldb emits edges/nodes for drawer tasks, and how a drawer task is resolved to `task:<frontmatter id>`, is unspecified.
5. Contradiction: implementation step 1 calls `runs/planning/graph-missing-baseline.txt` "a committed artifact", while Resolved Decisions says the executor does not commit.
6. Comparison mechanics are unspecified: baseline is produced with old ids but the check compares "mapped" ids; the mapping direction and whether unmatched ids are errors is not stated.
7. `runs/planning/graph-id-mapping.md` has no format/ordering/column spec ("old->new id table" only).
8. `tests/test_materialization_contract.py` is named as a pin but is not in the `files:` list or Scope's update list; unclear if it may be edited.
9. `deskops/operations.py:1728,2287` "(or their moved copies)" — no way to know whether those files/lines still exist or where moved.
10. Acceptance is under-specified for deletion: Done When says extract_edges.py "no longer parses frontmatter reference fields", but it does not say whether the old parsing code is deleted, dead-but-present, or retained for the no-`__references__` models.
11. `graph missing` output contract (CLI exit code, printed format) is not specified; validation only runs the command.
12. Golden-snapshot determinism (node/edge ordering, serialization) is not specified, so "id change only" diffs are not machine-checkable as stated.
13. Task `status: deferred` and it has five unclosed `depends_on` tasks; nothing states whether it is dispatchable now or whether dependencies must close first.
14. `runs/planning/deskops-rewrite-inventory.md` is cited as the plan but is not provided, so the phase-F4 context cannot be verified.
