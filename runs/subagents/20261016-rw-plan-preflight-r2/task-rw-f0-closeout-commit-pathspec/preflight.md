RESTATEMENT:

1. Read `deskops/operations.py` around the `_auto_commit_task_closure` body (docs cite lines ~1537 for `git rm --cached` and ~1549-1552 for `git commit -m`) to see how removed bundle paths are derived, how the task's `files` are known in that scope, and how the Board path is referenced today.
2. Replace the bare `git commit -m <msg>` call with `git commit -m <msg> -- <paths>`, where `<paths>` = removed bundle paths + `desk/tasks/Board.md` + each entry of the task's `files` that git reports as changed.
3. Apply the same pathspec to the amend invocation: `git commit --amend --no-edit -- <paths>`.
4. Change the `git rm --cached` calls to use a checked return code; on nonzero, execute the existing failure branch: restore the Board, unstage, and raise `RuntimeError` including git's stderr.
5. In `tests/test_lifecycle_end_to_end.py`, reuse `_make_repo` and `_cli` to build a throwaway repo in `tmp_path` (`git init`, one seed commit, `python -m deskops desk install <root>`).
6. In the new test, stage an unrelated file, close a task through the CLI, then assert via `git diff --cached --name-only` that the unrelated file is still staged, and via `git show --name-only --format= HEAD` that it is absent from the closeout commit.
7. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`.
8. Do not make a closeout commit; leave the diff for the supervisor.

AMBIGUITIES:

1. "task's `files` that have changes" is undefined: changed vs HEAD, changed vs index, or staged-only? Which command (`git diff --name-only`, `git diff --cached --name-only`, `git status --porcelain`) decides membership?
2. Whether a file in `files` that is only unstaged-modified should be implicitly committed by the pathspec (partial-commit semantics) or excluded.
3. Whether untracked files, deletions, or renames in `files` count as "changed."
4. "Removed bundle paths" is not defined here (what generates the bundle list, and whether it is file paths or already-staged deletions) — needs reading of `_auto_commit_task_closure`.
5. `git rm --cached` "checked return code" mechanism unspecified: `check=True` raises `CalledProcessError` before the custom `RuntimeError`, so how to capture stderr and route to the failure branch is undefined.
6. The existing failure branch (restore Board, unstage, raise) is referenced but not shown; its exact restore/unstage scope and message format are unknown.
7. Contradiction: amend is listed out of scope ("the amend rule" is another task) yet Implementation Path step 2 requires editing the amend invocation.
8. `desk/tasks/Board.md` is hardcoded, but the resolved decisions scaffold desk into a temp root; whether the Board path is root-relative or configurable via the desk root is unstated.
9. Test command is "close a task through the CLI" but the rationale names `deskops advance`; whether to drive `advance` (vs any close path) is ambiguous.
10. `git diff --cached --name-only` and `git show --name-only --format= HEAD` exact assertions are given, but there is no assertion that the task's own files and Board were committed.
11. Empty pathspec case: behavior when the computed path list is empty (`git commit -- ` with no paths) is unspecified.
12. `depends_on: task-rw-f0-merge-retarget-whole-tokens` status is not stated, so whether the target lines are already changed by that task is unknown.
13. Line numbers (1537, 1549-1552) may be stale if the dependency task landed; no function anchor is given beyond the name.
