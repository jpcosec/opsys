RESTATEMENT:
1. Read `deskops/cli/main.py` and run `deskops --help`, `deskops graph --help`, `deskops graph build --help`, `deskops graph reflect --help`, `deskops closeout commit --help` to learn exact command paths, flags, arg names, and output file paths.
2. Create `tests/fixtures/golden_desk/` with a valid desk: `desk/tasks/Board.md`, 2 task docs, 2 atoms under `desk/atoms/`, 1 pill under `desk/contexts/`, 1 drawer task under `desk/drawer/tasks/`, plus whatever deskops init/store artifacts are needed.
3. Create `tests/conftest.py` that registers a `--update-golden` option (pytest_addoption + helper fixture). Nothing else.
4. Create `tests/test_output_goldens.py`: copy `golden_desk/` into `tmp_path`, `git init`, seed commit, run `python -m deskops init <root>`, commit fixture files, then run `graph build`, `graph reflect`, generate `runs/subagents/index.jsonl`, `closeout commit --run-dir <dir>`, and `closeout commit --no-run --reason <why>` via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`.
5. Implement normalizers: ISO timestamps -> `<ts>`, absolute paths -> `<root>`, commit/other hashes -> `<sha>`.
6. Collect and normalize `.sldb/runtime/graphs/deskops.kg.json`, `deskops.nx.json`, `.sldb/runtime/self_reflection_findings.json`, `runs/subagents/index.jsonl`, closeout commit trailers as `[{route, trailers}]`, and compare against `tests/fixtures/golden/`.
7. Enumerate every command path reachable from `deskops --help` recursively; run each `--help`; write `help/deskops.txt` and `help/deskops_<sub>[_<subsub>].txt`.
8. When `--update-golden` is passed, write/overwrite all goldens instead of asserting.
9. Run `pytest tests/test_output_goldens.py` and `pytest tests`.
10. Manually rename a key in the snapshot writer, confirm the test fails, revert.

AMBIGUITIES:
1. Fixture content unspecified (task ids, titles, atom/pill/drawer filenames and bodies); goldens depend on it, so all fixture text is a guess.
2. Pill location: task says "1 pill" but not the directory; repo convention is `desk/contexts/`.
3. Exact `graph build` / `graph reflect` invocation (args such as root/store/schema) not given; must be derived from code.
4. Writer of `runs/subagents/index.jsonl` is not named; no command or record format given to produce run index content (only `graph reflect` is stated as the sole writer of self_reflection_findings.json).
5. Whether `closeout commit --run-dir` requires a pre-existing run manifest inside the run dir, and its format, is unspecified.
6. `closeout_trailers.json` route value format (e.g. `"--no-run"` / `"--run-dir"` / command string) is unspecified.
7. Normalization scope for hashes: does `<sha>` also replace `Session-Sha256`, content/merkle hashes inside the snapshot, and hashes embedded in `Run-Id`? Unspecified; over-normalizing weakens the test.
8. Help output may wrap to terminal width; no instruction to pin `COLUMNS`/width or to disable wrapping, making goldens environment-dependent.
9. `--help` output may include `argv[0]`/program path; no normalization rule for that.
10. Help enumeration method (recursive parsing of help text vs CLI introspection) and handling of aliases/hidden commands is unspecified.
11. Contradiction-ish: implementation step 2 says copy -> git init -> `graph build`, omitting the `python -m deskops init <root>` step that Resolved Decisions require.
12. Whether fixture files must be git-committed before graph build (tracked vs untracked affects snapshot) is unspecified.
13. Which of the 2 fixture tasks is closed, and whether it must be promoted to `desk/tasks/` first, is unspecified.
14. Git identity/committer dates and commit count for determinism are unspecified (mitigated only if hashes/dates are normalized).
15. Location of normalization helpers (conftest vs test module) is unspecified.
16. Done-When manual mutation check ("key renamed in the snapshot writer") has no named file/function, so the check target is a guess.
17. No acceptance criterion for the number/exact set of help files, so completeness ("every command path reachable") cannot be verified objectively.
