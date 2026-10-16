RESTATEMENT:
1. Confirm which owner decision applies (handling A/B/C; marker choice). Task is `status: blocked`; no decision recorded in the document. Proceeding on the recommended pair: option C + `record: true`.
2. Read `deskops/graph/extract_edges.py` path scanner (per-line path scanner producing `missing_declared_target` / `source-file-reference`) and `deskops/cli/main.py` `_graph_missing` (~lines 296-311).
3. Add `record: true` frontmatter to `desk/drawer/issues/diagnosis-archive.md` and `desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`.
4. In `extract_edges.py`, detect the record marker on every extracted document (not only under `desk/drawer/`) and tag resulting findings as informational.
5. Update `_graph_missing` in `main.py`: print failing findings, then an `Informational (archived records):` heading with record findings; summary line `N missing, M informational`; exit 1 iff ≥1 non-record finding.
6. Add tests in `tests/test_graph_declared_edges.py`: (a) marked record with a dangling path → informational, exit 0; (b) unmarked live drawer task with the same dangling path → failure, exit 1.
7. Run `pytest tests/test_graph_declared_edges.py tests/test_graph_cli.py`.
8. Run `deskops graph missing --root .`; expect exit 0.
9. Run `pytest tests`.
10. Report diff to supervisor; do not commit. Supervisor closes with `deskops closeout commit --task task-rw-f0-graph-missing-ignores-archived-records --run-dir <dir>` (or `--no-run --reason <why>`).

AMBIGUITIES:
1. Handling option (A/B/C) not chosen; task is `blocked`. B would change scope entirely and bypass the scanner/output work.
2. Record marker not chosen among `record: true` frontmatter, title contains 'archived', or `## Status` resolving/archived. Each needs different detection code and different edits to the two files.
3. No existing frontmatter parser location specified for the path scanner to read `record: true`; unclear whether one exists in `extract_edges.py` or must be added.
4. Contradiction: Goal says "one general rule (no per-file allowlist)", but marking two named files' frontmatter is itself a per-file edit.
5. Unclear whether adding `record: true` frontmatter requires SLDB model registration and whether it affects `sldb stores check --store .sldb` or other gates. Not stated.
6. Scope says the record check runs "on every extracted document, not only under desk/drawer/", but under option A record documents are skipped in the scanner — the two statements conflict depending on the chosen option.
7. Test target for the "live drawer task with a dangling path" is unspecified: repo `desk/` (mutating tracked desk) vs a sandbox/tmp root. Repo rules push mutating tests to `.tmp/deskops-cli-test`.
8. Baseline count is fixed at 99 findings from two files (checked 2026-10-16), but the exit-0 criterion has no rule for new non-record findings beyond "list them in the closeout and do not hide them" — whether they block exit 0 is undefined.
9. Exact output string `N missing, M informational` may conflict with existing assertions in `tests/test_graph_cli.py`; no spec of that file's expected format.
10. `depends_on: []`, yet Scope references `task-rw-f4-graph-on-sldb-edge-index` as related/out of scope; ordering and interaction are unspecified.
11. Closeout invocation requires a `--run-dir` or `--no-run --reason`; neither the run directory nor a reason is provided.
12. "Both new tests pass" is required in Done When, but test names/files beyond `tests/test_graph_declared_edges.py` are not fixed, and no assertion for the informational heading is specified.
