RESTATEMENT
1. Read `task-rw-f4-request-sldb-unresolved-references` to obtain the agreed sldb edge-index and unresolved-reference API (names, signatures, return shapes); confirm deps f0/f1/f3 and that API actually exists.
2. Before edits, run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`.
3. Inspect current behavior/schemes in `deskops/graph/extract_edges.py`, `extract_docs.py:59-115,183-193`, `extract_sources.py:108-112`.
4. Replace frontmatter/declared-field edge parsing in `extract_edges.py` with sldb public edge-index calls; preserve local-only edges: `_diagram_source_declarations`, `_section_declarations`, `_atom_declarations` (extract_edges.py:244), per-line path scanner. Leave coverage extractor untouched.
5. Change node ids in `extract_docs.py`: frontmatter-id kinds keep `<kind>:<frontmatter id>`; `drawer_task:<path>` -> `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) keep `<kind>:<path>`; file nodes keep `source_file:<path>`/`test_file:<path>`; no old-id aliases.
6. Update `deskops/graph/snapshot.py` and the closeout graph context in `deskops/services/closeout_gates.py` for the new ids.
7. Update other old-id hard-codes: `deskops/graph/self_reflection.py:164,173,450`, `deskops/operations.py:1728,2287` (or moved copies), `deskops/cli/parser.py:323`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, `tests/test_graph_extract_docs.py:48-53`.
8. Make `graph missing` use sldb's unresolved-reference report (still surfacing local-edge dangling refs).
9. Update `tests/fixtures/golden/graph_snapshot.kg.json` and graph tests (`test_graph_cli.py`, `test_graph_declared_edges.py`, `test_graph_extract_edges.py`) for the id change only; write old->new table to `runs/planning/graph-id-mapping.md`.
10. Compare dangling-ref sets as `(kind, mapped source id, mapped target id)` tuples, ignoring order, against baseline.
11. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, `deskops graph missing --root .`, `pytest tests`.
12. Confirm `extract_edges.py` no longer parses frontmatter reference fields; leave all commits to supervisor.

AMBIGUITIES
1. The sldb edge-index/unresolved-reference API is not in this document; only "per the API agreed in task-rw-f4-request-sldb-unresolved-references". No names, signatures, or return shapes.
2. Dependency state unknown: status is `deferred` and depends_on tasks (f0/f1/f3/f4-request-sldb) completion is not stated, so readiness cannot be confirmed.
3. Which exact frontmatter fields count as "declared edges" is never enumerated.
4. Edge `kind` values/labels produced by sldb vs local extractor are undefined; the comparison tuple includes `kind` with no mapping rule.
5. No method specified for mapping baseline (pre-change) source/target ids to new ids — especially `drawer_task:<path>` -> `task:<frontmatter id>`, which needs path->frontmatter-id resolution not present in the baseline text file.
6. No mechanism specified to execute the baseline set comparison (test, script, or manual).
7. Contradiction: "graph missing uses sldb's unresolved-reference report" vs "keep local edges" (diagram/section/YAML/per-line) — unclear whether `graph missing` merges sldb report + local dangling detection or fully replaces local.
8. `snapshot.py` and `closeout_gates.py` are "in scope" with no described change.
9. "Update tests for the id change only" conflicts with switching extraction source (regex -> sldb), which can change edges beyond ids; whether golden files may change for non-id differences is unspecified.
10. Line-number references (`extract_docs.py:59-115,183-193`, `operations.py:1728,2287`, `self_reflection.py:164,173,450`, `parser.py:323`, `extract_edges.py:244`) may be stale; "or their moved copies" leaves file locations undetermined.
11. Path-keyed ids `<kind>:<path>` — path base (repo root vs desk root) and normalization unspecified.
12. No test named for the Done-When claim "extract_edges.py no longer parses frontmatter reference fields"; enforcement method unspecified.
13. Collision behavior when `drawer_task:<path>` becomes `task:<frontmatter id>` and collides with an existing `task:<id>`, given "old ids get no alias", is unaddressed.
14. Ordering/determinism of sldb-returned edges for the golden fixture is unstated.
15. Contradiction: step 1 requires a "committed artifact" baseline, while Resolved Decisions says the executor does not commit.
16. `runs/planning/graph-id-mapping.md` format is unspecified.
17. No test-double/fixture strategy given for sldb edge index, so unit-testability without live sldb is undefined.
18. Rationale references `runs/planning/deskops-rewrite-inventory.md`, not in the files list; whether it must be read/updated is unclear.
