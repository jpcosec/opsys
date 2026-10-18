# result summary: task-closeout-commit-accepts-directory-paths

Done by the supervisor directly; sldb-04 reported the bug.

- `deskops/services/closure.py`: the task file counts as committed only if HEAD has it (`git cat-file -e HEAD:<path>`), not merely because it is staged. A never-committed task that a directory in --paths staged is unstaged (`git rm --cached`) and removed from disk; it is not added to the pathspec. Before committing, pathspec entries that git knows neither in the index nor in HEAD are dropped (`_git_knows`), and an explicit --paths that matches nothing raises ClosureCommitError instead of committing the whole index.
- `tests/test_closeout.py`: `test_closeout_commit_accepts_a_directory_holding_the_task[new-task|committed-task]`. Before the fix, new-task failed: "pathspec desk/tasks did not match any file(s) known to git".

Full suite: see validation.log.
