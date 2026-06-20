---
id: board-001
scope: desk
tasks:
- desk/tasks/task-add-desk-health-and-recovery-surface-deskops-slice.md
- desk/tasks/task-add-drift-check-review-loop.md
- desk/tasks/task-add-json-output-for-modeled-documents.md
- desk/tasks/task-add-per-project-desk-config-and-version-contract.md
- desk/tasks/task-define-atom-lifecycle-operations.md
- desk/tasks/task-define-materialization-contract-slice-deskops-surface.md
- desk/tasks/task-design-operational-cli-grammar.md
- desk/tasks/task-detect-and-migrate-legacy-desk-workspaces.md
- desk/tasks/task-enforce-pill-to-atom-knowledge-graduation-during-task-closeout.md
- desk/tasks/task-establish-horizontal-desk-discovery-and-canonical-identity.md
- desk/tasks/task-make-cross-desk-inbox-delivery-verifiable-and-actionable.md
- desk/tasks/task-make-list-behavior-data-integrity-safe.md
- desk/tasks/task-make-task-lifecycle-runnable-from-intake-to-closeout.md
- desk/tasks/task-wire-closeout-to-knowledge-gates.md
- desk/tasks/task-write-end-to-end-deskops-operator-manual.md
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
- desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
- desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
rituals:
- desk/rituals/phase.md
- desk/rituals/execution.md
- desk/rituals/closeout.md
- desk/rituals/testing.md
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

- Local-desk commands are now documented with the implicit current-repo default unless the example is specifically about alternate roots, cross-repo targeting, or sandbox behavior.
- Add desk health and recovery surface (deskops slice) [active] - Detect and repair common broken desk states safely (deskops-owned surfaces only).
- Add drift check review loop [active] - Add a review-only drift check that compares atoms, materializations, graph links, tests, diagrams, and implementation surfaces.
- Add JSON output for modeled documents [active] - Make modeled document `list` and `show` commands scriptable with JSON output.
- Add per-project desk config and version contract [active] - Give each project desk one explicit local configuration contract that declares desk identity, desk/version expectations, and per-project testing defaults such as sandbox behavior.
- Define atom lifecycle operations [active] - Define and implement atom creation, validation, split, merge, deletion, and traceability operations.
- Define materialization contract slice (deskops surface) [active] - Implement the deskops CLI and contract definition surface for materialization.
- Design operational CLI grammar [active] - Align deskops CLI commands with spoken workflow nouns and user intent.
- Detect and migrate legacy desk workspaces [active] - Make deskops detect legacy or hand-rolled desk layouts explicitly and provide a safe adaptation path into the current modeled workspace contract.
- Enforce pill-to-atom knowledge graduation during task closeout [active] - Make task closeout verify that durable knowledge discovered through pills is promoted into atoms before transient execution context is deleted.
- Establish horizontal desk discovery and canonical identity [active] - Make desks discoverable to each other through one canonical per-project identity path, so cross-repo workflow commands can resolve sibling desks without ambiguous local heuristics.
- Make cross-desk inbox delivery verifiable and actionable [active] - Make cross-desk inbox communication operationally useful by ensuring the sender, target, delivery result, and follow-up path are explicit across project desks.
- Make list behavior data-integrity-safe [active] - Ensure `deskops list` commands do not silently hide malformed workflow documents.
- Make task lifecycle runnable from intake to closeout [active] - Turn the documented task lifecycle into an executable deskops path.
- Wire closeout to knowledge gates [active] - Make closeout check tests, atoms, graph links, materialization status, cleanup, and commit evidence before work leaves the active desk.
- Write end-to-end deskops operator manual [active] - Consolidate the methodology into one operational playbook after runnable slices are stable.

## Task Details

_Generated from the task references above._

- Add desk health and recovery surface (deskops slice) [active] - Detect and repair common broken desk states safely (deskops-owned surfaces only).
- Add drift check review loop [active] - Add a review-only drift check that compares atoms, materializations, graph links, tests, diagrams, and implementation surfaces.
- Add JSON output for modeled documents [active] - Make modeled document `list` and `show` commands scriptable with JSON output.
- Add per-project desk config and version contract [active] - Give each project desk one explicit local configuration contract that declares desk identity, desk/version expectations, and per-project testing defaults such as sandbox behavior.
- Define atom lifecycle operations [active] - Define and implement atom creation, validation, split, merge, deletion, and traceability operations.
- Define materialization contract slice (deskops surface) [active] - Implement the deskops CLI and contract definition surface for materialization.
- Design operational CLI grammar [active] - Align deskops CLI commands with spoken workflow nouns and user intent.
- Detect and migrate legacy desk workspaces [active] - Make deskops detect legacy or hand-rolled desk layouts explicitly and provide a safe adaptation path into the current modeled workspace contract.
- Enforce pill-to-atom knowledge graduation during task closeout [active] - Make task closeout verify that durable knowledge discovered through pills is promoted into atoms before transient execution context is deleted.
- Establish horizontal desk discovery and canonical identity [active] - Make desks discoverable to each other through one canonical per-project identity path, so cross-repo workflow commands can resolve sibling desks without ambiguous local heuristics.
- Make cross-desk inbox delivery verifiable and actionable [active] - Make cross-desk inbox communication operationally useful by ensuring the sender, target, delivery result, and follow-up path are explicit across project desks.
- Make list behavior data-integrity-safe [active] - Ensure `deskops list` commands do not silently hide malformed workflow documents.
- Make task lifecycle runnable from intake to closeout [active] - Turn the documented task lifecycle into an executable deskops path.
- Wire closeout to knowledge gates [active] - Make closeout check tests, atoms, graph links, materialization status, cleanup, and commit evidence before work leaves the active desk.
- Write end-to-end deskops operator manual [active] - Consolidate the methodology into one operational playbook after runnable slices are stable.
