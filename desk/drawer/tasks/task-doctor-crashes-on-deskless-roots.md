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
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:health
- topic:cli
---

# Doctor crashes with UnboundLocalError on desk-less roots

## Rationale

Discovered during cold review of `task-doctor-proposes-missing-model-registration`.
Reproduced on an empty root: `python -m deskops doctor --root /tmp/empty` exits with
`Unexpected: cannot access local variable 'unreadable_docs' where it is not associated
with a value`. In `deskops/cli/commands/doctor.py`, `unreadable_docs` is defined only
inside `if desk_dir.exists():` but is read in the findings section outside that block.
The same block also carries a dead `tracked_mds` assignment that is immediately shadowed.

## Goal

`deskops doctor` on a root without `desk/` reports the missing-desk-structure finding
and exits cleanly instead of crashing. Initialize `unreadable_docs` (and remove the dead
`tracked_mds` re-assignment) so all finding variables exist on every code path.

## Resolved Decisions

- Fix lives in `deskops/cli/commands/doctor.py` only.
- Behavior on desk-less roots: missing-desk-structure finding (with scaffold repair under
  `--repair`), no crash.

## Open Ambiguities

None.
