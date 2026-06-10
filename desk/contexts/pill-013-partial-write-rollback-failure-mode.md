# Failure Mode: partial writes and orphaned desk artifacts

ID: pill-013

## What

Deskops write commands must not leave partially created task bundles, primitives, board entries, or generated files when a later step fails.

## Why

Several deskops commands create multiple files and then update routing state. If a failure happens halfway through, future list/show/advance operations see orphaned or inconsistent artifacts and subagents inherit bad context.

## When

Apply to tasks involving `--from-yaml`, bundle creation, board append, rollback, dry-run, init/bootstrap, repo registration, and any multi-file write.

## Where

Primary owner files:

- `tools/deskops/deskops/operations.py`
- `tools/deskops/deskops/runtime/primitives.py`
- `tools/deskops/tests/`
- generated files under a test `desk/` root

## Required Reads

- Read the task file.
- Read this pill and `pill-012-deskops-cli-artifact-contract.md`.
- Read the write path in `operations.py` for the command under repair.
- Read tests that create temporary desk roots.

## Execution Boundary

Fix atomicity for the assigned command path. If other commands share the same helper, keep the helper narrow and covered by tests; do not redesign every write command unless the task says so.

## Validation Contract

Use a temporary root. Force a mid-operation failure. Confirm no orphaned files remain, no board row is added incorrectly, and repeated command execution starts from a clean state. For dry-run, confirm no filesystem writes occur.

## How Not

Do not rely on manual cleanup after exceptions. Do not add rollback that deletes pre-existing user files. Do not report success when routing state was not updated.

## Drift Signals

- A failed command creates files that `deskops list` can see.
- Rollback removes files that existed before the command.
- The command warns but still writes partial state.
- Tests only check exceptions, not filesystem state after failure.

## Tags

- system:deskops
- topic:rollback
- topic:failure-mode
