RESTATEMENT:

1. Read `deskops/operations.py` around `_auto_commit_task_closure` (lines ~1500-1560) and `tests/test_lifecycle_end_to_end.py` (`_make_repo`, `_cli` helpers) to understand current staging/commit flow.
2. In `_auto_commit_task_closure`, build an explicit path list:
   - the removed bundle paths (the paths being `git rm --cached`'d, ~line 1537),
   - `desk/tasks/Board.md`,
   - each entry in the task's `files` list for which both `git ls-files --error-unmatch -- <path>` succeeds AND `git diff --name-only HEAD -- <path>` prints it.
3. Restrict the existing `git add` (currently at operations.py:1518, adding every listed file) to only paths that pass the above filter.
4. Change `git rm --cached` calls (line ~1537) to use a checked return code (`check=True`); on failure take the existing failure branch: restore the Board, unstage, raise `RuntimeError` with git's stderr.
5. Commit with `git commit -m <msg> -- <paths>`; when amending, use `git commit --amend --no-edit -- <paths>`.
6. Add a test in `tests/test_lifecycle_end_to_end.py` following the `_make_repo`/`_cli` pattern:
   - build throwaway repo in `tmp_path` (git init, seed commit), `python -m deskops desk install <root>`,
   - create a fixture task via `deskops add task --root <root> '{"id": ..., ...}'` (explicit id),
   - stage an unrelated file,
   - close the task through the CLI,
   - assert unrelated file still staged via `git diff --cached --name-only` and absent from `git show --name-only --format= HEAD`.
7. Run `pytest tests/test_lifecycle_end_to_end.py` then `pytest tests`; confirm new test passes, existing lifecycle test still commits the task's files, suite green.
8. Do not commit; supervisor reviews diff and runs `deskops closeout commit`.

AMBIGUITIES:

1. "removed bundle paths" — the doc never defines what a "bundle path" is or where the removal list comes from; I would have to infer it from the existing `git rm --cached` calls at operations.py:1537 and the surrounding routine/bundle logic.
2. What `<msg>` is for the commit is unspecified; must be read from existing code.
3. "existing failure branch (restore the Board, unstage, raise RuntimeError)" — the exact ordering/scope of "restore the Board" and "unstage" is not defined in the document; must be reverse-engineered from current code.
4. Behavior when the task's `files` list is empty or when `desk/tasks/Board.md` is not in the task's `files` list is not stated (doc says Board.md is always included, but does not say whether that overrides the tracked-and-differing filter for Board.md specifically).
5. The doc says commit includes "the removed bundle paths, `desk/tasks/Board.md`, and those entries of the task's `files` list that git tracks and that differ from HEAD" — but does not say whether bundle paths and Board.md themselves are subject to any tracked/differing filter, or always committed as-is.
6. `depends_on: task-rw-f0-merge-retarget-whole-tokens` — no indication whether that dependency is already satisfied; cannot tell if prerequisites are met.
7. Amend rule is declared out of scope, but the Implementation Path step 5 says to use `--amend --no-edit -- <paths>` when amending; unclear how the amend branch is triggered or how to test it without touching the explicitly out-of-scope amend rule.
8. Task status is `deferred`; no acceptance criteria clarify what un-defers it.
9. "one test" in scope vs. Done When mentioning "the existing lifecycle test still commits the task's files" — unclear whether existing tests require modification or only the new test is added.
