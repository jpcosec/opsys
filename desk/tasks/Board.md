---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-add-deskops-desk-update-to-reconcile-a-desk-and-its-store.md
- desk/tasks/task-document-the-atom-model-and-the-tag-namespace-workflow.md
- desk/tasks/task-report-knowledge-drift-stale-atoms-missing-materializations-and-unrouted-findings.md
- desk/tasks/task-make-cross-repo-inbox-delivery-work-from-a-canonical-identity.md
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

- Add deskops desk update to reconcile a desk and its store [ready_for_testing] - One command reports and repairs the divergence between a desk, its tracked documents and the current models: missing structure, untracked documents, stale hashes, unregistered models, with a dry-run default and an explicit apply.
- Document the atom model and the tag namespace workflow [ready_for_testing] - A durable doc, materializing the atoms that already carry these rules, that explains creating an atom, choosing the 5WH1+ question, how namespaces select the atom's folder, and how to add a namespace when existing ones do not cover the knowledge.
- Report knowledge drift: stale atoms, missing materializations and unrouted findings [ready_for_testing] - A drift command that reports, from the desk and the graph: atoms whose declared targets or materializations no longer resolve, documents that point at atoms with no inbound trace, and graph findings that no atom or issue covers.
- Make cross-repo inbox delivery work from a canonical identity [ready_for_testing] - One identity path usable for both questions, and cross-repo delivery that either reaches the target or fails with the reason, with the sender able to see that the target acknowledged or closed the note.
