---
id: task-message-selector-rejects-ambiguous-fragments
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
- tests/test_message_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# message read/ack and inbox --show/--ack reject an ambiguous slug fragment with exit 2

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-19, `deskops message ack 20261019-120241` acknowledged note 20261019-120253 instead of 20261019-120241. The 120253 note's title, and so its stem, quotes '20261019-120241'. MessageCommand._resolve_note returns the first substring match in reverse-sorted order, so an ambiguous fragment silently picks one note, even though the help promises a unique slug fragment.

## Goal

_Describe the concrete result this task must produce._

When a fragment matches more than one note, _resolve_note raises UsageError (exit 2) naming every candidate and acts on none. An exact filename or stem still wins, and a fragment matching exactly one note still works.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/message.py (_resolve_note, used by message read/ack and inbox --show/--ack) and tests/test_message_cli.py. Out of scope: the drawer and desk_paths selectors, which already reject ambiguity.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In _resolve_note, collect every fragment match; if there is more than one, raise UsageError listing the stems. 2. Test: two notes, where the second's stem contains the first's timestamp prefix; `message ack <prefix>` exits 2, lists both and leaves both open; the exact stem still acks the right one. 3. Check the test fails without the fix.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_message_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The ambiguous fragment exits 2 without acknowledging anything, the test reproduces the 120241/120253 case, and `pytest tests` is green.
