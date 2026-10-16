## RESTATEMENT

1. Read `deskops/operations.py` around `_auto_commit_task_closure` (~line 1499) and its call site(s) to see what task metadata (id, title, goal, scope, implementation_path, done_when) is available in scope, plus how the delete/untrack/commit steps consume the collected primitive list.
2. Load pill `desk/contexts/pill-001-task-closure-commit.md` and `desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md`.
3. Replace the glob `*-{task_id}*.md` (line 1533) with an exact-id set: call `compile_task_bundle_spec(self.spec_registry, {...})` from `deskops/specs/compiler.py:30`, passing the closing task's id plus its stored title/goal/scope/implementation_path/done_when, and collect `routine_payload['id']` and the `id` of every item in `condition_payloads`, `checklist_payloads`, `operator_payloads`, `edge_payloads` (routine + 17 ids).
4. In the delete/untrack loop: delete a file under `desk/primitives/{conditions,checklists,operators,edges}/` only when its stem is in that id set; delete a file under `desk/primitives/hooks/` only when its `target` field value is in that set. Remove the glob entirely from the selection path.
5. Replace the amend check at line 1547: run `git log -1 --format=%(trailers:key=Task-Id,valueonly)`, strip, and amend only when it equals `task_id`. A HEAD without that trailer never amends.
6. Leave the closeout commit message trailer `Task-Id: <id>` (line 1539) unchanged.
7. In `tests/test_lifecycle_end_to_end.py`, add test (a) using `_make_repo` + `_cli`: create `task-foo` and `task-foo-bar` (so both bundles exist), close `task-foo` via the CLI path that triggers `_auto_commit_task_closure`, assert all 17 `task-foo-bar` primitive files still exist on disk and appear in `git ls-files desk/primitives`.
8. Add test (b): in a tmp repo create a commit whose subject is `closeout: task-foo-bar` with trailer `Task-Id: task-foo-bar`, then close `task-foo`, assert `git rev-parse HEAD~1` equals that foo-bar commit (a new commit was created rather than amend).
9. Run `pytest tests/test_lifecycle_end_to_end.py` before the fix to confirm both new tests fail, then after the fix to confirm they pass.
10. Run `pytest tests` and confirm green.

## AMBIGUITIES

1. Compiler spec keys: the task says pass "title/goal/scope/implementation_path/done_when", but `compile_task_bundle_spec` expects a specific dict shape; the exact key names and how to read the stored values (frontmatter? section headings like `# Goal`, `# Scope`?) are not specified.
2. Where the closing task's title/goal/scope/implementation_path/done_when are available inside `_auto_commit_task_closure` at runtime is not stated; guessing whether they are already passed in, read from the task doc file, or must be threaded through.
3. File-naming convention: the task assumes primitive file stems equal the primitive ids (step 2), but never states that mapping; if stems differ, the "stem in id set" comparison is wrong.
4. Hook `target` field: not stated whether `target` is a scalar, a list, frontmatter, or SLDB field, or how a hook with multiple targets is compared.
5. Whether the existing untrack step uses its own separate glob (out-of-scope per the doc) or reuses the selection loop's list; if separate, the fix may not fully cover untrack.
6. Which CLI command/entry point actually invokes `_auto_commit_task_closure` (used to "close `task-foo`" in the tests) is not named.
7. Behavior when `compile_task_bundle_spec` fails or a task has no bundle/primitives (e.g., task-foo created without `desk install`-generated primitives) is unspecified.
8. Exact expected set of 17 ids is enumerated in the task, but if `compile_task_bundle_spec` emits a different count/names for the current registry, no guidance on which wins.
9. Acceptance criterion "both new tests fail on the current code" implies running tests pre-fix, but the task does not say whether that pre-fix run must be recorded or is only a sanity step.
10. `pills` lists `pill-real-cli-surfaces-prove-operator-contracts.md` but it is not in `files`; whether it constrains test structure (real CLI only) or is informational is unclear.
