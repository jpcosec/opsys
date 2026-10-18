---
id: task-close-a-task-as-superseded
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-closeout-commit-accepts-directory-paths
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- desk/rituals/closeout.md
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# A task whose subject no longer exists closes as superseded, with a reason and a reference

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. TaskDoc's lifecycle only ends in `closed`, reached through `closeout commit` with tests, atom and commit evidence. A task whose subject was removed has no honest way to close. Example: graph_ui task-feed-hum-body-from-sldb-serve-remove-hardcoded-content targets apps/review-workbench/src/features/hum-body/, which the owner deleted in 9f64f0f. Closing it through closeout would record it as done. `advance --to closed` is refused since a0e00e3.

## Goal

_Describe the concrete result this task must produce._

`deskops closeout supersede --task <id> --reason <text> --ref <commit-or-path> --root <repo>` closes a task from any lifecycle node. It requires the reason and at least one resolvable ref: a commit that is HEAD or an ancestor, or an existing path. The task's status and history record `superseded`, and the commit trailers say so (`Closeout-Mode: superseded`, `Closeout-Reason`, `Closeout-Ref`). It removes the task from the Board in one commit, the same way the closeout commit does, and the run index line marks it as superseded.

## Scope

_State what is in scope and what is out of scope._

In scope: a `supersede` subcommand under `closeout`, implemented in deskops/services/closure.py by reusing its single commit path (no new commit logic), the closeout ritual text in desk/rituals/closeout.md, and tests. Out of scope: lifecycle graph edges (supersede is a closure mode, not a transition, so the graph stays unchanged), and Board rendering beyond removal.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Read deskops/services/closure.py and deskops/cli/commands/closeout.py (close_manual / close_with_run). 2. Add close_superseded(task, reason, refs) that skips the evidence gates, validates the refs (commit ancestry through deskops/services/closeout_gates.py reference_points_to_commit, or path existence), sets status superseded and appends `superseded` to history before the closure, then calls the shared _close with trailers Closeout-Mode superseded, Closeout-Reason and Closeout-Ref. 3. CLI `deskops closeout supersede`, with help and an example. 4. Tests from a task at ritual-execution, covering the happy path, a missing --reason, and an unresolvable ref, which must fail and leave the tree unchanged. 5. Document the mode in desk/rituals/closeout.md as the only way to close a task whose subject no longer exists.

## Validation

_List the checks required before this task can close._

- PYTHONPATH=<worktree> python -m pytest tests/test_closeout.py -q
- PYTHONPATH=<worktree> python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The new tests pass, an unresolvable ref is refused with a clean tree, and `pytest tests` is green.
