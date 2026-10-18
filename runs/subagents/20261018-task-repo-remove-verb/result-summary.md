# result-summary: task-repo-remove-verb

## What changed

- `deskops/cli/commands/repo.py`
  - `RepoCLI.run`: dispatches `repo_command == "remove"`.
  - `RepoCLI.remove`: resolves the registry entry by id, filename stem, or `repo-<id>`; returns 1 with the known ids when missing; returns 1 on ambiguous matches; otherwise deletes the registry file and untracks its RepositoryDoc through one `doc_io.DocTransaction(root)` and prints the deleted path.
- `deskops/cli/registry.py`
  - Added `("repo", "remove")` `Command` with `selector`, `--root`, `--store`, `mutates=True`.
- `tests/test_command_registry.py`
  - Added `("repo", "remove")` to `MUTATING_COMMANDS`.
- `tests/test_registry_robustness.py`
  - `_init_ecosystem` helper.
  - `test_repo_remove_then_register_same_path_under_correct_id`: real store via `SLDBBootstrap().init_local_store`, registers `graph-ui`, verifies tracking, removes it, verifies the file and tracking are gone, checks a missing selector exits 1, re-registers the same root as `graph_ui --id graph_ui`, and checks `repo whoami` prints `graph_ui`.
  - `test_repo_remove_missing_id_lists_existing_ids`: missing selector exits 1 and names existing ids.
- `tests/fixtures/golden/help/deskops_repo.txt` (modified) and `tests/fixtures/golden/help/deskops_repo_remove.txt` (new), refreshed with `pytest --update-golden`.

No commit, no `git add`, no deskops mutation of this worktree's `desk/`.

## Validation

- `PYTHONPATH=/tmp/rw/wt/repormv python -m pytest tests/test_repo_identity.py tests/test_registry_robustness.py tests/test_command_registry.py -q`
  - `16 passed in 3.79s`
- `PYTHONPATH=/tmp/rw/wt/repormv python -m pytest tests -q`
  - `519 passed, 3 skipped in 804.50s (0:13:24)`
- `PYTHONPATH=/tmp/rw/wt/repormv python -m deskops --help`
  - exit 0.
- Help golden refresh (needed after registry change):
  - `PYTHONPATH=/tmp/rw/wt/repormv python -m pytest tests/test_output_goldens.py::test_help_goldens -q --update-golden`
  - `1 passed in 123.23s (0:02:03)`

## Test against unfixed code

Extracted `HEAD` with `git archive HEAD` into `/tmp/repormv-unfixed`, copied only the new `tests/test_registry_robustness.py`, and ran:

`PYTHONPATH=/tmp/repormv-unfixed python -m pytest tests/test_registry_robustness.py -q -k repo_remove`

Result: `2 failed, 3 deselected in 3.25s` (both new tests fail because `repo remove` is not registered).

## Task issues / ambiguities

- Goal says `deskops repo remove <id> --root <repo>`, while `repo register` is anchored by `--store`. Implemented both flags: `--root` selects the desk tree; `--store` is still accepted and `resolve_context` maps it back to its project root.
- The default id slug replaces underscores with hyphens, so `repo register graph_ui ...` needs the explicit `--id graph_ui` (as the rationale already shows). Tests use the explicit id.
- No sldb bug found; no sldb files changed.
