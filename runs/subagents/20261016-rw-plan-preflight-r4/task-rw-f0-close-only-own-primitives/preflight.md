RESTATEMENT:
1. Open `deskops/operations.py`, read `_auto_commit_task_closure` (around line 1499), the primitive glob `*-{task_id}*.md` (~1533), and the amend check `head_subject.startswith(f"closeout: {task_id}")` (~1547).
2. Read `compile_task_bundle_spec` at `deskops/specs/compiler.py:30` to learn its signature and the exact dict keys it expects; note the explicit-`id` override at line 37.
3. In `_auto_commit_task_closure`, call `compile_task_bundle_spec(self.spec_registry, {...})` with the task's id plus stored title/goal/scope/implementation_path/done_when; collect `routine_payload['id']` and the `id` of every entry in `condition_payloads`, `checklist_payloads`, `operator_payloads`, `edge_payloads`.
4. Replace the glob-based deletion: under `desk/primitives/conditions|checklists|operators|edges/` delete a file only when its stem is in the computed id set; under `desk/primitives/hooks/` delete only when the file's `target` field is in the set; remove the glob.
5. Replace the amend check: run `git log -1 --format=%(trailers:key=Task-Id,valueonly)`, strip, and amend only when it equals `task_id`.
6. Add test (a) to `tests/test_lifecycle_end_to_end.py` using `_make_repo`/`_cli`: create `task-foo` and `task-foo-bar` via `deskops add task`, `git add -A && git commit`, close `task-foo`, assert all 17 `task-foo-bar` primitive files exist and appear in `git ls-files desk/primitives`.
7. Add test (b): seed HEAD as a commit with subject `closeout: task-foo-bar` and trailer `Task-Id: task-foo-bar`, close `task-foo`, assert `HEAD~1` is that same commit (a new commit was created, not amended).
8. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`; verify the two new tests fail on unpatched code and pass after the fix.

AMBIGUITIES:
1. Source of the task's title/goal/scope/implementation_path/done_when inside `_auto_commit_task_closure` is unspecified (task doc read vs in-memory object), and the exact dict key names `compile_task_bundle_spec` expects are not given.
2. Step 2 lists only conditions/checklists/operators/edges/hooks, but step 1 also collects `routine_payload['id']`; it is unclear whether/how the routine file is deleted or where it lives.
3. How to parse a hook's `target` field (format/frontmatter key) and whether it is a string or list is not stated.
4. The exact CLI invocation that triggers `_auto_commit_task_closure` is not named; tests say "close task-foo" without specifying the command or args (run-dir, reasons).
5. The amend commit's resulting message/content is unspecified beyond the trailer; whether the amend must preserve the existing pathspec or message is not stated.
6. No procedure is given for demonstrating the new tests fail on current code (revert/stash workflow) before applying the fix.
7. The 17 `task-foo-bar` primitive filenames are not enumerated literally; they must be derived from the naming pattern.
8. It is unspecified whether closing `task-foo` should also delete/untrack `task-foo`'s own primitives in the same commit, and whether that affects the `git ls-files` assertion for `task-foo-bar`.
9. Trailer matching rules are only partly specified: behavior when HEAD has no trailer or multiple `Task-Id` trailers, and exact key casing for `%(trailers:key=Task-Id,...)`, are not defined.
