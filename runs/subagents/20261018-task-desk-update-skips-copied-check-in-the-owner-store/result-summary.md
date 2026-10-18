# result summary: task-desk-update-skips-copied-check-in-the-owner-store

Done by the supervisor directly.

- `deskops/cli/commands/desk.py`: when the store being updated is the deskops owner store itself, `DeskCLI.update` sets owner_store to None for the copied-model check, so it no longer lists the models it registers directly as copies.
- `tests/test_desk_sync.py`: `test_desk_update_does_not_call_the_owner_store_models_copies` builds a store with directly registered models (init without an owner). Pointed at another owner store, it still reports copies. Pointed at itself, it reports none. The test fails on the unfixed code.
- `deskops desk update --root .` in this repo now prints "Desk is up to date.".

Full suite: see validation.log.
