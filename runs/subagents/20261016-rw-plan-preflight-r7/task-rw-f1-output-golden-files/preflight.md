RESTATEMENT:

1. Create fixture desk `tests/fixtures/golden_desk/` containing exactly 2 task docs, 2 atoms, 1 pill, 1 drawer task (plus minimal boards/meta the CLI needs to run).
2. Create `tests/conftest.py` (does not exist) registering only a pytest `--update-golden` option via `pytest_addoption`.
3. Create `tests/test_output_goldens.py` that, per test run: copies `golden_desk` into `tmp_path`, `git init` + one seed commit, and drives the real CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
4. In the sandbox run `graph build`, then `graph reflect` (to write `.sldb/runtime/self_reflection_findings.json`), then `closeout commit --run-dir <dir>`, then `closeout commit --no-run`.
5. Capture outputs: `.sldb/runtime/graphs/deskops.kg.json`, `deskops.nx.json`, `self_reflection_findings.json`, `runs/subagents/index.jsonl`, and the closeout commit trailers.
6. Capture `--help` text for root `deskops` and for every command path reachable from `deskops --help`.
7. Normalize volatile values: timestamps → `<ts>`, absolute paths → `<root>`, commit hashes → `<sha>`.
8. Compare normalized outputs to goldens in `tests/fixtures/golden/`: `graph_snapshot.kg.json`, `graph_snapshot.nx.json`, `self_reflection_findings.json`, `run_index.jsonl`, `closeout_trailers.json` (list of `{route, trailers}`), and `help/deskops.txt` + `help/deskops_<sub>[_<subsub>].txt`.
9. In `--update-golden` mode rewrite the goldens; otherwise assert equality.
10. Run `pytest tests/test_output_goldens.py`, then `pytest tests`.
11. Manually rename a key in the snapshot writer, confirm the golden test fails, then revert.

AMBIGUITIES:

1. Exact fixture-desk content is unspecified: IDs, titles, statuses, bodies, phase tags, board contents of the 2 tasks / 2 atoms / 1 pill / 1 drawer task; goldens depend on these.
2. Contradiction: Implementation Path copies `tests/fixtures/golden_desk/`, but Resolved Decisions scaffolds the sandbox via `python -m deskops desk install <root>` (and `_make_repo`/`_cli`); which seeds the desk is unclear.
3. No source stated for `runs/subagents/index.jsonl` or for the run dir passed to `closeout commit --run-dir`.
4. Normalization scope is underspecified: which exact fields count as timestamps/hashes, whether `Session-Sha256`, `Run-Id`, run-dir names, session ids, durations, and key ordering are normalized, and how `<root>` is matched (string vs regex, symlinked tmp_path).
5. `closeout_trailers.json` schema underspecified: allowed `route` values, whether `trailers` is a dict or a list of `Key: value`, and exactly which trailer keys are captured.
6. Help collection underspecified: recursion depth of "reachable from `deskops --help`", filename mapping when subcommands contain hyphens/dots, stdout vs stderr, trailing newline/whitespace, exit codes, inclusion of commands requiring args, `--help` vs `-h`.
7. Whether `_make_repo`/`_cli` should be imported from `tests/test_lifecycle_end_to_end.py` or re-implemented, given conftest is constrained to only `--update-golden`.
8. `--update-golden` mechanics unspecified: option flag form, how tests read it (fixture vs `request.config.getoption`), and whether update mode normalizes before writing.
9. Determinism/failure mode unspecified: whether comparison is raw-byte or normalized-structural, and whether JSON must be sorted/pretty-printed.
10. Done When references renaming "a key in the snapshot writer" but no writer module/symbol is named.
11. Done When requires a manual fail check "then revert" with no requirement to record or automate it.
12. No acceptance criteria for handling pre-existing nondeterminism (NX node/edge ordering, dict ordering).
13. Task `status: deferred` and nine `depends_on` entries; no way from this doc to confirm those are complete before execution.
14. Whether `desk install` is required in the fixture repo at all conflicts with the pre-built fixture-desk approach (see 2).
