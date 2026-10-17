RESTATEMENT:
1. Open `deskops/operations.py`, read `_auto_commit_task_closure` (~1086–1130): locate the `head_subject` fetch, the `head_subject.startswith(f"closeout: {task_id}")` amend gate (~1123), and the commit-message build emitting `Task-Id: <id>` (~1115).
2. Replace the amend gate with a trailer read: run `git log -1 --format=%(trailers:key=Task-Id,valueonly)` in the repo, strip the output, and amend only when it `== task_id`.
3. Ensure empty/missing trailer output means "no amend" (new commit path taken).
4. Leave the closeout commit message unchanged (it already carries `Task-Id: <id>`).
5. In `tests/test_lifecycle_end_to_end.py`, add one regression test using `_make_repo` / `_cli`: init repo, create fixture task `task-foo` via `deskops add task --root <root> '{"id": "task-foo", ...}'` (CLI-created, tracked/routed), and make HEAD a commit with subject `closeout: task-foo-bar` and trailer `Task-Id: task-foo-bar`.
6. Drive closeout of `task-foo` through the real CLI (subprocess `[sys.executable, '-m', 'deskops', ...]`) so `_auto_commit_task_closure` runs.
7. Assert HEAD~1 equals the fixture `task-foo-bar` commit (i.e., a new commit was created rather than amending).
8. Run `pytest tests/test_lifecycle_end_to_end.py`.
9. Run `pytest tests`.
10. Confirm the new test fails on unmodified code and passes after the fix.

AMBIGUITIES:
1. Which exact CLI invocation reaches `_auto_commit_task_closure` (lifecycle `advance`/closeout vs `deskops closeout commit --task ...`) is not stated; the test must guess the command that triggers auto-commit.
2. Whether `closeout commit` needs `--run-dir` or `--no-run --reason` in this test is unspecified.
3. Closeout preconditions are unstated: whether closing `task-foo` requires `done_when`/validation satisfied, a clean worktree, or staged/untracked state for the commit path to run.
4. No stated check that the amend gate is not also guarded by other conditions in `_auto_commit_task_closure` (e.g., run dir presence), which could bypass the new trailer logic.
5. Whether a positive-path assertion (HEAD trailer == task_id still amends) is required is unstated; scope says one regression test only.
6. Minimum git version supporting `%(trailers:key=...)` (≥2.32) is not stated as a constraint.
7. Whether the fixture commit must be created via raw git or through deskops is unspecified (implementation path implies raw git is acceptable).
8. Concrete assertion form for "HEAD~1 is that commit" (hash compare vs subject compare) is unspecified.
9. Cited line numbers may have drifted; the task does not say whether to rely on them or locate by symbol.
