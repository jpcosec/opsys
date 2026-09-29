---
id: task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task
status: ready_for_testing
summary: Sync .pi skills with the removed promote drawer-task-to-active-task; document
  add task --from-drawer; add a skill/CLI drift guard test.
tags:
- workspace:desk
- artifact:task
routine: routine-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task
current_node: checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-closeout-ready
history:
- operator-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-activate
- operator-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-ready-for-testing
references:
- desk/atoms/atom-git-ignored-skill-trees-need-tracked-drift-guards.md
- tests/test_skill_cli_drift.py
- issue:issue-skill-surfaces-lack-graph-provenance-links
- 40dedb963ded4f046854fcf35f0505484264f547
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-zero-context-preflight-precedes-executor.md
- desk/contexts/pill-cli-gaps-become-tracked-work.md
- desk/contexts/pill-real-cli-surfaces-prove-operator-contracts.md
- desk/contexts/pill-drift-checks-are-review-surfaces-not-mutators.md
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- .pi/skills/use-deskops/SKILL.md
- .pi/skills/deskops-task-lifecycle/SKILL.md
- tests/test_skill_cli_drift.py
checklists:
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-execution-ready
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-testing-ready
- checklist-task-sync-pi-skills-with-the-deliberate-removal-of-promote-drawer-task-to-active-task-closeout-ready
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms:
- desk/atoms/workflow-model/atom-drawers-feed-tasks-through-promotion.md
- desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md
- desk/atoms/workflow-model/atom-cli-gaps-become-tracked-work.md
from_drawer: desk/drawer/tasks/task-sync-pi-skills-with-promote-removal.md
closeout_evidence_verified: false
pill_graduation_verified: false
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

Two skill docs (.pi/skills/use-deskops/SKILL.md and .pi/skills/deskops-task-lifecycle/SKILL.md; locate stale text by content, not line number) plus one guard test (tests/test_skill_cli_drift.py). No CLI or deskops/ code changes. Historical mentions in runs/, desk/inbox/, desk/drawer/issues/ stay untouched. Do not harmonize other .pi vs .opencode divergences. The Executor does not commit; closure runs through deskops closeout verify and deskops closeout commit.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) In .pi/skills/use-deskops/SKILL.md, replace the stale promote line with the --from-drawer promotion line copied verbatim from the CLI surface block of .opencode/skills/use-deskops/SKILL.md; the documented command must show the full flag form (--title --goal --scope --validation), never the bare --from-drawer form. 2) In .pi/skills/deskops-task-lifecycle/SKILL.md, rewrite Paso 2 step 2 in Spanish — author the active task with deskops add task --from-drawer task-ID --title --goal --scope --validation, note the drawer file is kept for manual cleanup, and state (paraphrased, WITHOUT the literal removed-command token, matching the .opencode copy) that direct drawer-to-active promotion was deliberately removed for placeholder-filling; keep elided placeholders and the rest of the protocol intact. 3) Add tests/test_skill_cli_drift.py that rglobs SKILL.md under .pi/skills, .agents/skills, and .opencode/skills (README files excluded by design), counts missing dirs as empty, asserts at least one skill file was collected, asserts none contains drawer-task-to-active-task (the token is forbidden everywhere, including removal mentions), and asserts --from-drawer appears in exactly the two use-deskops copies (.pi and .opencode; .agents has none). Guard asserts token absence plus from-drawer presence only; the full-flag-form rule is an editing rule, not a test assertion. Verify d35726a and the existing removal test before editing. Editing rules — if the copied line's bullet style differs from the surrounding list, adapt the bullet marker while keeping the command string verbatim; if the copied line ever conflicts with real CLI grammar, the real CLI grammar wins (check deskops add task --help) and the sandbox proof validates the exact documented command.

## Validation

_List the checks required before this task can close._

- pytest
- grep -rn drawer-task-to-active-task .pi/skills .agents/skills .opencode/skills (expect no hits)
- grep -c from-drawer .pi/skills/use-deskops/SKILL.md and .opencode/skills/use-deskops/SKILL.md (expect >= 1 each)
- sandbox proof of the documented operator path - seed a drawer file in .tmp/deskops-cli-test and run deskops add task --from-drawer there, confirming the active task bundle is authored with real field values (pill-real-cli-surfaces-prove-operator-contracts)

## Done When

_Name the observable condition that makes the task complete._

grep -rn drawer-task-to-active-task .pi/skills .agents/skills .opencode/skills returns nothing, the new guard test passes, and the full pytest suite is green.
