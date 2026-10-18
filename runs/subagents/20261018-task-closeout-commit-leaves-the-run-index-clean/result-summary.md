# Result summary — `closeout commit` leaves the run index clean

## What changed

- `deskops/services/closure.py`
  - `ClosureService`: added a docstring describing the index rule (entry names the task/run; `commit` is null; resolve via `git log --grep 'Task-Id: <id>'`).
  - `ClosureService._close`: after the closing commit is made, append the index entry with `commit: null`, stage `runs/subagents/index.jsonl`, and fold it into the same closing commit with one `git commit --amend --no-edit -- <index-rel>`. On failure the previous index bytes are restored and the path is unstaged. Both `--run-dir` and `--no-run` routes take this path.
- `deskops/cli/commands/closeout.py`: `CloseoutCLI` docstring updated (no longer claims the hash is recorded).
- `deskops/cli/registry.py`: `closeout commit` epilog updated with the same rule.
- `tests/fixtures/golden/help/deskops_closeout_commit.txt`: regenerated for the epilog text.
- `tests/test_closeout.py`
  - Run-linked and manual tests assert `entry["commit"] is None` and resolve the closing commit via `git log -1 --grep 'Task-Id: task-x'`.
  - Manual test now expects `runs/subagents/index.jsonl` in the closing commit.
  - New parameterized test `test_closeout_commit_leaves_the_working_tree_clean[run-dir|no-run]`: asserts `git status --porcelain` is empty, the index file is tracked, `task_id` is recorded, `commit` is null, and the HEAD resolves from the Task-Id trailer.

## Validation

Final tree, exact task commands:

- `PYTHONPATH=/tmp/rw/wt/index python -m pytest tests/test_closeout.py -q`
  - Before fix: `5 failed, 16 passed in 3.05s` (new clean-tree test failed with `assert '?? runs/' == ''`).
  - Final: `21 passed in 4.38s`.
- `PYTHONPATH=/tmp/rw/wt/index python -m pytest tests -q`
  - Final: `451 passed, 3 skipped in 802.68s (0:13:22)`.
- `PYTHONPATH=/tmp/rw/wt/index python -m deskops closeout commit --help` → rc 0 (help golden test also green).

## Notes on the task text / environment

- The Goal says the index still records the closing commit hash, but the Implementation Path correctly notes that amending changes the hash. Chose the path's option: `commit: null` plus resolution via the `Task-Id` trailer. No production reader of the `commit` field exists (only tests/goldens did).
- Pre-existing unrelated breakage: `desk/drawer/tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md` had no YAML front matter, so `tests/test_taskdoc_read_without_overlay.py` failed at HEAD. Added minimal front matter so the suite can be green.
- The sibling `sldb` checkout changed extraction semantics during this session (notably `9dcabd9a`, `d31180e4`), which temporarily reddened `test_doc_readability`, `test_lifecycle_graph`, and command-output goldens. Aligned those tests/goldens with current sldb, using the same adaptations already present in the main deskops checkout. The final live-sldb full run is green.
- No confirmed sldb bug found; nothing under sldb was modified.

## Supervisor note

Only the task's own files were integrated: closure.py, closeout.py, registry.py, the closeout commit help golden and tests/test_closeout.py. The worker had also repaired the release drawer task and the sldb-driven goldens; main already had those fixes (25c0149, 623f6c7).
