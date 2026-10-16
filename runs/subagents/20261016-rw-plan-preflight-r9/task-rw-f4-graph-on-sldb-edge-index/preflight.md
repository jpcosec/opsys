RESTATEMENT:
1. Confirm dependency tasks are complete and the task has been promoted/committed by the supervisor; do not commit.
2. Capture baseline before edits: `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`.
3. Read the sldb public edge-index API agreed in `task-rw-f4-request-sldb-unresolved-references`.
4. Inspect `deskops/graph/extract_edges.py`, `extract_docs.py`, `snapshot.py`, `deskops/services/closeout_gates.py`, `deskops/graph/self_reflection.py`, `deskops/cli/parser.py`, and `deskops/operations.py`.
5. Replace declared-field edge extraction in `extract_edges.py` with sldb edge-index calls.
6. Keep local edges for diagram `source:` (`_diagram_source_declarations`), section-declared atom refs (`_section_declarations`), YAML-fenced atom declarations (`_atom_declarations`, `extract_edges.py:244`), and the per-line path scanner.
7. Map each sldb edge role back to its `field` metadata so roles stay unchanged (`depends_on`, `pills`, etc.).
8. Change document node ids: frontmatter-id kinds keep `<kind>:<frontmatter id>`; `drawer_task:<path>` becomes `task:<frontmatter id>`; path-keyed kinds `doc`, `spec`, `diagram` keep `<kind>:<path>`.
9. Keep file nodes as `source_file:<path>` and `test_file:<path>`.
10. Do not add aliases for old ids.
11. Update `graph missing` to use sldb’s unresolved-reference report.
12. Update hard-coded old ids in `self_reflection.py:164,173,450`, `operations.py:1728,2287` or moved copies, `cli/parser.py:323`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, and `tests/test_graph_extract_docs.py:48-53`.
13. Update `tests/fixtures/golden/graph_snapshot.kg.json` and graph tests only for the id change.
14. Write old-to-new id table to `runs/planning/graph-id-mapping.md`.
15. Compare old and new dangling references as sets of `(kind, mapped source id, mapped target id)` tuples, ignoring order.
16. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`.
17. Run `deskops graph missing --root .`.
18. Run `pytest tests`.
19. Confirm `extract_edges.py` no longer parses frontmatter reference fields.
20. Leave changes uncommitted for supervisor review.

AMBIGUITIES:
1. The sldb public edge-index API is not defined in this task; it depends on another task not included here.
2. Exact sldb edge metadata shape for recovering `field` is unspecified.
3. Mapping sldb `references`/`contains` edges back to original roles is described only by example, not fully defined.
4. Baseline is called a “committed artifact,” but the executor is instructed not to commit; unclear who commits it.
5. Whether `runs/planning/graph-missing-baseline.txt` already exists or must be regenerated is unspecified.
6. `graph missing` tuple `kind` values and exact comparison logic are unspecified.
7. Mapping old dangling ids to new ids may require resolving `drawer_task:<path>` to `task:<frontmatter id>` for records that may not expose an id.
8. `deskops/operations.py` “or their moved copies” is ambiguous without current file locations.
9. The “closeout graph context” in `deskops/services/closeout_gates.py` is not described.
10. `runs/planning/graph-id-mapping.md` format is unspecified.
11. It is unclear whether the golden snapshot must preserve ordering, metadata, or only ids.
12. The boundary of the “coverage extractor” out of scope is not defined.
13. Dependency completeness is unknown from the task document alone.
14. Task status is `deferred`, but the document describes active implementation; execution timing is unclear.
