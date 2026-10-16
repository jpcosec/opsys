RESTATEMENT

1. Confirm dependencies are closed: verify status of the 9 `depends_on` tasks in `desk/tasks/` and `desk/drawer/tasks/`.
2. Read `runs/planning/deskops-rewrite-inventory.md` (phase F1) for the intent of "CLI must not change".
3. Read `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md`; load `use-deskops`.
4. Read `deskops/cli/parser.py:67-89` and the `add` subparser group to enumerate exact subcommand names and required args/options.
5. Read `tests/test_cli.py:1137`, `tests/test_domain_tree.py:104`, `tests/test_herdr_runtime.py`, and `tests/test_lifecycle_end_to_end.py` (`_make_repo`, `_cli` helpers).
6. Create `tests/test_cli_contract.py`.
7. Add a fixture: `_make_repo(tmp_path)` → `git init`, one seed commit; then run `python -m deskops desk install <root>` to scaffold `desk/`. Never touch the repo's own `desk/`.
8. Add one test per subcommand from Rationale:
   - `runtime init`, `runtime status`, `runtime attach`, `runtime stop`, `runtime workers`, `runtime supervise`
   - `closeout commit` (invoked through `main`)
   - `atoms list`, `atoms show`
   - `add board`, `add faq-doc`, `add ritual`, `add step`, `add operator`, `add checklist`, `add hook`, `add edge`
9. Parametrize where shape repeats (e.g. `add *` with per-case args).
10. Stub the Herdr client for all `runtime` tests using the pattern in `tests/test_herdr_runtime.py`; ensure Herdr is never started.
11. Assert exit code and one stable output line per test, capturing via `capsys`.
12. For any test that reveals a defect: create a new drawer task file under `desk/drawer/tasks/`, mark the test `@pytest.mark.xfail(strict=True, reason='<task id>')`.
13. Run `pytest tests/test_cli_contract.py`, then `pytest tests`.
14. Hand off; do not commit (supervisor promotes task, reviews diff, runs `deskops closeout commit`).

AMBIGUITIES

1. Contradiction: Goal and Implementation Path step 3 say tests call `deskops.cli.main.main([...])` in-process; Resolved Decisions say drive the CLI via `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`. Resolutions are authoritative, so the Goal/IP text is stale — confirm which is executed.
2. Contradiction: Implementation Path says pass `--root <sandbox>`; Resolved Decisions say `cwd=root`. Unclear whether `--root` exists, should also be passed, or both.
3. `desk install` vs `deskops desk install`: exact invocation to scaffold `desk/` is not uniquely specified.
4. Required positional/flag arguments for each subcommand (e.g. `add step`, `add edge`, `atoms show`, `closeout commit`) are not listed.
5. "One stable line of output" — which line, and which stream (stdout vs stderr) per subcommand, is unspecified.
6. Expected exit codes per subcommand (success vs usage error) are unspecified.
7. `runtime attach`/`stop`/`supervise` may require a running state; how to reach that state in a sandbox without Herdr is unspecified.
8. Drawer task file format, id, and where it lives under `desk/drawer/tasks/` are not specified.
9. Whether the drawer board (`desk/drawer/tasks/Board.md`) must be updated when adding those drawer tasks is unstated.
10. Baseline health of `pytest tests` before this work is unknown; "green" may require pre-existing failures to be resolved (out of scope).
11. Strict xfail fails the suite if a test unexpectedly passes, which conflicts with "suite is green"; unclear which takes precedence.
12. Dependency completion state cannot be verified from the task document alone.
