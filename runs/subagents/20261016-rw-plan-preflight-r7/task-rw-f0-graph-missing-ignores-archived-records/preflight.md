RESTATEMENT:

1. Read the bound pills (`desk/contexts/pill-009-source-file-graph-traceability.md`, `desk/contexts/pill-010-graph-runtime-output-policy.md`) and inspect `deskops/graph/extract_edges.py` (per-line path scanner) and `deskops/cli/main.py` `_graph_missing` (lines ~296-311).
2. Obtain the owner decision on handling (A/B/C) and on the record marker, because `status: blocked` and both Open Ambiguities are unresolved; no code change can be chosen without them.
3. Add the chosen record marker to both `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`.
4. Implement the chosen handling: tag findings originating from record documents as informational in the path scanner of `deskops/graph/extract_edges.py`, and for option C adjust `_graph_missing` in `deskops/cli/main.py` to print records under a separate `Informational (archived records):` heading after failing findings, exclude them from the failure count, set exit code 1 iff ≥1 non-record finding exists, and change the summary to `N missing, M informational`.
5. Add two tests in `tests/test_graph_declared_edges.py`: a marked record with a dangling path (expect informational, exit 0) and an unmarked live drawer task with the same dangling path (expect failure, exit 1).
6. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`, `deskops graph missing --root .`, and `pytest tests`.
7. Verify Done When (exit 0 on repo desk, both new tests pass, `pytest tests` green); do not commit — hand the diff to the supervisor.

AMBIGUITIES:

1. Handling option A/B/C is not chosen; task is `blocked` — execution cannot start.
2. Record marker is not chosen (`record: true` frontmatter vs title containing 'archived' vs `## Status` saying resolved/archived).
3. Single marker contradiction: `diagnosis-archive.md` has no frontmatter and only its title says 'archived'; the issue-session file has no 'archived' title and only a `## Status` saying 'resolved'. No single marker option in the list cleanly covers both files without editing one file's title or adding a status section.
4. Layer contradiction: Scope says option C is "the output and exit code of `_graph_missing` in deskops/cli/main.py", while Implementation Path step (2) says implement the handling "in the path scanner of extract_edges.py". Which layer detects records vs. formats output is unspecified.
5. For a frontmatter marker: required key name, value format, and placement are not specified, and it is unclear whether desk drawer issue docs may carry frontmatter.
6. How `extract_edges.py`'s per-line scanner is supposed to read the record marker (frontmatter/status/title) is not specified.
7. "one general rule (no per-file allowlist)" vs adding markers to two specific files is not reconciled.
8. "'Informational (archived records):' heading after the failing ones" — ordering, sorting, and whether records of other finding kinds are included are unspecified.
9. Summary line `N missing, M informational` — whether `M` counts findings or documents is unspecified; impact on existing summary-format assertions in `tests/test_graph_cli.py` is unknown.
10. Which existing tests currently assert the old heading/summary/exit behavior is not identified.
11. Test construction is unspecified: fixture files vs temp dirs vs sandbox desk root.
12. Whether the two new tests belong in `tests/test_graph_declared_edges.py` while the changed logic is in `main.py`/`_graph_missing` (validated via `tests/test_graph_cli.py`) is not reconciled.
13. "a live drawer task with a dangling path still exits 1" — definition of "live" and of the dangling path used is unspecified.
14. "if new non-record findings appear before this task runs, list them in the closeout" conflicts with the Resolved Decision that the supervisor performs closeout, not the executor.
15. The document shows `status: blocked` and `source:drawer`, conflicting with the Resolved Decision that promotion to `desk/tasks/` and its commit happen before dispatch (i.e., the given doc should already be a promoted active task).
16. Acceptance criteria do not specify expected printed output text/format beyond the heading and summary string.
