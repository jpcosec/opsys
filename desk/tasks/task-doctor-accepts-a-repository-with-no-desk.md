---
id: task-doctor-accepts-a-repository-with-no-desk
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
- deskops/cli/commands/doctor.py
- tests/test_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops doctor` on a repository with no desk reports that there is no desk and exits 0

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. On the coordinator's order, pron stopped being a desk repository: it has no desk/ and no desk/config.json (7f6b3c7), and no registry lists it. `deskops doctor --root pron` still reports "Missing desk structure: desk/", suggests --repair, and exits 1. Any ecosystem-wide doctor run (suite-check) therefore shows pron red, even though having no desk is a valid choice there.

## Goal

_Describe the concrete result this task must produce._

When a root has neither desk/ nor desk/config.json, `deskops doctor` prints that it found no desk at the root (with the hint that `deskops init` creates one), suggests no repair, and exits 0. A partially present desk (config without desk/, desk/ missing required files) stays a finding with exit 1, as today. `doctor --repair` on a root with no desk does not scaffold one: scaffolding stays the job of `deskops init`.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/doctor.py (the 'absent' classification branch), tests covering the absent and partial cases, and the doctor help text if it describes the absent case. Out of scope: desk update.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In doctor, when inspect_desk classifies the root as absent and there is no desk/config.json, print `No desk at <root>: this repository has no desk/ (run deskops init to create one).` and return 0 with no repair suggestion. 2. Make --repair a no-op there that prints the same message. 3. Keep the current findings for partial desks. 4. Update the tests that expect a finding on an absent desk, after checking what they are proving (the F0 deskless-root fix, 8121c5e, must still not crash).

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli.py tests/test_doctor_model_registration.py -q -k doctor
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

doctor on an empty directory or a repo without desk/ exits 0 with the message, partial desks still fail, and `pytest tests` is green.
