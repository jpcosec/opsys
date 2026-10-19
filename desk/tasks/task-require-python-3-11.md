---
id: task-require-python-3-11
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
- CHANGELOG.md
- .github/workflows/tests.yml
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops requires Python >=3.11

## Rationale

_Explain why this task exists or the business driver behind it._

The coordinator decided on 2026-10-18. spec2viz-49's candidate run (spec2viz tools/suite-check.sh, matrix 3.10/3.12/3.13) showed that deskops does not even collect on 3.10: deskops/models/atom.py uses enum.StrEnum, which exists only from 3.11, yet pyproject.toml declares requires-python >=3.10. spec2viz, graph_ui and pron already declare >=3.11, so the suite's real floor is 3.11. StrEnum stays as it is.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml declares requires-python >=3.11, the CHANGELOG 0.2.0 section records it, and CI runs pytest on a 3.11/3.12/3.13 matrix.

## Scope

_State what is in scope and what is out of scope._

In scope: pyproject.toml, CHANGELOG.md, .github/workflows/tests.yml, and closing spec2viz's candidate-run inbox note. Out of scope: rewriting StrEnum.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Set requires-python and update the classifiers, if there are any. 2. Add a line under [0.2.0] Changed. 3. Turn the CI python-version into a matrix ["3.11", "3.12", "3.13"] and drop the comment that pins 3.13 for the help goldens; since 623f6c7 the help goldens do not depend on the Python version. 4. Run pytest locally on 3.13 and run the help goldens on 3.12 (/tmp/rw/venv312).

## Validation

_List the checks required before this task can close._

- python -m pytest tests -q
- /tmp/rw/venv312/bin/python -m pytest tests/test_output_goldens.py -q -k help_goldens

## Done When

_Name the observable condition that makes the task complete._

The metadata says >=3.11, the CI matrix runs 3.11 to 3.13, and `pytest tests` is green.
