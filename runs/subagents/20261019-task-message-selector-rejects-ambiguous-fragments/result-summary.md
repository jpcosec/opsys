# result summary: task-message-selector-rejects-ambiguous-fragments

Done by the supervisor directly.

- `deskops/cli/commands/message.py` `_resolve_note`: an exact filename or stem still wins. A fragment that matches several notes now raises `UsageError` (exit 2), naming every candidate stem, and acts on none. A fragment matching a single note still resolves. The function backs `message read/ack` and `inbox --show/--ack`.
- `tests/test_message_cli.py::test_message_ack_rejects_a_fragment_that_matches_two_notes` reproduces the 120241/120253 case: a second note whose title quotes the first note's timestamp prefix. The prefix exits 2, lists both notes and leaves both open; the exact stem then acks only the first. Without the fix the test fails with exit 0, acking one note silently.
- Checked on this repo: `message read 20261019-120241` and `inbox --show 20261019-120241` both exit 2.
- The wrong ack from the incident: 120253 was acknowledged in place of 120241. Its own ack was due anyway, since its hash correction was applied. 120241 was then acknowledged by its full stem in 338a4a4, so the final state is correct and needs no further change.

Full suite: see validation.log.
