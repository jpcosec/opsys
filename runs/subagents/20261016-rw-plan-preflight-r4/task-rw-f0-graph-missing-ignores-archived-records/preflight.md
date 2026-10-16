RESTATEMENT:
1. Await unblock: confirm with owner the handling option (A/B/C) and the record marker definition.
2. If option C chosen: mark `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` with the chosen marker (add `record: true` frontmatter to both files, which currently have no frontmatter).
3. In `deskops/graph/extract_edges.py`, locate the per-line path scanner emitting `missing_declared_target` findings with `source-file-reference` provenance and add record detection there (general rule applied to every extracted document, not just under `desk/drawer/`).
4. Tag findings from record documents as informational; keep all others as failures.
5. In `deskops/cli/main.py` `_graph_missing` (currently lines 296-311): print non-record findings first, then a separate `Informational (archived records):` heading with record findings; set exit code 1 iff ≥1 non-record finding exists; print summary as `N missing, M informational`.
6. Add tests in `tests/test_graph_declared_edges.py`: one for a marked record with a dangling path, one for an unmarked live drawer task with the same dangling path (expect exit 1).
7. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`.
8. Run `deskops graph missing --root .` and verify exit 0.
9. Run `pytest tests` and verify green.
10. Record any new non-record findings in closeout (do not hide). Do not commit; supervisor promotes the drawer task and performs the closeout commit.

AMBIGUITIES:
1. Task `status: blocked`; owner decisions in Open Ambiguities (handling A/B/C, marker) are unresolved, so the work cannot start.
2. Contradiction: Scope says "In scope with option C" and Implementation Path says "Option C precisely", while Open Ambiguities lists handling as an open owner decision — cannot tell which is authoritative.
3. Marker undecided in Open Ambiguities (`record: true` frontmatter vs title 'archived' vs `## Status` resolved/archived); task text assumes a marker but never fixes which.
4. If handling is A (skip record documents) or B (edit quoted paths), the steps for marker application and tests differ from those written; Implementation Path only specifies option C exactly.
5. The scanner function/emitting code in `extract_edges.py` is not named; where the record check goes is unspecified.
6. Whether changing the summary format (`N missing, M informational`) breaks existing assertions in `tests/test_graph_cli.py` is unknown; that file is not in `files`.
7. Output ordering/section layout beyond the given heading string and summary line is unspecified.
8. How "record" is detected for a file without frontmatter when using the frontmatter marker — adding frontmatter is stated but parsing location is unknown.
9. No acceptance criterion distinguishes the two Open-Ambiguity branches in Done When; exit 0 could be reached by either rule.
10. The 99 HEAD findings were counted 2026-10-16; whether new non-record findings exist at execution time is unknown, and no procedure is given for reconciling them with the exit-0 goal.
