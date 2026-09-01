---
id: task-define-materialization-contract-slice-deskops-surface
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-define-materialization-contract-slice-deskops-surface
current_node: checklist-task-define-materialization-contract-slice-deskops-surface-closeout-ready
history:
- operator-task-define-materialization-contract-slice-deskops-surface-activate
- operator-task-define-materialization-contract-slice-deskops-surface-ready-for-testing
references:
- af89a89
- tests/test_materialization_contract.py
- atom:atom-materialization-contracts-bind-source-output-validation
depends_on: []
pills:
- desk/contexts/pill-materialization-contracts-declare-source-intent-and-target.md
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
files: []
checklists:
- checklist-task-define-materialization-contract-slice-deskops-surface-execution-ready
- checklist-task-define-materialization-contract-slice-deskops-surface-testing-ready
- checklist-task-define-materialization-contract-slice-deskops-surface-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-materialization-contracts-bind-source-output-validation
closeout_evidence_verified: true
pill_graduation_verified: true
---

# Define materialization contract slice (deskops surface)

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Implement the deskops CLI and contract definition surface for materialization.

## Scope

_State what is in scope and what is out of scope._

- source atom references
- target artifact identity/path
- materialization intent model
- validation checks
- generated/projection metadata

KGDB relation extraction for materialization is routed to the sibling `kgdb` repo's inbox. This task assumes the extraction API exists.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Model name: `MaterializationContractDoc` in `deskops/models/materialization.py`, mirroring `AtomDoc` (semantics + template).
- Fields: `id` (`materialization-{slug}`), `title`, `source_atoms: list[str]`, `target_kind: str`, `target_identity: str`, `intent: str`, `validation: list[str]`, `tags: list[AtomTag]`, `provenance: str | None`.
- Storage: `desk/materializations/`; scaffold in `ensure_workspace`.
- CLI: reuse the auto-generated `add`/`edit`/`list`/`show` via `ARTIFACT_SUBJECTS` (no bespoke command group).
- Validation depth for this slice: reference-resolution only (source_atoms resolve to real atoms; target_identity resolves). Drift/staleness comparison is OUT (owned by the drift-check task).
- Do NOT adopt the orphaned `spec/fields/materializes_into.yaml`; add explicit field specs.
- Atom-lifecycle materialization-link rerouting is OUT (owned by the atom-lifecycle task).

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
