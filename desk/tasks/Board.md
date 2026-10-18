---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-derived-atom-trace-index.md
- desk/tasks/task-detect-and-clean-task-policy-leaks.md
- desk/tasks/task-repo-remove-verb.md
- desk/tasks/task-message-tracks-only-in-the-target-store.md
- desk/tasks/task-closeout-subject-names-the-task-file.md
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

- Add a derived atom use-site index [draft] - Provide a read-only `atom_use_sites(root, atom_id)` helper that derives reverse traceability from
`extract_declared_edges`, plus a test proving that no atom document is mutated.
- Detect and clean global policy leaks in task files [draft] - Add a review-only `task-policy-leak` finding to `deskops drift check`, then remove the current
leak from the active task set without changing any global policy text.
- `deskops repo remove` takes a repository out of the registry so it can be registered again [draft] - `deskops repo remove <id> --root <repo>` deletes desk/registry/repo-<id>.md, untracks its RepositoryDoc, and prints the path. Afterwards `repo register` can add the entry again under the right id. A missing id exits 1 with the ids that do exist.
- A sent note is tracked only in the target repo's store, never in the sender's [draft] - `deskops message send` and the deprecated `deskops inbox` alias, in every addressing form (--root, --repo, --to), track the delivered note only in the target repo's store, with a target-relative path. The sender's store does not change.
- The default closeout commit subject names the task file, not a bare id [draft] - Without -m, every closure route (commit, supersede, retire) uses `closeout: <task file stem>`, for example `closeout: 001-define-graph-ui-data-contract`. When the stem equals the id, the subject stays as it is today. The Task-Id trailer always carries the id.
