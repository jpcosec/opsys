RESTATEMENT:
1. Open `deskops/operations.py`, function `_auto_commit_task_closure` (staging ~line 1104, `git rm --cached` ~line 1113, commit ~lines 1125–1128).
2. Build the committed path set: the removed task file, `desk/tasks/Board.md`, plus each entry of the task's `files` list for which `git status --porcelain -- <path>` prints output (including `??` untracked).
3. For those paths only, replace the current "add every listed file" call with `git add -A -- <path>` per path.
4. Run the `git rm --cached` call(s) with a checked return code; on failure execute the existing failure branch: restore the Board, unstage, `raise RuntimeError` including git's stderr.
5. Commit with `git commit -m <msg> -- <paths>`; when amending, `git commit --amend --no-edit -- <paths>`, so unrelated staged changes remain staged and excluded.
6. Add one test in `tests/test_lifecycle_end_to_end.py` using `_make_repo`/`_cli`: build the throwaway repo, stage an unrelated file, create and close a task through the CLI, then assert the unrelated file is still listed by `git diff --cached --name-only` and absent from `git show --name-only --format= HEAD`.
7. Confirm the existing lifecycle test still commits its listed untracked atom and test file.
8. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`.

AMBIGUITIES:
1. Contradiction: Scope excludes "the amend rule" but Implementation Path step 2 tells you to implement `git commit --amend --no-edit -- <paths>`. Whether to touch amend now is unresolved.
2. "Checked return code" on `git rm --cached` is unspecified: `check=True` (raises) vs. manual `returncode` inspection invoking the failure branch.
3. Ordering unspecified: is the `git status --porcelain` filter evaluated before or after `git add -A`? If after, pre-staged changes to a listed file appear as "a change" and get pulled in, contradicting "unrelated staged changes stay out."
4. Whether the removed task file and `desk/tasks/Board.md` are included unconditionally or also gated on `git status --porcelain` printing something.
5. Board path is written as `desk/tasks/Board.md`; unclear if hardcoded or derived (drawer vs desk location).
6. What "restore the Board, unstage" concretely resets is not specified, nor whether that failure branch already exists.
7. Exact CLI invocation that "closes a task through the CLI" is not given; the fixture task starts at `ritual-execution`, so the required advance sequence is unknown.
8. The commit message `<msg>` is not stated (assumed the existing `closeout: <task>` string).
9. Behavior when the computed path list is empty (no changes) is unspecified.
10. Whether `git add -A -- <path>` also runs for the removed task file (staging a deletion) or only for `files` entries.
11. How the task's `files` list is accessed inside `_auto_commit_task_closure` (field/attribute name) is not given.
12. Whether the `git rm --cached` call(s) are still required at all under the new pathspec-based commit.
