RESTATEMENT:
1. Read `tests/test_cli.py:1124`, `tests/test_herdr_runtime.py`, and `tests/test_lifecycle_end_to_end.py` (`_make_repo`, `_cli`) to copy the in-process `main([...])` + `capsys` pattern and the Herdr stubbing pattern.
2. Create `tests/test_cli_contract.py` with a fixture that builds a throwaway sandbox repo in `tmp_path` (git init, one empty seed commit) and initializes deskops state (command TBD — see ambiguities) inside that root.
3. Add one test per subcommand: `add faq-doc`, `atoms list`, `atoms show`, `runtime init`, `runtime status`, `runtime attach`, `runtime stop`, `runtime supervise` (8 total; use `parametrize` where shapes repeat).
4. Each test calls `deskops.cli.main.main([...])` in-process with `--root <sandbox>`, captures stdout/stderr via `capsys`, and asserts the exit code plus one stable output line.
5. Stub the Herdr client for the `runtime` tests as `tests/test_herdr_runtime.py` does, so no Herdr process starts.
6. Never touch the repo's real `desk/`; keep all mutations inside the sandbox.
7. Run the tests; for each subcommand that fails a stated contract, create a new drawer task file under `desk/drawer/tasks/` and mark that test `pytest.mark.xfail(strict=True, reason='<new task id>')`.
8. Run `pytest tests/test_cli_contract.py`, then `pytest tests`.

AMBIGUITIES:
1. Contradiction: Implementation Path step 1 says the fixture runs `desk install`; Resolved Decisions says the sandbox is built with `python -m deskops init <root>` (or the `lifecycle_desk` fixture). Which command initializes the sandbox is unresolved.
2. No expected exit codes are given for any subcommand.
3. No expected output text/line is given; "one stable line of output" is undefined.
4. Which stream (stdout vs stderr) the asserted line comes from is unspecified.
5. Whether `--root` is a valid top-level flag for `deskops.cli.main.main` is not verified in the task.
6. `runtime attach`, `runtime status`, `runtime stop`, and `runtime supervise` behavior with no running runtime is unspecified, so pass/fail expectations cannot be derived.
7. `runtime supervise` may block or run continuously; no termination/timeout guidance is given.
8. The Herdr stub is only referenced ("the way tests/test_herdr_runtime.py does"); no fixture name, patch target, or API is specified.
9. "where the shape repeats" for `parametrize` is left to executor judgment, but Done When demands one test per subcommand.
10. Drawer task file naming/format for recorded surprises is unspecified.
11. Chicken-and-egg: strict xfail requires knowing a test fails, but the contract (exit code, output line) is undefined, so "surprise" is undecidable without guessing expected values.
12. If a subcommand unexpectedly passes, `xfail(strict=True)` would itself fail, but no rule covers that case.
13. Dependencies (`task-rw-f0-*`, etc.) are assumed closed; nothing confirms it.
