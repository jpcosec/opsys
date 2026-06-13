# Stabilize init local store failures

ID: task-stabilize-init-local-store-failures
Status: deferred
Priority: high

## Goal

Make `deskops init` failure behavior safe and understandable for first-use repositories.

## Scope

- local `.sldb` setup
- local model registration
- existing store preservation
- first-use output that distinguishes global bootstrap, local store setup, and desk scaffolding

## Done When

- Existing stores remain untouched on failure.
- New local store setup either rolls back safely or reports a recoverable partial state.
- Tests cover happy path, existing `.sldb`, local store init failure, and model registration failure.
