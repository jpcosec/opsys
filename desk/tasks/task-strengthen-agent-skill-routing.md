---
id: task-strengthen-agent-skill-routing
status: active
references:
- desk/drawer/tasks/task-strengthen-agent-skill-routing.md
depends_on: []
pills: []
files: []
routine: routine-task-strengthen-agent-skill-routing
checklists:
- checklist-task-strengthen-agent-skill-routing-execution-ready
- checklist-task-strengthen-agent-skill-routing-testing-ready
- checklist-task-strengthen-agent-skill-routing-closeout-ready
current_node: checklist-task-strengthen-agent-skill-routing-execution-ready
history: []
tags:
- workspace:desk
- artifact:task
- source:drawer
---

# Strengthen agent skill routing

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Make the repo onboarding and deskops skill enforce the local workflow and route agents toward the role-specific skills for deskops, SLDB, KGDB, spec2viz, and opencode configuration work.

## Scope

_State what is in scope and what is out of scope._

- Clarify that repo-local project work starts in `desk/drawer/tasks/`, not `desk/inbox/`.
- Require a commit after creating drawer work and another commit after promoting drawer work to the active board.
- Make `AGENTS.md` call out when to load each local role skill.
- Strengthen `.opencode/skills/use-deskops/SKILL.md` so agents do not bypass drawer, promotion, phase gates, or task closeout.

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-strengthen-agent-skill-routing.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
