---
id: task-rw-f2-transactional-doc-io
status: deferred
references: []
depends_on:
- task-rw-f2-typed-errors-and-exit-codes
pills:
- desk/contexts/pill-012-create-operations-transactional-rollback.md
- desk/contexts/pill-008-kgdb-sldb-boundary.md
files:
- deskops/doc_io.py
- deskops/operations.py
- deskops/identity.py
- deskops/bootstrap.py
- deskops/cli/commands/desk.py
- deskops/cli/commands/repo.py
- deskops/cli/commands/message.py
- deskops/cli/commands/promote.py
- tests/test_doc_io.py
- runs/planning/sldb-requests.md
- desk/contexts/pill-012-create-operations-transactional-rollback.md
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f2
- topic:sldb-boundary
- topic:transactions
---

# One doc_io module talks to sldb through its public API, transactionally

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory findings D6, D7 and S6. deskops imports about 30 private sldb internals (for example `sldb.cli.commands.model.ModelCLI().add(SimpleNamespace)`, `DocCLI().untrack`, `sldb.store.ops.track_document` with 9 positional args, `sldb.store.io.*`). In `_auto_commit_task_closure` the untrack runs after the closeout commit and before each file's unlink, and a failure only logs a warning, so the file is deleted anyway (operations.py:1143-1156, with `store=None` and `pythonpath='.'`). The `create_task_bundle` rollback does not untrack, the `merge_atom` rollback does not restore rewritten referrers, and `_write_doc` untracks then tracks in two steps under `except Exception`.

Plan: phase F2 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Every sldb store write in deskops (track, untrack, model registration, document update) goes through `deskops/doc_io.py`, which imports only `sldb.api.*` plus the private names listed in its module-level tuple `PRIVATE_SLDB_IMPORTS`, and offers a `DocTransaction` that restores files and store entries when any step fails. Plain file writes that do not touch the store are out of this goal.

## Scope

_State what is in scope and what is out of scope._

In scope: doc_io.py, migrating every sldb write call site, rollback tests, and an import-scan test. Closeout untrack moves before the commit, inside the transaction, and a failure aborts the closeout. Out of scope: editing sldb. When a needed operation has no `sldb.api` equivalent, keep the private call as a named helper in doc_io and append the gap (function, why, proposed API) to runs/planning/sldb-requests.md for the coordinator.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. `grep -rn 'from sldb\|import sldb' deskops` lists the call sites.
2. `DocTransaction(root)` is a re-entrant context manager (an inner `with` joins the outer transaction, so `create_task_bundle` -> `_write_doc` share one); `tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)` and `tx.delete(path)` record each path's original bytes and tracked state before acting; on exception it restores files and re-tracks or untracks to the recorded state, then re-raises. It replaces the `_with_rollback(write_fn, cleanup_fn)` helper that pill-012 prescribes; update that pill's How to name `DocTransaction`.
3. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` and the closeout untrack.
4. tests/test_doc_io.py injects a failure at each step (monkeypatch the sldb call to raise) and asserts file bytes and `sldb stores check` are as before; an import-scan test over the `deskops/` package only (tests may keep importing sldb internals) fails if any module other than doc_io imports a write-side sldb module: `sldb.cli.commands` (the CLI command classes, e.g. ModelCLI, DocCLI), `sldb.store.ops`, or a module (file) under `sldb.api.documents` whose name starts with `create_`, `delete_`, `update_`, `track_` or `untrack_`; and fails if doc_io imports a name outside `sldb.api` that is not in `PRIVATE_SLDB_IMPORTS`. Read-side imports (for example `sldb.store.io.load_store_index`, `sldb.store.resolver.find_local_store`, `sldb.store.layout`, `sldb.runtime.validation`, `sldb.core.exceptions`, `sldb.StructuredNLDoc`, and the read helpers `sldb.cli.model_utils`, `sldb.cli.store_context` and `sldb.cli.utils` used by identity.py, repo.py, message.py and operations.py) stay allowed everywhere.
5. doc_io also offers plain helpers for one-off writes outside a transaction: `track(root, path, model)`, `untrack(root, path)`, `register_model(root, model_ref)` (wrapping `sldb.api.add_model`) and `is_tracked(root, path)`. An inner `with DocTransaction(root)` finds the outer one through a module-level stack keyed by root; only the outermost exit commits or rolls back; rollback restores store entries first, then file bytes, and if restoring fails it logs that and re-raises the original error.
6. Store writes in operations.py beyond the four functions also move: `delete_atom` (719, via `_untrack_atom_document`, 1781) and `reorganize_atoms` (605, via `_retarget_atom_documents`, 1746). Writes outside operations.py also move: deskops/cli/commands/desk.py:256,280,291, deskops/cli/commands/repo.py:117, deskops/cli/commands/message.py:344, deskops/cli/commands/promote.py:86, deskops/bootstrap.py:138 and 156.

## Validation

_List the checks required before this task can close._

- pytest tests/test_doc_io.py
- pytest tests
- sldb stores check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

The import-scan and injected-failure tests pass, `pytest tests` is green, and `sldb stores check --store .sldb` passes.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.
- Read-only sldb calls (model lookups, extraction such as `sldb.runtime.validation.extract_model_data`) may stay where they are; this task moves writes.

## Open Ambiguities

None.
