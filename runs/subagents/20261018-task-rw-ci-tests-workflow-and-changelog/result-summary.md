# Result summary: task-rw-ci-tests-workflow-and-changelog

## Changes

### `.github/workflows/tests.yml` (new)
- Runs on `push` and `pull_request` to `main`.
- One `ubuntu-latest` job with Python 3.12 via `actions/setup-python@v5`.
- Installs `structuredLanguageDB` from `git+https://github.com/jpcosec/sldb.git@main`, then `pip install -e . pytest pytest-asyncio`.
- Sets a global git identity for tests that create commits.
- Runs `python -m pytest tests -q`.
- Per supervisor correction, there is **no kgdb install step**.

### `tests/test_skill_cli_drift.py`
- Added `import pytest` and `PI_SKILLS = ROOT / ".pi" / "skills"`.
- `test_use_deskops_copies_document_the_from_drawer_authoring_path` now calls `pytest.skip(...)` when `.pi/skills` is absent (gitignored, so absent in a clean clone). When `.pi/skills` exists it runs the same two assertions as before.
- Updated the module docstring to record the skip.
- `test_no_skill_document_contains_the_removed_promotion_command` still runs in clean clones because `.opencode/skills` and `.agents/skills` are tracked.

### `CHANGELOG.md` (new)
- Keep a Changelog format with `## [Unreleased]`.
- Groups Added / Changed / Removed / Fixed for the commits in `v-stable-2026.08.29..HEAD`.
- Includes the lifecycle-in-the-graph change and every F0 closeout fix.
- Removed section includes exactly the requested line: "Removed the kgdb dependency; the graph layer now comes from sldb."

## Validation commands and final results

Worktree `/tmp/rw/wt/ci`:

```bash
PYTHONPATH=/tmp/rw/wt/ci python -m pytest tests -q
# 346 passed, 3 skipped in 209.56s

PYTHONPATH=/tmp/rw/wt/ci python -m pytest tests
# 346 passed, 3 skipped in 723.80s

PYTHONPATH=/tmp/rw/wt/ci python -m pytest tests/test_skill_cli_drift.py -q
# 2 passed in 0.01s
```

Fresh clone `/tmp/rw/f0/ci-clone` (no `.pi/`), workflow reproduction with the pending kgdb->sldb migration applied in the clone only:

```bash
/tmp/rw/f0/venv2/bin/python -m pip install "git+https://github.com/jpcosec/sldb.git@main"
/tmp/rw/f0/venv2/bin/python -m pip install -e . pytest pytest-asyncio
/tmp/rw/f0/venv2/bin/python -m pytest tests -q
# 345 passed, 4 skipped in 205.82s
```

The fourth skip is the new `.pi`-absent skip in `tests/test_skill_cli_drift.py`.

## Unfixed-code run

Baseline clone at commit `c1dd728`, fresh venv, full suite before any change:

```text
1 failed, 345 passed, 3 skipped in 272.49s
FAILED tests/test_skill_cli_drift.py::test_use_deskops_copies_document_the_from_drawer_authoring_path
AssertionError: missing use-deskops skill copy: .../.pi/skills/use-deskops/SKILL.md
```

## Task issues and ambiguities

- The original task text says to install kgdb with `pip install --no-deps "git+https://github.com/jpcosec/kgdb.git@1247139"`. The supervisor correction superseded that; the workflow now installs no kgdb.
- The current branch is **not yet migrated off kgdb**: `pyproject.toml` still declares `kgdb>=0.1.0`, `deskops/graph/snapshot.py` imports `kgdb.contracts.io`, `deskops/cli/main.py` imports `kgdb.graph`, and `tests/test_graph_snapshot.py` imports `kgdb.contracts.io`. On this branch the corrected workflow's install step fails, so the clone reproduction above applies the pending migration only inside the throwaway clone:
  ```text
  ERROR: Could not find a version that satisfies the requirement kgdb>=0.1.0 (from deskops) (from versions: 0.0.1)
  ERROR: No matching distribution found for kgdb>=0.1.0
  ```
- With the pending migration applied (`kgdb` imports switched to `sldb.api.graph.snapshot`, dependency removed), the workflow reproduction is green.
- The task's scope lists only `.github/workflows/tests.yml` and `CHANGELOG.md`, so the kgdb->sldb code migration was left to its separate task and is not part of this diff.
- CHANGELOG's "Removed the kgdb dependency" line therefore describes the combined post-migration state, not the current worktree's `pyproject.toml`.
- The original install line `pip install -e . pytest pytest-asyncio` also failed on the pre-migration branch because pip enforces the unmet `kgdb>=0.1.0` requirement; this is not a workflow defect once the migration lands.

## sldb issues

None found. `sldb.api.graph.snapshot` provides `GraphSnapshot`, `load_graph`, and `save_graph` and worked as the kgdb replacement in the clone reproduction.
