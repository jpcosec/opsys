RESTATEMENT:
1. Read `pyproject.toml`; locate the existing `[tool.pytest.ini_options]` table.
2. Add the single key `testpaths = ["tests"]` to that table, leaving `pythonpath` and `asyncio_default_fixture_loop_scope` unchanged.
3. From repo root, run bare `pytest` and confirm collection is limited to `tests/` and the run is green.
4. Run `pytest tests` and confirm it is green with the same passed count as step 3.
5. Do not commit; leave the diff for the supervisor.
6. Report the diff and both command outputs; supervisor closes with `deskops closeout commit --task task-rw-f0-pytest-collects-only-tests --run-dir <dir>` or `--no-run --reason <why>`.

AMBIGUITIES:
1. The task status is `deferred` and `depends_on` `task-rw-f0-declare-runtime-dependencies` is also deferred; it is unstated whether this task may be executed now.
2. Goal and Scope contain only template placeholder text; only the title, Rationale, Implementation Path, and Done When define the deliverable.
3. "Same passed count" has no recorded baseline number, so equality cannot be verified against a written value.
4. If `pytest tests` collects or imports the untracked `tools/` checkout (e.g. via rootdir conftest, imports, or plugin autoload), "same passed count" may be unsatisfiable by `testpaths` alone; no fallback (e.g. `--ignore`, `norecursedirs`) is specified.
5. TOML formatting expectations are unstated: whether key ordering, line style (inline array vs multi-line), and quoting must match existing table conventions.
6. Validation lists `pytest` and `pytest tests` but does not state whether failures inside `tools/` triggered by `pytest tests` count against the task.
7. No acceptance criterion is given for warning/error counts (only passed count), so a green run with new warnings is neither required nor forbidden.
8. Whether `tests/` exists at the repo root and is currently collectible is not stated in the task document.
