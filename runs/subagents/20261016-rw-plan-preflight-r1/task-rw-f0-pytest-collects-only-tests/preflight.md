RESTATEMENT:
1. Read `pyproject.toml`; locate `[tool.pytest.ini_options]`.
2. If the table exists, add `testpaths = ["tests"]` to it; if not, create the table with that key.
3. From repo root, run `pytest` with no arguments and record collected count/result.
4. Run `pytest tests` and compare collected count and exit status.
5. Confirm bare `pytest` is green and matches `pytest tests`; stop.

AMBIGUITIES:
1. Task `status: deferred` and `depends_on: task-rw-f0-declare-runtime-dependencies` — no indication whether that dependency is complete or whether this task may execute now.
2. "the untracked `tools/` checkout" — no statement of whether `tools/` exists in this workspace, so I cannot know what currently fails.
3. No instruction on whether `[tool.pytest.ini_options]` already exists in `pyproject.toml` or what it contains; overwriting/merging behavior is guesswork.
4. Whether restricting collection to `tests/` should intentionally exclude any real tests under `tools/` is unstated.
5. "Open Ambiguities: None" contradicts items 1–4; no resolution rule is given.
6. No acceptance criterion for what happens to `tools/` test failures after the change (hidden vs. still runnable).
7. `Validation` lists bare `pytest` only; unclear whether `pytest tests` comparison is required evidence or just informal.
8. No mention of committing the change, though repo policy requires a task-closing commit.
