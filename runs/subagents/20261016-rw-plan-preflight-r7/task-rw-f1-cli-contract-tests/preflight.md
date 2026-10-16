RESTATEMENT:
1. Verify all 9 `depends_on` tasks are closed and this task has been promoted from `desk/drawer/tasks/` to `desk/tasks/` and appears on `desk/tasks/Board.md` (supervisor does promotion/commit).
2. Create `tests/test_cli_contract.py`.
3. Add a fixture that builds a throwaway repo in pytest `tmp_path`: `git init`, one seed commit, then run `python -m deskops desk install <root>` via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` to scaffold `desk/`. Reuse/adapt helper patterns `_make_repo` and `_cli` from `tests/test_lifecycle_end_to_end.py`.
4. Add an in-process invocation helper calling `deskops.cli.main.main([...])` with `--root <sandbox>` and capturing stdout/stderr via `capsys` (not subprocess) for the 9 subcommands.
5. Write one in-process test per subcommand, parametrizing where shape repeats:
   - `add hook`
   - `add faq-doc`
   - `atoms list`
   - `atoms show`
   - `runtime init`
   - `runtime status`
   - `runtime attach`
   - `runtime stop`
   - `runtime supervise`
6. For all `runtime` tests, stub the Herdr client the same way `tests/test_herdr_runtime.py` does, so no Herdr process starts.
7. Assert per test: exit code and one stable output line from the captured stream.
8. If a test surfaces a defect, do not fix it: create a new drawer task file under `desk/drawer/tasks/` for that defect and mark the test `pytest.mark.xfail(strict=True, reason='<task id>')`.
9. Run `pytest tests/test_cli_contract.py`, then `pytest tests`; ensure green (strict xfails counted).
10. Do not commit; hand the diff to the supervisor for closeout via `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:
1. No expected output strings are given: which exit codes and which "stable line" each of the 9 subcommands should assert is unknown.
2. Whether `--root <sandbox>` is a global flag on `main` or a per-subcommand option (and its placement before/after the subcommand) is unspecified.
3. Whether to import `_make_repo`/`_cli` from `tests/test_lifecycle_end_to_end.py` or reimplement them is not stated.
4. `runtime supervise` may block or run indefinitely; no instruction on how to invoke it non-blocking or with a timeout.
5. "one test per subcommand" vs "parametrize where the shape repeats" conflict on whether a single parametrized test satisfies the per-subcommand Done When.
6. "9 uncovered subcommands" depends on counting the `runtime init|status|attach|stop|supervise` group as 5; if counted as 1 the total is 5, so the target count is interpretation-dependent.
7. Which subcommands are expected to currently pass vs. need strict `xfail` is unknown until execution; no list of known surprises is provided.
8. New drawer task files: naming convention, required frontmatter, and whether they count as task scope are unspecified.
9. Contradiction: Resolved Decisions say the executor does not commit, but `AGENTS.md` requires committing drawer task creation before promotion — unclear how the executor records new drawer tasks without committing.
10. Which output stream (stdout vs stderr) carries the asserted "stable line" is unspecified.
