RESTATEMENT:
1. Confirm dependency `task-rw-f2-typed-errors-and-exit-codes` is closed; if not, stop.
2. Read `desk/contexts/pill-012-create-operations-transactional-rollback.md`, pill-008, and `runs/planning/deskops-rewrite-inventory.md` F2 section; inspect `../sldb` for the `sldb.api.*` surface.
3. Run `grep -rn 'from sldb\|import sldb' deskops`; classify each hit read-side vs write-side.
4. Create `deskops/doc_io.py` with module-level tuple `PRIVATE_SLDB_IMPORTS` listing every allowed non-`sldb.api` private name.
5. Implement re-entrant `DocTransaction(root)` using a module-level stack keyed by root; per-path record original bytes + tracked state; methods `write(path, model, payload)`, `track(path, model)`, `untrack(path)`, `delete(path)`.
6. On exception: restore store entries first, then file bytes, then re-raise; log restore failures and re-raise the original error; only the outermost exit commits/rolls back.
7. Add plain helpers `track(root, path, model)`, `untrack(root, path)`, `register_model(root, model_ref)` (wrap `sldb.api.add_model`), `is_tracked(root, path)`; keep gap private calls as named helpers in doc_io and append `(function, why, proposed API)` entries to `runs/planning/sldb-requests.md`.
8. Port in `deskops/operations.py`: `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc`; ensure `create_task_bundle` → `_write_doc` share one transaction.
9. Move closeout untrack in `_auto_commit_task_closure` (operations.py:1567–1580) to before the commit, inside the transaction; failure aborts closeout; drop `store=None`/`pythonpath='.'`.
10. Port `delete_atom` (775, via `_untrack_atom_document` 2205) and `reorganize_atoms` (663, via `_retarget_atom_documents` 2170).
11. Port write sites at `deskops/cli/commands/desk.py:223,249,262`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,156`.
12. Update pill-012 "How" to name `DocTransaction` instead of `_with_rollback(write_fn, cleanup_fn)`.
13. Add `tests/test_doc_io.py`: monkeypatch each sldb call step to raise; assert file bytes and `sldb stores check` state unchanged; add import-scan test over `deskops/` package implementing the stated allow/deny rules.
14. Run `pytest tests/test_doc_io.py`, `pytest tests`, `sldb stores check --store .sldb`.
15. Do not commit; leave diff for supervisor closeout.

AMBIGUITIES:
1. Dependency `task-rw-f2-typed-errors-and-exit-codes` completion state is not stated; task is `status: deferred` while Resolved Decisions describe dispatch.
2. `PRIVATE_SLDB_IMPORTS` contents are not enumerated; the import-scan rule ("not in `PRIVATE_SLDB_IMPORTS`") is circular since the tuple is defined in the module under test.
3. Parameter types for `tx.write(path, model, payload)` and `track(path, model)` are undefined (model ref vs model name; payload shape).
4. `tx.delete(path)` semantics undefined (unlink only vs unlink+untrack).
5. Rollback behavior for paths that did not previously exist or were not tracked ("recorded state") is undefined.
6. Whether outer-exit "commit" is a no-op over eager writes or applies buffered writes is not stated.
7. Nested transactions across different roots and thread/concurrency behavior are unspecified.
8. The import-scan deny rule does not cover direct write functions under `sldb.api` (e.g. `add_model`) imported by non-doc_io modules; unclear if that is a violation.
9. Existence/correct name of `sldb.api.add_model` is asserted, not verified.
10. Which operations `bootstrap.py:138` and `:156` perform (track vs register model) is not stated.
11. Line numbers may have drifted; "every sldb write call site" has no acceptance criterion beyond the scan, so out-of-scope writes (e.g. `sldb.store.io`) may be missed.
12. "Inject a failure at each step" does not define what counts as a step, nor the store fixture used to assert "as before" (only `sldb stores check` is named).
13. `merge_atom` referrer restoration: which referrers and how to verify is not specified.
14. Whether an existing `_with_rollback` helper must be deleted is not stated.
15. Required format/schema for appended `runs/planning/sldb-requests.md` entries and whether the file exists is unspecified.
16. Editing a pill file (pill-012) vs AGENTS.md rule that substantive rule changes start in atoms is not reconciled.
17. `deskops/identity.py` is listed in `files` but no work on it is described.
18. Baseline green state of `pytest tests` and whether tests may mutate the real `.sldb` (vs a sandbox) are unstated.
