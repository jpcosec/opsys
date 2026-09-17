---
id: task-deskops-rebuilt-on-pron-total-refactor-fireproof-test
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test
current_node: checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-execution-ready
history: []
references:
- desk/drawer/tasks/task-deskops-on-pron-total-rewrite.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-execution-ready
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-testing-ready
- checklist-task-deskops-rebuilt-on-pron-total-refactor-fireproof-test-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops rebuilt on pron (total refactor, fireproof test)

## Rationale

_Explain why this task exists or the business driver behind it._

Operator directive (2026-09-17): rebuild deskops íntegramente using pron as the
only library door to sldb/kgdb. Double purpose: fireproof test for pron's
library API and total refactoring of deskops. The only carried-over code is the
document models (`deskops/models/`), with conservative improvements if
possible.

## Goal

_Describe the concrete result this task must produce._

In worktree `../deskops-pron` (branch `deskops-pron`): deskops' Python
rewritten so every sldb/kgdb contact goes through a single seam
(`deskops/world.py` → `pron.World`), CLI verb surface preserved 1:1, the 273
existing tests passing as the behavioral contract, and a gap log
(`desk/pron-gap-log.md`) capturing every pron limitation found for pron's
inbox.

## Scope

_State what is in scope and what is out of scope._

- In: seam module, models carried + improvements, operations split into
  `repo_ops/`, CLI wiring on pron, bootstrap/identity/domain_tree/
  workspace/materializers/doctor rewrites, gap log, phase commits.
- Out: `desk/` content changes beyond the gap log; graph extractor logic
  (stays); pron code changes (gaps are reported, not patched in pron).

## Implementation Path

_Outline the expected implementation route or affected surface._

Follow `docs/plan-pron-rewrite.md` §2 architecture and §3 lanes (P0–P6).
Implementation is coordinated via herdr subagents, one lane per dispatch,
sequentially, with pytest verification between lanes. Promote this task to
active before any implementation dispatch.

## Validation

_List the checks required before this task can close._

- Per lane: lane gate from plan §3 + `pytest -q`. At closeout: full pytest,
- `python -m deskops --help`, `deskops faq`, `deskops graph build`,
- `deskops graph missing`, gap-log review, atomic commit per lane.

## Done When

_Name the observable condition that makes the task complete._

- All lanes closed with green gates and atomic commits on `deskops-pron`.
- Gap log complete and exported to pron's inbox.
- Phase-closing commit made.
