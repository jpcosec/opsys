---
id: task-message-tracks-only-in-the-target-store
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/cli/commands/message.py
- tests/test_message_delivery.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# A sent note is tracked only in the target repo's store, never in the sender's

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. `deskops inbox --repo sldb --sender graph_ui ...` (the deprecated alias) wrote the note into sldb/desk/inbox correctly, but it also tracked it as an InboxNoteDoc in the sender's store (graph_ui/.sldb), with an absolute path into sldb. graph-ui-59 reverted that write by hand. ec68ef5 made `message send` track the note in the target store; this path, and possibly `message send --repo`, still writes to the sender's.

## Goal

_Describe the concrete result this task must produce._

`deskops message send` and the deprecated `deskops inbox` alias, in every addressing form (--root, --repo, --to), track the delivered note only in the target repo's store, with a target-relative path. The sender's store does not change.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/message.py and the deprecated inbox alias path, plus tests. Out of scope: the note format.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Reproduce with two sandbox repos, both registered: send from A to B with --repo, then with the deprecated `inbox` alias. Assert that A's .sldb is byte-identical before and after, and that B's store tracks desk/inbox/<note>.md relative to B. 2. Fix the store selection so it always uses the target repo's .sldb. 3. Cover --root, --repo and --to.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_message_delivery.py tests/test_message_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The three addressing forms leave the sender's store unchanged in tests, and `pytest tests` is green.
