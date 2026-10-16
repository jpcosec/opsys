RESTATEMENT:

1. Confirm dependency `task-rw-f0-declare-runtime-dependencies` is complete, and confirm the task has been promoted from `desk/drawer/tasks/` to `desk/tasks/` (supervisor step, per Resolved Decisions).
2. Open `pyproject.toml` and locate the existing `[tool.pytest.ini_options]` table (known keys: `pythonpath`, `asyncio_default_fixture_loop_scope`).
3. Add one key: `testpaths = ["tests"]` inside that table; leave all other keys unchanged.
4. Do not modify `tools/`, test files, or any other file.
5. Run `pytest tests` from repo root; record passed count.
6. Run bare `pytest` from repo root; confirm it collects only `tests/` and reports the same passed count as step 5, both green.
7. Report the diff (`pyproject.toml` only) and both command outputs to the supervisor; do not commit.
8. Supervisor makes the closeout commit via `deskops closeout commit --task task-rw-f0-pytest-collects-only-tests --run-dir <dir>` (or `--no-run --reason <why>`), requiring `pytest tests` green.

AMBIGUITIES:

1. Task header says `status: deferred` and `source:drawer`, yet Resolved Decisions assume promotion to `desk/tasks/` before dispatch — current dispatchability is unclear.
2. `depends_on: task-rw-f0-declare-runtime-dependencies` is itself `status: deferred`; whether that dependency is satisfied is not stated and cannot be verified from the task doc.
3. Done When requires "both are green", but no baseline is given for whether `pytest tests` currently passes; if it is red, the task cannot close.
4. No criterion for what bare `pytest` previously collected, so "collects only `tests/`" is only verifiable by comparing collection output, which is not specified.
5. Whether other pytest config (e.g., `norecursedirs`, CI config) also needs to exclude `tools/` is out of scope per Scope, but nothing states CI uses bare `pytest`.
6. `<dir>` for `--run-dir` in the closeout command is unspecified.
7. No instruction on whether `pyproject.toml` formatting/ordering of keys matters for review.
