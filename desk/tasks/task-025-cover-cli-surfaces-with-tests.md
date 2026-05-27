# Cover CLI surfaces with tests

ID: task-025
Status: planned

## Goal

Add targeted tests for the real CLI surfaces so first-use regressions are caught automatically.

## Scope

In scope: tests for `faq`, `inbox`, entrypoint behavior, and the stabilized `desk install` contract.

Out of scope: exhaustive integration tests for every SLDB store behavior.

## References

- tests/test_composition.py
- tests/test_atom_materialization.py
- desk/cli/main.py
- desk/cli/commands/faq.py
- desk/cli/commands/inbox.py
- desk/cli/commands/desk.py

## Dependencies

- task-022
- task-024

## Pills

- pill-002
- pill-003

## Files

- tests/
- desk/cli/main.py
- desk/cli/commands/faq.py
- desk/cli/commands/inbox.py
- desk/cli/commands/desk.py

## Implementation Path

Cover the smallest stable public behaviors first: help output, FAQ listing, and inbox read/write flows.

Once `desk install` is stabilized, add tests for its success and failure paths instead of freezing today's ambiguous behavior.

## Validation

- CLI-facing tests fail when entrypoint or runtime dependency regressions are reintroduced
- first-use command paths are exercised without relying on manual inspection only

## Done When

The repo has automated coverage for the primary CLI behaviors needed to judge first-use readiness.

## Tags

- system:opsys
- workspace:desk
- topic:tests
- topic:cli
