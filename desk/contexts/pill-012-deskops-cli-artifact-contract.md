---
id: pill-012
tags:
- system:deskops
- topic:cli
- topic:artifacts
- topic:zero-context
---

# Pattern: dispatch deskops CLI artifact fixes from the artifact contract

## What

This pill gives a fresh subagent the minimum context needed to execute deskops CLI/artifact tasks without reading the whole deskops implementation.

## Why

Deskops commands manipulate modeled Markdown artifacts under `desk/`. Many current failures come from mismatches between CLI payload normalization, artifact file naming, board updates, and runtime primitives. Without this pill, executors drift into broad workflow redesign.

## When

Apply to root tasks `046` through `059` and any task that touches `deskops add`, `show`, `list`, `advance`, `repo`, `graph`, `faq`, `inbox`, or artifact normalization.

## Where

Primary owner files:

- `tools/deskops/deskops/operations.py`
- `tools/deskops/deskops/cli/commands/`
- `tools/deskops/deskops/runtime/primitives.py`
- `tools/deskops/deskops/models/`
- `tools/deskops/tests/`

## How



## How Not

Do not solve deskops by migrating to a new atom model unless the assigned task says so. Do not preserve generated test artifacts as active pills or tasks. Do not let `Unexpected:` tracebacks, absolute path leaks, or suffix-glob matches remain in user-facing behavior.
