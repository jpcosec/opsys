# task-rw-f0-pytest-collects-only-tests — Result

## Changes

- `pyproject.toml`
  - `[tool.pytest.ini_options]`: added `testpaths = ["tests"]`.
  - Existing keys `pythonpath = ["."]` and `asyncio_default_fixture_loop_scope = "function"` kept unchanged.
- No other files changed. No `desk/` edits, no commits, no `git add`.

## Unfixed-code baseline

Command:
```
PYTHONPATH=/tmp/rw/wt/testpaths python -m pytest -q
```
Result line:
```
1 failed, 388 passed, 3 skipped in 180.75s (0:03:00)
```
Failure:
```
FAILED tools/repopackage/tests/test_delivery_fixture.py::test_ecosystem_fixture_resolution_and_validation
```
Reproduced the reported problem: bare `pytest` collected the untracked `tools/` checkout and failed.

Note: the traceback rendered paths under `/home/jp/proyectos/wikipu-ecosystem/repopackage/...`, not `tools/repopackage/...`. Cause is stale `__pycache__/*.pyc` files copied with the checkout (they embed the original source path); the `.py` files themselves are under `tools/repopackage/`. Not modified or deleted, per instructions.

## Validation after the change

`PYTHONPATH=/tmp/rw/wt/testpaths python -m pytest -q` (bare, task validation item "pytest"):
```
337 passed, 3 skipped in 171.64s (0:02:51)
```

`PYTHONPATH=/tmp/rw/wt/testpaths pytest --collect-only -q`:
```
340 tests collected in 0.41s
```
(only `tests/` paths; matches `pytest tests` collection)

`PYTHONPATH=/tmp/rw/wt/testpaths python -m pytest tests -q` (task validation item "pytest tests"):
```
337 passed, 3 skipped in 150.51s (0:02:30)
```

Done When met: bare pytest and `pytest tests` report the same passed count (337 passed, 3 skipped), both green.

## Task accuracy / ambiguities

- No cited line numbers in the task; the `[tool.pytest.ini_options]` table is at `pyproject.toml:30-33` as described. No discrepancy.
- Scope stayed at one added key.
- No sldb issues encountered.
