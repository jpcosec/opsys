# Align first-use docs with deskops

ID: task-023
Status: planned

## Goal

Make the repo documentation describe this package's real install and usage paths instead of inherited `sldb` guidance.

## Scope

In scope: README and FAQ usage instructions, package naming, and basic first-use examples.

Out of scope: comprehensive conceptual documentation for all desk models or cross-repo workflow design.

## References

- README.md
- docs/faq.md
- desk/README.md
- desk/tasks/task-022-stabilize-cli-first-use-entrypoints.md

## Dependencies

- task-022

## Pills

- pill-002
- pill-003
- pill-004

## Files

- README.md
- docs/faq.md
- desk/README.md

## Implementation Path

Update the top-level docs only after the public CLI name and invocation are stable.

Keep the edits focused on installation, invocation, dependency expectations, and where `desk/` fits in this repo.

## Validation

- README install and invocation examples work as written
- FAQ no longer tells users to run `sldb` for this package
- docs use the same public command name consistently

## Done When

The repository docs give correct first-use guidance for `deskops` without sending users to the wrong tool.

## Tags

- system:opsys
- workspace:desk
- topic:docs
- topic:onboarding
