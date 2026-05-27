# Make desk install match documented structure

ID: task-024
Status: planned

## Goal

Make `desk install` produce a coherent desk surface that matches the repo's documented structure and fails safely when prerequisites are missing.

## Scope

In scope: scaffolded directories and files, install flow behavior, and failure handling around registration assumptions.

Out of scope: broader repository discovery features or a full redesign of desk registry semantics.

## References

- desk/README.md
- desk/cli/commands/desk.py
- desk/cli/commands/repo.py
- desk/tasks/task-021-operate-over-sldb-desk-tasks.md

## Dependencies

- task-022

## Pills

- pill-002
- pill-003
- pill-004
- pill-007

## Files

- desk/cli/commands/desk.py
- desk/cli/commands/repo.py
- desk/README.md

## Implementation Path

First decide which structure is canonical: the documented desk layout or the current scaffold output.

Then make `desk install` either remain a pure scaffold command or validate its registration prerequisites before partially mutating the target repo.

## Validation

- `desk install` creates the documented structure or the docs are updated to match intentionally
- installation does not leave a half-configured desk because of late registration failure
- targets outside the detected ecosystem root fail clearly or are handled intentionally

## Done When

`desk install` has a clear contract, produces the expected structure, and handles its prerequisite boundaries safely.

## Tags

- system:opsys
- workspace:desk
- topic:cli
- topic:bootstrap
