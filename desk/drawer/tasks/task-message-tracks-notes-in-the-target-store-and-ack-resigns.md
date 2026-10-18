---
id: task-message-tracks-notes-in-the-target-store-and-ack-resigns
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/cli/commands/message.py
- tests/test_message_cli.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- source:graph_ui
- topic:messaging
- topic:sldb
---

# `message`/`inbox` track a note in the target repo's store, and `--ack` re-signs it

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. (1) `deskops inbox --root <other repo>` run from graph_ui writes the note into the target desk (correct) but tracks the InboxNoteDoc in graph_ui's own store with an absolute path into the other repo: `MessageCLI._verify_and_track_note` (deskops/cli/commands/message.py:334) takes the store from `_store_context_safe(args.store)` (line 192), which falls back to `find_local_store()` of the cwd, not the target desk's repo. This happened with graph_ui's notes to spec2viz (graph_ui ae2978b) and to deskops (desk/inbox/20261018-003127-...). (2) `deskops inbox --root . --ack <slug>` (`_ack_note`, line 134) rewrites the note (status closed, acknowledged_by, acknowledged_at) and then calls the same `_verify_and_track_note`, which runs `track_document` again and fails with `Doc '<id>' already tracked`; the file is left changed but the store hash is stale, so `sldb stores check` FAILs with data_mutation and doctor reports an invalid document.

## Goal

_Describe the concrete result this task must produce._

A delivered note is tracked in the store of the repo that owns the target desk (the `.sldb` next to the target `desk/`), or not tracked with a warning when that repo has no store; `--ack` updates the tracked note so `sldb stores check` passes afterwards in the target repo.

## Scope

_State what is in scope and what is out of scope._

In scope: store selection for delivery and ack, and re-signing on ack, in message.py; tests. Out of scope: the `--sender` registry requirement (a repo must be in desk/registry to name itself; unchanged), and moving message.py onto doc_io (task-rw-f2-transactional-doc-io, which will port whatever this task leaves).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Store for a note = the `.sldb` directory of the target desk's repo (`desk_root.parent / '.sldb'`), unless `--store` is given explicitly; if it does not exist, deliver and print the existing 'Not tracked in the target store' warning. Track with paths relative to that repo, not absolute.
2. Ack: if the note is already tracked in that store, refresh it instead of tracking again; prefer the public `sldb.api` (for example `untrack_document` followed by `track_document_file`, or a public refresh/update call if sldb.api has one); a failure leaves the note file as it was before the ack (keep its bytes and restore them).
3. Tests in tests/test_message_cli.py with two sandbox repos A and B, each initialized (`deskops init`): deliver from cwd A to B's desk and assert A's store does not track the note, B's store does (`sldb.api.doc_status` or `sldb stores check --store B/.sldb` PASS) and its tracked path is relative; then `--ack` the note in B and assert exit 0, status closed, and `sldb stores check --store B/.sldb` PASS.

## Validation

_List the checks required before this task can close._

- pytest tests/test_message_cli.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both tests pass, B's store passes `sldb stores check` after delivery and after ack, A's store never tracks B's note, and `pytest tests` is green.

## Resolved Decisions

- CLI tests build a throwaway repo in pytest's `tmp_path` with the `lifecycle_desk` fixture (tests/conftest.py) or `_make_repo`/`_cli` from tests/test_lifecycle_end_to_end.py, and drive the real CLI. Never mutate the repo's own `desk/`.
- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
