RESTATEMENT:
1. Verify the four `depends_on` tasks are closed: `task-rw-f4-request-sldb-unresolved-references`, `task-rw-f3-atoms-service`, `task-rw-f0-graph-missing-ignores-archived-records`, `task-rw-f1-output-golden-files`.
2. Before any edits, run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`.
3. Read `deskops/graph/extract_edges.py`, `extract_docs.py`, `snapshot.py`, `deskops/services/closeout_gates.py`, `deskops/graph/self_reflection.py`, `deskops/cli/parser.py`, `deskops/operations.py`, and the listed tests/fixtures.
4. Replace declared-field (frontmatter reference field) edge extraction in `extract_edges.py` with calls to sldb's public edge index, using the API shape defined by `task-rw-f4-request-sldb-unresolved-references`.
5. Keep as local extraction: diagram `source:` edges (`_diagram_source_declarations`), section-declared atom refs (`_section_declarations`), and the per-line path scanner. Leave the coverage extractor untouched.
6. Change document node ids in `extract_docs.py`: frontmatter-`id`-keyed kinds → `<kind>:<frontmatter id>`; `drawer_task:<path>` → `task:<frontmatter id>`; path-keyed kinds (doc, spec, diagram) → `<kind>:<path>`. No aliases for old ids. Keep `source_file:<path>` and `test_file:<path>` for file nodes.
7. Route `graph missing` through sldb's unresolved-reference report.
8. Update hard-coded old ids at `deskops/graph/self_reflection.py:164,173,450`, `deskops/operations.py:1728,2287` (or moved copies), `deskops/cli/parser.py:323`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, `tests/test_graph_extract_docs.py:48-53`, and the closeout graph context in `deskops/services/closeout_gates.py`.
9. Update `tests/fixtures/golden/graph_snapshot.kg.json` and the graph tests only for the id change.
10. Write the old→new id table to `runs/planning/graph-id-mapping.md`.
11. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`.
12. Run `deskops graph missing --root .` and compare to baseline as sets of `(kind, mapped source id, mapped target id)` tuples, ignoring order.
13. Run `pytest tests`.
14. Confirm `extract_edges.py` no longer parses frontmatter reference fields, dangling set matches baseline modulo mapping, and `pytest tests` is green.
15. Do not commit; supervisor reviews diff and makes the closeout commit.

AMBIGUITIES:
1. The sldb public edge-index API is not given; it lives in `task-rw-f4-request-sldb-unresolved-references`, which is not provided.
2. The full list of frontmatter-`id`-keyed kinds is only referenced as "the rest in deskops/graph/extract_docs.py:183-193"; the file is not provided, so the kind set is unknown.
3. Contradiction: Implementation Path step 1 says the baseline is "a committed artifact", but Resolved Decisions says the executor does not commit.
4. Whether `depends_on` tasks must be closed before execution, and how to verify closure, is not stated; task status is `deferred`.
5. `deskops/operations.py:1728,2287` is cited with "or their moved copies", but `deskops/operations.py` is not in the `files` list and no move target is named.
6. The "closeout graph context" in `closeout_gates.py` is not identified by function or line.
7. Expected new content of `tests/fixtures/golden/graph_snapshot.kg.json` and of the id-only test updates is not derivable from the document.
8. `runs/planning/graph-id-mapping.md` format/content beyond "old->new id table" is unspecified; whether it must cover every id appearing in the baseline is unstated.
9. Baseline comparison method is specified but the mapping table must cover baseline old ids; coverage requirement is not stated.
10. Fallback is unspecified when sldb cannot supply a declared edge and it is not one of the three named local edge types.
11. Exact-equality of the dangling set vs. a tolerance is not stated; the term "same set" is used without an explicit comparator beyond the tuple definition.
