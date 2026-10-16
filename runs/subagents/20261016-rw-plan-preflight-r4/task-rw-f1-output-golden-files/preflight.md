# RESTATEMENT

1. Create `tests/fixtures/golden_desk/`: minimal desk with 2 tasks in `desk/tasks/`, 2 atoms in `desk/atoms/`, 1 pill in `desk/contexts/`, 1 drawer task in `desk/drawer/tasks/`, plus the `Board.md` files and any `desk/` metadata needed for valid SLDB graph and closeout.
2. Create `tests/conftest.py` with a single `pytest_addoption` registering `--update-golden` (store_true); no other options.
3. Create `tests/test_output_goldens.py` with helpers to copy `golden_desk/` into `tmp_path`, `git init` + seed commit, and run the CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
4. Define normalization: timestamps → `<ts>`, absolute paths → `<root>`, commit hashes → `<sha>` (apply before comparison and before `--update-golden` writes).
5. Run `graph build`; capture `.sldb/runtime/graphs/deskops.kg.json` and `deskops.nx.json`; write `tests/fixtures/golden/graph_snapshot.kg.json`, `graph_snapshot.nx.json`.
6. Run `graph reflect`; capture `.sldb/runtime/self_reflection_findings.json`; write `tests/fixtures/golden/self_reflection_findings.json`.
7. Run a `closeout commit --run-dir <dir>` on one fixture task; capture trailers.
8. Run a `closeout commit --no-run --reason <reason>` on another fixture task; capture trailers.
9. Collect `runs/subagents/index.jsonl`; write `tests/fixtures/golden/run_index.jsonl`.
10. Write `tests/fixtures/golden/closeout_trailers.json` as a JSON list of `{route, trailers}` objects (one per closeout route).
11. Enumerate every command path reachable from `deskops --help` (recursively); write `tests/fixtures/golden/help/deskops.txt` (root) and `help/deskops_<sub>[_<subsub>].txt` per path.
12. In `test_output_goldens.py`, assert each normalized output equals its golden; on mismatch, fail with a diff; if `--update-golden` is set, rewrite goldens instead of asserting.
13. Run `pytest tests/test_output_goldens.py`, then `pytest tests`.
14. Manually rename a key in the snapshot writer, confirm the golden test fails, revert the rename.

# AMBIGUITIES

1. Fixture desk content unspecified: task ids, task bodies, atom contents, pill text, Board rows, and drawer task content must be invented.
2. Whether `tests/fixtures/golden_desk/` is hand-authored or scaffolded via `desk install`; Implementation Path implies hand-authored, Resolved Decisions implies `desk install` scaffolding.
3. Whether the fixture desk ships with a pre-built `.sldb/` store or the store is generated at test time from scratch.
4. Whether a seed commit after `git init` is required here (Resolved Decisions mentions one for CLI tests; Implementation Path only says `git init`).
5. Whether the test reuses `_make_repo`/`_cli` helpers from `tests/test_lifecycle_end_to_end.py` or reimplements them.
6. Exact normalization patterns (regex) for `<ts>`, `<root>`, `<sha>` are unspecified.
7. Whether `Session-Sha256` trailer is normalized to `<sha>`.
8. Whether normalization is applied uniformly to `--help` text (which has no volatile values).
9. `route` values inside `closeout_trailers.json` and their ordering are unspecified.
10. Which two fixture task ids are used for the two closeout commits, and how the `--run-dir` directory is produced in the fixture.
11. Command-path enumeration method (parse `--help` output vs. introspection) and treatment of hidden/alias commands and depth limit are unspecified.
12. Filename mapping rules for `help/deskops_<sub>[_<subsub>].txt` beyond depth 2 are unspecified.
13. `--update-golden` semantics: rewrite all goldens vs. only mismatches, directory creation, and exit code are unspecified.
14. No acceptance criteria on golden file contents/formats beyond filenames (e.g., expected key sets in `kg.json` vs `nx.json`).
15. Out-of-scope "changing any output format" may conflict with non-deterministic current outputs (e.g., key ordering) that would need canonicalization to be golden-stable.
16. Done When requires a hand-run failure check; whether that step must be recorded/evidenced for closeout is unspecified.
17. `depends_on` prerequisites are assumed complete; no state is provided.
18. Whether `graph reflect` must run after `graph build` in the same tmp copy is unstated (only implied).
19. Test isolation: whether each test gets its own tmp copy or they share one is unspecified.
