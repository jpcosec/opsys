---
id: task-rw-f0-payload-from-drawer-resolves
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files:
- deskops/cli/commands/operations.py
- tests/test_add_task_from_drawer.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-payload-from-drawer-resolves.md
---

# `from_drawer` given in a YAML or JSON payload is resolved like the flag

## Rationale

_Explain why this task exists or the business driver behind it._

Found by the plan rehearsal (2026-10-16). `deskops add task --from-drawer <selector>` resolves the selector to a repo-relative drawer path in `OperationsCLI.run` (deskops/cli/commands/operations.py:21-27, through `DeskopsOperations.resolve_drawer_source` and `attach_drawer_source`, operations.py:493 and 525; the resolver already raises ValueError on an ambiguous selector, operations.py:520-522). The same key inside `--from-yaml` or an inline JSON payload skips that step: deskops/specs/compiler.py:57 copies the raw string, so the task records `from_drawer: rw-f0-x` instead of `desk/drawer/tasks/task-rw-f0-x.md`, and a missing or ambiguous selector is accepted silently.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

A `from_drawer` value from the flag, a YAML payload or an inline JSON payload is resolved and stored as the same repo-relative drawer path; an unknown or ambiguous selector fails with exit 1 and creates nothing.

## Scope

_State what is in scope and what is out of scope._

In scope: the add-task branch of `OperationsCLI.run` and one new test file. If both the flag and the payload carry a value, the flag wins and the payload value is ignored without being checked. A payload value that is absent, empty or null means no drawer source (as the flag's `if` at cli/commands/operations.py:21). Out of scope: the drawer routing service (task-rw-f3-drawer-routing-service).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In `OperationsCLI.run`, take the selector from `args.from_drawer`, else from `payload.get("from_drawer")`, and run the existing resolve/attach step on it; keep the existing `Error: ...` message and `return 1` on `FileNotFoundError`/`ValueError`.
2. New tests/test_add_task_from_drawer.py, all in one sandbox repo with one drawer entry (payloads need at least `title`; give each task its own `id`): (a) the same drawer stem given via `--from-drawer`, via `--from-yaml`, and via inline JSON produces three tasks with identical `from_drawer` paths; (b) an unknown selector in a JSON payload exits 1 and creates no `desk/tasks/` file; (c) with two drawer entries that share a fragment, that fragment in a JSON payload exits 1 and creates nothing.

## Validation

_List the checks required before this task can close._

- pytest tests/test_add_task_from_drawer.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both new tests pass and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
