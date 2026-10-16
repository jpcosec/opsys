RESTATEMENT:

1. Read `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md` and `desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md` to fix the contract expectations.
2. Confirm the nine `depends_on` tasks are closed (F0 rewrite tasks, doctor-deskless-roots, declare-runtime-dependencies, graph-skips-vendored, pytest-collects-only-tests, payload-from-drawer-resolves); stop if any is open.
3. Read `tests/test_lifecycle_end_to_end.py` and copy its `_make_repo` and `_cli` helpers into the new `tests/test_cli_contract.py` (or import them).
4. Build a pytest fixture on `tmp_path` that: `git init`, one seed commit, runs `python -m deskops desk install <root>` to scaffold `desk/`.
5. Enumerate runtime subcommands: `python -m deskops runtime --help`.
6. Write one test per subcommand in `tests/test_cli_contract.py`, driving the CLI as `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` and asserting exit code plus one stable output line.
7. Cover: every `runtime` subcommand (install/start/status/attach/stop + remainder), `closeout commit`, `atoms list`, `atoms show`, and `add board|faq-doc|ritual|step|operator|checklist|hook|edge`.
8. Parametrize tests whose argument shape repeats (e.g. the `add` family, the `runtime` family).
9. Stub the Herdr client the way `tests/test_herdr_runtime.py` does so no runtime test starts Herdr.
10. For each test that fails due to product behavior, create a new drawer task file under `desk/drawer/tasks/` and mark that test `pytest.mark.xfail(strict=True, reason='<task id>')`.
11. Run `pytest tests/test_cli_contract.py`, then `pytest`.
12. Do not commit; leave the diff for supervisor closeout with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:

1. Goal + Implementation Path say call `deskops.cli.main.main([...])` and capture via `capsys`; Resolved Decisions say use `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)`. Direct contradiction on the invocation mechanism.
2. Resolved Decisions use `cwd=root`; Implementation Path says pass `--root <sandbox>`. Unclear whether `--root` exists and is required on every listed subcommand or whether cwd is the sole mechanism.
3. Stubbing the Herdr client is impossible in a subprocess; no guidance on how the stub is injected across a process boundary.
4. `files:` lists only `tests/test_cli_contract.py`, but the helper-copy instruction implies touching/importing `tests/test_lifecycle_end_to_end.py`. Unclear whether editing that file is allowed.
5. "One stable line of output" is unspecified per subcommand — no expected string given for any of them.
6. The exact set of `runtime` subcommands is unknown until `--help` is run, so acceptance ("every subcommand listed in Rationale") is not checkable against a fixed list.
7. `closeout commit` through `main` requires a run-dir/`--no-run --reason`; required arguments and preconditions are not stated.
8. `atoms show` requires a target atom; sandbox content is unspecified, so the resolvable target is unknown.
9. Each `add <kind>` subcommand's required arguments and valid inputs are not stated.
10. Scope says "new tests only" but also instructs creating new drawer task files — contradiction about in-scope artifacts.
11. Scope says xfail strict is used "where tied to a new drawer task", yet Done When says "suite is green (strict xfails only where tied to a new drawer task)"; unclear whether xfailing tests count as green.
12. "Parametrize where the shape repeats" — the grouping is left to the executor, so test count/structure is unspecified.
13. `desk install` (Implementation Path) vs `python -m deskops desk install <root>` (Resolved Decisions) — different command forms.
14. Open Ambiguities says "None" while contradictions 1–3 exist in the task text itself.
15. Whether the nine `depends_on` tasks are actually closed is not stated.

None.
