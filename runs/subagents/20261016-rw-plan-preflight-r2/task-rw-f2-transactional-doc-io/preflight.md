RESTATEMENT:
1. Run `grep -rn 'from sldb\|import sldb' deskops` to enumerate every sldb call site and classify read vs write.
2. Create/rewrite `deskops/doc_io.py`: module docstring listing the allowlisted named private helpers; imports restricted to `sldb.api.*` (plus allowlisted private helpers).
3. Implement `DocTransaction` context manager in `doc_io.py`: no-op on enter; raise if entered twice (nesting unsupported); methods `tx.write(path, model, payload)`, `tx.track(path, model)`, `tx.untrack(path)`, `tx.delete(path)` each record the path's original bytes and tracked state before acting; on exception restore files and re-track/untrack to recorded state, then re-raise.
4. Port write call sites to go through `DocTransaction`: `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` (locate via grep across `deskops/operations.py`, `deskops/identity.py`, `deskops/bootstrap.py`).
5. Move closeout untrack (currently `operations.py:1567-1580`) to before the closeout commit and inside the transaction; make failure abort the closeout.
6. For any needed operation with no `sldb.api` equivalent, keep the private call as a named helper in `doc_io.py` and append a gap entry (function, why, proposed API) to `runs/planning/sldb-requests.md`.
7. Write `tests/test_doc_io.py`: monkeypatch the sldb call at each step to raise; assert file bytes and `sldb stores check` are unchanged after rollback; add an import-scan test failing if any non-`doc_io` module imports `sldb.` outside `sldb.api`, or `doc_io` imports a private name not in its allowlist.
8. Run `pytest tests/test_doc_io.py`, `pytest tests`, `sldb stores check --store .sldb`; confirm all green.
9. Do not commit; leave the diff for the supervisor's closeout commit.

AMBIGUITIES:
1. Which functions live in which file: task names `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc` but not their defining modules; `identity.py` and `bootstrap.py` are listed as files with no stated write call sites.
2. The private-helper allowlist contents are not given; I must decide which private names exist and which to allow.
3. `sldb.api` surface is unknown from the task text; I cannot know which write operations have public equivalents without inspecting sldb.
4. Undefined rollback semantics for a path with no prior file (new file) or no prior tracked state; not stated whether to delete or untrack.
5. `sldb stores check` invocation is given but not the working directory / store root assumption (`--store .sldb` presumes repo root).
6. Import-scan test scope unspecified: whole repo, only `deskops/`, or excluding tests/fixtures.
7. Monkeypatch granularity unspecified ("inject a failure at each step"): per-method, per-sldb-call, or per-port call site.
8. Injection mechanism unspecified: which sldb call is patched and at what layer (api vs private helper).
9. "Failure aborts the closeout" has no stated mechanism (exit code, exception type, message) or test.
10. Depends_on `task-rw-f2-typed-errors-and-exit-codes` was not provided; I cannot confirm prerequisite state or exit-code conventions.
11. Referenced artifacts not provided: `runs/planning/deskops-rewrite-inventory.md`, `runs/planning/sldb-requests.md` current format, pills `pill-012`, `pill-008`.
12. Whether `deskops/doc_io.py` already exists (rewrite vs create) is not stated.
13. "Every file+store write in deskops" scope boundary: whether writes outside the four listed files exist and must also be migrated.
14. Test data isolation not specified (repo `desk/` vs sandbox root), despite AGENTS.md sandbox guidance.
15. No stated acceptance count for migrated call sites, so "all migrated" is unverifiable except via the import scan.
