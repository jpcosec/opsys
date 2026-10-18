---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-canonical-atom-reference-metadata.md
- desk/tasks/task-classify-large-docs-materialization.md
- desk/tasks/task-derived-atom-trace-index.md
- desk/tasks/task-detect-and-clean-task-policy-leaks.md
- desk/tasks/task-next-why-explanation.md
- desk/tasks/task-edit-reaches-drawer-tasks-and-rituals-by-id.md
# List of pill-xxx paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
# List of ritual-xxx paths
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._



## Notes

_Add short operational notes about the current routed set._

- Make role prompts sldb-tracked RoleDocs with pi-agent materialization [active] - Roles become canonical sldb-tracked documents; installed pi agents become regenerated artifacts; drift is detectable via `deskops drift check`.

## Task Details

_Generated from the task references above._

- Canonical atom reference field and role vocabulary [draft] - Make `atoms` the only structured artifact field for atom references, validate the five allowed
roles, and report legacy aliases and invalid roles through `deskops drift check` without adding
a hard closeout gate.
- Declare composed materialization metadata for large docs [draft] - Encode the audited inventory: every composed document declares `atoms:` frontmatter with role
`documents`, and `deskops/data/faq.md` is enforced as a byte-identical projection of
`docs/faq.md`.
- Add a derived atom use-site index [draft] - Provide a read-only `atom_use_sites(root, atom_id)` helper that derives reverse traceability from
`extract_declared_edges`, plus a test proving that no atom document is mutated.
- Detect and clean global policy leaks in task files [draft] - Add a review-only `task-policy-leak` finding to `deskops drift check`, then remove the current
leak from the active task set without changing any global policy text.
- Add --why to deskops next [draft] - `deskops next --why` prints a `Why:` section that names the selection route, the matched workflow
state, the merged pill sources, and the source files, without mutating the desk.
- `deskops edit` reaches drawer tasks, and finds rituals by their id [draft] - `deskops edit task <id>` edits a task in desk/drawer/tasks/ when no active task matches, and `deskops edit ritual <id>` accepts the ritual's frontmatter id as well as its file stem.
