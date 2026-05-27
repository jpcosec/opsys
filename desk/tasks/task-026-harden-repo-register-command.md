# Harden repo register command

ID: task-026
Status: active

## Goal

Make `repo register` validate all prerequisites before any filesystem mutation, so it cannot leave a half-configured registry directory when store or model dependencies are missing.

## Scope

In scope: preflight ordering, clear failure messages, and consistent store-path resolution between `repo register` and other desk CLI commands.

Out of scope: full redesign of the registry semantics, automatic store initialization, or cross-repo discovery features.

## References

- desk/cli/commands/repo.py
- desk/cli/parser.py
- desk/models/repository.py
- docs/faq.md

## Dependencies

- task-022
- task-024

## Pills

- pill-002
- pill-003
- pill-004
- pill-006
- pill-007

## Files

- desk/cli/commands/repo.py
- tests/test_cli.py
- docs/faq.md

## Implementation Path

Reorder the register method so that store context and model registration are resolved before any directory creation or file write. Fail clearly with a non-zero exit and no side effects when prerequisites are missing.

## Validation

- `repo register` without a store context fails clearly without creating files
- `repo register` with store and registered model succeeds
- the exit code distinguishes preflight failure from post-write failure

## Done When

`repo register` has a clear preflight contract: it validates prerequisites before mutating the filesystem and fails cleanly when they are missing.

## Tags

- system:opsys
- workspace:desk
- topic:cli
- topic:registry
