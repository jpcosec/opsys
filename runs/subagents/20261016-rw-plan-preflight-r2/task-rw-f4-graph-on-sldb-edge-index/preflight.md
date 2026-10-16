RESTATEMENT:
1. Verify the three `depends_on` tasks are closed and their outputs (sldb edge-index API, atoms service, archived-record filtering in `graph missing`) exist in the tree; load pills 008, 009, 010.
2. Run `deskops graph missing --root .` and save the pre-change output to `runs/planning/graph-missing-baseline.txt`.
3. Enumerate current node ids (`task:`, `atom:`, `pill:`, `doc:`, `board:`, `drawer_task:<path>` in `deskops/graph/extract_docs.py:59-115`; `source_file:`/`test_file:` in `extract_sources.py:108-112`) and build an old→new id mapping table.
4. In `deskops/graph/extract_docs.py`: replace id construction with one `<kind>:<id>` scheme; fold `drawer_task` into `task`; keep file nodes as `source_file:<path>`/`test_file:<path>`.
5. In `deskops/graph/extract_edges.py`: delete the regex frontmatter/field-reference parsing; obtain declared-field edges from sldb's public edge-index API (per `task-rw-f4-request-sldb-unresolved-references`); keep local `_diagram_source_declarations`, `_section_declarations`, and the per-line path scanner.
6. Rewire `graph missing` to sldb's unresolved-reference report; adapt `deskops/graph/snapshot.py` and the closeout graph context in `deskops/services/closeout_gates.py` to the new ids/edge source.
7. Update `tests/test_graph_extract_edges.py`, `tests/test_graph_declared_edges.py`, `tests/test_graph_cli.py`, and `tests/fixtures/golden/graph_snapshot.kg.json` for id changes only.
8. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, then `deskops graph missing --root .`, then `pytest tests`.
9. Compare the post-change dangling-reference set to the baseline after applying the id mapping; require equality.
10. Do not commit; leave the diff and record the id mapping in the closeout for supervisor review.

AMBIGUITIES:
1. All three `depends_on` tasks are unverified here; no info on whether their APIs/behaviors exist.
2. The sldb "public edge index" API is not named — module, function, signature, and return shape unknown.
3. sldb's "unresolved-reference report" entry point and output format unknown.
4. `<id>` for each kind is undefined (filename stem vs frontmatter `id` vs path).
5. `drawer_task:<path>` → `task:<id>`: post-promotion id collision/identity semantics with active `task:` ids not specified.
6. Baseline comparison method is unspecified (manual diff vs scripted), and the baseline has old ids while output has new ids.
7. `tests/fixtures/golden/graph_snapshot.kg.json` is required by Implementation Path but missing from `files:`.
8. `extract_sources.py` is referenced for `source_file:`/`test_file:` but absent from `files:`.
9. "the per-line path scanner" is not identified by file/function name.
10. Where "list every id mapping in the closeout" must be written (task doc vs run-dir artifact) is unspecified.
11. No check covers node-id consumers outside the listed graph files, so id renaming could break unlisted code undetected.
12. "Compared after mapping" lacks a definition of done for ordering/duplicates/counts, only set equality.
13. The doc claims Open Ambiguities: None, contradicting items 1-12.
