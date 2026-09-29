---
id: task-sync-pi-skills-with-promote-removal
status: deferred
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
tags:
- workspace:desk
- artifact:task
- source:drawer
- topic:skills
- topic:drift
- topic:cli
---

# Sync .pi/skills with the deliberate removal of `promote drawer-task-to-active-task`

## Rationale

Commit d35726a deliberately removed `deskops promote drawer-task-to-active-task`
(it filled every required task field with placeholders) and replaced the drawer-to-active
flow with `deskops add task --from-drawer <selector>`. The removal is recorded in
`desk/drawer/issues/issue-session-20260910-handoff-uncommitted-work-and-open-items.md`
and protected by
`tests/test_inbox_promote_cli_gaps.py::test_drawer_to_active_task_promotion_no_longer_exists`.

During the 2026-09-29 session, agents loading `.pi/skills/` executed the documented but
nonexistent command. The `.opencode/skills/use-deskops/SKILL.md` parallel copy and
`~/.claude/skills/deskops-workflow/` were already fixed in the 2026-09-10 session; the
`.pi/skills/` copies were missed. Stale references confirmed by grep:

- `.pi/skills/use-deskops/SKILL.md` line 125 — CLI surface block lists
  `deskops promote drawer-task-to-active-task <task-selector>`
- `.pi/skills/deskops-task-lifecycle/SKILL.md` line 50 — "Paso 2: Promoción y Commit
  de Preparación" instructs the removed command

Superseded conclusion from the same session: the sldb inbox note
`desk/inbox/20260928-213500-unclear-spec-no-se-empaqueta-promote-falla-fuera-del-repo.md`
section 2 concluded "the installed CLI is newer than the repo". That is wrong: the
anaconda binary is an editable install resolving to this repo's source; there is one
source of truth. That note's section 1 (spec/ packaging gap) remains separate open
work and is out of scope here.

## Goal

Every tracked agent-facing skill documents drawer-to-active promotion exactly as the
CLI implements it: drawer items become active tasks only by authoring them with
`deskops add task --from-drawer`. No tracked skill instructs
`deskops promote drawer-task-to-active-task`, and a regression test keeps it that way.

## Implementation Path

1. `.pi/skills/use-deskops/SKILL.md`: replace the stale CLI line (line 125) with the
   `--from-drawer` promotion line, mirroring the already-correct `.opencode` copy:
   `deskops add task --root . --from-drawer <drawer-selector> --title <title> --goal <goal> --scope <scope> --validation <check>`
2. `.pi/skills/deskops-task-lifecycle/SKILL.md`: rewrite "Paso 2: Promoción y Commit de
   Preparación" step 2 to author the active task from the drawer item with
   `deskops add task --from-drawer task-<id> --title ... --goal ... --scope ... --validation ...`,
   noting that the drawer file is kept for manual cleanup and that
   `promote drawer-task-to-active-task` was deliberately removed. Keep the rest of the
   protocol intact.
3. Add `tests/test_skill_cli_drift.py`: walk every `SKILL.md` under `.pi/skills/` and
   `.agents/skills/` and assert the string `drawer-task-to-active-task` does not appear;
   also assert `.pi/skills/use-deskops/SKILL.md` documents `--from-drawer`.

## Resolved Decisions

- Code is authoritative: the removal is deliberate and test-protected; the skills are
  stale materializations, not a code regression.
- Do not harmonize other `.pi` vs `.opencode` copy divergences (frontmatter description,
  sub-skill routing table, role logic) — those are intentional per-runtime adaptations.
- Do not touch the sldb inbox note or the spec/ packaging gap in this task.
- Scope is two skill docs plus one guard test; no CLI or `deskops/` code changes.
- Historical mentions of the removed command in `runs/`, `desk/inbox/`, and
  `desk/drawer/issues/` stay untouched: they are evidence records, not instructions.

## Open Ambiguities

None.
