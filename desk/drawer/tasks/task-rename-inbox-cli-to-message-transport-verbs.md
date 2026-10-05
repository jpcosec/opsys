---
id: task-rename-inbox-cli-to-message-transport-verbs
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-operational-cli-grammar-follows-spoken-workflow.md
- desk/contexts/pill-cross-desk-inbox-needs-delivery-verification-and-follow-up.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-machine-readable-cli-output-needs-stable-contract.md
files:
- deskops/cli/commands/message.py
- deskops/cli/commands/inbox.py
- deskops/cli/parser.py
- deskops/cli/main.py
- tests/test_message_cli.py
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:cli
- topic:cross-repo
---

# Rename the `inbox` CLI to `message` transport verbs

## Rationale

_Explain why this task exists or the business driver behind it._

Extracted from the abandoned `iso-lab/deskops` worktree commit `f857d72`
("rename inbox CLI to 'message' with send/list/read/ack transport verbs"). The
observed failure was semantic: agents reading the command name `inbox` wrote a
local `desk/inbox/*.md` file instead of routing a message through the CLI, so
coordination notes never reached the target desk.

Renaming the command to a transport noun with explicit verbs removes the
ambiguity between "the `desk/inbox/` storage directory" and "the act of sending
a cross-desk message".

## Goal

_Describe the concrete result this task must produce._

`deskops message` becomes the canonical CLI surface for cross-desk coordination
with verbs `send`, `list`, `read`, `ack`, while `deskops inbox` remains as a
deprecated alias so existing docs, pills, and scripts keep working.

## Scope

_State what is in scope and what is out of scope._

- IN: `message send|list|read|ack` parser surface; `MessageCLI`; `inbox` kept as a
  deprecation alias with its legacy flags; docs/skill/atom updates; tests.
- OUT: renaming the `InboxNoteDoc` model or the `artifact.inbox_note` spec
  artifact. `desk/inbox/**` is intentionally not SLDB-modeled (see
  `deskops.workspace.desk_doc_unmodeled_reason`), so the document contract stays
  as-is; only the command grammar changes.

## Implementation Path

_Outline the expected implementation route or affected surface._

- `deskops/cli/commands/message.py`: `MessageCLI` with subcommand dispatch plus a
  legacy-flags path reused by the `inbox` alias.
- `deskops/cli/commands/inbox.py`: thin `InboxCLI(MessageCLI)` deprecation shim.
- `deskops/cli/parser.py`: `_add_message_commands` with `send/list/read/ack`;
  `_add_inbox_commands` kept and marked deprecated.
- `deskops/cli/main.py`: route both `message` and `inbox`.

## Validation

_List the checks required before this task can close._

- pytest
- `python -m deskops message --help`
- `python -m deskops inbox --help` still works

## Done When

_Name the observable condition that makes the task complete._

`deskops message send|list|read|ack` works end to end, `deskops inbox` still
works as a deprecated alias, tests pass, and the change is committed.
