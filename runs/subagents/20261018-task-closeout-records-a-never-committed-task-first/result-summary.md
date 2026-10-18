# Result: task-closeout-records-a-never-committed-task-first

## Changes

- `deskops/services/closure.py`
  - `ClosureService._close`: before the `DocTransaction`, calls `_record_uncommitted_task(task_id, task_path, task_rel)` when the task file exists on disk.
  - `ClosureService._in_head(path)`: new helper; wraps `git cat-file -e HEAD:<path>` (replaces the inline check at the removal step).
  - `ClosureService._record_uncommitted_task(...)`: new helper. Returns immediately if the task is in HEAD; otherwise runs `git add -- <task_rel>` and `git commit -m "desk: registra <stem>\n\nTask-Id: <id>\nCloseout-Mode: record" -- <task_rel>`, so only that path is committed and other staged changes stay staged.
  - The closing-commit amend check now reads `Closeout-Mode` from HEAD and refuses to amend when it is `record`: `if head_task_id == task_id and head_mode != "record"`. HEAD after the record commit therefore becomes the parent of a new closing commit instead of being amended into the record commit.
- `tests/test_closeout.py`
  - Added `test_closeout_records_a_never_committed_task_before_the_closing_commit`: asserts two commits (`closeout: task-x`, then `desk: registra task-x`), record trailers, task body readable via `git show HEAD~1:desk/tasks/task-x.md`, task removed, clean tree.
  - Added `test_closeout_committed_task_keeps_a_single_closing_commit`: asserts one closing commit, no record commit, clean tree.
- `tests/test_lifecycle_end_to_end.py`
  - `test_closeout_amends_only_head_with_its_own_task_id`: adapted the existing assertion for the now-expected record commit. It still proves no amend of another task's closeout: `HEAD~1` is the `desk: registra task-foo` record commit and its parent is `other_closeout`.

## Validation (all run with the required PYTHONPATH prefix)

- `PYTHONPATH=/tmp/rw/wt/recordfirst python -m pytest tests/test_closeout.py -q` -> `47 passed in 6.43s`
- `PYTHONPATH=/tmp/rw/wt/recordfirst python -m pytest tests -q` -> `537 passed, 3 skipped in 718.95s (0:11:58)`
- Manual sandbox check of `closeout supersede` on a never-committed task (`/tmp/rw/f0/sandbox-supersede`): produced `desk: registra task-y` (`Task-Id`, `Closeout-Mode: record`) followed by `closeout: task-y` (`Closeout-Mode: superseded`); body readable at `HEAD~1`; working tree clean apart from the untracked `.deskops.log`.

## Test against unfixed code

- Command: `PYTHONPATH=/tmp/rw/wt/recordfirst python -m pytest tests/test_closeout.py -q -k "never_committed or committed_task_keeps"`
- Result before the fix: `1 failed, 1 passed, 45 deselected`; the never-committed test failed because only `['closeout: task-x']` existed (`Right contains one more item: 'desk: registra task-x'`).

## Exact sentence for `desk/rituals/closeout.md` purpose (apply via `deskops edit ritual ritual-closeout`, do not hand-edit)

When a closed task was never committed, the closeout first records its body in one commit (`desk: registra <task stem>`, with `Task-Id` and `Closeout-Mode: record` trailers) before the closing commit removes it, so the task's rationale, goal, scope, validation, and done-when stay in git history.

## Notes / ambiguities

- No sldb bug observed; no sldb files were touched.
- The task's Validation list did not anticipate the existing end-to-end assertion in `tests/test_lifecycle_end_to_end.py`, which assumed the closing commit's parent was the previous unrelated closeout. It needed the one-line adaptation above to stay green; the assertion's intent is preserved.
- The record commit intentionally carries `Task-Id`, so the amend guard must key on `Closeout-Mode`, not on the absence of `Task-Id`; implemented as described in Implementation Path step 4.

## Supervisor note
The sentence for the ritual was added to the closeout ritual's purpose with `deskops edit ritual ritual-closeout purpose`.
