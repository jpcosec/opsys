RESTATEMENT:

1. Open `deskops/operations.py`; locate `_auto_commit_task_closure` (rationale cites ~1490-1552).
2. Identify the "removed bundle paths" currently passed to the `git rm --cached` calls (~line 1537).
3. Compute the commit path list = removed bundle paths + `desk/tasks/Board.md` + each entry of the task's `files` list for which `git status --porcelain -- <path>` prints output.
4. Replace the unconditional staging at ~line 1518 with `git add -A -- <path>` applied only to that computed path list.
5. Change the commit call to `git commit -m <msg> -- <paths>`.
6. Change the amend call to `git commit --amend --no-edit -- <paths>`.
7. Change the `git rm --cached` calls (~line 1537) to check the return code instead of `check=False`; on failure run the existing failure branch (restore `desk/tasks/Board.md`, unstage, raise `RuntimeError` including git stderr).
8. Add one test in `tests/test_lifecycle_end_to_end.py` using the `_make_repo`/`_cli` helpers: init throwaway repo, `desk install`, create a task via `deskops add task`, stage an unrelated file, close the task through the real CLI, assert the unrelated file is still listed by `git diff --cached --name-only` and absent from `git show --name-only --format= HEAD`.
9. Confirm the existing lifecycle test (which lists an untracked atom and test file) still commits those files.
10. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
11. Do not commit; hand diff to supervisor.

AMBIGUITIES:

1. The "removed bundle paths" set is not enumerated; must be inferred from existing code.
2. The exact CLI invocation that "closes a task" (`deskops advance` args, task id, run state) is unspecified.
3. How to detect the "amending" case is not stated (the amend rule itself is out of scope in task-rw-f0-close-only-own-primitives).
4. Whether pathspecs and `git status --porcelain` run relative to repo root or cwd is not stated.
5. Behavior when the computed path list is empty is not specified.
6. Path-list ordering/dedup is not specified.
7. Failure-branch behavior when one `git rm --cached` succeeds and a later one fails (restore/unstage ordering) is not specified.
8. Whether `desk/tasks/Board.md` is included even when unchanged is implied but not explicit.
9. "Restore the Board" mechanism (e.g. `git checkout --`, `git restore`) is not stated.
10. Whether dependency `task-rw-f0-merge-retarget-whole-tokens` is complete/merged is not known.
11. The unrelated file's path/type and the cwd for the assertion commands are not specified.
