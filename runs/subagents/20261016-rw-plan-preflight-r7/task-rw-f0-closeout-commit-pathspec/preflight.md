RESTATEMENT:

1. Read `deskops/operations.py` around `_auto_commit_task_closure` (cited lines 1518, 1537, 1549-1552) to see how the removed bundle paths, `desk/tasks/Board.md`, and the task's `files` list are currently staged and committed.
2. Build an explicit path list: (a) the removed bundle paths, (b) `desk/tasks/Board.md`, (c) each entry in the task's `files` for which `git status --porcelain -- <path>` (run with repo cwd) prints non-empty output; skip listed paths with no output.
3. Replace the blanket `git add` (operations.py:1518) with `git add -A -- <path>` applied only to that filtered path list, so untracked new files in the list are still added.
4. Change the `git rm --cached` calls (line 1537) to a checked return code; on failure run the existing failure branch (restore Board, unstage, raise `RuntimeError` carrying git's stderr).
5. Change the commit call (lines 1549-1552) to `git commit -m <msg> -- <paths>`, and the amend path to `git commit --amend --no-edit -- <paths>`.
6. In `tests/test_lifecycle_end_to_end.py`, add a test using `_make_repo`/`_cli`: create a fixture task via `deskops add task --root <root> '{...}'`, write and stage an unrelated file, close the task via the CLI, then assert `git diff --cached --name-only` still lists the unrelated file and `git show --name-only --format= HEAD` does not.
7. Confirm the existing lifecycle test (untracked atom + test file listed in `files`, expected in the commit) still passes.
8. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`.

AMBIGUITIES:

1. "The removed bundle paths" is undefined in the task; I must read the code to learn what a "bundle" is and which paths it yields (line 1537's `git rm --cached` targets).
2. Contradiction: Scope says the amend rule is out of scope, but Implementation Path step 2 says to also produce `git commit --amend --no-edit -- <paths>`. Unclear whether to implement the amend pathspec now.
3. Which CLI invocation closes a task and triggers `_auto_commit_task_closure` for the new test (`deskops advance`, or another command) is not stated.
4. How to "stage an unrelated file" (path, content, `git add`) and where in the test flow relative to `deskops add task` is unspecified.
5. "Run `git rm --cached` with a checked return code" — whether this means `subprocess.run(..., check=True)` or manual `returncode != 0` inspection is unspecified.
6. The existing failure branch ("restore the Board, unstage, raise RuntimeError with git's stderr") is referenced but not quoted; exact restore/unstage commands and how stderr is captured (`capture_output=True, text=True`) must be inferred from the current code.
7. Path relativity of `files` entries and of `desk/tasks/Board.md` (relative to the sandbox root vs. the git repo root created by `desk install`) is not stated.
8. Whether the path list must be de-duplicated or ordered is unspecified.
9. No acceptance criterion checks that unrelated *unstaged* changes are excluded; the goal only mentions staged ones.
10. Whether the same fix must be applied where `deskops closeout commit` shares this code is not stated (Scope declares `deskops/cli/commands/closeout.py` out of scope, but code-path sharing is unknown without reading).
11. Cited line numbers (1518, 1537, 1549-1552) may not match current code; no fallback identification is given beyond function name.
