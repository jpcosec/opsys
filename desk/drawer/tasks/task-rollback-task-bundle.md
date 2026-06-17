---
id: task-rollback-task-bundle
scope: deskops
tags:
- system:deskops
- topic:operations
- topic:rollback
---

# Rollback-safe task bundle creation

Status: deferred
Priority: high

## Goal

Make `create_task_bundle` — which writes multiple files + appends to board — clean up fully on failure.

## Scope

- `create_task_bundle` current rollback (lines 195-198) only removes written files
- Board append via `_append_task_to_board` is not rolled back if it succeeds but a subsequent step fails
- Use `_with_rollback` utility from Slice A
- Coordinate multi-file + single-board-mutation rollback

## Current behavior

`create_task_bundle` catches `Exception` and deletes `written_paths`. But:
- Board append is not tracked in the rollback list
- Partial writes inside `_write_doc` are not handled
- The rollback is implicit (no utility, no pattern reuse)

## Done When

- Task file, routine file, all primitives, and board append all roll back on any failure
- Partial board append (line appended before crash) is reverted
- No orphan files left in `desk/tasks/`, `desk/routines/`, or `desk/primitives/`
- Tests cover: mid-write failure, board append failure, post-board failure, pre-board failure

## Parent

- `desk/tasks/task-make-create-operations-rollback-safe.md`
