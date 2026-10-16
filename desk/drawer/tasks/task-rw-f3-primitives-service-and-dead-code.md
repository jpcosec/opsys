---
id: task-rw-f3-primitives-service-and-dead-code
status: deferred
references: []
depends_on:
- task-rw-f3-drawer-routing-service
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/services/primitives.py
- deskops/operations.py
- tests/test_operational.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f3
- topic:refactor
- topic:dead-code
---

# Primitive helpers move to a service; dead code is deleted

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding S12. In deskops/operations.py the `_default_*_payloads` methods (lines 1296-1487) have no callers, `PRIMITIVE_DIRS` is unused, and `_setup_logging` is defined twice. The primitive helpers are `PRIMITIVE_KINDS` (68), `create_primitive` (462), `list_primitives` (729), `show_primitive` (1012), `parse_primitive_input` (1115), `_normalize_primitive_payload` (1218) and `_primitive_path` (2609).

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/primitives.py` (`PrimitivesService(root)`, which carries root and desk_root itself) holds those helpers as methods with the same parameters (they are instance methods today, so only `self` changes; `PRIMITIVE_KINDS` is a module-level dict and moves as a module constant of the service); collaborators they call (`ensure_workspace`, `_write_new_doc`, `_read_doc`, `_resolve_glob`, `_coerce_list`) are reached through `deskops.doc_io`, `deskops.desk_paths` or a shared helper module, `DeskopsOperations` keeps one-line wrappers so callers (deskops/cli/commands/operations.py and tests/test_operational.py) keep working, and the dead code above is deleted.

## Scope

_State what is in scope and what is out of scope._

In scope: the move and the three deletions, each proven dead with grep first. `deskops/specs/mermaid.py` and `deskops/materializers/atoms.py` are re-exported public modules used only by tests; they stay (removing public API is not part of this task). Out of scope: `RunDoc` and the self-reflection ledger.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. For each dead item, record `grep -rn '<name>' deskops tests` output in the closeout as proof.
2. Delete the items; keep the `_setup_logging` definition that the entrypoint calls.
3. Move the helpers into the service (follow the pattern set by task-rw-f3-drawer-routing-service). tests/test_operational.py:37 monkeypatches `operations._write_doc` to test rollback; point that patch at the doc_io function the service now uses, keeping what the test asserts.

## Validation

_List the checks required before this task can close._

- pytest tests
- python -m deskops next --diagram

## Done When

_Name the observable condition that makes the task complete._

deskops/services/primitives.py exists, `grep -n '_default_.*_payloads\|PRIMITIVE_DIRS' deskops` is empty, `_setup_logging` is defined once, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
