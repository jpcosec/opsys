# Stabilize CLI first-use entrypoints

ID: task-022
Status: active

## Goal

Make the package install and first-use CLI entry surface work predictably in a clean environment.

## Scope

In scope: declared runtime dependencies, executable Python module entry, and consistent user-facing CLI naming across the first-run surface.

Out of scope: rewriting the full onboarding docs, changing store semantics, or redesigning desk scaffolding behavior.

## References

- pyproject.toml
- README.md
- docs/faq.md
- desk/cli/main.py
- desk/cli/parser.py

## Dependencies

- 

## Pills

- pill-002
- pill-003
- pill-004
- pill-007

## Files

- pyproject.toml
- desk/cli/main.py
- desk/cli/parser.py

## Implementation Path

Start with the smallest runtime correctness fixes: declare missing dependencies and make module execution work.

Then resolve the public command naming mismatch on the CLI surface so the package name, parser program name, and documented invocation do not contradict each other.

Leave the broader README and FAQ rewrite to task-023, but do not preserve contradictory naming inside the runnable CLI surface itself.

## Validation

- install-time runtime dependencies are sufficient for `faq` and `inbox`
- the top-level CLI imports cleanly in a clean environment with declared runtime dependencies
- `python -m desk.cli.main --help` works
- the CLI help text uses the same public name as packaging and docs

## Done When

A first-time user can install the package and discover the CLI without hitting missing imports or contradictory command names.

## Tags

- system:opsys
- workspace:desk
- topic:cli
- topic:packaging
