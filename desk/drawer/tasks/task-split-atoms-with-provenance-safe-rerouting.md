# Split atoms with provenance-safe rerouting

ID: task-split-atoms-with-provenance-safe-rerouting
Status: deferred
Priority: medium

## Rationale

Atom split operations were explicitly deferred from `task-define-atom-lifecycle-operations` to keep the shipped slice bounded and safe.

## Goal

Define and implement a split workflow for atoms that preserves provenance and handles downstream references explicitly.

## Scope

- define `deskops atoms split ...` contract
- preserve or reroute provenance links
- detect and handle inbound references before mutation
- add sandbox CLI tests

## Non-goals

- merge operations
- create-from-source flows

## Validation

- `pytest`
- focused CLI tests for split behavior
