---
id: task-require-sldb-0-1-13
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

# deskops declares structuredLanguageDB>=0.1.13

## Rationale

_Explain why this task exists or the business driver behind it._

deskops relies on sldb features that are not in 0.1.12: unlink_store, link_store(replace=True) and broken_links (691f1ae, used by the owner-link repair in 33c0482), and the extraction fixes 9dcabd9a and d31180e4 that the goldens record. On 2026-10-18 sldb-04 bumped sldb main to 0.1.13 (a0b86941). There is no tag and no PyPI release, by the owner's no-deploy rule. pip now accepts the floor from the checkout. The coordinator asked to declare it as soon as sldb announced it.

## Goal

_Describe the concrete result this task must produce._

pyproject.toml requires structuredLanguageDB>=0.1.13, `pip install -e .` resolves against the sldb checkout, CI (which installs sldb from git main) stays green, and the release drawer task no longer lists the floor as pending.

## Scope

_State what is in scope and what is out of scope._

In scope: pyproject.toml, the CHANGELOG [Unreleased] entry, and the release drawer task text. Out of scope: tagging or publishing anything.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Change the dependency floor. 2. Run `pip install --no-deps -e .` in the base env and check it resolves. 3. Add a CHANGELOG line. 4. Update the release drawer task with `deskops edit task` (it reaches drawer tasks since b970352) to drop step 1. 5. Run `pytest tests`.

## Validation

_List the checks required before this task can close._

- pip install --no-deps -e .
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

pip accepts the floor against the checkout and `pytest tests` is green.
