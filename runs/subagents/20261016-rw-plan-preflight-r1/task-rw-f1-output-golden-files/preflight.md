RESTATEMENT:
1. Wait/confirm deps: all 9 `depends_on` tasks are closed and their output-shape changes are merged before starting.
2. Create a fixture desk under `tests/fixtures/` (exact subdir unspecified) containing 2 task docs, 2 atoms, 1 pill, 1 drawer task, with a store/runtime layout that can host `.sldb/runtime/graphs/deskops.kg.json`, `.nx.json`, `.sldb/runtime/self_reflection_findings.json`, and `runs/subagents/index.jsonl`.
3. In `tests/conftest.py`, add a `--update-golden` pytest option (registered via `pytest_addoption`) plus any shared copy/normalize helpers.
4. In `tests/test_output_goldens.py`, for each target output: copy the fixture desk into `tmp_path`, run `graph build` (exact CLI form TBD) and a closeout (exact CLI form TBD) against the copy.
5. Normalize volatile fields: timestamps, absolute paths, commit hashes (exact field list and rule TBD).
6. Compare each normalized result to the corresponding committed file under `tests/fixtures/golden/*.json`; write/overwrite goldens only when `--update-golden` is passed.
7. Add coverage proving the test fails if a key is renamed in the snapshot writer (mechanism unspecified).
8. Run `pytest tests/test_output_goldens.py`, then `pytest`, and fix until green.

AMBIGUITIES:
1. `status: deferred` — unclear whether this preflight/execution should proceed now or only after promotion.
2. `Rationale`, `Goal`, `Scope` bodies are unfilled template placeholders (`_Explain why..._`), so the actual required result is not written.
3. `Open Ambiguities` says "None", contradicting the placeholder sections and the gaps below.
4. No fixture path given; "under tests/fixtures/" is not a concrete directory.
5. Fixture contents unspecified: IDs, field values, file format (Markdown vs `.sldb` store), and whether atom/pill/task files are valid SLDB models.
6. Golden file names, count, and directory structure unknown (`tests/fixtures/golden/*.json` only); closeout trailers are not JSON, so their golden location/format is undefined.
7. Rationale says `Task-Id`/`Run-Dir` trailers are pinned, but Implementation Path never says how to produce or capture a closeout commit in `tmp_path` (git init, config, author/date control).
8. `.nx.json`, `.sldb/runtime/self_reflection_findings.json`, and `runs/subagents/index.jsonl` are named in Rationale but no command in Implementation Path produces them; unclear if in scope.
9. Exact CLI invocations for `graph build` and closeout (flags, roots, store path) are unspecified.
10. Normalization rules undefined: which fields, JSON key ordering, JSONL line ordering, path→placeholder tokens, hash replacement value, whitespace/newline handling.
11. `--update-golden` semantics unspecified: option name exactness, whether it also creates missing goldens, and whether CI forbids it.
12. "fail when a key is renamed in the snapshot writer" has no defined mechanism (mutation test, separate unit assertion, or manual instruction).
13. Snapshot schema `deskops_kgdb_graph_snapshot_v1` is named but no assertion on the schema field is required.
14. Comparison method unspecified: byte-exact vs semantic JSON equality.
15. No acceptance criteria for behavior on missing golden files (fail vs skip).
16. No Python version, OS, or git-availability assumptions stated for the test environment.
