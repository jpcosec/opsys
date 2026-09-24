---
id: task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store
current_node: checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-testing-ready
history:
- operator-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-activate
references: []
depends_on: []
pills: []
files: []
checklists:
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-execution-ready
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-testing-ready
- checklist-task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store-closeout-ready
task_type: feature
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence_verified: false
pill_graduation_verified: true
---

# Add deskops desk update to reconcile a desk and its store

## Rationale

_Explain why this task exists or the business driver behind it._

desk/drawer/issues/issue-add-desk-update-sync-command.md: desk install scaffolds a desk but nothing reconciles an existing one with the current models, structure or conventions. This session hit the consequence repeatedly: a store whose payload hashes describe older document text, untracked documents, and models that were never registered, with no command to repair any of it.

## Goal

_Describe the concrete result this task must produce._

One command reports and repairs the divergence between a desk, its tracked documents and the current models: missing structure, untracked documents, stale hashes, unregistered models, with a dry-run default and an explicit apply.

## Scope

_State what is in scope and what is out of scope._

A new CLI command plus the operations behind it, and tests. Does not migrate desk content between formats and does not touch the graph.

## Implementation Path

_Outline the expected implementation route or affected surface._

Define the command in deskops/cli/parser.py and deskops/cli/commands/, drive it through sldb's track/untrack and stores update APIs (the same ones the write path already uses), and report through the doctor's vocabulary so the two surfaces agree. Tests must cover a store with a stale hash, an untracked document and an unregistered model.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py tests/test_desk_sync.py -q

## Done When

_Name the observable condition that makes the task complete._

On a desk with each of those three defects, the command reports them and, with apply, leaves sldb stores check passing; a dry run changes nothing.
