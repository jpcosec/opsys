---
id: task-rw-f3-atoms-service
status: deferred
references: []
depends_on:
- task-rw-f3-tasks-service
pills:
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
- desk/contexts/pill-012-create-operations-transactional-rollback.md
files:
- deskops/services/atoms.py
- deskops/operations.py
- tests/test_atoms_merge.py
- tests/test_atoms_split.py
task_type: implementation
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f3
- topic:refactor
- topic:atoms
---

# Atom operations move to a service; merge and split roll back fully

## Rationale

_Explain why this task exists or the business driver behind it._

Atoms are the largest domain left in deskops/operations.py after the earlier F3 tasks; merge and split write several files and their rollbacks are partial (inventory D7).

Plan: phase F3 of `runs/planning/deskops-rewrite-inventory.md`.

## Goal

_Describe the concrete result this task must produce._

`deskops/services/atoms.py` (`AtomsService(root)`) owns atom create, edit, split, merge, retarget and delete; every write goes through doc_io; merge and split run inside one `DocTransaction` each; operations.py keeps only wrappers.

## Scope

_State what is in scope and what is out of scope._

In scope: the move and the two transactions. 'Unchanged behavior' means tests/test_atoms_cli.py, tests/test_atoms_split.py, tests/test_atoms_create_from_source.py and tests/test_atoms_merge.py pass unmodified. Out of scope: new atom features.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Move the atom methods and `_find_inbound_atom_references`/`_rewrite_inbound_atom_references`.
2. Wrap `merge_atom` and `split_atom` each in one `DocTransaction`.
3. Failure-injection tests: make the doc_io track step raise after the referrer rewrite (merge) and after the first new atom is written (split); assert every touched file's bytes equal the originals and `sldb stores check` is unchanged.

## Validation

_List the checks required before this task can close._

- pytest tests/test_atoms_cli.py tests/test_atoms_merge.py tests/test_atoms_split.py tests/test_atoms_create_from_source.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`grep -n 'def merge_atom' deskops/services/atoms.py` matches, operations.py only delegates, both injection tests pass, and `pytest tests` is green.

## Resolved Decisions

- The supervisor promotes this drawer task to desk/tasks/ and commits that promotion before dispatch. The executor does not commit; the supervisor reviews the diff and makes the closeout commit with `deskops closeout commit --task <id> --run-dir <dir>` or `--no-run --reason <why>`. Closing always requires `pytest tests` green in addition to the task's own Done When.

## Open Ambiguities

None.
