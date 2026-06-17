---
id: pill-012
tags:
- system:deskops
- pill-type:guardrail
- topic:operations
- topic:data-integrity
- topic:rollback
---

# Guardrail: create operations must be transactional

## What

Every deskops create operation must either complete fully or restore the prior state. Partial writes, orphan files, and half-appended board listings are knowledge-system failures.

## Why

Silent orphan artifacts erode trust in deskops. The execution ritual expects clean state before and after every task. A create that leaves debris forces manual cleanup and breaks closeout gates.

## When

Apply this pill whenever a create operation is written, reviewed, or refactored. Especially when the operation writes multiple files, appends to the board, or calls tracking APIs after the primary write.

## Where

Applies to `deskops/operations.py` create methods: `create_artifact`, `create_primitive`, `create_routine`, `create_task_bundle`, and any future create that writes durable artifacts.

## How

Use a reusable `_with_rollback(write_fn, cleanup_fn)` utility that captures the written path before the write, catches any exception after the write, and runs cleanup. For multi-step creates (task bundle), track every written path and board mutation in a list and iterate cleanup in reverse.

## How Not

Do not rely on bare `try`/`except` blocks scattered across each create method without a shared rollback utility. Do not leave board append unreverted when a subsequent write fails. Do not silently swallow cleanup exceptions.
