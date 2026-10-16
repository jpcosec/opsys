RESTATEMENT:
1. In `/home/jp/proyectos/SLDB_1/deskops`: run `grep -rn 'from sldb\|import sldb' deskops` and read `deskops/operations.py` (`_write_doc`, `create_task_bundle`, `merge_atom`, `split_atom`, `_auto_commit_task_closure`), `deskops/identity.py`, `deskops/bootstrap.py`, `deskops/cli/commands/{desk,repo,message,promote}.py` to enumerate every sldb write call site and its current shape.
2. Inspect `../sldb` to determine which writes have a public `sldb.api.*` equivalent (track, untrack, model registration, document update) and which must stay private.
3. Create `deskops/doc_io.py` containing: module-level tuple `PRIVATE_SLDB_IMPORTS`; named private-call helper functions (e.g. model registration via `ModelCLI().add(SimpleNamespace)`, untrack, `store.ops.track_document`); and `DocTransaction(root)` as a re-entrant context manager where an inner `with` joins the outer transaction and does not roll back itself. Methods: `write(path, model, payload)`, `track(path, model)`, `untrack(path)`, `delete(path)`; each records the path's original bytes and tracked state before acting; on outer exception it restores files and re-tracks/untracks to the recorded state, then re-raises.
4. Replace `_with_rollback(write_fn, cleanup_fn)` with `DocTransaction` in `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc`; make `_write_doc` a single transactional step instead of untrack-then-track under `except Exception`; make `create_task_bundle` rollback untrack; make `merge_atom` rollback restore rewritten referrers.
5. In `_auto_commit_task_closure` (operations.py:1567-1580) move the untrack before the closeout commit and inside the transaction, drop `store=None`/`pythonpath='.'`, and make failure abort the closeout instead of logging a warning.
6. Migrate remaining writes to doc_io helpers: `deskops/cli/commands/desk.py:223,249,262`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,156`, and `identity.py`'s `sldb.store` resolver/layout imports.
7. For each operation with no `sldb.api` equivalent, keep the private call as a named doc_io helper and append `(function, why, proposed API)` to `runs/planning/sldb-requests.md`.
8. Write `tests/test_doc_io.py`: monkeypatch each transactional sldb call to raise, assert file bytes and store state are unchanged (via `sldb stores check`).
9. Add an import-scan test over the `deskops/` package only: fail if any module other than `doc_io` imports from `sldb.cli` or `sldb.store`, or if `doc_io` imports a non-`sldb.api` name absent from `PRIVATE_SLDB_IMPORTS`; keep `sldb`, `sldb.runtime.validation`, `sldb.core.exceptions` allowed everywhere.
10. Update `desk/contexts/pill-012-create-operations-transactional-rollback.md` How section to name `DocTransaction`.
11. Run `pytest tests/test_doc_io.py`, `pytest tests`, `sldb stores check --store .sldb`; report to supervisor without committing.

AMBIGUITIES:
1. The contents of `PRIVATE_SLDB_IMPORTS` are not given; which of the ~30 private imports survive as named helpers vs. get replaced by `sldb.api` is undetermined, and no inventory of these private calls exists in the task.
2. Whether `../sldb` actually exposes api equivalents for track, untrack, model registration, and document update is unknown; if none exist, the entire migration could become helper wrappers with no api usage.
3. `PRIVATE_SLDB_IMPORTS` format is unspecified (bare names, `(module, name)` pairs, …), and the import-scan test's pass/fail semantics depend on it.
4. Nested-context behavior is vague: what the inner `with` does on exception (swallow, mark transaction failed, re-raise) is unspecified.
5. Rollback failure behavior (what happens if a restore file-write or re-track fails mid-rollback) is unspecified.
6. `DocTransaction(root)` — `root` is undefined: repo root, desk root, or `.sldb` store root.
7. `tx.write(path, model, payload)` argument types are undefined: is `model` a name string, a class, or an sldb model instance; is `payload` a dict, text, or `SimpleNamespace`.
8. `tx.delete(path)` — whether it only unlinks or also untracks is unspecified.
9. Restoring "store entries" to a recorded state has no stated mechanism or comparison beyond running `sldb stores check`; how the test proves store restoration is unspecified.
10. "Closeout untrack moves before the commit, inside the transaction, and a failure aborts the closeout" spans a git commit; DocTransaction rollback of a git commit is not defined.
11. Step 5's call-site list may be incomplete relative to "every sldb store write in deskops"; it is unresolved whether sites found by grep but absent from the list are in scope.
12. Whether unlisted read-only uses of `sldb.cli`/`sldb.store` (if any exist) violate the import-scan is unspecified.
13. Line numbers (desk.py:223,249,262; operations.py:1567-1580; bootstrap.py:138,156) may be stale; mapping each to a specific operation is not given.
14. Whether `tests/test_doc_io.py` already exists (create vs. modify) is not stated.
15. `depends_on: task-rw-f2-typed-errors-and-exit-codes` has status `deferred`; whether that dependency is complete, and whether its error types are required by doc_io, cannot be determined from this document.
16. How the import-scan test detects imports (AST vs. regex) and whether it must ignore dynamic imports is unspecified.
17. `runs/planning/sldb-requests.md` append ordering/format beyond the three fields, and whether accumulating gaps blocks the Done When, is unspecified.
18. No acceptance criteria state what happens if a needed sldb api operation does not exist — the task says to keep the helper, but the Done When does not account for that outcome.
