RESTATEMENT:
1. Confirm `task-rw-f0-declare-runtime-dependencies` is closed, since this task `depends_on` it.
2. Open `pyproject.toml`; locate the existing `[tool.pytest.ini_options]` table and verify it currently contains `pythonpath` and `asyncio_default_fixture_loop_scope`.
3. Add `testpaths = ["tests"]` to that table, leaving all other keys unchanged.
4. Run `pytest tests` from the repo root; record the passed count; require green.
5. Run bare `pytest` from the repo root; confirm collection is limited to `tests/` and record the passed count; require green.
6. Verify the two passed counts are equal and both runs are green.
7. Do not commit; report the diff to the supervisor for promotion/closeout.

AMBIGUITIES:
1. How to verify the `depends_on` task is actually complete (no status-check command or gate is specified).
2. "Same passed count" — whether it means only the pass count, or also identical collected/skipped/deselected counts.
3. Whether the `tools/` checkout exists in the validation environment; if it is absent, bare `pytest` is trivially green and the fix is unverified.
4. No specified command/proof that bare `pytest` no longer collects `tools/` (e.g., `pytest --collect-only` output check); only counts are compared.
5. Whether `testpaths` alone is sufficient, or `norecursedirs`/`rootdir` changes are also needed, is not stated.
6. `status: deferred` conflicts with Resolved Decisions stating the supervisor promotes it to `desk/tasks/` before dispatch; which state the executor actually receives it in is unclear.
7. Exact TOML key ordering/formatting within the table is not specified.
8. Who runs the closeout-time `pytest tests` check (executor vs supervisor) and when is not specified beyond "green required".
