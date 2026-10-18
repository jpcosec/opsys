---
id: task-rw-f6-migrate-tracking-stores
status: deferred
references: []
depends_on:
- task-rw-f6-taskdoc-contract-cleanup
pills:
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
files:
- scripts/migrate_desk_stores.py
- tests/test_migrate_desk_stores.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f6
- topic:models
- topic:migration
---

# Migrate every store that tracks deskops models

## Rationale

_Explain why this task exists or the business driver behind it._

About 24 stores on this machine track TaskDoc; a contract change leaves each in FAIL until it runs `sldb models update` and `deskops desk update --apply`.

Plan: phase F6 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

scripts/migrate_desk_stores.py migrates every discovered store and logs per-store before/after `sldb stores check` results; every store passes afterwards.

## Scope

_State what is in scope and what is out of scope._

Discovery: directories named `.sldb` under $HOME whose `core/models/TaskDoc.yaml` exists, excluding paths containing `/.tmp/`, `/.venv/`, `/node_modules/`, `/tools/` or `/tmp/` (matched on whole path segments of the `.sldb` path relative to the discovery root, so a test tree under pytest's `tmp_path` is not excluded by its own location), and only when `git -C <parent of .sldb> rev-parse --is-inside-work-tree` prints `true`. Walk with `os.walk(followlinks=False)`, skip directories that raise PermissionError, and do not descend into a matched store. Each store's repo commit is its owner's.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `--dry-run` (default) lists stores and the commands it would run and exits 0 iff at least one store was found; `--apply` runs them. `--home <dir>` (default `~`) sets the discovery root so tests can use a fake tree. Each command gets a 300 s timeout; a timeout is a FAIL.
2. Per store (`<store>` = the `.sldb` dir, `<target>` = its parent repo, `<deskops>` = this deskops checkout, so `deskops.models` imports): `sldb stores check --store <store>`, then `sldb models update <Model> --store <store> --pythonpath <deskops>` for each deskops model whose contract hash changed (TaskDoc for task-rw-f6-taskdoc-contract-cleanup), then `deskops desk update --root <target> --apply`, then check again; on failure record FAIL and continue.
3. Exit 0 only if at least one store was found and every store passes; re-running is safe.
4. Log to runs/planning/store-migration-<YYYYMMDD>.md, starting with the full discovered list and its count.
5. tests/test_migrate_desk_stores.py covers discovery and exclusion on a fake tree in `tmp_path`.

## Validation

_List the checks required before this task can close._

- pytest tests/test_migrate_desk_stores.py
- python scripts/migrate_desk_stores.py --dry-run
- python scripts/migrate_desk_stores.py --apply
- sldb stores check --store .sldb
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The log shows every discovered store PASS after `--apply`.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- Owner decision (2026-10-18, delegated to the SLDB_1 coordinator): F6 enters this cycle.

## Open Ambiguities

None.
