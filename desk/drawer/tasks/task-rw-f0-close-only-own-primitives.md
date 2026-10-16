---
id: task-rw-f0-close-only-own-primitives
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/operations.py
- tests/test_lifecycle_end_to_end.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:closeout
- topic:data-loss
---

# Closeout deletes and amends only the closing task's own artifacts

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory findings D1 and D2. `DeskopsOperations._auto_commit_task_closure` (deskops/operations.py:1499) collects primitives with the glob `*-{task_id}*.md` (line 1533) over conditions, checklists, operators, edges and hooks. Closing `task-foo` therefore deletes, untracks and commits away the 17 primitives of `task-foo-bar` (reproduced in a sandbox). The amend check at line 1547 uses `head_subject.startswith(f"closeout: {task_id}")`, so if HEAD is `closeout: task-foo-bar`, closing `task-foo` amends the other task's commit.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Closing a task removes exactly the primitives its own bundle created (plus hooks that target them) and amends HEAD only when HEAD is that same task's closeout commit.

## Scope

_State what is in scope and what is out of scope._

In scope: the primitive-selection loop and the amend decision inside `_auto_commit_task_closure`, and two regression tests. Out of scope: the commit pathspec (task-rw-f0-closeout-commit-pathspec), untrack and rollback transactions (task-rw-f2-transactional-doc-io), and how primitive ids are generated.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Compute the exact id set the bundle created: call `compile_task_bundle_spec(self.spec_registry, {...})` (deskops/specs/compiler.py:30) with the task's id and its stored title/goal/scope/implementation_path/done_when, and collect `routine_payload['id']` plus the `id` of every item in `condition_payloads`, `checklist_payloads`, `operator_payloads` and `edge_payloads`. For any task this is the routine plus these 17 primitives: condition-<id>-{has-implementation-path,has-validation,has-closeout-evidence,pill-knowledge-graduated,ready-for-closeout}, checklist-<id>-{execution-ready,testing-ready,closeout-ready}, operator-<id>-{activate,ready-for-testing,close}, edge-<id>-{execution-to-activate,activate-to-testing,testing-to-ready,ready-to-closeout,closeout-to-close,close-to-complete}.
2. Delete a file under desk/primitives/{conditions,checklists,operators,edges}/ only when its stem is in that set. Delete a file under desk/primitives/hooks/ only when its `target` field is in that set. Remove the glob.
3. Decide the amend from the trailer: amend only when `git log -1 --format=%(trailers:key=Task-Id,valueonly)` (stripped) equals `task_id`. The closeout commit message already carries `Task-Id: <id>` (operations.py:1539); a HEAD without that trailer never amends.
4. Add two tests to tests/test_lifecycle_end_to_end.py: (a) create `task-foo` and `task-foo-bar`, commit everything (`git add -A && git commit`), close `task-foo`, then assert each of the 17 `task-foo-bar` primitive files exists and is listed by `git ls-files desk/primitives`; (b) make HEAD a commit whose subject is `closeout: task-foo-bar` with trailer `Task-Id: task-foo-bar`, close `task-foo`, assert HEAD~1 is that commit (a new commit was created).

## Validation

_List the checks required before this task can close._

- pytest tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both new tests fail on the current code and pass after the fix, and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one seed commit), run `python -m deskops desk install <root>` to scaffold `desk/`, and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- Create fixture tasks through the CLI so each gets its routine and primitives, e.g. `deskops add task --root <root> '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d", "validation": ["pytest"]}'`; an explicit `id` overrides the title slug (deskops/specs/compiler.py:37). A raw file write leaves the task without a routine, and `advance` then exits 1.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
