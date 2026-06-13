---
id: pill-013
tags:
- system:deskops
- topic:rollback
- topic:failure-mode
---

# Failure Mode: partial writes and orphaned desk artifacts

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

## How



## How Not

Do not rely on manual cleanup after exceptions. Do not add rollback that deletes pre-existing user files. Do not report success when routing state was not updated.
