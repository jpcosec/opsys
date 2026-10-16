RESTATEMENT:
1. Read `desk/contexts/pill-008-kgdb-sldb-boundary.md`, `pill-009-source-file-graph-traceability.md`, `pill-010-graph-runtime-output-policy.md`, the four `depends_on` task docs, and phase F4 of `runs/planning/deskops-rewrite-inventory.md`.
2. Consume the sldb public edge-index API and unresolved-reference report delivered by `task-rw-f4-request-sldb-unresolved-references`; confirm its method names/signatures.
3. Inventory every edge kind currently emitted in `deskops/graph/extract_edges.py` and map each to its sldb source; record kinds sldb cannot provide.
4. Rewrite `deskops/graph/extract_edges.py` to source declared edges from the sldb edge index; delete its frontmatter regex parsing.
5. Rewrite document-node extraction (`deskops/graph/extract_docs.py`) to come from sldb; keep local file-node extraction, emitting `source_file:` and `test_file:` nodes.
6. Normalize node ids in `deskops/graph/snapshot.py` to a single `<kind>:<id>` scheme.
7. Update the closeout graph context in `deskops/services/closeout_gates.py` (relocated there by `task-rw-f3-closeout-gates-service`).
8. Update the F1 golden file only for the id change; list the changed file.
9. Point `graph missing` at the new sldb report.
10. Run `pytest tests/test_graph_cli.py tests/test_graph_declared_edges.py tests/test_graph_extract_edges.py`, then `deskops graph missing --root .`, then `pytest tests`.

AMBIGUITIES:
1. `Rationale` and `Goal` are placeholder text (`_Explain why..._`, `_Describe..._`) with no content.
2. The F1 golden file is never named or path-specified.
3. The sldb edge-index API and unresolved-reference report are undefined here; behavior blocked until the dependency task is done (status is `deferred`).
4. `kind` vocabulary for `<kind>:<id>` is unspecified; unclear how the 5 existing schemes collapse into it.
5. No disposition given for edge kinds "sldb cannot provide"; the list is requested but no handling rule stated.
6. "`graph missing` matches the previous findings" has no recorded baseline output; equality is unverifiable.
7. Potential contradiction: ids are changed in step 3, yet `graph missing` output must match previous findings.
8. Whether "one node-id scheme" applies to all nodes or only document nodes is unclear.
9. Current vs target location/state of the closeout graph context is unknown; edit scope vs. f3 relocation overlap is unclear.
10. Whether the three named test files are to be modified or only run is unstated.
11. Coverage extractor is out of scope but no path is given to identify it.
12. No acceptance criteria for the missing-reference report format/content.
13. All four `depends_on` tasks' completion state is unknown; task is `deferred`.
