RESTATEMENT:

1. Open `deskops/operations.py`; read `DeskopsOperations._auto_commit_task_closure` (≈line 1499), the primitive glob `*-{task_id}*.md` (line 1533), the amend check `head_subject.startswith(f"closeout: {task_id}")` (line 1547), and the closeout commit message build carrying `Task-Id: <id>` (line 1539).
2. Add `from deskops.specs.compiler import compile_task_bundle_spec` (or reference via existing import path) and, inside the function, call `compile_task_bundle_spec(self.spec_registry, {...})` passing the task's id/title/goal/scope/implementation_path/done_when as read from the task's stored document.
3. From the compiler result build a set: `routine_payload['id']` plus the `id` of every entry in `condition_payloads`, `checklist_payloads`, `operator_payloads`, `edge_payloads` (expected: routine + 5 conditions + 3 checklists + 3 operators + 6 edges).
4. Remove the `*-{task_id}*.md` glob. For each of `desk/primitives/conditions`, `checklists`, `operators`, `edges`, delete a file only when its stem is in the id set.
5. For `desk/primitives/hooks`, delete a file only when its `target` field value is in the id set.
6. Replace the amend condition: run `git log -1 --format=%(trailers:key=Task-Id,valueonly)`, strip, and amend only when the result equals `task_id`; otherwise create a new commit.
7. In `tests/test_lifecycle_end_to_end.py`, using existing `_make_repo`/`_cli` helpers (tmp_path repo, `git init`, seed commit, `python -m deskops desk install <root>`), add test (a): create `task-foo` and `task-foo-bar` via `deskops add task --root <root> '<json with explicit ids>'`, `git add -A && git commit`, run the closeout command for `task-foo`, assert all 17 `task-foo-bar` primitive files exist and appear in `git ls-files desk/primitives`.
8. Add test (b): create a commit whose subject is `closeout: task-foo-bar` with trailer `Task-Id: task-foo-bar`, run closeout for `task-foo`, assert `HEAD~1` is that commit (a new commit was created).
9. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`.

AMBIGUITIES:

1. How `_auto_commit_task_closure` obtains the task's stored title/goal/scope/implementation_path/done_when — its signature and available task object/root are not given; reading the task doc is not described.
2. Exact dict keys and whether the compiler call also needs `validation` (the fixture CLI JSON includes it and the id set expects a `has-validation` condition).
3. On-disk primitive/hook layout and extension (`.md`? `.sldb`?) and whether file stems equal the payload `id` exactly.
4. How to read a hook's `target` field (Markdown frontmatter vs SLDB store) is unspecified.
5. Whether the routine's own file (`routine_payload['id']`) must be deleted or its id is collected only to match edges/hooks; the original glob covered only conditions/checklists/operators/edges/hooks.
6. Which CLI invocation the tests must use to trigger `_auto_commit_task_closure` (e.g. `deskops closeout commit --task <id> --run-dir <dir>` vs `--no-run --reason`) and whether a run dir is mandatory.
7. Test (b): whether `task-foo` must be created with primitives so the closeout has changes to commit; behavior when there is nothing to commit is unspecified.
8. Acceptance criteria never assert that `task-foo`'s own primitives/hooks were removed, nor that `task-foo-bar`'s routine survives.
9. No stated check that the fix leaves `task-foo-bar`'s hooks/edges intact beyond the file-listing assertion.
