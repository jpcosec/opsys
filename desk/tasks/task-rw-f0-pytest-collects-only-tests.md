---
id: task-rw-f0-pytest-collects-only-tests
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-rw-f0-declare-runtime-dependencies
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- pyproject.toml
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-rw-f0-pytest-collects-only-tests.md
---

# Bare `pytest` collects only the tests/ directory

## Rationale

_Explain why this task exists or the business driver behind it._

AGENTS.md names bare `pytest` as the minimum validation, but it also collects the untracked `tools/` checkout (another project's code), whose test fails, so the documented gate is red for reasons outside deskops. pyproject.toml already has a `[tool.pytest.ini_options]` table with `pythonpath` and `asyncio_default_fixture_loop_scope`.

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

Running `pytest` with no arguments from the repo root collects only `tests/`.

## Scope

_State what is in scope and what is out of scope._

In scope: one key in `[tool.pytest.ini_options]`. Out of scope: the contents of `tools/`, which deskops does not own.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add `testpaths = ["tests"]` to the existing `[tool.pytest.ini_options]` table, keeping its other keys.

## Validation

_List the checks required before this task can close._

- pytest
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Bare `pytest` reports the same passed count as `pytest tests` and both are green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
