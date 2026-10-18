---
id: task-rw-f6-apply-store-migration
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f6-migrate-tracking-stores
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- runs/planning/store-migration-20261018.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f6-apply-store-migration.md
---

# Run the store migration with `--apply` on every discovered store

## Rationale

_Explain why this task exists or the business driver behind it._

Split by the supervisor from task-rw-f6-migrate-tracking-stores on 2026-10-18. That task delivered scripts/migrate_desk_stores.py, validated with `--dry-run` only. Its dry-run discovers 40 stores under /home/jp, excluding `.cache`, `.claude`, `.tmp`, `.venv`, `node_modules`, `tools` and `tmp`. They span other owners' repositories: AntonIA (chatbot, grifo, mepu, manifest), Upla, legacy hum-*, office/humble, wittgenstein, TraderBot, setup, and the SLDB_1 repos. For each store, `--apply` runs:
- `sldb models update` for every deskops model whose contract moved;
- `deskops desk update --root <repo> --apply`, which on legacy desks deletes desk/routines and desk/primitives and rewrites tasks.

That mutates repositories this desk does not own, so it needs the owner's explicit confirmation before it runs. The dry-run output is in the closing run of task-rw-f6-migrate-tracking-stores (runs/subagents/20261018-task-rw-f6-migrate-tracking-stores/dry-run.txt).

## Goal

_Describe the concrete result this task must produce._

Every store the owner confirms is migrated, and the log shows each one PASS.

## Scope

_State what is in scope and what is out of scope._

In scope: running the script on the confirmed list (all of it, or a subset the owner names). Out of scope: committing in the other repositories, which their owners do.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Get the owner's confirmation and the list.
2. `python scripts/migrate_desk_stores.py --apply`, restricted to the confirmed stores (add a `--only` option if the owner names a subset).
3. Report the stores that FAIL with their output, and tell each repo's owner what changed in their working tree.

## Validation

_List the checks required before this task can close._

- the dated log under runs/planning/ lists every confirmed store as PASS

## Done When

_Name the observable condition that makes the task complete._

The log shows PASS for every confirmed store.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch.

## Open Ambiguities

- Owner confirmation: run `--apply` on all 40 stores, on a subset, or not at all.
