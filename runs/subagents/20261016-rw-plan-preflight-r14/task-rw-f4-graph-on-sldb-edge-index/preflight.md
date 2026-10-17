RESTATEMENT:

1. Read `AGENTS.md` startup route; read the task's bound pills `desk/contexts/pill-008-kgdb-sldb-boundary.md`, `pill-009-source-file-graph-traceability.md`, `pill-010-graph-runtime-output-policy.md`; read dependency doc `task-rw-f4-request-sldb-unresolved-references` for the agreed sldb edge-index API.
2. Before edits, run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt` and treat it as a committed artifact.
3. In `deskops/graph/extract_edges.py`, replace regex extraction of declared fields for store-tracked documents with edges read from sldb's public edge index; for each sldb edge set role = its metadata `field` (preserving roles like `depends_on`, `pills`).
4. Keep the local extractors for: diagram `source:` edges (`_diagram_source_declarations`), section-declared atom refs (`_section_declarations`), YAML-fenced atom declarations (`_atom_declarations`, extract_edges.py:244), the per-line path scanner, `_declarations_from_mapping` for models with no `__references__`/`__containment__` (MaterializationContractDoc `source_atoms`, `target_identity`), and frontmatter edges of untracked documents (drawer tasks, other untracked desk docs).
5. In `deskops/graph/extract_docs.py`, apply the id scheme: frontmatter-id kinds (atom, task, pill, board, rest at 183-193) → `<kind>:<frontmatter id>`; `drawer_task:<path>` → `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) → `<kind>:<path>`; `source_file:<path>`/`test_file:<path>` unchanged; emit no aliases for old ids.
6. Update hardcoded old ids: `deskops/graph/self_reflection.py:164,173,450`; `deskops/operations.py:1304,1863` (or moved copies); `deskops/cli/parser.py:323`; `tests/fixtures/knowledge_graph/static_desk_source_graph.json`; `tests/test_graph_extract_docs.py:48-53`; also `deskops/graph/snapshot.py` and the closeout graph context in `deskops/services/closeout_gates.py`.
7. Update `tests/fixtures/golden/graph_snapshot.kg.json` and the graph tests only for the id change; fix any other diff as a regression.
8. Write the old→new id table to `runs/planning/graph-id-mapping.md`.
9. Validate: `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`; `deskops graph missing --root .`; compare dangling-reference sets as (kind, mapped source id, mapped target id) tuples ignoring order against the baseline; then `pytest tests`.
10. Do not commit; hand the diff to the supervisor.

AMBIGUITIES:

1. The sldb public edge-index API is not specified here; `task-rw-f4-request-sldb-unresolved-references` is not provided (no module, function, store path, or return shape).
2. How `graph missing` obtains and formats sldb's unresolved-reference report is unspecified.
3. The "kind" component of the comparison tuple is undefined, and the baseline output format may not expose parseable (kind, source, target).
4. "Modulo the id mapping" is directionally unclear: baseline holds old ids, mapping is old→new, but old ids get no alias, so it is unspecified how mapping applies to baseline strings (especially path-shaped `drawer_task:<path>`).
5. Untracked, non-drawer desk documents are not assigned a kind or id for their locally-extracted frontmatter edges.
6. The required change to "the closeout graph context in `deskops/services/closeout_gates.py`" is not described.
7. "or their moved copies" of `deskops/operations.py:1304,1863` leaves the actual target location unknown.
8. Role mapping is undefined when an sldb edge has no `field` metadata, or for containment edges (field name vs `contains`).
9. "The per-line path scanner" and "the coverage extractor" are not identified by file or function.
10. No required format or content is given for `runs/planning/graph-id-mapping.md`.
11. No check is defined for "extract_edges.py no longer parses the declared reference fields of store-tracked documents" (e.g., no test asserting the regex path is gone).
12. Whether store-tracked MaterializationContractDocs' frontmatter edges could be emitted twice (local `_declarations_from_mapping` plus any sldb path) is unspecified.
