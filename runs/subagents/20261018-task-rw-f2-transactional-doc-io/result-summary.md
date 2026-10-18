# task-rw-f2-transactional-doc-io — result summary

## What changed

### New: `deskops/doc_io.py`
- `DocTransaction(root)`: re-entrant file+store transaction keyed by root (inner `with` joins the outer).
  - `write(path, model, payload)`, `track(path, model)`, `untrack(path_or_name)`, `delete(path)`, `record(path)`.
  - Records original bytes + tracked model/name before acting.
  - Rollback: untracks store entries created by the transaction / resets moved entries, restores file bytes, then re-tracks documents that were tracked before. Logs rollback failures and lets the original exception propagate.
- One-off helpers: `track`, `untrack`, `register_model`, `is_tracked`.
- Named wrappers for store-lifecycle writes: `link_store_alias`, `inherit_model_from`, `init_store_at`, `init_relations_in`, `update_store_indexes_in`, `remove_model_from`.
- Imports only `sldb.api` plus `PRIVATE_SLDB_IMPORTS = ("sldb.runtime.validation",)` (renderer only; no public re-export).

### `deskops/operations.py`
- `create_task_bundle`, `create_artifact`, `split_atom`, `merge_atom`: single `DocTransaction` per operation.
- `merge_atom` / `_rewrite_inbound_atom_references`: rewritten referrers are recorded in the transaction, so rollback restores them.
- `delete_atom`: `transaction.delete`.
- `_retarget_atom_documents`, `_untrack_atom_document`, `_track_created_document`: use `doc_io`.
- `_write_doc`: writes through `DocTransaction.write`; `_write_through_store`, `_document_is_tracked`, `_rollback` removed.
- `_auto_commit_task_closure`: whole closure inside one `DocTransaction`; task untracked **before** staging/commit; `.sldb` staged and included in the closeout commit; post-commit untrack removed.

### Other call sites
- `cli/commands/desk.py`: track/untrack/update-store through `doc_io`.
- `cli/commands/repo.py`: old positional `track_document` seam delegates to `doc_io.track`.
- `cli/commands/message.py`: same seam for `track_document`/`untrack_document`, delegates to `doc_io`.
- `cli/commands/promote.py`: `DocCLI().untrack` replaced by `doc_io.untrack`.
- `bootstrap.py`: link/inherit/init-relations/update-indexes/init-store through `doc_io`.
- `lifecycle.py`: `init_relations`, ritual track, untrack through `doc_io`.
- `lifecycle_migration.py`: `remove_model`, `update_store_indexes` through `doc_io`.
- `desk/contexts/pill-012-...md`: How now names `DocTransaction`.
- `.sldb` index refreshed with `sldb stores update` for the pill edit (not hand-edited).
- `runs/planning/sldb-requests.md`: recorded the missing `render_model_markdown` re-export.

### New tests: `tests/test_doc_io.py`
- Import scan: no module except `doc_io` imports `sldb.cli.commands`, `sldb.store.ops`, or write-side `sldb.api.documents.{create,delete,update,track,untrack}_*`.
- Import scan: `doc_io` imports only `sldb.api*` plus `PRIVATE_SLDB_IMPORTS`.
- Injected failures: re-track after write, track of a new file, delete, untrack, nested transaction; each asserts restored bytes and unchanged `check_store`.
- Closeout: after `advance` to complete, `git status --porcelain -- .sldb` is empty.

## Validation commands and final lines

```bash
PYTHONPATH=/tmp/rw/wt/docio python -m pytest tests/test_doc_io.py -q
# 8 passed in 5.91s

PYTHONPATH=/tmp/rw/wt/docio python -m pytest tests -q
# 395 passed, 3 skipped in 338.29s

PYTHONPATH=/tmp/rw/wt/docio python -m sldb stores check --store .sldb
# exit=0
# PASS: store integrity — 221 documents in 17 models
```

Also ran: `PYTHONPATH=... python -m deskops --help` and `... deskops faq` (both exit 0).

## Tests against unfixed code

None executed. The pre-change failure mode (closeout untrack after the commit) was read from the old `_auto_commit_task_closure`, not reproduced by running the new test against the old code.

## Task issues / ambiguities

- The task's line numbers are stale; call sites were located with grep and ported by function, not by line.
- Existing tests monkeypatch `deskops.cli.commands.message.track_document`/`untrack_document` and `deskops.cli.commands.repo.track_document` with the old 9-argument signature. Kept compatibility seams with those names that delegate to `doc_io`, instead of rewriting the tests.
- `sldb.api` does not re-export `render_model_markdown`; imported lazily from `sldb.runtime.validation` and declared in `PRIVATE_SLDB_IMPORTS`, with the gap recorded in `runs/planning/sldb-requests.md`.
- `lifecycle.py` and `lifecycle_migration.py` also held store writes though task item 6 did not list them; migrated them to satisfy "every sldb write call site".
- `identity.py` needed no change (read-only sldb imports only).
- Editing pill-012 directly made `sldb stores check` report a `data_mutation`; resolved with `python -m sldb stores update --store .sldb --pythonpath .` (exit 0). That is a store-index refresh, not a desk edit.
- No sldb bug found.
