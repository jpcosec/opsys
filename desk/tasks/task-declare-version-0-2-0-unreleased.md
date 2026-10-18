---
id: task-declare-version-0-2-0-unreleased
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
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops declares version 0.2.0 (unreleased) in pyproject and CHANGELOG

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18 the coordinator noticed that pyproject.toml says 0.1.0 while the release drawer task targets 0.2.0. spec2viz is waiting for a clean deskops main to run its candidate suite. Under the owner's rule there are no tags or releases yet, so the version is declared but not published.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml says version 0.2.0, and CHANGELOG.md has its current entries under `## [0.2.0] - Unreleased`, with no date and an empty `## [Unreleased]` above it. No tag is created.

## Scope

_State what is in scope and what is out of scope._

In scope: pyproject.toml, CHANGELOG.md, and the release drawer task text (its remaining steps), edited through `deskops edit task`. Out of scope: tags, PyPI and dates.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Bump the version. 2. Rename the CHANGELOG heading and add an empty [Unreleased] section. 3. Run `pip install --no-deps -e .` and check that importlib.metadata reports 0.2.0. 4. Update the release drawer task so its steps are only the date, the tag and the push. 5. Run `pytest tests`.

## Validation

_List the checks required before this task can close._

- python -c "import importlib.metadata as m; print(m.version('deskops'))"
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The installed metadata says 0.2.0, the CHANGELOG has the unreleased 0.2.0 section, and `pytest tests` is green.
