# An empty selector resolves to the wrong document and fails with a raw validation error

## Kind

bug

## Status

open

## Problem

An empty selector is not rejected. It falls through to the document lookup and
picks up whatever matches first, so the user sees an internal Pydantic error for
a document they never asked for:

```
$ deskops show task "" --root .
Invalid value: 1 validation error for TaskDoc
status
  Field required [type=missing, input_value={'title': 'Desk Board', ...}, input_type=dict]
```

It resolved to the board, not to a task.

## Impact

An empty selector is the most likely typo (an unset shell variable). The error
names a field of a document the user did not mention, which sends them looking
in the wrong place.

## Desired outcome

An empty or whitespace-only selector is rejected with a clear message naming the
command and the subject, before any document lookup happens.

## Found by

Stress-test round 3; still reproducible as of 2026-09-24. Roadmap item H3 in
`issue-stress-test-fix-backlog.md`.
