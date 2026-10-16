RESTATEMENT:
1. Check `task-rw-f2-typed-errors-and-exit-codes` is closed (dependency); if not, halt — task is `status: deferred` and must be promoted from drawer with a promotion commit before implementation (AGENTS.md).
2. Read `desk/contexts/pill-012-create-operations-transactional-rollback.md`, `desk/contexts/pill-008-kgdb-sldb-boundary.md`, `runs/planning/deskops-rewrite-inventory.md` (findings D6, D7, S6), and `deskops/{doc_io.py,operations.py,identity.py,bootstrap.py}`, `tests/test_doc_io.py`.
3. Run `grep -rn 'from sldb' deskops` to enumerate every call site.
4. Read `../sldb` public API surface; enumerate what `sldb.api.*` actually exports; map each call site (`ModelCLI().add`, `DocCLI().untrack`, `sldb.store.ops.track_document`, `sldb.store.io.*`) to a public equivalent or mark as gap.
5. Implement in `deskops/doc_io.py`: `DocTransaction` context manager that on enter records original bytes (and existence) and tracked state per path; on exception restores bytes/removes created files and re-tracks/untracks to match original state.
6. Port `create_task_bundle`, `merge_atom`, `split_atom`, `_write_doc`, and the closeout untrack in `operations.py` (lines ~1567-1580) onto `DocTransaction`.
7. For any operation lacking a public sldb API, wrap one private call in a named helper inside `doc_io.py` and record the gap.
8. Fix `identity.py` / `bootstrap.py` sldb imports if any.
9. Add failure-injection tests in `tests/test_doc_io.py` for each transaction step; assert disk bytes and tracked/untracked state are unchanged.
10. Run `pytest`, `sldb stores check --store .sldb`, and `grep -rn 'from sldb' deskops | grep -v doc_io.py | grep -v 'sldb.api'`.
11. Close with one atomic commit.

AMBIGUITIES:
1. Task is `status: deferred` and its dependency has unknown status — the doc gives no promotion or readiness instruction.
2. `sldb.api.*` is assumed to exist and to cover `ModelCLI().add`, `DocCLI().untrack`, `track_document`, and `sldb.store.io.*` — unverifiable from the doc.
3. Contradiction: "record the gap for the sldb inbox" vs "do not write into the sldb repo" — no location given for recording the gap.
4. `DocTransaction` API is unspecified: signature, nesting behavior, path-vs-store granularity, and whether one transaction spans multiple files.
5. Undefined behavior for paths that did not exist before the transaction (restore-by-delete?).
6. No specification of what "tracked state" is queried through, or how to re-track/untrack to match it.
7. Closeout untrack currently only warns; unclear whether it must now hard-fail and roll back, and what `store=None` / `pythonpath='.'` should become.
8. Unclear whether `_write_doc` becomes a nested transaction inside `create_task_bundle` or a separate one.
9. `merge_atom` rollback restore of rewritten referrers requires those referrers be in transaction scope — scope not stated.
10. Implementation path step 1 says "every `from sldb` import outside doc_io" but step 3 names only four functions; whether `bootstrap.py`/`identity.py` sites are in scope is unclear.
11. No acceptance criteria for failure-injection coverage: which steps, how many, what mechanism.
12. Unclear whether `tests/test_doc_io.py` exists or is created.
13. Validation commands give no working directory or sandbox requirement, though AGENTS.md requires a sandbox desk root for mutating CLI tests.
14. Validation grep excludes all of `doc_io.py` and any `sldb.api` line, so it cannot detect remaining private `sldb.api`-adjacent leakage.
15. "Done When" allows "or only documented gaps" without defining what counts as documented.
