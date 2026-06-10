# Pattern: dispatch deskops CLI artifact fixes from the artifact contract

ID: pill-012

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
- `tools/deskops/desk/models/`
- `tools/deskops/tests/`

## Required Reads

- Read the assigned task file.
- Read this pill and `pill-007-phase-gated-task-flow.md`.
- Read only the command handler and model files named by the task location.
- Read stress-test findings only when the task lacks reproduction commands.

## Execution Boundary

Fix the command and artifact behavior named by the task. Keep generated artifact shape compatible with the existing desk models unless the task explicitly changes the model. If a fix exposes another artifact type with the same failure, either add a narrow shared helper or create a follow-up task; do not redesign every artifact flow.

## Validation Contract

Validate through `deskops` CLI commands plus focused tests. For write operations, check file creation, rollback, board update, and no orphaned artifacts. For read operations, check exact ID matching, empty IDs, invalid files, and user-friendly errors.

## How Not

Do not solve deskops by migrating to a new atom model unless the assigned task says so. Do not preserve generated test artifacts as active pills or tasks. Do not let `Unexpected:` tracebacks, absolute path leaks, or suffix-glob matches remain in user-facing behavior.

## Drift Signals

- The executor edits unrelated artifact types without a shared failing path.
- The executor keeps generated test pills/tasks as active context.
- The executor changes model shape without updating payload normalization and tests.
- The executor fixes direct Python calls but not the public `deskops` command.

## Tags

- system:deskops
- topic:cli
- topic:artifacts
- topic:zero-context
