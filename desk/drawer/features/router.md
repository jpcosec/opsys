---
# Imported from paper_IEEE desk/agents/router.md
---

# Desk agent router

## Purpose
Route work between **desk operational roles** and **project runtime logic**.

This file exists to keep repo-operation instructions separate from the ETM specialist runtime implementation.

## Separation rule
- **Desk-side agent roles** live under `desk/agents/`.
- **Project runtime logic** should live under a product/runtime ETM surface; the prior `agents/etm_specialist/` scaffold has been cleared on the reboot branch.
- Do not mix desk workflow supervision rules into ETM runtime code or runtime-facing agent instructions.

## Role selection
Choose exactly one operational role before acting:

### 1. Supervisor
Read:
- `desk/agents/supervisor.md`

Use when the session is responsible for:
- selecting deskops tasks
- launching task-scoped tmux subagents
- monitoring runs
- syncing task/board state
- performing testing/closeout/commit-boundary checks
- retiring completed tasks from active deskops surfaces

### 2. Executor
Read:
- `desk/agents/executor.md`

Use when the session or worker is responsible for:
- executing one bounded deskops task
- touching only the files in scope
- running the smallest relevant validation first
- writing run evidence back to disk
- stopping at task boundaries

## Runtime boundary
If the work concerns the actual ETM runtime implementation, use the product/runtime ETM surfaces chosen on the reboot branch rather than desk-side workflow files.

Those files define product runtime behavior, not the desk-side workflow roles.
