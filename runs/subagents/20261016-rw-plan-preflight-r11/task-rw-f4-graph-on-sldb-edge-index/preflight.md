RESTATEMENT:
1. Read this task's dependencies' artifacts first: `task-rw-f4-request-sldb-unresolved-references` (defines the sldb edge-index/unresolved-reference API to call), `task-rw-f3-atoms-service`, `task-rw-f3-closeout-gates-service`, `task-rw-f0-graph-missing-ignores-archived-records`, `task-rw-f1-output-golden-files`; read pills `desk/contexts/pill-008-kgdb-sldb-boundary.md`, `pill-009-source-file-graph-traceability.md`, `pill-010-graph-runtime-output-policy.md`; read `desk/rituals/execution.md`, `testing.md`, `closeout.md`.
2. Run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt` before any edit; keep as committed artifact.
3. Read `deskops/graph/extract_edges.py` (`_diagram_source_declarations`, `_section_declarations`, `_atom_declarations` ~line 244, per-line path scanner, `_declarations_from_mapping`), `deskops/graph/extract_docs.py` (node-id construction ~59-115, kind table ~183-193), `deskops/graph/extract_sources.py` (~108-112), `deskops/graph/snapshot.py`, `deskops/services/closeout_gates.py`.
4. Replace declared-frontmatter-field edge extraction in `extract_edges.py` with calls to sldb's public edge index (API per dependent task); delete regex re-implementation of those fields.
5. Keep local edges unchanged: diagram `source:` (`_diagram_source_declarations`), section-declared atom refs (`_section_declarations`), YAML-fenced body atom declarations (`_atom_declarations`), per-line path scanner, and frontmatter fields of models lacking `__references__`/`__containment__` (MaterializationContractDoc `source_atoms`, `target_identity`).
6. Map each sldb edge to role = its `field` metadata (sldb emits `references`/`contains`), preserving existing roles (`depends_on`, `pills`, ...).
7. Renumber node ids: frontmatter-id kinds (atom, task, pill, board, rest of extract_docs.py:183-193) → `<kind>:<frontmatter id>`; `drawer_task:<path>` → `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) stay `<kind>:<path>`; file nodes stay `source_file:<path>`/`test_file:<path>`; no aliases.
8. Update hard-coded old ids: `deskops/graph/self_reflection.py:164,173,450`, `deskops/operations.py:1728,2287` (or moved copies), `deskops/cli/parser.py:323`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, `tests/test_graph_extract_docs.py:48-53`.
9. Make `graph missing` consume sldb's unresolved-reference report.
10. Update `tests/fixtures/golden/graph_snapshot.kg.json` and graph tests for the id change only; fix any other diff as regression; write old→new id table to `runs/planning/graph-id-mapping.md`.
11. Verify baseline equivalence: compare `(kind, mapped source id, mapped target id)` sets from `runs/planning/graph-missing-baseline.txt` vs new output, order-insensitive.
12. Validate: `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`; `deskops graph missing --root .`; `pytest tests`.
13. Confirm Done When: `extract_edges.py` no longer parses frontmatter reference fields, dangling set matches baseline modulo id mapping, `pytest tests` green. Do not commit; supervisor reviews diff and runs `deskops closeout commit`.

AMBIGUITIES:
1. The sldb edge-index and unresolved-reference APIs are defined only in `task-rw-f4-request-sldb-unresolved-references`, which is not provided; exact call names/signatures/return shapes are unknown.
2. Baseline must be "a committed artifact" but the executor does not commit; unclear who commits it and in what order relative to promotion.
3. `deskops/services/closeout_gates.py` is in scope but no required change is described.
4. Edge role mapping only covers `references`/`contains` with `field`; what role to use when sldb edge metadata has no `field` (or for `__containment__` fields) is unspecified.
5. Collision behavior when `drawer_task:<path>` maps to `task:<frontmatter id>` and that frontmatter id already exists as an active task is unspecified.
6. No independent check is defined to validate the old→new id mapping itself; comparing new output to a baseline mapped by the executor's own table can be vacuous.
7. "anything else that changes is a regression" gives no threshold for which diffs in `graph_snapshot.kg.json` are acceptable id-only changes.
8. Scope says the "graph tests listed below" may be updated (lists `tests/test_graph_extract_docs.py`), but Validation's pytest command omits that file; unclear whether it is required passing.
9. Exact format/schema of `runs/planning/graph-missing-baseline.txt` and of `graph-id-mapping.md` beyond "old->new id table" is unspecified.
10. Whether the full enumerated set of "kinds keyed by frontmatter id" and path-keyed kinds is exhaustive is not stated; unlisted kinds have no assigned scheme.
11. Task `status: deferred` with unresolved `depends_on` tasks; unclear whether execution may start before those dependencies are closed.
12. Comparison tuples use `(kind, source id, target id)` but "kind" is not defined for file nodes or for edges whose endpoints are not document nodes.
