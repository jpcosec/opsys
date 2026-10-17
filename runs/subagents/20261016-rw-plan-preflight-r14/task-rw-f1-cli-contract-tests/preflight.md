RESTATEMENT:
1. Read `deskops/cli/parser.py:67-89` to get exact argument signatures for the 8 targets: `add faq-doc`, `atoms list`, `atoms show`, `runtime init`, `runtime status`, `runtime attach`, `runtime stop`, `runtime supervise`.
2. Read `tests/conftest.py` to learn the `lifecycle_desk` fixture's API (name, what path it yields, what state the sandbox is in).
3. Read `tests/test_cli.py:1124` for the in-process `main([...])` call pattern and `tests/test_herdr_runtime.py` for the Herdr stub pattern.
4. Create `tests/test_cli_contract.py`.
5. For each subcommand, add a test that: obtains the sandbox root from `lifecycle_desk`, calls `deskops.cli.main.main([...])` in-process with `--root <sandbox>` and the subcommand args, captures stdout/stderr via `capsys`, and asserts exit code plus one stable output line.
6. For `runtime init|status|attach|stop|supervise`, stub the Herdr client the same way `tests/test_herdr_runtime.py` does so no real Herdr starts; possibly parametrize the runtime shapes.
7. Run `pytest tests/test_cli_contract.py`, then `pytest tests`.
8. For any subcommand that crashes/misbehaves, create a new drawer task file under `desk/drawer/tasks/` and mark that test `pytest.mark.xfail(strict=True, reason='<task id>')`.

AMBIGUITIES:
1. "One stable line of output" per subcommand is unspecified; the exact line and exit code must be discovered by running each command, so acceptance depends on observation not the task text.
2. Contradiction: Scope says "record each surprise as a new drawer task file" (mutates repo `desk/drawer/`), but Resolved Decisions says "Never mutate the repo's own `desk/`".
3. Contradiction: Resolved Decisions says "the executor does not commit", so newly created drawer task files would be left uncommitted; task does not say who commits them.
4. Scope says "parametrize where the shape repeats" but Done When requires "its own test" per subcommand; unclear whether a parametrized case counts as "its own test".
5. `atoms show` requires an atom identifier; no atom in the `lifecycle_desk` sandbox is named, so what to pass is unknown.
6. `runtime attach` requires a target (worker id?); not specified.
7. `runtime supervise` likely blocks/loops; how to run it in-process without hanging is not specified.
8. `runtime init` expected exit code ambiguous if `deskops init` (or `lifecycle_desk`) already initializes runtime, vs a fresh repo.
9. `add faq-doc` argument shape (path vs inline content) not stated.
10. Herdr stub target for in-process `main` may differ from `test_herdr_runtime.py`'s pattern (which may assume subprocess); instruction assumes they are interchangeable.
11. Whether `main([...])` argv includes the program name (`'deskops'`) or starts at the subcommand is not stated; only inferrable from `test_cli.py:1124`.
12. Drawer task file naming/path convention under `desk/drawer/tasks/` is unspecified.
13. `lifecycle_desk` fixture vs Resolved Decisions default `_make_repo`/`_cli` subprocess helper: task says use the fixture, but the mapping of fixture output to required `--root` value is not written.
14. No defined behavior if a command is already covered or absent, though Rationale asserts the 8 list is exhaustive as of 2026-10-16.
