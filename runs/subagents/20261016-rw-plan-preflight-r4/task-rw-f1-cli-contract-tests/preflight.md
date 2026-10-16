RESTATEMENT

1. Create `tests/test_cli_contract.py`.
2. Add a fixture that builds a throwaway repo in pytest `tmp_path`: `git init`, one seed commit, then run `python -m deskops desk install <root>` to scaffold `desk/`. Reuse helper patterns (`_make_repo`, `_cli`) from `tests/test_lifecycle_end_to_end.py`.
3. Write one in-process test per listed subcommand, calling `deskops.cli.main.main([...])` (not subprocess) with `--root <sandbox>`, capturing stdout/stderr via `capsys`.
4. Cover these subcommands (from Rationale):
   - `runtime init|status|attach|stop|workers|supervise`
   - `closeout commit` (through `main`)
   - `atoms list`
   - `atoms show`
   - `add board|faq-doc|ritual|step|operator|checklist|hook|edge`
   (17 subcommands total.)
5. Parametrize tests where the invocation shape repeats (e.g., the `add` family).
6. In each test, assert the exit code and one stable line of output.
7. For `runtime` tests, stub the Herdr client the way `tests/test_herdr_runtime.py` does so Herdr never starts.
8. If a command fails/surprises, create a new drawer task file under `desk/drawer/tasks/` and mark that test `pytest.mark.xfail(strict=True, reason='<task id>')`; do not fix the command.
9. Run `pytest tests/test_cli_contract.py`, then `pytest tests`.

AMBIGUITIES

1. "One stable line of output" is unspecified: which line per subcommand, and how to select it from multiline output.
2. Expected exit codes are not given per subcommand (all 0 assumed, but not stated).
3. Required arguments/flags for each subcommand to succeed in the sandbox are not specified (e.g., `atoms show <id>`, `add step` target, `add edge` node ids, `closeout commit` `--run-dir` vs `--no-run --reason`).
4. `closeout commit` needs prior task/run state; it is unclear what minimal state the fixture must set up for it to succeed.
5. How to stub the Herdr client for *in-process* calls is not specified; `tests/test_herdr_runtime.py` is referenced but its stubbing mechanism (monkeypatch vs subprocess env) is not stated.
6. Whether `desk install` in the fixture is run via subprocess (per Resolved Decisions) or in-process is not restated in Implementation Path step 1.
7. `add` subcommands' required inputs and whether they must create new artifacts vs. reference existing ones are unspecified.
8. Whether tests must assert stderr as well as stdout is not stated (capsys captures both, but only "one stable line" is required).
9. Naming/format convention for the new drawer task files created on surprises is unspecified.
10. Done When says "Every subcommand listed in Rationale appears in a test" — count/coverage is not defined (e.g., is parametrized coverage of all 17 required, and does an xfail'd test count?).
11. Rationale cites `parser.py:67-89` line ranges, which may not match the current tree; no fallback given if the list differs.
12. No acceptance criterion distinguishing success vs. a legitimately non-zero exit code being acceptable for any listed command.
