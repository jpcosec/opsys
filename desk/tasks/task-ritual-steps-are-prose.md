---
id: task-ritual-steps-are-prose
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
- deskops/models/ritual.py
- tests/fixtures/model_contract_hashes.json
- desk/rituals/phase.md
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Ritual steps are prose items, not StepDoc references

## Rationale

_Explain why this task exists or the business driver behind it._

Found on 2026-10-18 by `sldb edges unresolved --store .sldb --local`: 36 of the repo's 39 unresolved references are RitualDoc.steps items such as "1. Run the smallest relevant test scope first.". RitualDoc declares `__containment__ = {"steps": ["StepDoc"]}`, so sldb reads every step sentence as a StepDoc name that does not exist. desk/rituals/phase.md cannot be tracked at all: one step contains ": ", so YAML reads that list item as a mapping ("steps.7 Input should be a valid string"). The Board routes phase.md, so `edges unresolved` also reports it as an unknown path.

## Goal

_Describe the concrete result this task must produce._

RitualDoc.steps is plain text, `sldb edges unresolved --local` reports no RitualDoc.steps findings, desk/rituals/phase.md is tracked as RitualDoc:ritual-phase, and every store migrates through `desk update --apply`.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/models/ritual.py (remove steps from __containment__; keep or drop the `step_details` composition according to what it renders, and check for StepDoc references across deskops/ and tests/), the RitualDoc contract hash in tests/fixtures/model_contract_hashes.json, desk/rituals/phase.md (the step with ": " must stay a string after re-rendering through RitualDoc, through the CLI or sldb), and the migration of this repo's store. Out of scope: the StepDoc model itself.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. grep -rn "StepDoc\|step_details\|__containment__" deskops tests. 2. Make steps prose: no containment, plus the composition change if needed. 3. Update the contract hash. 4. Re-render or track desk/rituals/phase.md as RitualDoc:ritual-phase, so the step with a colon is quoted. 5. Run `sldb stores update`, then check `edges unresolved --local` has no RitualDoc entries. 6. Tests: a RitualDoc whose step contains ": " round-trips, and the declared graph edges no longer emit ritual -> step containment (tests/test_graph_declared_edges.py).

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_model_templates.py tests/test_graph_declared_edges.py tests/test_model_contract_snapshot.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

`edges unresolved --local` in this repo reports no RitualDoc.steps findings, phase.md is tracked, and `pytest tests` is green.
