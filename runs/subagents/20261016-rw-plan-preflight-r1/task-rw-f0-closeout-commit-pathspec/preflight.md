RESTATEMENT:
1. Locate `_auto_commit_task_closure` in `deskops/operations.py` (doc cites ~line 1552) and read how it currently stages, commits, and handles failure.
2. Identify the exact path set: (a) removed task-bundle paths produced by the existing removal logic, (b) `desk/tasks/Board.md`, (c) each entry in the closing task's `files` frontmatter list.
3. Replace the bare `git commit -m <msg>` with `git commit -m <msg> -- <paths...>`; for the amend branch use `git commit --amend --no-edit -- <paths...>`.
4. Change the `git rm --cached` invocations to `check=True`; on failure, surface git stderr and abort closeout, restoring the Board the same way the existing failure branch does.
5. Add a test in `tests/test_lifecycle_end_to_end.py`: stage an unrelated file in a test git sandbox, run a task close through the CLI, assert the unrelated file is still staged and does not appear in `git show --name-only HEAD`.
6. Update/extend the existing lifecycle test so it still verifies the task's own `files` land in the closeout commit.
7. Run `pytest tests/test_lifecycle_end_to_end.py` then `pytest`.
8. Commit as a single atomic task commit.

AMBIGUITIES:
1. Task `status: deferred` with `depends_on: task-rw-f0-tokenized-atom-retarget`; doc never states the dependency is complete or whether promotion to active is required first.
2. Rationale, Goal, and Scope body sections are placeholder underscore text; the only real acceptance text is "Done When".
3. Exact composition of "removed task bundle files" is never enumerated (task doc only? pills/atoms/contexts?).
4. Whether the binding pill `close-only-own-primitives` (named out of scope) overlaps the removal path set is unresolved.
5. "restoring the Board as the existing failure branch does" — the current failure branch is not described; unclear if it is `git checkout -- Board.md`, `git restore`, or reset of staging.
6. Board path not fixed: `desk/tasks/Board.md` vs a computed/constant path.
7. `git commit --amend --no-edit -- <paths>` behavior when the pathspec excludes previously committed paths is unspecified (possible pruning/error).
8. Behavior when the computed path list is empty is unspecified (empty commit, error, or `--allow-empty`).
9. Error contract for `check=True` failure unspecified: exception type, exit code, stderr formatting, and whether Board restore happens before or after abort.
10. Commit message template/`<msg>` format not given; unclear if existing format must be preserved.
11. How the test stages/isolates git state and constructs a sandbox desk root is unspecified (tests may mutate the real repo, contrary to AGENTS sandbox rule).
12. No named test function or fixture; unclear whether to extend the existing lifecycle test or add a new one.
13. No acceptance check beyond the test for verifying unrelated staged changes remain staged.
14. Line reference `deskops/operations.py:1552` may be stale; no function signature given.
