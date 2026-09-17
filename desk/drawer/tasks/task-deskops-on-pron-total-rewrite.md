---
id: task-deskops-on-pron-total-rewrite
status: deferred
references:
- docs/plan-pron-rewrite.md
depends_on: []
pills:
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/operations.py
- deskops/models/
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:pron
---

# deskops rebuilt on pron (total refactor, fireproof test)

## Rationale

Operator directive (2026-09-17): rebuild deskops íntegramente using pron as the
only library door to sldb/kgdb. Double purpose: fireproof test for pron's
library API and total refactoring of deskops. The only carried-over code is the
document models (`deskops/models/`), with conservative improvements if
possible.

## Goal

In worktree `../deskops-pron` (branch `deskops-pron`): deskops' Python
rewritten so every sldb/kgdb contact goes through a single seam
(`deskops/world.py` → `pron.World`), CLI verb surface preserved 1:1, the 273
existing tests passing as the behavioral contract, and a gap log
(`desk/pron-gap-log.md`) capturing every pron limitation found for pron's
inbox.

## Scope

- In: seam module, models carried + improvements, operations split into
  `repo_ops/`, CLI wiring on pron, bootstrap/identity/domain_tree/
  workspace/materializers/doctor rewrites, gap log, phase commits.
- Out: `desk/` content changes beyond the gap log; graph extractor logic
  (stays); pron code changes (gaps are reported, not patched in pron).

## Implementation Path

Follow `docs/plan-pron-rewrite.md` §2 architecture and §3 lanes (P0–P6).
Implementation is coordinated via herdr subagents, one lane per dispatch,
sequentially, with pytest verification between lanes. Promote this task to
active before any implementation dispatch.

## Validation

Per lane: lane gate from plan §3 + `pytest -q`. At closeout: full pytest,
`python -m deskops --help`, `deskops faq`, `deskops graph build`,
`deskops graph missing`, gap-log review, atomic commit per lane.

## Done when

- All lanes closed with green gates and atomic commits on `deskops-pron`.
- Gap log complete and exported to pron's inbox.
- Phase-closing commit made.
