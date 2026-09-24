---
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-write-end-to-end-deskops-operator-manual
- desk/tasks/task-protoatoms-mandatory-domain-crossroads-and-protoatom-typing.md
- desk/tasks/task-derive-declared-graph-edges-from-model-containment-and-references.md
- desk/tasks/task-give-pilldoc-the-lifecycle-slots-its-commands-already-write.md
- desk/tasks/task-make-terminal-node-completion-commit-before-it-deletes-the-bundle.md
- desk/tasks/task-drive-sldb-in-process-during-bootstrap-instead-of-one-subprocess-per-model.md
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

- Protoatoms, mandatory domain crossroads and protoatom typing [draft] - Add ProtoAtomDoc and CrossroadDoc, enforce that every domain path prefix has a written crossroad, and add an explicit operation that types a protoatom into another sldb model while keeping a redirect stub.
- Derive declared graph edges from model containment and references [draft] - extract_declared_edges consumes each model's __containment__ and __references__ to emit edges for the declared fields, so a task's routine, checklists, pills and atoms and a board's tasks appear as edges in the snapshot.
- Give PillDoc the lifecycle slots its commands already write [draft] - PillDoc carries the lifecycle fields the pill commands read and write, so editing them persists and round-trips, and edit pill resolves pills in the drawer as well.
- Make terminal-node completion commit before it deletes the bundle [draft] - Completing a task through the terminal node commits the closing change and untracks what it deletes from the store, and refuses to delete while the change is uncommitted.
- Drive sldb in process during bootstrap instead of one subprocess per model [draft] - Bootstrap drives sldb in process when it is importable and keeps the subprocess path only as a fallback, so init and the suite drop to roughly a second.
