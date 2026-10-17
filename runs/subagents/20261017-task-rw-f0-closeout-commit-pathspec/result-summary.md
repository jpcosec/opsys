# result-summary: task-rw-f0-closeout-commit-pathspec

## Changes

`deskops/operations.py` — `DeskopsOperations._auto_commit_task_closure`:

- Builds an explicit commit path list: removed task file (when tracked), `desk/tasks/Board.md`, and only those `files` entries where `git status --porcelain -- <path>` is non-empty.
- Stages only those listed changed paths with `git add -A -- <path>`; Board with `git add -- desk/tasks/Board.md`.
- Reads the task bytes into memory, then `git rm -f -- <task rel>` (checked) so the deletion is in both disk and index before the pathspec commit. `-f` is required because tracked task bundles carry uncommitted lifecycle edits at closeout.
- New-commit branch: `git commit -m <msg> -- <paths>`; trailer-based amend branch: `git commit --amend --no-edit -- <paths>`. Both are pathspec-limited.
- On commit or `git rm` failure: restores the task bytes, rewrites the Board from `board_before`, runs `git restore --staged -- <paths+task>`, and raises `RuntimeError` with git stderr.
- Untracked task bundles (existing test scenario) are not passed to `git rm`/the pathspec (git rejects unknown pathspecs); they remain for the existing untrack/unlink step.
- Untrack/unlink step unchanged.

`tests/test_lifecycle_end_to_end.py` — new test `test_auto_commit_task_closure_commits_only_its_own_paths`:

- New-commit branch: stages `unrelated.txt`, closes a task via the real CLI; asserts the unrelated file is still in `git diff --cached --name-only` and absent from `git show --name-only --format= HEAD`; asserts Board, untracked atom, and untracked test file are in the commit and the task file is deleted (`D` in `--name-status`).
- Amend branch: makes HEAD a same-task closeout commit, stages `unrelated-amend.txt`, closes; asserts HEAD was amended (`HEAD~1` unchanged), unrelated file stays staged and out of the commit, and Board/atom/test/deletion are included.

## Build-up commands (test-first)

1. Added test, ran against unfixed code:
   `PYTHONPATH=/tmp/rw/wt/pathspec python -m pytest tests/test_lifecycle_end_to_end.py::test_auto_commit_task_closure_commits_only_its_own_paths -q`
   Result: `1 failed in 6.96s` — failed at `assert "unrelated.txt" in staged`: unfixed code swept the unrelated staged file into HEAD, leaving no staged changes.
2. Implemented fix.
3. First full-suite run exposed that a tracked task file has local modifications at closeout (`test_show_list_and_advance_task_uses_operational_runtime`); switched `git rm --` to `git rm -f --`. Task text said `git rm --`; `-f` is required for the standard flow.

## Validation commands and final lines

- `PYTHONPATH=/tmp/rw/wt/pathspec python -m pytest tests/test_lifecycle_end_to_end.py -q`
  → `5 passed in 34.15s`
- `PYTHONPATH=/tmp/rw/wt/pathspec python -m pytest tests -q`
  → `346 passed, 3 skipped in 153.93s (0:02:33)`

(Intermediate targeted run: `6 passed in 33.41s`.)

## Task discrepancies / ambiguities

- `git rm -- <task path>` (as specified) fails on tracked task files with uncommitted lifecycle edits; used `git rm -f --`. Without this, `test_show_list_and_advance_task_uses_operational_runtime` fails.
- "The removed task file" can only be part of the pathspec when git tracks it. The existing lifecycle test closes an untracked task file (git rejects unknown pathspecs), so that case keeps the previous behavior: the file is left for the untrack/unlink step.
- Board assertion in the amend scenario required committing the Board's task addition first; otherwise removing the task restores Board content identical to HEAD and it legitimately does not appear in the commit.

## sldb

No sldb issues observed.

## Worktree

Modified only: `deskops/operations.py`, `tests/test_lifecycle_end_to_end.py`. No commits, no staging, no `desk/` mutations.
