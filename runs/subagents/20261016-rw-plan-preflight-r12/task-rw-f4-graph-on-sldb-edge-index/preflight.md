RESTATEMENT:

1. Capture baseline: run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt` and leave it as a committed artifact (supervisor commits).
2. Read `task-rw-f4-request-sldb-unresolved-references` to obtain the agreed sldb public edge-index API (entry point, import path, return shape, unresolved-reference report) and note it in `runs/planning/graph-id-mapping.md` or a scratch note.
3. In `deskops/graph/extract_edges.py`, replace regex/frontmatter re-implementation of declared-field edges (`_declarations_from_mapping` path) with calls into the sldb edge index; map each returned sldb edge back to `role = edge.field` so role names (`depends_on`, `pills`, `references`, ...) are unchanged; emit `references`/`contains` only as sldb yields them.
4. Keep local extraction for the explicitly out-of-reach cases: `_diagram_source_declarations`, `_section_declarations`, YAML-fenced `_atom_declarations` (extract_edges.py:244), the per-line path scanner, frontmatter fields of models with no `__references__`/`__containment__` (MaterializationContractDoc `source_atoms`, `target_identity`), and frontmatter edges of documents the store does not track (drawer tasks, untracked desk docs under `.sldb/core/documents/`).
5. In `deskops/graph/extract_docs.py`: unify document node ids to `<kind>:<id>`; keep `<kind>:<frontmatter id>` for id-keyed kinds (atom, task, pill, board, and the kinds at lines 183-193); map `drawer_task:<path>` -> `task:<frontmatter id>`; keep `<kind>:<path>` for doc, spec, diagram. No aliases for old ids.
6. Keep file-node ids `source_file:<path>` / `test_file:<path>` (extract_sources.py:108-112).
7. In `deskops/graph/snapshot.py`, ensure snapshot assembly uses the new sldb-sourced edges and the unified id scheme; no duplicate/legacy edges.
8. In `deskops/graph/self_reflection.py` (lines ~164, 173, 450), `deskops/operations.py` (~1728, ~2287), `deskops/cli/parser.py:323`, update hard-coded old ids/schemes.
9. Wire `graph missing` to sldb's unresolved-reference report via `deskops/services/closeout_gates.py` graph context and the graph CLI path.
10. Update `tests/test_graph_extract_docs.py:48-53`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, `tests/fixtures/golden/graph_snapshot.kg.json` for the id change only.
11. Write the old->new id table to `runs/planning/graph-id-mapping.md`.
12. Verify `graph missing` set equality with baseline modulo the mapping: compare sets of `(kind, mapped source id, mapped target id)`, order-insensitive.
13. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, then `deskops graph missing --root .`, then `pytest tests`.
14. Confirm extract_edges.py no longer parses frontmatter reference fields.

AMBIGUITIES:

1. The sldb public edge-index API (function name, import path, signature, returned edge/field metadata, unresolved-reference report shape) is not in this document; `task-rw-f4-request-sldb-unresolved-references` is only a title reference.
2. No spec for detecting which documents the store tracks vs not (whether to read `.sldb/core/documents/` directly or via an sldb API), which decides which frontmatter edges stay local.
3. `drawer_task:<path>` -> `task:<frontmatter id>` collision behavior is unspecified if a drawer task and an active task share a frontmatter `id`, or if a drawer task lacks `id` frontmatter.
4. `runs/planning/graph-id-mapping.md` cannot cover dangling/unresolvable targets that never had a node id; how to map or compare those in the baseline tuple set is unspecified.
5. Baseline capture semantics are unspecified: whether `runs/planning/graph-missing-baseline.txt` is produced before or after dependency `task-rw-f0-graph-missing-ignores-archived-records` lands, and its assertion count/serialization format.
6. `files:` frontmatter omits `deskops/operations.py` and `extract_sources.py` while Scope names them; which list is authoritative is unclear. Line numbers cited (self_reflection.py:164,173,450; operations.py:1728,2287; extract_edges.py:244) will drift and no anchors are given.
7. Scope says update "any other untracked desk document" frontmatter edges locally, but the set of untracked kinds is open-ended ("today" wording), so completeness cannot be verified from this document.
8. Mechanism for regenerating `tests/fixtures/golden/graph_snapshot.kg.json` (which command, or hand-edit) is not stated, nor how to distinguish "id-change-only" diffs from regressions.
9. "Edges declared by model fields" vs "frontmatter fields of models that declare no `__references__`/`__containment__`" — whether `__references__`/`__containment__` presence is checked per model or per field is unspecified.
10. Resolved Decisions say the executor does not commit, but step 1 labels the baseline file a "committed artifact"; who creates vs commits it is unspecified.
11. Open Ambiguities states "None", which contradicts the missing sldb API contract and unmappable-target rules above.
