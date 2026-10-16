RESTATEMENT:
1. Open `pyproject.toml` and locate the existing `[tool.pytest.ini_options]` table (has `pythonpath`, `asyncio_default_fixture_loop_scope`).
2. Add one key to that table: `testpaths = ["tests"]`. Leave all existing keys unchanged; change no other table.
3. Run `pytest` from repo root; record passed count and green/red.
4. Run `pytest tests` from repo root; record passed count and green/red.
5. Compare: both must be green and report the same passed count.
6. Do not commit; hand the diff to the supervisor for closeout.

AMBIGUITIES:
1. Whether the untracked `tools/` checkout exists in this environment, or whether anything under `tools/` has its own `conftest.py`/`pytest.ini` that could still pull it into the run despite `testpaths`.
2. Whether `pyproject.toml` already contains a `testpaths` key; the task asserts only that other keys exist.
3. Whether any other pytest config source (`pytest.ini`, `tox.ini`, `setup.cfg`) exists and would override `pyproject.toml`; undocumented.
4. "Same passed count" specifies no number, and does not state whether skips/xfails/warnings must also match — "both green" is satisfiable while counts differ through skipped tests.
5. `depends_on: task-rw-f0-declare-runtime-dependencies` — the doc does not state whether that dependency is already closed, so I cannot tell if I may execute now.
6. Status is `deferred`; the doc does not say who flips it to active or whether validation should run before promotion.
7. No acceptance criterion covers the case where `tests/` is empty or collection errors; "green" is undefined for an error-only run.
8. Exact placement/formatting of the new key within the table is unspecified (TOML-semantically irrelevant, but not stated).
