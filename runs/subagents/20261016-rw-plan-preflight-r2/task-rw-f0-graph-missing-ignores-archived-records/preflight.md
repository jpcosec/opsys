RESTATEMENT:
(Assumes recommended options: handling C, marker `record: true`.)

1. Blocked input: confirm owner picked handling C and marker `record: true`; otherwise stop.
2. Add YAML frontmatter with `record: true` to `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md` (neither currently has frontmatter).
3. In `deskops/graph/extract_edges.py` path scanner (`source-file-reference` provenance), read the record marker from each source doc; tag every finding whose source doc is a record as informational instead of failing. One general rule, no per-file allowlist.
4. In `deskops/cli/main.py:296-311`, split findings into failing (non-record) vs informational (record). Print failing findings first, then a separator heading `Informational (archived records):`, then record findings. Exit 1 iff ≥1 non-record finding; summary line `N missing, M informational`.
5. Add two tests in `tests/test_graph_declared_edges.py`: (a) a marked record doc quoting a dangling path → informational only, no failure, exit 0; (b) an unmarked live drawer task quoting the same dangling path → failure, exit 1.
6. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`.
7. Run `deskops graph missing --root .`; expect exit 0.
8. Run `pytest tests`.
9. Do not commit; leave the diff for the supervisor.

AMBIGUITIES:

1. Handling choice (A/B/C) is unresolved; task is `status: blocked` on it. Restatement above assumes C. Cannot execute until owner decides.
2. Marker choice is unresolved: `record: true` frontmatter vs title containing 'archived' vs `## Status` resolved/archived. Task recommends `record: true` but does not decide.
3. No frontmatter schema/format given for drawer issue docs; correct frontmatter shape (keys, delimiters, position) is a guess.
4. `deskops/cli/main.py:296-311` is cited in Rationale/Implementation Path but absent from the `files:` list — unclear whether it is in scope to edit.
5. `tests/test_graph_cli.py` is required in Validation but absent from `files:` — unclear whether it may be modified or is run-only.
6. Unclear whether findings are computed live per run or from a built/persisted edge index; whether `deskops graph build`/cache must be re-run for `--root .` to reflect changes.
7. Exact print target (stdout vs stderr) and exact ordering/format of the `Informational (archived records):` heading and summary line are unspecified.
8. "one general rule" scope: unclear whether record detection applies only to `desk/drawer/**` docs or any doc carrying the marker.
9. Behavior when a record doc produces a finding kind other than `missing_declared_target` is unspecified (only other finding kinds are declared out of scope).
10. Whether suppressed record findings should still propagate into the graph edge index (consumed downstream) or be dropped at extraction is unspecified.
11. Pill contents (`pill-009`, `pill-010`) are not included, so compliance with them cannot be verified.
12. Acceptance "exits 0 on the repo desk" could be falsified by non-record dangling references in currently active desk docs; no inventory is given proving 99 is the full set.
13. "Done When" says "both new tests pass" while Validation requires the full `pytest tests` suite — unclear if full-suite green is required for closure.
