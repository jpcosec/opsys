RESTATEMENT:
1. Confirm dependency `task-rw-f2-typed-errors-and-exit-codes` is closed and that this task was promoted to `desk/tasks/` (promotion commit exists) before writing code.
2. Inventory write call sites: `grep -rn 'from sldb\|import sldb' deskops`; classify each as read or write; list private names needed.
3. Create `deskops/doc_io.py` with module-level `PRIVATE_SLDB_IMPORTS` tuple enumerating every non-`sldb.api` private name doc_io needs.
4. Implement `DocTransaction(root)` as a re-entrant context manager backed by a module-level stack keyed by root; inner `with` joins outer; only outermost exit commits or rolls back.
5. Implement `tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)`, `tx.delete(path)`; each records the path's original bytes and tracked state before acting.
6. On exception: restore store entries first, then file bytes, to recorded state (re-track or untrack as recorded), then re-raise original error; if restore itself fails, log it and still re-raise the original error.
7. Add plain helpers outside transactions: `track(root, path, model)`, `untrack(root, path)`, `register_model(root, model_ref)` (wrapping `sldb.api.add_model`), `is_tracked(root, path)`.
8. Delete/replace the `_with_rollback(write_fn, cleanup_fn)` helper in `operations.py`; update pill `desk/contexts/pill-012-create-operations-transactional-rollback.md` How section to name `DocTransaction`.
9. Port `create_task_bundle`, `merge_atom` (restore rewritten referrers on rollback), `split_atom`, `_write_doc` (single transactional step) to doc_io/DocTransaction.
10. In `_auto_commit_task_closure` (operations.py ~1143-1156) move the untrack before the closeout commit and inside the transaction; a failure aborts closeout.
11. Port `delete_atom` (~719 via `_untrack_atom_document` ~1781) and `reorganize_atoms` (~605 via `_retarget_atom_documents` ~1746).
12. Port non-operations write sites: `deskops/cli/commands/desk.py:256,280,291`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,156`.
13. For any needed operation with no `sldb.api` equivalent, keep a named private helper in doc_io and append `(function, why, proposed API)` to `runs/planning/sldb-requests.md`.
14. Write `tests/test_doc_io.py`: monkeypatch each sldb call step to raise; assert file bytes unchanged and `sldb stores check` result unchanged (compare against pre-transaction state).
15. Write an import-scan test over the `deskops/` package only: fail if any module other than doc_io imports `sldb.cli.commands`, `sldb.store.ops`, or a file under `sldb.api.documents` named `create_*`/`delete_*`/`update_*`/`track_*`/`untrack_*`; fail if doc_io imports a name outside `sldb.api` not in `PRIVATE_SLDB_IMPORTS`. Allow read-side imports everywhere (`sldb.store.io.load_store_index`, `sldb.store.resolver.find_local_store`, `sldb.store.layout`, `sldb.runtime.validation`, `sldb.core.exceptions`, `sldb.StructuredNLDoc`, `sldb.cli.model_utils`, `sldb.cli.store_context`, `sldb.cli.utils`).
16. Run `pytest tests/test_doc_io.py`, `pytest tests`, `sldb stores check --store .sldb`.
17. Do not commit; hand the diff to the supervisor for the closeout commit.

AMBIGUITIES:
1. `PRIVATE_SLDB_IMPORTS` contents are not enumerated; I must discover the exact private names/gaps from the sldb source, which is not in this document.
2. Contradiction: the doc_io import-scan rule forbids imports outside `sldb.api` unless listed in `PRIVATE_SLDB_IMPORTS`, yet doc_io must implement `is_tracked` and other reads and read-side imports are declared "allowed everywhere" (`sldb.store.io.load_store_index`, `sldb.cli.*`). Unclear whether read imports in doc_io must be listed in `PRIVATE_SLDB_IMPORTS` or are exempt.
3. Existence and actual layout of `sldb.api` / `sldb.api.documents` and which write functions they expose is unverifiable from this document; the scan rule presupposes package structure I cannot confirm.
4. `tx.write(path, model, payload)` payload shape is unspecified (dict, model data, rendered bytes, field ops?).
5. Does `tx.write` imply tracking, and does `tx.track` imply file write? Ordering/relationship between file write and store write is unspecified.
6. Rollback for paths created new inside the transaction (no prior bytes/tracked state) is unspecified — whether to delete the file and untrack.
7. Rollback for `tx.delete` is unspecified beyond "restore": whether original tracked state is knowable after the delete and how the pre-state is recorded.
8. Nested transactions with different `root` values are unspecified.
9. "Tracked state" recording mechanism is unspecified (per-path check via which read API vs. store index snapshot).
10. `deskops/identity.py` is listed in `files` but the Implementation Path names no write call site there; unclear whether it requires any change.
11. Failure-injection coverage: "a failure at each step" is not enumerated, so test completeness is undefined.
12. How the test should run `sldb stores check` (subprocess vs. Python API) is unspecified.
13. No acceptance criteria for `runs/planning/sldb-requests.md` entries (only format given); no validation that gaps were correctly recorded.
14. `register_model` behavior when the model is already registered (idempotency, error) is unspecified.
15. Behavior change for closeout untrack previously run with `store=None` and `pythonpath='.'` (sandbox/no-store contexts): whether closeout must still succeed without a store is unspecified.
16. Editing bound pill `pill-012` during implementation vs. treating pills as external atomic truths: the doc explicitly instructs the edit but does not say whether that edit is part of this task's commit scope or the phase ritual.
