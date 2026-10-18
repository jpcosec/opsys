---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual.md
- desk/tasks/task-closeout-commit-leaves-the-run-index-clean.md
- desk/tasks/task-closeout-commit-accepts-directory-paths.md
- desk/tasks/task-close-a-task-as-superseded.md
- desk/tasks/task-ritual-steps-are-prose.md
- desk/tasks/task-message-delivery-resolves-unregistered-desks.md
- desk/tasks/task-init-repairs-a-broken-owner-link.md
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

- Write end-to-end deskops operator manual [active] - Consolidate the methodology into one operational playbook after runnable slices are stable.
- `closeout commit` leaves the run index clean [draft] - After `deskops closeout commit` (both --run-dir and --no-run) the working tree is clean, and runs/subagents/index.jsonl still records the closing commit's hash.
- `closeout commit` accepts a directory in --paths that contains the closing task [draft] - `closeout commit --paths desk/tasks ...` closes a task that was never committed, and a task that was, with one commit and a clean tree.
- A task whose subject no longer exists closes as superseded, with a reason and a reference [draft] - `deskops closeout supersede --task <id> --reason <text> --ref <commit-or-path> --root <repo>` closes a task from any lifecycle node. It requires the reason and at least one resolvable ref: a commit that is HEAD or an ancestor, or an existing path. The task's status and history record `superseded`, and the commit trailers say so (`Closeout-Mode: superseded`, `Closeout-Reason`, `Closeout-Ref`). It removes the task from the Board in one commit, the same way the closeout commit does, and the run index line marks it as superseded.
- Ritual steps are prose items, not StepDoc references [draft] - RitualDoc.steps is plain text, `sldb edges unresolved --local` reports no RitualDoc.steps findings, desk/rituals/phase.md is tracked as RitualDoc:ritual-phase, and every store migrates through `desk update --apply`.
- `message send` and `message ack` work when the target desk does not register the sender or itself [draft] - A note can always be delivered and acknowledged. The sender identity comes from the sender's own desk config or registry, never from the target's registry. A target desk without project_identity takes its id from the directory name, with a warning. `ack` falls back to the repo's own desk config when a local registry does not list the repo itself.
- `deskops init` repairs a broken `deskops` store link instead of skipping it [draft] - `deskops init` and `bootstrap`, on a store whose `deskops` link is broken, re-point the link at the current owner store with `replace=True` and register the models. A healthy link to a different store is still left alone, with the warning.
