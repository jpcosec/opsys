---
id: task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- source:drawer
routine: routine-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization
current_node: checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-execution-ready
history: []
references:
- desk/drawer/tasks/task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization.md
depends_on: []
pills: []
files: []
checklists:
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-execution-ready
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-testing-ready
- checklist-task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization-closeout-ready
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Make role prompts sldb-tracked RoleDocs with pi-agent materialization

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Scope

_State what is in scope and what is out of scope._

- add `RoleDoc` model in `deskops/models/role.py` and register it in the store index
- move canonical role sources to `desk/roles/` as tracked RoleDocs
- implement the deferred `deskops materialize` surface for pi agent targets (renders RoleDoc + pi frontmatter into `~/.pi/agent/agents/deskops-*.md`)
- extend `deskops drift check` to compare renders vs installed agent files
- regenerate the three deskops role agents from the tracked sources
- relate each role doc to its agent file with the `materializes` edge role

## Implementation Path

_Outline the expected implementation route or affected surface._

Promoted from desk/drawer/tasks/task-make-role-prompts-sldb-tracked-roledocs-with-pi-agent-materialization.md.

## Validation

_List the checks required before this task can close._

- pytest

## Done When

_Name the observable condition that makes the task complete._

Promoted work is completed, validated, and closed with a commit.
