RESTATEMENT:
1. Read `_auto_commit_task_closure` in `deskops/operations.py` (staging at ~1104, `git rm --cached` at ~1113, commit at ~1125-1128) to capture the current flow and rollback points.
2. Compute the path list: the removed task file path, `desk/tasks/Board.md`, and every entry of the task's `files` list where `git status --porcelain -- <path>` prints non-empty. Skip unchanged paths.
3. Keep the `git add -A -- <path>` on those listed paths only (drop staging of unchanged listed files).
4. Read the task file bytes into memory, then replace `git rm --cached -- <task path>` (with `check=False`) by `git rm -- <task path>` with check enabled, so the file is deleted from disk and index before the pathspec commit records the working tree.
5. Commit with a pathspec: `git commit -m <msg> -- <paths>` (amend variant `git commit --amend --no-edit -- <paths>` if that branch shares the call).
6. On any failure: rewrite the task file from the in-memory bytes, restore `desk/tasks/Board.md`, `git restore --staged` the touched paths, and raise `RuntimeError` containing git's stderr.
7. Leave the later untrack/unlink step doing only the untrack, since the file is already removed.
8. In `tests/test_lifecycle_end_to_end.py`, add a test using the throwaway `tmp_path` repo helpers (`_make_repo`, `_cli`) / `lifecycle_desk` fixture: stage an unrelated file with `git add`, create a fixture task via `deskops add task --root <root> '{"id": ..., ...}'`, drive closeout through the CLI.
9. Assert: `git diff --cached --name-only` still lists the unrelated file; `git show --name-only --format= HEAD` does not list it; HEAD's diff deletes the task file.
10. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`; confirm the existing lifecycle test that expects untracked atom/test files in the commit still passes.

AMBIGUITIES:
1. Exact CLI invocation(s) that drive a task to closure (`deskops advance` call count, required flags, node progression) are not specified.
2. Order of `git add -A -- <paths>` relative to `git rm -- <task path>` is not fixed.
3. Which paths `git restore --staged` must target during rollback (all touched paths vs. a subset) is unspecified.
4. Whether the amend invocation in the same commit call must also receive a pathspec, given the amend rule is out of scope.
5. Required `RuntimeError` message format/prefix (to match existing conventions) is not given.
6. Test function name, unrelated-file path, and fixture payload fields beyond the one example are unspecified.
7. Whether directories or glob patterns can appear in the task `files` list (affecting `git add -A` / `git status --porcelain` behavior) is not stated.
8. Path quoting/escaping rules for pathspecs containing spaces or special characters are unspecified.
9. "HEAD's diff deletes the task file" leaves the assertion mechanism open (`--diff-filter=D`, `git show --stat`, etc.).
