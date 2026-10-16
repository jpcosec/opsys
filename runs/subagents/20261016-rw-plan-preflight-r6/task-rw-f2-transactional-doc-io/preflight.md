RESTATEMENT:
1. Confirm dependency `task-rw-f2-typed-errors-and-exit-codes` is closed; read `deskops/doc_io.py`, `deskops/operations.py`, `deskops/identity.py`, `deskops/bootstrap.py`, the four CLI command modules, `sandbox`-safe test harness, and `desk/contexts/pill-012-create-operations-transactional-rollback.md`.
2. `grep -rn 'from sldb\|import sldb' deskops` to list every sldb import and call site, separating read-side from write-side.
3. Determine which write operations have `sldb.api.*` equivalents; for each without one, keep it as a named helper inside `deskops/doc_io.py` and append `(function, why, proposed API)` to `runs/planning/sldb-requests.md`.
4. Write `deskops/doc_io.py`: module-level `PRIVATE_SLDB_IMPORTS` tuple listing the only private sldb names allowed; `DocTransaction(root)` as a re-entrant context manager (inner `with` joins the outer transaction).
5. Implement `DocTransaction` record/apply/rollback: `write(path, model, payload)`, `track(path, model)`, `untrack(path)`, `delete(path)`; record each path's original bytes plus tracked state before acting; on exception restore file bytes and re-track/untrack to recorded state, then re-raise.
6. Remove `_with_rollback(write_fn, cleanup_fn)` usage; make `DocTransaction` the single mechanism; edit pill-012's How section to name `DocTransaction`.
7. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` in `deskops/operations.py` to route all store writes through `DocTransaction`; ensure nested `create_task_bundle -> _write_doc` joins one transaction; ensure `merge_atom` rollback restores rewritten referrer files.
8. Move closeout untrack before the closeout commit and inside the transaction, and make a failure abort the closeout (drop the log-warning-only path, drop `store=None`/`pythonpath='.'` workaround).
9. Migrate remaining write call sites to `doc_io`: `deskops/cli/commands/desk.py` (around 223, 249, 262), `repo.py` (~117), `message.py` (~344), `promote.py` (~86), `bootstrap.py` (~138, 156).
10. Create `tests/test_doc_io.py`: monkeypatch each sldb call step to raise, then assert pre/post file bytes and `sldb stores check` state are unchanged; cover transaction nesting and closeout-abort.
11. Add import-scan test over the `deskops/` package only: fail on any write-side sldb import outside `doc_io` (`sldb.cli*`, `sldb.store.ops`, `sldb.api.documents.create_*|delete_*|update_*|track_*|untrack_*`); also fail if `doc_io` imports a non-`sldb.api` sldb name not in `PRIVATE_SLDB_IMPORTS`. Keep read-side imports (`sldb.store.io.load_store_index`, `sldb.store.resolver.find_local_store`, `sldb.store.layout`, `sldb.runtime.validation`, `sldb.core.exceptions`, `sldb.StructuredNLDoc`) allowed everywhere.
12. Run `pytest tests/test_doc_io.py`, then `pytest tests`, then `sldb stores check --store .sldb`; report diff; do not commit.

AMBIGUITIES:
1. Task `status: deferred` with `source:drawer`, while Resolved Decisions say the supervisor promotes it first; whether I should execute now or wait is unclear.
2. Exact contents of `PRIVATE_SLDB_IMPORTS` are not given; I must guess which private names are legitimate.
3. `DocTransaction(root)` — is `root` the store root (`.sldb`), the desk root, or the repo root?
4. `payload` shape for `tx.write(path, model, payload)` is unspecified (dict, dataclass, SimpleNamespace, raw text).
5. Rollback semantics for a path with no prior bytes (new file) are not stated explicitly; delete-on-rollback is inferred.
6. Whether `tx.delete(path)` also untracks, or only unlinks, is unspecified.
7. `sldb.api` equivalents for track/untrack/model registration are unknown; the "no equivalent" threshold and where to inspect sldb are undefined.
8. How `store=None` and `pythonpath='.'` (operations.py:1567-1580) map onto `DocTransaction` is unstated.
9. "a failure aborts the closeout" — the observable behavior (raise, non-zero exit, transaction-only) is not specified.
10. Test method for asserting `sldb stores check` state is unspecified (subprocess CLI vs python API vs store diff).
11. Import-scan implementation method is unspecified: AST/source parsing vs runtime inspection; whether `deskops/cli/**` subpackages and `__init__.py` re-exports count.
12. Fill-in line numbers in cited files may have drifted; whether to match by content or by line is unclear.
13. `depends_on: task-rw-f2-typed-errors-and-exit-codes` — its status is not stated, so readiness cannot be confirmed from this document alone.
14. "monkeypatch the sldb call to raise" per step — granularity (per write/track/untrack/delete, per call site, or per ported function) is unspecified.
