---
id: task-desk-update-skips-copied-check-in-the-owner-store
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
- deskops/cli/commands/desk.py
- tests/test_desk_sync.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `desk update` does not report the deskops store's own models as copies

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18. In the deskops repo, `deskops desk update --root .` always reports "Copied deskops models: CrossroadDoc, AtomDoc, ..." and exits 1. This repo's .sldb is the deskops owner store: it registers the models directly, and other stores link to it. The copy check compares against the owner store without excluding the owner itself, so the dry-run is never clean here, and `--apply` "converts" models it should leave alone. The conversion skipped adding a self-link, so it did no harm.

## Goal

_Describe the concrete result this task must produce._

In the owner repo, `desk update` reports no copied models and exits 0 when nothing else diverges, while other stores still get the copied-model check.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/desk.py (skip the copied check when the store is the owner store) and a test. Out of scope: the federation design.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In DeskCLI.update, treat owner_store as absent for the copy check when store_dir.resolve() == owner_store.resolve(). 2. Test: point the owner store at a sandbox store that registers models directly; desk update reports no copied models. Also keep a test where another store with direct registrations still reports them.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_desk_sync.py -q
- python -m deskops desk update --root .
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

`deskops desk update --root .` in this repo prints "Desk is up to date.", the tests pass, and `pytest tests` is green.
