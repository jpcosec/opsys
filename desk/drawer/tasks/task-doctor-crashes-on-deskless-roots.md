---
id: task-doctor-crashes-on-deskless-roots
status: deferred
references: []
depends_on: []
pills:
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
files:
- deskops/cli/commands/doctor.py
- tests/test_doctor_unmodeled_surfaces.py
tags:
- workspace:desk
- artifact:task
- source:drawer
- plan:deskops-rewrite
- phase:f0
- topic:health
- topic:cli
---

# Doctor crashes with UnboundLocalError on desk-less roots

## Rationale

_Explain why this task exists or the business driver behind it._

Discovered during cold review of `task-doctor-proposes-missing-model-registration`.
Reproduced on an empty root: `python -m deskops doctor --root /tmp/empty` exits with
`Unexpected: cannot access local variable 'unreadable_docs' where it is not associated
with a value`. In `deskops/cli/commands/doctor.py`, `unreadable_docs` is defined only
inside `if desk_dir.exists():` but is read in the findings section outside that block.
The same block also carries a dead `tracked_mds` assignment that is immediately shadowed.

## Goal

_Describe the concrete result this task must produce._

`deskops doctor` on a root without `desk/` reports the missing-desk-structure finding
and exits cleanly instead of crashing. Initialize `unreadable_docs` (and remove the dead
`tracked_mds` re-assignment) so all finding variables exist on every code path.

## Scope

_State what is in scope and what is out of scope._

In scope: `deskops/cli/commands/doctor.py` (initialize `unreadable_docs` before the
`if desk_dir.exists():` block, drop the dead `tracked_mds` assignment at line 78 that line
80 shadows) and one regression test. Out of scope: other doctor findings and the
`Unexpected:` handler in `deskops/cli/main.py` (task-rw-f2-typed-errors-and-exit-codes).
Plan: phase F0 of `runs/planning/deskops-rewrite-inventory.md` (finding X1).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Move `unreadable_docs: list[str] = []` above the `if desk_dir.exists():` block.
2. Delete the shadowed `tracked_mds = set(inspection.tracked_surface_docs)` line.
3. Add a test in `tests/test_doctor_unmodeled_surfaces.py` that runs
   `python -m deskops doctor --root <empty tmp dir>` and asserts exit code 1 (without
   `--repair` doctor reports findings and returns 1, `deskops/cli/commands/doctor.py:213-215`;
   the crash also exits 1, so the exit code alone does not prove the fix), the
   missing-desk-structure finding in stdout, and no `Unexpected:` text in stderr.

## Validation

_List the checks required before this task can close._

- pytest tests/test_doctor_unmodeled_surfaces.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

`deskops doctor --root <empty dir>` prints the missing-desk-structure finding without
`Unexpected:` and the new test passes.

## Resolved Decisions

- Fix lives in `deskops/cli/commands/doctor.py` only.
- Behavior on desk-less roots: missing-desk-structure finding (with scaffold repair under
  `--repair`), no crash.

## Open Ambiguities

None.
