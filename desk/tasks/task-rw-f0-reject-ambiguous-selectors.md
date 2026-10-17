---
id: task-rw-f0-reject-ambiguous-selectors
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f0-closeout-amends-only-its-own-commit
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md
files:
- deskops/operations.py
- tests/test_operational.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-reject-ambiguous-selectors.md
---

# Prefix selectors fail on ambiguity instead of picking the first match

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding D5. `DeskopsOperations._resolve_glob` (deskops/operations.py:2077-2084) returns `matches[0]` of `{doc_id}*.md` when no exact file exists, so `advance task task-foo` can advance `task-foo-bar`, and `inherits_from` can inherit from the wrong parent. Its callers are at lines 674, 955 and 1964 (all resolve tasks). The other resolver, `_resolve_artifact_selector` (2112), already refuses ambiguity through `_one_artifact_match` (2203).

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`_resolve_glob` raises on more than one prefix match, naming every candidate, while an exact file name and a single prefix match keep resolving as today.

## Scope

_State what is in scope and what is out of scope._

In scope: `_resolve_glob` and two CLI tests. Out of scope: merging the resolvers into one module (task-rw-f2-selector-resolution-module).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In `_resolve_glob`, after the exact-match check, if `len(matches) > 1` raise `ValueError(f"Ambiguous id '{doc_id}' in {directory}: {', '.join(p.stem for p in matches)}")`, the same shape as `_one_artifact_match`.
2. `deskops.cli.main.main` already maps `ValueError` to `Invalid value: ...` on stderr and exit 1 (deskops/cli/main.py, `main`); no CLI change.
3. Tests in tests/test_operational.py, importing `_make_repo` and `_cli` from tests/test_lifecycle_end_to_end.py (that module has the sandbox harness; test_operational.py does not): (a) with `task-foo-bar` and `task-foo-baz` only, `deskops advance task task-foo` exits 1, stderr names both stems, and both task files' text is unchanged (read before and after); (b) with `task-foo` and `task-foo-bar`, `deskops advance task task-foo` exits 0, its stdout contains `Task: task-foo`, and `task-foo-bar.md` is unchanged.

## Validation

_List the checks required before this task can close._

- pytest tests/test_operational.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both new tests pass and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` (git init, one empty seed commit), run `python -m deskops init <root>` (creates the store, the desk and the lifecycle graph that `advance` reads; the `lifecycle_desk` fixture in tests/conftest.py gives the same thing faster), and drive the real CLI, by default with `subprocess.run([sys.executable, '-m', 'deskops', ...], cwd=root)` (helpers `_make_repo` and `_cli` in tests/test_lifecycle_end_to_end.py); a task that says 'in-process' calls `deskops.cli.main.main([...])` with `capsys` instead. Files created in the sandbox are untracked until the test commits them. Never mutate the repo's own `desk/`.
- Create fixture tasks through the CLI so each is tracked and routed on the Board, e.g. `deskops add task --root <root> '{"id": "task-foo", "title": "Foo", "goal": "g", "scope": "s", "implementation_path": "i", "done_when": "d", "validation": ["pytest"]}'`; an explicit `id` overrides the title slug (deskops/specs/compiler.py:36). The task starts at the lifecycle node `ritual-execution`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
