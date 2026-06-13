# Make create operations rollback-safe

ID: task-make-create-operations-rollback-safe
Status: deferred
Priority: high

## Goal

Prevent partial workflow artifacts when create operations fail mid-write.

## Scope

- `create_task_bundle`
- `create_artifact`
- `create_primitive`
- `create_routine`
- board append rollback during task bundle creation

## Done When

- Simulated write, render, board update, or tracking failures remove newly created files.
- Existing files are never deleted or overwritten unexpectedly.
- Regression tests prove no orphaned task, routine, primitive, or artifact files remain after failure.
