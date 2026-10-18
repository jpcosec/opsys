# Result summary — `message` tracks notes in the target repo's store, `--ack` re-signs

Worktree: `/tmp/rw/wt/msgstore` (no commits, no `desk/` mutations).

## Changes

`deskops/cli/commands/message.py`
- Added `from sldb.api import untrack_document`.
- Replaced `_store_context_safe(store_arg)` with `_note_store_context(args, desk_root)`:
  - explicit `--store` still wins via `get_store_context`;
  - otherwise returns `(desk_root.parent / ".sldb", desk_root.parent)` when that store exists;
  - otherwise returns `None`.
- `_verify_and_track_note(args, path, desk_root)`:
  - returns `None` and prints `Warning: no .sldb store at ...; not tracking ...` when the target repo has no store;
  - tracks through the target repo's store/root, so `track_document` records a repo-relative path;
  - on `SLDBStoreError` containing `already tracked`, calls public `sldb.api.untrack_document` and re-tracks.
- `_deliver_note` passes `desk_root` to `_verify_and_track_note`.
- `_ack_note` keeps the note's original bytes, writes the closed/ack payload, and restores the original bytes if tracking fails before re-raising.

`tests/test_message_cli.py`
- Added `_cli`, `_sldb_stores_check`, `_init_repos` (two real `deskops init` repos, A and B), `_deliver`.
- `test_message_delivery_tracks_note_in_target_repo_store`: A's store does not track; B's store does; tracked path is `desk/inbox/<name>.md` (relative); `sldb stores check --store B/.sldb` PASS.
- `test_message_ack_refreshes_note_tracked_in_target_repo_store`: ack exits 0, status closed, acknowledged_by repo-b, B check PASS, A still missing.
- `test_message_ack_restores_note_when_tracking_fails`: failed refresh exits 1, note bytes unchanged, B check PASS.

## Validation

Pre-fix (tests written first):
- `PYTHONPATH=/tmp/rw/wt/msgstore python -m pytest tests/test_message_cli.py -q`
  - `3 failed, 4 passed in 29.43s` (all three new tests failed)
- `PYTHONPATH=/tmp/rw/wt/msgstore python -m pytest tests/test_message_cli.py::test_message_delivery_tracks_note_in_target_repo_store -q`
  - `1 failed in 10.05s`, at `assert doc_status(repo_a / ".sldb", note.stem).status == "missing"` → `assert 'ok' == 'missing'` (bug reproduced: sender A tracked B's note).

Post-fix:
- `PYTHONPATH=/tmp/rw/wt/msgstore python -m pytest tests/test_message_cli.py`
  - `7 passed in 29.08s`
- `PYTHONPATH=/tmp/rw/wt/msgstore python -m pytest tests -q`
  - `351 passed, 3 skipped in 743.97s`

## Task notes / ambiguities

- Cited line numbers were accurate in the unmodified tree (`_ack_note` 134, `_store_context_safe` 192, `_verify_and_track_note` 334).
- Implementation Path says to prefer public `sldb.api` for refresh (e.g. `untrack_document` + `track_document_file`). `sldb.api` has no public refresh/update call. I used public `untrack_document` for the refresh and kept the pre-existing low-level `track_document` call, which existing `tests/test_cli.py` mocks and which already records a relative path when given the target repo root.
- "Not tracked when the repo has no store" applies to ack too: ack still succeeds and prints the existing "Not tracked in the target store..." line.
- No sldb bug observed; no sldb files changed.
