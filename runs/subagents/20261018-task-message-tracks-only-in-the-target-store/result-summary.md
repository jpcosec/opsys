# result-summary: task-message-tracks-only-in-the-target-store

## Changes

- `deskops/cli/commands/message.py`
  - `MessageCLI._note_store_context`: `--store` is now honored only when its
    `get_store_context` project root equals the target repo root
    (`desk_root.parent`). Otherwise the target repo's own `<target>/.sldb` is
    used. The sender's store is no longer a fallback, so tracking always writes
    to the target store with a target-relative path.
- `tests/test_message_delivery.py`
  - Added `_store_snapshot` helper (relative path -> bytes).
  - Added `test_send_with_root_tracks_only_in_target_store`.
  - Added `test_send_to_registered_repo_tracks_only_in_target_store`
    (canonical `--to` form).
  - Added `test_legacy_inbox_repo_tracks_only_in_target_store`
    (deprecated `inbox --repo` form).
  - Each asserts the sender's `.sldb` is byte-identical before/after and the
    target tracks `desk/inbox/<note>.md` (relative, status ok).
- `tests/test_cli.py`
  - `_setup_inbox_identity_env` now creates the target repo's `.sldb`. The old
    fixture modeled one shared ecosystem store, which conflicts with the new
    target-store-only contract.

## Validation

- `PYTHONPATH=/tmp/rw/wt/msgtarget python -m pytest tests/test_message_delivery.py tests/test_message_cli.py -q`
  -> `15 passed in 82.00s (0:01:21)`
- `PYTHONPATH=/tmp/rw/wt/msgtarget python -m pytest tests -q`
  -> `520 passed, 3 skipped in 737.67s (0:12:17)`

## Against the unfixed code

- Manual repro before the fix: `message send --to b` wrote
  `.sldb/core/documents/InboxNoteDoc/...` etc. into the sender's store with
  `path='/tmp/rw/repro/B/desk/inbox/...'`, while the target's `doc_status` was
  `missing`.
- New tests run against `HEAD`'s `message.py`:
  -> `2 failed, 1 passed` (`--to` and legacy `--repo` failed; `--root` already
  passed because that form was already correct).

## Task notes / ambiguity

- The task says to verify cited line numbers, but cites none. Located
  `_note_store_context` directly.
- `message send` has no `--repo`; its registry form is `--to` (dest `repo`).
  The deprecated `inbox` alias has `--repo`. Both were fixed and tested.
- No sldb bug observed.
