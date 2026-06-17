# Add desk health and recovery surface (deskops slice)

ID: task-add-desk-health-and-recovery-surface
Status: deferred
Priority: medium

## Goal

Detect and repair common broken desk states safely (deskops-owned surfaces only).

## Scope

- missing or invalid `desk/` structure
- untracked modeled documents
- stale graph runtime files (`.sldb/runtime/`)
- invalid atom/task/pill documents

SLDB store health and model registration checks are routed to the sibling `sldb` repo's inbox (`20260614-000002`, `20260614-000003`). This task assumes those APIs exist and wraps them.

## Done When

- `deskops doctor` detects missing `desk/`, untracked docs, stale runtime files, and invalid workflow documents
- Clear repair instructions or non-destructive fixes for each
- SLDB store checks delegate to `sldb stores check`
