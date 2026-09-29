---
id: task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
routine: routine-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task
current_node: checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-execution-ready
history: []
references:
- desk/atoms/workflow-model/atom-drawers-feed-tasks-through-promotion.md
- desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md
- desk/atoms/workflow-model/atom-cli-gaps-become-tracked-work.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-zero-context-preflight-precedes-executor.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
files:
- .pi/skills/use-deskops/SKILL.md
- .pi/skills/deskops-task-lifecycle/SKILL.md
- tests/test_skill_cli_drift.py
checklists:
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-execution-ready
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-testing-ready
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-sync-pi-skills-with-promote-removal.md
---

# Sync .pi/skills with the deliberate removal of promote drawer-task-to-active-task

## Rationale

_Explain why this task exists or the business driver behind it._

Agents loading .pi/skills run the documented-but-removed command; skills drifted from the CLI they live beside.

## Goal

_Describe the concrete result this task must produce._

Every tracked agent-facing skill documents drawer-to-active promotion via deskops add task --from-drawer only, with a regression test asserting the removed command appears in no tracked skill.

## Scope

_State what is in scope and what is out of scope._

Two skill docs (.pi/skills/use-deskops/SKILL.md line 125, .pi/skills/deskops-task-lifecycle/SKILL.md Paso 2) plus one new guard test (tests/test_skill_cli_drift.py). No CLI or deskops/ code changes. Historical mentions in runs/, desk/inbox/, desk/drawer/issues/ stay untouched. Do not harmonize other .pi vs .opencode divergences.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Replace the stale CLI line in use-deskops with the --from-drawer line mirroring the .opencode copy. 2) Rewrite Paso 2 of deskops-task-lifecycle to author the active task via deskops add task --from-drawer task-<id>, noting the drawer file is kept for manual cleanup. 3) Add tests/test_skill_cli_drift.py: every SKILL.md under .pi/skills and .agents/skills must not contain drawer-task-to-active-task; use-deskops must document --from-drawer.

## Validation

_List the checks required before this task can close._

- pytest
- grep -rn drawer-task-to-active-task .pi .agents || true (expect no hits)
- grep -c from-drawer .pi/skills/use-deskops/SKILL.md (expect >= 1)

## Done When

_Name the observable condition that makes the task complete._

grep -rn drawer-task-to-active-task .pi .agents returns nothing in skills, the new guard test passes, and the full pytest suite is green.
