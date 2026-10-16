RESTATEMENT:

1. Locate current state: read `deskops/doc_io.py`, `deskops/operations.py`, `deskops/identity.py`, `deskops/bootstrap.py`, `deskops/cli/commands/{desk,repo,message,promote}.py`, and `runs/planning/sldb-requests.md`.
2. Run `grep -rn 'from sldb\|import sldb' deskops` and enumerate every sldb import and its call site; flag writes vs the read-only calls (Resolved Decisions: model lookups, `sldb.runtime.validation.extract_model_data` stay).
3. Create/complete `deskops/doc_io.py` so all deskops sldb interactions are imports from `sldb.api.*`, except named private helpers declared in the module docstring.
4. Implement `DocTransaction` as a context manager constructed over one or more paths:
   - `__enter__` does nothing.
   - Methods: `tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)`, `tx.delete(path)`.
   - Before each action, record that path's original bytes and tracked state.
   - On exception: restore files, re-track or untrack back to the recorded state, then re-raise.
   - Raise if the context manager is entered twice; no nesting support.
5. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` so their file+store writes run inside `DocTransaction`, including untrack-on-rollback for `create_task_bundle` and referrer restoration for `merge_atom`.
6. Move the closeout untrack to before the commit and inside the transaction; make an untrack failure abort the closeout.
7. Move the other write sites into doc_io/DocTransaction: `deskops/cli/commands/desk.py:223,249,262`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,155`.
8. For each sldb operation with no `sldb.api` equivalent, keep it as a named private helper in doc_io and append `(function, why, proposed API)` to `runs/planning/sldb-requests.md`.
9. Write `tests/test_doc_io.py`: monkeypatch each sldb step to raise; assert file bytes and `sldb stores check --store .sldb` are unchanged after rollback.
10. Add an import-scan test over the `deskops/` package (not `tests/`) that fails if a write-side sldb import appears outside doc_io, or doc_io imports a private name not in its module-docstring allowlist.
11. Run `pytest tests/test_doc_io.py`.
12. Run `pytest tests`.
13. Run `sldb stores check --store .sldb`.
14. Do not commit; leave the diff for the supervisor.

AMBIGUITIES:

1. Current contents/state of `deskops/doc_io.py` are not given; unknown whether it exists, whether `DocTransaction` partly exists, or it must be created wholesale.
2. `DocTransaction` constructor is unspecified: how the store/root handle is passed (task says "over one or more paths"), and how tx methods reach `sldb stores check`'s store.
3. `tx.write(path, model, payload)` semantics are unspecified: bytes-only write vs write+track, order relative to recording original state, and what `payload` is.
4. Recording/restoring "tracked state" for a path that was not tracked is unspecified (how untracked is represented, and which model a restore untrack uses).
5. Rollback ordering (reverse vs any), behavior for recorded-but-not-yet-acted paths, and whether restore is best-effort or fails hard are unspecified.
6. "Raise if entered twice" mechanism is unspecified (instance flag, re-entrant `__enter__`, nested instances).
7. "Port" is ambiguous: move function bodies into doc_io.py, or leave them in operations.py and replace their writes with doc_io calls.
8. Whether fixing `merge_atom`'s missing rewritten-referrer restoration is required, and what "rewritten referrers" concretely are (which files/steps), is not defined.
9. Whether fixing `create_task_bundle`'s missing untrack and `_write_doc`'s two-step untrack/track is required beyond routing through the transaction is not stated.
10. Closeout untrack: which store/handle it should use (doc notes current `store=None`, `pythonpath='.'`), and the observable meaning of "aborts the closeout" (exit code, message) are unspecified.
11. Import-scan allowlist source ("listed in its module docstring") has no format; how to classify an import as write-side vs read-only is unspecified, as is whether `sldb.api` is the confirmed public path and whether relative imports count.
12. "Inject a failure at each step" does not enumerate what "each step" covers (each tx method, each ported function, or both).
13. The extra write sites (`desk.py:223,249,262`, `repo.py:117`, `message.py:344`, `promote.py:86`, `bootstrap.py:138,155`) are given only as line numbers; their content is unknown, line numbers drift after earlier edits, and it is not stated whether moving them means relocating code or routing existing calls.
14. The boundary of "every file+store write" is undefined; no measured inventory is provided to prove completeness.
15. `runs/planning/sldb-requests.md` entry format and whether the file exists are unspecified; whether the task blocks on an unresolved gap vs proceeding with a named helper is not stated.
16. Whether `sldb.api` actually exposes equivalents for track/untrack/write is unverified; task gives no capability list.
17. Task status is `deferred` and `depends_on: task-rw-f2-typed-errors-and-exit-codes` is not shown as satisfied; whether execution should proceed now is not stated.
18. Referenced pills (`pill-012`, `pill-008`) and their `when`/`where`/`how_not` content are not included, so their constraints cannot be checked here.
