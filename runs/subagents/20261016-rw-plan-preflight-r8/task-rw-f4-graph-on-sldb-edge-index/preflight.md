RESTATEMENT:

1. Run `deskops graph missing --root . > runs/planning/graph-missing-baseline.txt`; commit this artifact as the pre-change baseline. Record the set of dangling `(kind, source id, target id)` tuples.
2. Read `deskops/graph/extract_edges.py`, focusing on the frontmatter reference-field regex parsing, `_diagram_source_declarations`, `_section_declarations`, `_atom_declarations` (line ~244), and the per-line path scanner.
3. Read the sldb public edge-index API agreed in `task-rw-f4-request-sldb-unresolved-references` (dependency; must be available) to learn how to query declared edges and unresolved references, and how each edge's `field` metadata is exposed.
4. In `extract_edges.py`, replace the frontmatter reference-field regex extraction with edges obtained from the sldb edge index. For each sldb edge, set `role = edge["field"]` (not `references`/`contains`) so existing roles such as `depends_on`, `pills` are preserved.
5. Keep these local extractors unchanged: `_diagram_source_declarations` (`source:` diagram edges), `_section_declarations` (section-declared atom refs), `_atom_declarations` (YAML-fenced atom declarations in bodies), and the per-line path scanner. Leave the coverage extractor untouched (out of scope).
6. In `extract_docs.py`, collapse document node ids to one scheme `<kind>:<id>`:
   - Kinds keyed by frontmatter `id` today (atom, task, pill, board, and the rest listed at extract_docs.py:183-193) become `<kind>:<frontmatter id>`.
   - `drawer_task:<path>` becomes `task:<frontmatter id>` (drawer_task folded into task).
   - Path-keyed kinds (doc, spec, diagram) become `<kind>:<path>`.
   - File nodes keep `source_file:<path>` / `test_file:<path>` (extract_sources.py:108-112).
   - Do not emit aliases for old ids.
7. Update remaining hard-coded old ids: `deskops/graph/self_reflection.py:164,173,450`, `deskops/operations.py:1728,2287` (or moved copies), `deskops/cli/parser.py:323`, `tests/fixtures/knowledge_graph/static_desk_source_graph.json`, `tests/test_graph_extract_docs.py:48-53`.
8. Update `deskops/graph/snapshot.py` as needed so snapshots reflect the new id scheme.
9. Update the closeout graph context in `deskops/services/closeout_gates.py` for the new ids.
10. Write the old→new id mapping table to `runs/planning/graph-id-mapping.md`.
11. Update `tests/fixtures/golden/graph_snapshot.kg.json` for the id change only.
12. Update `tests/test_graph_cli.py`, `tests/test_graph_declared_edges.py` (incl. lines 78-92), `tests/test_graph_extract_edges.py` for the id change only; fix any other resulting diffs as regressions.
13. Change `graph missing` to use sldb's unresolved-reference report instead of the local implementation.
14. Compare the new `graph missing` dangling set against the baseline: same set of `(kind, mapped source id, mapped target id)` tuples, order ignored.
15. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, then `deskops graph missing --root .`, then `pytest tests`; all must pass.
16. Verify `extract_edges.py` no longer parses frontmatter reference fields, then hand the diff to the supervisor (executor does not commit).

AMBIGUITIES:

1. Name/signature/location of the sldb public edge-index API is not stated; it is deferred to `task-rw-f4-request-sldb-unresolved-references`, so the exact import, call, and edge/metadata shape are unknown.
2. "Per the API agreed in task-rw-f4-request-sldb-unresolved-references" cannot be verified: that task's content is not provided, and no confirmation exists that it is complete/merged.
3. `extract_edges.py:244` is cited for `_atom_declarations`, but other line citations (extract_docs.py:59-115,183-193; extract_sources.py:108-112; self_reflection.py:164,173,450; operations.py:1728,2287; parser.py:323; test_graph_declared_edges.py:78-92) may be stale; no commit/version pinned.
4. `deskops/operations.py:1728,2287` "(or their moved copies)" is indeterminate — the actual file/location to edit is unknown.
5. Baseline is saved at step 1, but the task `depends_on` four tasks; whether the baseline must be captured on the current (post-dependency) tree vs pre-dependency tree is unstated.
6. Whether `task-rw-f4-request-sldb-unresolved-references` and the other three dependencies are already merged is not stated; if unavailable, steps 3–4 and 13 are blocked.
7. Whether the sldb edge index covers every declared field currently regex-parsed (i.e., no field is lost) is not stated; a missing field would silently drop edges.
8. "the same set of dangling references as the baseline" — behavior for dangling refs whose source id changes kind (e.g., `drawer_task:` → `task:`) when matching baseline tuples is unspecified beyond "mapped source id"; the mapping function used for comparison is not defined.
9. No stated tolerance for changed counts versus the baseline other than exact set equality; whether duplicate tuple multiplicity matters (set vs multiset) is unclear.
10. `runs/planning/graph-missing-baseline.txt` is "a committed artifact," but the executor "does not commit"; who commits the baseline and when is contradictory.
11. Whether edge ordering in outputs/golden files must be stable after the source change (sorting) is unstated.
12. Whether path-keyed kinds (doc, spec, diagram) paths are repo-relative or absolute after the change is unstated.
13. `graph missing` output format/columns are not specified (needed to compare tuples and to update `tests/test_graph_cli.py`).
14. Whether any external consumers depend on old ids (no alias) is unstated; "Old ids get no alias" implies breakage but no migration check is defined.
15. Acceptance criteria do not state the expected value of the baseline comparison (e.g., empty diff) beyond "matches modulo id mapping"; `graph-id-mapping.md` format is unspecified.
