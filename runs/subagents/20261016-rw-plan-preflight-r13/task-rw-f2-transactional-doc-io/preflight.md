RESTATEMENT:

1. Confirm `task-rw-f2-typed-errors-and-exit-codes` is closed; task stays `deferred` until supervisor promotes it to `desk/tasks/` and commits the promotion.
2. Inventory call sites: `grep -rn 'from sldb\|import sldb' deskops`; classify each as read-side (leave) or write-side (migrate).
3. Create `deskops/doc_io.py` with module-level `PRIVATE_SLDB_IMPORTS` tuple, importing only `sldb.api.*` plus those names.
4. Implement `DocTransaction(root)` as a re-entrant context manager: module-level stack keyed by root; inner `with` joins the outer; only outermost exit commits (discards journal) or rolls back.
5. Implement `tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)`, `tx.delete(path)`; each records original bytes and tracked state before acting.
6. Implement rollback: restore store entries first, then file bytes, then re-raise the original error; log and re-raise if restore itself fails.
7. Implement plain helpers `track(root, path, model)`, `untrack(root, path)`, `register_model(root, model_ref)` (wrapping `sldb.api.add_model`), `is_tracked(root, path)`.
8. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` in `deskops/operations.py` to use `DocTransaction`; drop `store=None` / `pythonpath='.'` hacks.
9. Move closeout untrack in `_auto_commit_task_closure` (operations.py:1143-1156) to before the closeout commit, inside the transaction; failure aborts closeout.
10. Move `delete_atom`/`_untrack_atom_document` (719/1781) and `reorganize_atoms`/`_retarget_atom_documents` (605/1746).
11. Move `deskops/cli/commands/desk.py:256,280,291`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,156`.
12. For any needed operation with no `sldb.api` equivalent, wrap the private call as a named helper in doc_io and append (function, why, proposed API) to `runs/planning/sldb-requests.md`.
13. Edit `desk/contexts/pill-012-create-operations-transactional-rollback.md`: replace `_with_rollback(write_fn, cleanup_fn)` in How with `DocTransaction`.
14. Write `tests/test_doc_io.py`: monkeypatch each sldb call to raise, assert file bytes and store state (via `sldb stores check`) unchanged; add an import-scan test over `deskops/` excluding tests that fails on write-side sldb imports outside doc_io and on doc_io names outside `sldb.api` not in `PRIVATE_SLDB_IMPORTS`.
15. Run `pytest tests/test_doc_io.py`, `pytest tests`, `sldb stores check --store .sldb`.
16. Do not commit; supervisor reviews diff and runs `deskops closeout commit --task task-rw-f2-transactional-doc-io ...` with `pytest tests` green.

AMBIGUITIES:

1. `PRIVATE_SLDB_IMPORTS` contents are never enumerated; the required names cannot be derived without first resolving which operations lack `sldb.api` equivalents.
2. Blocked on a still-`deferred` dependency (`task-rw-f2-typed-errors-and-exit-codes`); the exception types and exit codes to raise when closeout aborts are undefined.
3. Import-scan rule wording "a module under `sldb.api.documents` whose name starts with `create_`…" does not say whether the prefix applies to module names or to function names within that module.
4. `tx.write(path, model, payload)` payload format (raw bytes vs. serialized fields vs. model dict) is unspecified.
5. How tracked state is read back for journaling (public API vs. private read) is unspecified; if private is needed it collides with items 1.
6. Whether `tx.delete(path)` untracks store entries is not stated.
7. Whether "commit" performs any store work or is purely a no-op journal discard is not stated.
8. Rollback semantics are undefined when the rollback itself partially fails; also whether exceptions during file restore skip remaining entries.
9. Re-entrancy behavior is undefined for nested `with DocTransaction(root)` using a different root, and for thread safety of the module-level stack.
10. Failure-injection mechanism is unspecified: doc_io is the only sldb caller, so monkeypatch targets inside doc_io must be chosen without guidance.
11. Whether existing helpers `_untrack_atom_document` / `_retarget_atom_documents` themselves move to doc_io or only their store calls, is unstated.
12. No acceptance criteria for what contents `runs/planning/sldb-requests.md` must have, or whether the coordinator must act before closeout.
13. Pill edit is prescribed, but AGENTS.md requires substantive rules to land in atoms first; whether a companion atom change is required is unstated.
14. `sldb stores check --store .sldb` is required both as a validation command and as an assertion inside tests; whether tests shell out or call the API is unspecified.
