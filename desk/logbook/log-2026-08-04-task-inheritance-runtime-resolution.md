# Task inheritance runtime resolution

Date: 2026-08-04
Scope: deskops central workflow harness
Triggered By: paper_v2 local workflow hardening

## Summary

Implemented operational task inheritance in deskops so `inherits_from` is resolved by the runtime instead of remaining documentation-only metadata.

## Why

A downstream repo (`paper_v2`) started using typed tasks plus `inherits_from` to carry workflow context, but deskops still treated that field as inert text. That left a gap between documented workflow policy and actual CLI/runtime behavior.

## Central Changes

- extended `TaskDoc` with:
  - `task_type`
  - `inherits_from`
  - `inherit_acceptance_context`
  - `atoms`
- extended runtime `Task` with effective inherited fields:
  - `effective_references`
  - `effective_pills`
  - `effective_tags`
  - `effective_atoms`
  - `effective_validation`
  - `effective_done_when`
- added recursive inheritance resolution with cycle detection in `deskops/operations.py`
- updated `show task` and `next` surfaces to expose inherited workflow context
- updated task input/compilation paths so CLI creation and spec compilation preserve the new fields
- added tests for template roundtrip and inherited task resolution

## Files Changed

- deskops/models/task.py
- deskops/runtime/primitives.py
- deskops/operations.py
- deskops/cli/parser.py
- deskops/cli/commands/operations.py
- deskops/specs/compiler.py
- tests/test_model_templates.py
- tests/test_cli.py

## Workflow Reflection

The important distinction is:

- downstream repos own their local workflow policy
- deskops owns whether that policy is operational in the harness

This entry belongs in deskops central because the change was a harness capability change, not a project-local workflow note.
