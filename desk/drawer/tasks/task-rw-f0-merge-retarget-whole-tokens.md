---
id: task-rw-f0-merge-retarget-whole-tokens
status: deferred
references: []
depends_on:
- task-rw-f0-reject-ambiguous-selectors
pills:
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files:
- deskops/operations.py
- tests/test_atoms_merge.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:atoms
- topic:data-loss
---

# Atom merge rewrites only whole `atom:<id>` tokens in referrers

## Rationale

_Explain why this task exists or the business driver behind it._

Inventory finding D4. `DeskopsOperations._rewrite_inbound_atom_references` (deskops/operations.py:2130), called only by `merge_atom` (line 980), checks that a line holds the exact token `atom:<id>`, then runs `original_text.replace(needle, replacement)` on the whole file (line 2162). Merging `atom-foo` into another atom therefore also rewrites every `atom:atom-foo-bar` in the same file. `split_atom` only reads inbound references (its `_find_inbound_atom_references` call is at line 879) and is not affected. The finder (`_find_inbound_atom_references`, line 2109) has no token boundary, so it may list a line such as `xatom:atom-foo` that the bounded rewrite then leaves alone; that is acceptable (the report lists a candidate, the rewrite stays exact).

Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`merge_atom` rewrites only exact `atom:<source id>` tokens in referrer files.

## Scope

_State what is in scope and what is out of scope._

In scope: the replace step of `_rewrite_inbound_atom_references` and one test. Out of scope: rollback of rewritten referrers on failure (task-rw-f3-atoms-service) and `split_atom`.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Replace the global `str.replace` with `re.sub(rf"(?<![A-Za-z0-9_.-]){re.escape(needle)}(?![A-Za-z0-9_.-])", replacement, original_text)`, the same token grammar as the matcher's `atom:[a-zA-Z0-9_.-]+`.
2. The `rewritten` report (path:line) lists only lines whose text the substitution actually changed.
3. Test in tests/test_atoms_merge.py: a referrer containing `atom:atom-foo` and `atom:atom-foo-bar`; merge `atom-foo` into a target; assert `atom:atom-foo-bar` is untouched and `atom:atom-foo` now names the target.

## Validation

_List the checks required before this task can close._

- pytest tests/test_atoms_merge.py tests/test_atoms_split.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The new test fails before the fix and passes after; `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
