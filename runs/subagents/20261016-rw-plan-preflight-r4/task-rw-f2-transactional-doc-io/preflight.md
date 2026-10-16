RESTATEMENT:
1. Read the routed material: `desk/contexts/pill-012-create-operations-transactional-rollback.md`, `desk/contexts/pill-008-kgdb-sldb-boundary.md`, and `runs/planning/deskops-rewrite-inventory.md` (findings D6/D7/S6) to get the contract and the call sites.
2. Enumerate sldb usage: `grep -rn 'from sldb\|import sldb' deskops`.
3. Create `deskops/doc_io.py` with a module-level `PRIVATE_SLDB_IMPORTS` tuple; import only `sldb.api.*` plus those private names.
4. Implement `DocTransaction(root)` as a re-entrant context manager exposing `write(path, model, payload)`, `track(path, model)`, `untrack(path)`, `delete(path)`; before each op record the path's original bytes and tracked state; on exception restore file bytes and re-track/untrack to the recorded state, then re-raise; inner `with` joins the outer (no independent commit).
5. Remove the `_with_rollback(write_fn, cleanup_fn)` helper in `deskops/operations.py` and replace its uses with `DocTransaction`; edit pill-012's How section to name `DocTransaction`.
6. Port `create_task_bundle`, `merge_atom`, `split_atom`, and `_write_doc` (in `deskops/operations.py`) to route store writes through the transaction (shared outer tx across nested calls).
7. Move the closeout untrack (currently `operations.py:1567-1580`, `store=None`, `pythonpath='.'`) to before the closeout commit and inside the transaction; a failure aborts closeout.
8. Migrate the remaining write call sites: `deskops/cli/commands/desk.py:223,249,262`; `repo.py:117`; `message.py:344`; `promote.py:86`; `bootstrap.py:138,156`; and `deskops/identity.py`'s `sldb.store` (resolver, layout) imports behind doc_io helpers.
9. For each needed operation with no `sldb.api` equivalent: add a named helper in `doc_io.py` using a listed private import, and append `(function, why, proposed API)` to `runs/planning/sldb-requests.md`.
10. Write `tests/test_doc_io.py`: monkeypatch each sldb call to raise, assert file bytes and `sldb stores check` output are unchanged after rollback; add an import-scan test over `deskops/` that fails if any module other than `doc_io` imports from `sldb.cli`/`sldb.store`, or `doc_io` imports a name outside `sldb.api` not in `PRIVATE_SLDB_IMPORTS`.
11. Run `pytest tests/test_doc_io.py`, `pytest tests`, and `sldb stores check --store .sldb`.

AMBIGUITIES:
1. `sldb.api` surface is never enumerated: which public functions do track/untrack/write/delete/query-tracked-state map to, and whether they exist at all, is left to discovery.
2. `PRIVATE_SLDB_IMPORTS` contents are not listed; the tuple's exact allowed names are the executor's choice, so the import-scan test's allowlist is self-defined.
3. `DocTransaction(root)` — `root` is undefined (desk root, repo root, or `.sldb` store root).
4. "tracked state" is not defined as a query: no API named for reading whether a path is currently tracked.
5. `payload` type in `tx.write(path, model, payload)` is unspecified (dict, model instance, rendered string, bytes), and `model` type/role is unspecified.
6. Whether `tx.write` also performs track/model-registration is unspecified, yet the Goal lists model registration as a write that must go through doc_io, and the transaction API has no registration method.
7. `tx.delete(path)` rollback semantics are unspecified: what "original bytes" means for a path that did not exist, and whether delete also untracks.
8. Re-entrancy semantics on normal inner `with` exit (commit? no-op?) and on inner failure are unspecified.
9. Restoration ordering (files vs store) and behavior if restoration itself fails are unspecified.
10. Nested `with` sharing "one transaction" — how a `root`-constructed inner instance finds the outer transaction is unspecified.
11. Import-scan rule tension: Goal says doc_io imports "only `sldb.api.*` plus `PRIVATE_SLDB_IMPORTS`", but the scan says `sldb.core.exceptions` (and `sldb`, `sldb.runtime.validation`) stay allowed "everywhere" — whether that override applies to doc_io is ambiguous.
12. Import-scan scope details unspecified: whether it scans `deskops/__init__.py`, dynamic/string imports, or only static `import`/`from` statements.
13. Test fixtures unspecified: whether `sldb stores check` is run via subprocess and against a temp sandbox store or the repo's `.sldb`; AGENTS.md mandates a sandbox for mutating CLI tests.
14. "asserts … `sldb stores check` are as before" — the expected baseline output/return code to compare against is not given.
15. Failure-injection points are not enumerated per step ("monkeypatch the sldb call to raise"), so which call to patch at each rollback test is a guess.
16. `create_task_bundle` -> `_write_doc` nesting is asserted as the sharing case, but the other three ports' nesting structure (`merge_atom`, `split_atom`, closeout) is not described.
17. Closeout path: which function/command performs the closeout commit and where exactly the untrack currently sits is only given as a line range; the resulting ordering vs. file unlink is not fully specified.
18. "Writes outside the four functions" — the four are never enumerated as a closed set, and the closeout untrack appears to be a fifth distinct write.
19. `deskops/identity.py` "resolver, layout" helpers' exact responsibility and how a layout/resolver call becomes a store write is not defined.
20. `files:` lists `runs/planning/sldb-requests.md` and the pill, but no acceptance criterion covers when/whether the pill edit or the sldb-requests append is verified.
21. Dependency `task-rw-f2-typed-errors-and-exit-codes` has no status in the doc; whether its error types must be used inside DocTransaction is unstated.
22. No specified public name/signature for the doc_io helpers besides the four tx methods, so the call-site migrations' target API is open.
