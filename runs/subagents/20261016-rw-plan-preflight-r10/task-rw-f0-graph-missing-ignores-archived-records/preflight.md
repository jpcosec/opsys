RESTATEMENT:

1. Do not start: task is `status: blocked` on two owner decisions (handling option A/B/C; marker choice).
2. Reproduce baseline: run `deskops graph missing --root .`; confirm exit 1 with 99 `missing_declared_target` findings from `source-file-reference` provenance (96 from `desk/drawer/issues/diagnosis-archive.md`, 3 from `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`).
3. Option A or C — mark both files with the chosen marker (if `record: true` frontmatter, add frontmatter to both, which currently have none).
4. Option A or C — in the per-line path scanner of `deskops/graph/extract_edges.py`, tag each edge from a record document with `record: true` in metadata (option A: drop those edges there instead).
5. Option A or C — in `deskops/graph/checks.py`, add `record: bool | None = None` to `GraphMissingFinding`; in `find_missing_graph_references` copy the flag onto the finding, True only for record findings. `to_dict` drops None, so live findings' dicts are unchanged (`tests/test_graph_checks.py:25,64`).
6. Option C only — in `_graph_missing` (`deskops/cli/main.py:297-309`), print record findings under a separate `Informational (archived records):` heading after the failing ones, exclude them from the count, exit 1 iff at least one non-record finding exists, and end with `N missing, M informational`.
7. Option B only — rewrite each quoted path in the two files as plain text (e.g. drop the directory part or wrap it) so it no longer matches the scanner; no code change.
8. Add tests in `tests/test_graph_declared_edges.py` using a `tmp_path` desk: a live issue under `desk/drawer/issues/` with a dangling path still yields a finding and exit 1 (scanner reads only `task` and `issue` documents, `extract_edges.py:93`); for A or C, a marked record issue with the same path yields no failing finding.
9. Run validation: `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py tests/test_graph_checks.py`; `deskops graph missing --root .`; `pytest tests`.
10. Verify Done When: repo-desk command exits 0 (C may print informational record findings), new tests pass, `pytest tests` green.
11. Do not commit; supervisor promotes the task and makes the closeout commit.

AMBIGUITIES:

1. Handling option A vs B vs C is undecided; task is blocked.
2. Marker choice is undecided (`record: true` frontmatter, title containing 'archived', or `## Status` resolved/archived).
3. If title-marker chosen, the `issue-session-...` file's rationale text says only its `## Status` says 'resolved' (no 'archived' title); unclear how it would be marked.
4. If frontmatter-marker chosen, both files need frontmatter added, but the task does not say which frontmatter keys/schema the scanner or document-type detection requires.
5. How document type (`task`/`issue`) is determined is not stated, and the two files have no frontmatter.
6. Scope says the record marker is checked on every extracted document, but no rule is given for documents beyond the two named; generic vs named-only is unspecified.
7. Option A says "skip record documents in the path scanner" but does not say whether only path-scan edges or all edges from that document are skipped.
8. Implementation Path step (2) describes the `record: true` metadata tag for both A and C, then says A drops edges instead — contradictory for A.
9. Option B's exact rewrite is unspecified ("drop the directory part or wrap it" is an example); no criterion defines a non-matching form.
10. Whether exit code under C must be 0 even when informational findings exist is stated as "exits 1 iff at least one non-record finding" but Done When only says "may print informational record findings," leaving the accepted count unverifiable.
11. No test asserts the C output format (`N missing, M informational` / heading), so format compliance is unverifiable.
12. `tests/test_graph_cli.py` and `tests/test_graph_checks.py` are in Validation but not in `files:`.
13. Line references (`main.py:297-309`, `extract_edges.py:93`, `test_graph_checks.py:25,64`) may have drifted; no instruction on drift.
14. "If new non-record findings appear before this task runs, list them in the closeout" — unclear whether that blocks Done When (exits 0).
15. No acceptance count is given for the 99 findings post-change (expected 0 missing, 99 informational under C).
