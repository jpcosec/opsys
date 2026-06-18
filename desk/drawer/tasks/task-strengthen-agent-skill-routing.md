# Strengthen agent skill routing

ID: task-strengthen-agent-skill-routing
Status: deferred
Priority: high

## Goal

Make the repo onboarding and deskops skill enforce the local workflow and route agents toward the role-specific skills for deskops, SLDB, KGDB, spec2viz, and opencode configuration work.

## Scope

- Clarify that repo-local project work starts in `desk/drawer/tasks/`, not `desk/inbox/`.
- Require a commit after creating drawer work and another commit after promoting drawer work to the active board.
- Make `AGENTS.md` call out when to load each local role skill.
- Strengthen `.opencode/skills/use-deskops/SKILL.md` so agents do not bypass drawer, promotion, phase gates, or task closeout.

## Done When

- `AGENTS.md` names the role skills and when they apply.
- `.opencode/skills/use-deskops/SKILL.md` documents the drawer-first workflow and commit boundaries.
- The task is promoted, implemented, validated, and closed through the desk workflow.
