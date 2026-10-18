---
id: task-rw-f3-closeout-gates-service
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f3-drawer-routing-service
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/services/closeout_gates.py
- deskops/operations.py
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f3-closeout-gates-service.md
---

# Closeout gates move to a service and verify real evidence

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding X6. The commit gate `_reference_points_to_commit` (deskops/operations.py:1818) accepts anything `git rev-parse --verify <ref>^{commit}` resolves, so `HEAD` or `main` pass; the tests gate `_reference_points_to_test` (1797-1816) strips `::node` and accepts any existing `.py` path. `references: ["HEAD", "deskops/x.py"]` passes closeout.

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/closeout_gates.py` owns the gates and the closeout graph context; the commit gate accepts only a 7-40 character lowercase hex id that resolves to a commit that is HEAD or an ancestor of it (existing tests pass HEAD's own hash, tests/test_closeout.py:335 and tests/test_lifecycle_end_to_end.py:126); the tests gate accepts only a `.py` path inside `<root>/tests/` (optionally followed by `::node`, whose node part is not validated) that exists.

## Scope

_State what is in scope and what is out of scope._

In scope: moving `_closeout_reference_evidence`, `_reference_points_to_commit`, `_reference_points_to_test` and `_build_closeout_graph_context` into the service with wrappers, tightening the two gates, and tests. Absolute paths and paths escaping `tests/` via `..` are rejected. Out of scope: the closure path itself (task-rw-f3-single-closure-path).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Move the functions (pattern from task-rw-f3-drawer-routing-service).
2. Commit gate: `re.fullmatch(r'[0-9a-f]{7,40}', ref)`, then `git rev-parse --verify <ref>^{commit}` (an ambiguous abbreviation fails here and is rejected), then `git merge-base --is-ancestor <full sha> HEAD`.
3. Tests gate: split off `::...`; reject the reference if `Path(ref).is_absolute()`; otherwise resolve it against root and require suffix `.py`, existence, and `resolved.is_relative_to((root / 'tests').resolve())`.
4. tests/test_closeout.py: `HEAD`, `main`, `deskops/x.py`, `/abs/tests/x.py` and `tests/../deskops/x.py` are rejected; a real ancestor hash and `tests/test_x.py::test_y` are accepted.

## Validation

_List the checks required before this task can close._

- pytest tests/test_closeout.py tests/test_lifecycle_end_to_end.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new gate tests pass, the lifecycle test still closes its task, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
