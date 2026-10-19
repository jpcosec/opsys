---
id: task-require-python-3-12
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
- pyproject.toml
- .github/workflows/tests.yml
- CHANGELOG.md
- tests/test_python_floor_compat.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops requires Python >=3.12 and drops 3.10/3.11 compatibility code

## Rationale

_Explain why this task exists or the business driver behind it._

Owner decision of 2026-10-19: Python 3.10 reaches end of life this month, so every repo in the suite raises its floor to 3.12 rather than holding code back for old interpreters. deskops declared >=3.11 since d8650c8. Its only compatibility code for older interpreters is tests/test_python_floor_compat.py, which guards against PEP 701 f-strings so that 3.10 and 3.11 could still import the package.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml declares requires-python >=3.12. CI runs pytest on a 3.12/3.13 matrix. The CHANGELOG 0.2.0 section states the floor. The 3.10/3.11 compatibility test is gone. No docs mention an older floor.

## Scope

_State what is in scope and what is out of scope._

In scope: pyproject.toml, .github/workflows/tests.yml, CHANGELOG.md, tests/test_python_floor_compat.py, and docs that state a Python version (none found by grep). Out of scope: the sldb capability guard in deskops/graph/snapshot.py, which checks for an sldb API, not a Python version.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Set requires-python. 2. Change the CI matrix to ["3.12", "3.13"]. 3. Replace the 3.11 CHANGELOG line with the 3.12 floor and say why. 4. Delete the compat test with deskops retire? No: it lives in tests/, not desk/, so delete it with git rm as part of the closeout paths. 5. grep for sys.version_info, typing_extensions and similar shims once more. 6. Run pytest.

## Validation

_List the checks required before this task can close._

- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The metadata says >=3.12, the CI matrix is 3.12 and 3.13, the compat test is removed, and `pytest tests` is green.
