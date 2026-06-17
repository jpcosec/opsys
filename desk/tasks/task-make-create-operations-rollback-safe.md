---
id: task-rollback-creates
scope: deskops
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-012-create-operations-transactional-rollback.md
tags:
- system:deskops
- topic:operations
- topic:data-integrity
- topic:rollback
---

# Make create operations rollback-safe

Status: active
Priority: high

## Goal

Prevent partial workflow artifacts when create operations fail mid-write.

## Scope

All deskops create operations must clean up after themselves on failure:

- `create_artifact`
- `create_primitive`
- `create_routine`
- `create_task_bundle` (multi-file + board append — most complex)

## Dependencies (in-repo)

- `task-rollback-single-file-creates` (Slice A — independent)
- `task-rollback-task-bundle` (Slice B — depends on Slice A pattern)

## Sub-slices

### Slice A — Rollback single-file creates

Files: `create_artifact`, `create_primitive`, `create_routine`
Pattern: extract `_with_rollback` utility, wire into single-write operations

### Slice B — Rollback task bundle + board

Files: `create_task_bundle`, `_append_task_to_board`
Pattern: extend utility for multi-write + board mutation coordination

## External dependencies

- `_write_doc` and `_track_created_artifact` as-is (no sldb changes needed)
- Board append mutation via `_append_task_to_board` (deskops-owned)

## Out of scope

- SLDB store writes (deskops never writes to `.sldb/` directly)
- Delete/update operations (separate task)
- KGDB graph mutation (deskops graph commands only read snapshots)

## Done When

- Simulated write, render, board update, or tracking failures remove newly created files
- Existing files are never deleted or overwritten unexpectedly
- Regression tests prove no orphaned task, routine, primitive, or artifact files remain after failure
- All sub-slices pass independently

## Related

- `desk/atoms/workflow-model/atom-create-operations-should-rollback-on-failure.md`
- `desk/drawer/tasks/task-rollback-single-file-creates.md`
- `desk/drawer/tasks/task-rollback-task-bundle.md`
