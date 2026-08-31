---
id: task-define-atom-lifecycle-operations
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-atom-lifecycle-preserves-provenance-and-materialization-links.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
files: []
routine: routine-task-define-atom-lifecycle-operations
checklists:
- checklist-task-define-atom-lifecycle-operations-execution-ready
- checklist-task-define-atom-lifecycle-operations-testing-ready
- checklist-task-define-atom-lifecycle-operations-closeout-ready
current_node: checklist-task-define-atom-lifecycle-operations-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Define atom lifecycle operations

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Define and implement atom creation, validation, split, merge, deletion, and traceability operations.

## Scope

_State what is in scope and what is out of scope._

- atom creation from scratch
- atom creation from pills, graph findings, and diagrams
- one-question validation
- tag namespace validation
- split/merge/delete rules
- relation to materialization contracts and provenance

## Resolved Decisions

Supervisor rulings to keep this a single coherent deliverable (the full six-capability set is decomposed; only the safe, high-value slice ships here):

- IN SCOPE this task: `deskops atoms validate [<id>|--all]` and `deskops atoms delete <id> [--force]`.
- `validate`: checks single 5WH1+ (already modeled), tag-namespace validity via `validate_atom_tag_namespaces`, provenance resolvability, id slug convention `atom-<slug>`. Exit non-zero on invalid.
- `delete`: scan inbound `atom:<id>` references across `desk/`; refuse unless `--force`; on delete remove file and untrack from `.sldb` store.
- Reference-rerouting default: BLOCK on inbound references (no silent auto-rewrite).
- OUT (deferred to new drawer tasks): split, merge, create-from-pill/graph/diagram. Capture as drawer backlog at closeout.
- CLI namespace stays plural: `deskops atoms ...`.
- Verify SLDB exposes an untrack API before relying on it; if absent, route a sldb inbox note and keep file removal + graph-check as the delete evidence.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add validate/delete subcommands in parser + atoms.py, logic in operations.py (reuse _reference_points_to_atom). Tests in tests/ using sandbox desk.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
