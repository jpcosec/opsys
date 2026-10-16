RESTATEMENT:

1. Confirm dependency `task-rw-f0-declare-runtime-dependencies` is closed and this task has been promoted from `desk/drawer/tasks/` to `desk/tasks/` (status `deferred` → active).
2. Open `pyproject.toml`; locate the existing `[tool.pytest.ini_options]` table and confirm keys `pythonpath` and `asyncio_default_fixture_loop_scope` are present.
3. Add `testpaths = ["tests"]` to that table; keep all other keys unchanged.
4. From repo root, run bare `pytest`; record collected/passed count and exit code.
5. From repo root, run `pytest tests`; record collected/passed count and exit code.
6. Verify both runs are green and report the same passed count.
7. Do not modify anything under `tools/`.
8. Do not commit; hand the diff to the supervisor for closeout.
9. Before closeout, re-run `pytest tests` to confirm it is green (closeout requirement).

AMBIGUITIES:

1. `status: deferred` + `source:drawer` vs. "Resolved Decisions" saying the supervisor promotes before dispatch: unclear whether this task is dispatchable now or blocked until promotion.
2. Dependencies are not verifiable from this document: `task-rw-f0-declare-runtime-dependencies` has no acceptance info or stated completion state.
3. No baseline test counts are given, so "same passed count as `pytest tests`" cannot be checked against a known before/after value.
4. `Rationale`, `Goal`, `Scope`, and `Implementation Path` bodies are unfilled template placeholders; intent is inferred only from the title, one-line plan, and the single-line implementation path.
5. No stated acceptance criterion for exit codes, warnings, or errors — only "green" and equal passed count.
6. Current contents of `[tool.pytest.ini_options]` cannot be confirmed from the document, so "keeping its other keys" cannot be verified.
7. Whether `tools/` contains a `conftest.py`/`pytest.ini` that affects rootdir or collection even after adding `testpaths` is unspecified.
8. No statement on which working directory or invocation (`python -m pytest` vs `pytest`) counts as "bare `pytest`".
9. Where the test count comes from (which counts as passed vs. skipped/xfailed) is undefined.
10. The bound pill `pill-real-cli-surfaces-prove-operator-contracts.md` is about CLI surfaces, but the change is pytest config; its applicability is unstated.
11. No instruction on whether adding `testpaths` interacts with the existing `pythonpath` key (import rootdir behavior) and whether that must be validated.
