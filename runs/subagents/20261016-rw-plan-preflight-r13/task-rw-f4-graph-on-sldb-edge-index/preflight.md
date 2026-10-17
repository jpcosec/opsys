RESTATEMENT:
1. Before any edits, generate and save `runs/planning/graph-missing-baseline.txt` via `deskops graph missing --root .`.
2. Read `task-rw-f4-request-sldb-unresolved-references` to get the agreed sldb public edge-index API and unresolved-reference report API.
3. Read `runs/planning/deskops-rewrite-inventory.md` and the referenced source lines (`extract_docs.py:59-115,183-193`, `extract_edges.py:244`, `extract_sources.py:108-112`).
4. In `deskops/graph/extract_edges.py`: replace frontmatter declared-field edge extraction with calls to the sldb edge index.
5. Keep local extraction for the explicit exceptions: `_diagram_source_declarations`, `_section_declarations`, `_atom_declarations`, the per-line path scanner, `_declarations_from_mapping` (MaterializationContractDoc `source_atoms`/`target_identity`), and frontmatter edges of untracked documents (drawer tasks etc.).
6. Map each sldb edge back to role = its `field` metadata so roles stay as today (`depends_on`, `pills`, ...).
7. In `deskops/graph/extract_docs.py`: change node ids to `<kind>:<id>`; id-keyed kinds keep `<kind>:<frontmatter id>`; `drawer_task:<path>` -> `task:<frontmatter id>`; keep `doc:<path>`, `spec:<path>`, `diagram:<path>`; keep `source_file:<path>`/`test_file:<path>`; no aliases for old ids.
8. Update id-dependent code: `deskops/graph/snapshot.py`, graph context in `deskops/services/closeout_gates.py`, `deskops/graph/self_reflection.py:164,173,450`, `deskops/operations.py:1304,1863` (or moved copies), `deskops/cli/parser.py:323`.
9. Update fixtures/tests for the id change only: `tests/fixtures/golden/graph_snapshot.kg.json`, `tests/test_graph_extract_docs.py:48-53`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, and the graph tests listed in `files`.
10. Make `graph missing` consume sldb's unresolved-reference report.
11. Write the old->new id table to `runs/planning/graph-id-mapping.md`.
12. Verify the new `graph missing` output equals the baseline as a set of `(kind, mapped source id, mapped target id)` tuples, ignoring order.
13. Run: `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, `deskops graph missing --root .`, `pytest tests`.

AMBIGUITIES:
1. The sldb public edge-index API (module, function, signature) is only referenced indirectly via `task-rw-f4-request-sldb-unresolved-references`, which is not provided.
2. The sldb unresolved-reference report API for `graph missing` is equally unspecified.
3. `deskops/operations.py:1304,1863 (or their moved copies)` — location/existence of moved copies unknown.
4. "the rest in `deskops/graph/extract_docs.py:183-193`" — full list of id-keyed kinds not enumerated; requires reading the file.
5. "the per-line path scanner" is unnamed; no function identifier given.
6. Contradiction: Done When says extract_edges.py "no longer parses frontmatter reference fields", but Scope keeps local frontmatter parsing for untracked docs and MaterializationContractDoc (`source_atoms`/`target_identity`). Which frontmatter parsing may remain is unresolved.
7. How sldb-derived edges and locally-derived dangling refs are merged for `graph missing` is unspecified.
8. No automated check is specified for "dangling-reference set matches the baseline"; whether a test enforces it or it is a manual comparison is unclear.
9. Behavior when an untracked document has no frontmatter `id` (needed for `task:<frontmatter id>`) is undefined.
10. Required format/content of `runs/planning/graph-id-mapping.md` is unspecified.
11. `tests/test_materialization_contract.py:163` is referenced as pinned but not listed in `files`; whether it may be edited is unclear.
12. Completion state of the five `depends_on` tasks is unknown from this document.
13. The three `pills` are listed but their content/constraints are not provided.
14. "anything else that changes is a regression to fix" gives no explicit criteria for distinguishing id-change effects from regressions.
15. Whether `extract_sources.py` requires edits: mentioned in Rationale but absent from `files`; Scope implies no change.
16. Whether the baseline file must be committed before implementation (given the executor does not commit) is not stated.
