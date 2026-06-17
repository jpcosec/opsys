---
id: task-rollback-single-file-creates
scope: deskops
tags:
- system:deskops
- topic:operations
- topic:rollback
---

# Rollback-safe single-file creates

Status: deferred
Priority: high

## Goal

Make `create_artifact`, `create_primitive`, and `create_routine` remove their output on failure.

## Scope

- Extract `_with_rollback(write_fn, cleanup_fn)` utility
- Wire into `create_artifact` (line 201, `operations.py`)
- Wire into `create_primitive` (line 220)
- Wire into `create_routine` (line 228)
- Each must clean up written file + tracking artifact on any exception

## Failure modes to handle

- `_write_doc` raises (disk full, permissions, invalid model)
- `_track_created_artifact` raises (store unavailable)
- Payload normalization raises before write (out of scope — handled by caller)

## Done When

- All three creates delete their written file if any step after write fails
- No orphan files left in `desk/<type>/` directory
- No orphan tracking entries in store
- Existing files never touched on failure
- Tests cover: happy path, write failure, tracking failure, payload failure

## Parent

- `desk/tasks/task-make-create-operations-rollback-safe.md`
