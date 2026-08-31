---
id: task-detect-and-migrate-legacy-desk-workspaces
status: active
references: []
depends_on: []
pills:
- desk/contexts/pill-legacy-desk-formats-need-explicit-adaptation.md
- desk/contexts/pill-doctor-separates-desk-repair-from-sldb-health.md
- desk/contexts/pill-list-surfaces-must-expose-malformed-docs.md
- desk/contexts/pill-project-local-config-carries-version-and-sandbox-policy.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files: []
routine: routine-task-detect-and-migrate-legacy-desk-workspaces
checklists:
- checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
- checklist-task-detect-and-migrate-legacy-desk-workspaces-testing-ready
- checklist-task-detect-and-migrate-legacy-desk-workspaces-closeout-ready
current_node: checklist-task-detect-and-migrate-legacy-desk-workspaces-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Detect and migrate legacy desk workspaces

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make deskops detect legacy or hand-rolled desk layouts explicitly and provide a safe adaptation path into the current modeled workspace contract.

## Scope

_State what is in scope and what is out of scope._

- detect legacy `desk/` layouts whose board, task, pill, or ritual docs do not satisfy current deskops models
- distinguish empty/fresh desks from incompatible/legacy desks
- report which current modeled surfaces are missing or malformed
- define a migration or adoption path for legacy boards, tasks, pills, and contexts
- preserve user-authored legacy content instead of overwriting it blindly
- clarify how this interacts with per-project config and desk/version contracts

## Resolved Decisions

Supervisor rulings:

- Add `classify_desk(root)` in deskops/workspace.py returning one of: `absent`, `empty`, `legacy`, `current`.
- Legacy markers (any triggers `legacy`): authored Board.md/tasks/pills present BUT missing `desk/config.json`, OR `config.json` lacks a recognized `desk_format` (use the shared desk_format constant from Wave A), OR modeled Board/Task/pill docs fail `sldb stores check` validation. `empty` = desk dir exists but no board/task/pill docs. Keep `empty` strictly distinct from `legacy`.
- Command surface: extend `deskops doctor` to emit a 'Legacy desk detected' finding listing missing/malformed surfaces (non-zero exit), AND add `deskops desk migrate --root <p>` for the adaptation path.
- Migration is STRICTLY ADDITIVE / preservation-first: scaffold ONLY missing modeled surfaces (reuse the non-destructive _write_if_missing pattern), write/patch config.json with the current desk_format, and NEVER overwrite authored Board/task/pill content. Emit a report of adopted vs preserved vs still-manual. Assert byte-identical authored files in tests.
- Migration does NOT auto-transform authored prose docs into modeled docs (leave for manual fixup; report them). Does NOT auto-`sldb docs track` (report as manual), matching current doctor behavior.
- Keep desk-repair vs SLDB-health separated (delegate store checks to sldb; do not reimplement).
- Provide at least one representative legacy fixture in tests (authored Board.md + a task, no config.json).

## Implementation Path

_Outline the expected implementation route or affected surface._

deskops/workspace.py classify_desk + additive migrate; doctor.py legacy findings; parser.py + main.py wire 'desk migrate'; tests/test_cli.py legacy/empty/current + non-destructive assertions.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
