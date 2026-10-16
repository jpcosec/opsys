RESTATEMENT:
1. Read `deskops/operations.py` around `_auto_commit_task_closure` (line ~1499) and `deskops/specs/compiler.py` (`compile_task_bundle_spec`, line ~30, id override at line ~37) to confirm the bundle spec shape and payload keys.
2. In `_auto_commit_task_closure`, replace the `*-{task_id}*.md` glob (line ~1533) with an exact id set: call `compile_task_bundle_spec(self.spec_registry, {...task fields...})` using the task's id, title, goal, scope, implementation_path, done_when; collect `routine_payload['id']` plus each `id` in `condition_payloads`, `checklist_payloads`, `operator_payloads`, `edge_payloads`.
3. For files under `desk/primitives/{conditions,checklists,operators,edges}/`, delete only when the stem is in that id set.
4. For files under `desk/primitives/hooks/`, delete only when the parsed `target` field is in that id set.
5. Change the amend decision (line ~1547) from `head_subject.startswith(f"closeout: {task_id}")` to reading the trailer: run `git log -1 --format=%(trailers:key=Task-Id,valueonly)`, strip it, amend only when the result equals `task_id`.
6. Add test (a) in `tests/test_lifecycle_end_to_end.py`: use `_make_repo`/`_cli`, create `task-foo` and `task-foo-bar` via `deskops add task --root ... --json`, close `task-foo`, assert all 17 `task-foo-bar` primitive files still exist and appear in `git ls-files desk/primitives`.
7. Add test (b): create commit with subject `closeout: task-foo-bar` and trailer `Task-Id: task-foo-bar`, close `task-foo`, assert HEAD~1 is that commit (a new commit was created rather than amended).
8. Run `pytest tests/test_lifecycle_end_to_end.py -k <new tests>` before the fix to confirm both fail, then after the fix confirm both pass.
9. Run `pytest tests/test_lifecycle_end_to_end.py`, then `pytest tests`; leave committing to the supervisor.

AMBIGUITIES:
1. The 17-primitive list and exact id formats (`condition-<id>-...`, `edge-<id>-...`) are asserted in the task text; whether `compile_task_bundle_spec` returns precisely these keys/naming for the current code version is unverified and could differ.
2. "hooks that target them" — the task says delete a hook when its `target` is in the set, but does not specify whether `target` can be a list, comma-separated, or a different field name; no hook schema given.
3. File stem vs full id match: whether primitive filenames equal ids exactly (e.g. `condition-task-foo-has-validation.md` stem `condition-task-foo-has-validation`) is not stated.
4. Test (b) does not say how to construct the HEAD commit (empty commit? which files? on which branch), nor whether a new commit must have a distinct subject/trailer.
5. No acceptance criterion specifies the exact assertion for "still exist and are listed" (count 17 vs presence), and no criterion defines how to count/verify the 17 items.
6. Whether `compile_task_bundle_spec` requires the task's stored fields (title/goal/scope/implementation_path/done_when) in a particular key mapping or ordering is not specified.
7. How the amend-check git command is invoked (cwd, helper method, existing git wrapper in operations.py) is not specified.
