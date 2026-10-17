RESTATEMENT:

1. Wait for owner to pick option (A, B, or C) and marker scheme before any edit; task is `blocked`.
2. If option B: edit `desk/drawer/issues/diagnosis-archive.md`, `issue-session-20260910-handoff-uncommitted-work-and-open-items.md`, `issue-refactor-primitives-to-ast-driven-task-nodes.md` to rewrite each scanner-matching quoted path (drop directory part or wrap) so it no longer matches the per-line path scan; make no code change; add tests in `tests/test_graph_declared_edges.py` using `tmp_path` asserting the live-issue case still yields a finding and exit 1.
3. If option A or C: add the chosen record marker (recommended `record: true` frontmatter, adding frontmatter to the two files that have none) to all three files.
4. In `deskops/graph/extract_edges.py`, in the per-line path scanner, detect record documents and either drop their edges (A) or tag each edge metadata with `record: true` (C).
5. In `deskops/graph/checks.py`, add field `record: bool | None = None` to `GraphMissingFinding`; in `find_missing_graph_references`, copy the edge flag onto the finding, setting True only for record findings so live findings keep `to_dict` output identical (None dropped).
6. Option C only: in `_graph_missing` (`deskops/cli/main.py:280`), print record findings under a separate `Informational (archived records):` heading after failing findings, exclude them from the count, exit 1 iff ≥1 non-record finding, and end with `N missing, M informational`.
7. Tests (all options) in `tests/test_graph_declared_edges.py` with a `tmp_path` desk: a live `issue` (or `task`) doc under `desk/drawer/issues/` with a dangling path yields a finding and exit 1 (scanner reads only `task`/`issue` docs, `extract_edges.py:93`); for A/C a marked record issue with the same path yields no failing finding.
8. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py`, then `deskops graph missing --root .` (must exit 0), then `pytest tests` (must be green).
9. Report any new non-record findings appearing before execution in the closeout rather than hiding them.
10. Do not commit; supervisor promotes the drawer task, reviews diff, and makes the closeout commit.

AMBIGUITIES:

1. Which option (A/B/C) — unresolved owner decision.
2. Which marker detection rule (`record: true` frontmatter, 'archived' in title, or `## Status` resolved/archived) — unresolved; affects whether frontmatter must be added to two files and whether a general rule or per-file edit applies.
3. Rationale findings counts contradict: `102` total vs `96 + 3` (then `98 + 3`) + 1; arithmetic does not reconcile, so the true finding set/count is unclear.
4. Scope says "the record marker is checked on every extracted document, not only under desk/drawer/", but the scanner only reads `task` and `issue` documents (`extract_edges.py:93`); unclear which documents the "every document" rule actually covers and what makes a doc a "record".
5. Unclear whether record status is determined by an explicit marker, by file location, or by resolver logic — no definition of "record document".
6. Contradiction: status is `blocked`, yet `Done When` and `Validation` are stated as if executable; no unblocking acceptance criterion or owner sign-off form is specified.
7. Adding frontmatter to `diagnosis-archive.md` and the session handoff file may alter preserved verbatim history (option A/C); no instruction on preserving original content/lines, and this clashes with option B's explicit "loses verbatim history" concern.
8. Unclear what "resolved by afdec7f and becomes a record" requires operationally (does the task write the resolution status, or just apply the marker?).
9. Option C semantics: exact format of `Informational (archived records):` heading, ordering, and wording of `N missing, M informational` (whether M counts only records in this run) are unspecified.
10. Whether the new `record` flag must also appear in JSON/`to_dict` output for record findings (only "drops None" for live findings is specified) is unspecified.
11. Tests placement: Implementation Path names only `tests/test_graph_declared_edges.py`, but also cites `tests/test_graph_checks.py:25,64`; unclear whether new `record` flag tests belong in `test_graph_checks.py` too.
12. Test mechanism (direct function call vs subprocess CLI) for asserting exit 1 / exit 0 is unspecified.
13. No specified behavior when a record document contains a live (non-missing) path, or when a live document is later archived.
14. "if new non-record findings appear before this task runs" gives no threshold, file, or decision rule for what to do if they do appear.
15. No criteria for what counts as success with `depends_on: []` while Rationale says it is phase F0 of the rewrite plan; no explicit dependency on `task-rw-f4-graph-on-sldb-edge-index` beyond "out of scope".
