---
id: task-init-repairs-a-broken-owner-link
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-tests-never-touch-the-real-global-store
pills:
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- deskops/bootstrap.py
- tests/test_doctor_model_registration.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-init-repairs-a-broken-owner-link.md
---

# `deskops init` repairs a broken `deskops` store link instead of skipping it

## Rationale

_Explain why this task exists or the business driver behind it._

Since 66f81ff, `_ensure_owner_link` in deskops/bootstrap.py warns and skips registration when a store's existing `deskops` link points somewhere else, because sldb had no way to replace a link. On 2026-10-18 sldb-04 added `sldb.api.unlink_store(store, name)` and `link_store(store, other, name, replace=True)` (CLI: `sldb stores remove <name>` and `sldb stores add <path> --name N --replace`) in sldb main 691f1ae, not yet released. `check_store()` now returns `broken_links` (`{name, path, resolved, status}`) for links whose target is missing or not a store. sldb-04's guidance: replace only a broken link (status `missing`/`not-a-store`), never a healthy link to another store.

## Goal

_Describe the concrete result this task must produce._

`deskops init` and `bootstrap`, on a store whose `deskops` link is broken, re-point the link at the current owner store with `replace=True` and register the models. A healthy link to a different store is still left alone, with the warning.

## Scope

_State what is in scope and what is out of scope._

Coordinator decision (2026-10-18): while there are no releases, development uses sldb main (the editable checkout), which has unlink_store, link_store(replace=True) and broken_links (691f1ae). In scope: deskops/bootstrap.py repairs a 'deskops' link that points at a missing or different store. It uses link_store(..., replace=True) when sldb exposes it, and keeps today's warning on an sldb without it (feature check, not a version check), plus tests. The dependency floor moves to structuredLanguageDB>=0.1.13 together with the release task, once sldb main declares 0.1.13: pinning it now breaks 'pip install -e .' because sldb main still reports 0.1.12. Out of scope: sldb itself.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Read the link's status from sldb (`check_store(...)["broken_links"]`, or the store_links status). If it is broken, call `link_store(..., replace=True)`. If it is healthy and points elsewhere, keep the warning and skip.
2. Tests with an isolated HOME: (a) a store whose `deskops` link points to a deleted directory is repaired by `deskops init`, and `sldb stores check` passes; (b) a store linked to another real store is left unchanged, with the warning.

## Validation

_List the checks required before this task can close._

- pytest tests/test_doctor_model_registration.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

Both tests pass and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

- Waiting on the sldb release that contains 691f1ae.
