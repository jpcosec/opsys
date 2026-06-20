# Bind next-phase pills to active tasks

ID: task-bind-next-phase-pills-to-active-tasks
Status: deferred
Priority: high

## Goal

Bind the reconciled reusable pill set onto the currently active tasks, add any missing reusable pills exposed by that pass, and make the many-to-many pill model explicit in operator-facing guidance.

## Scope

- add any missing reusable pills needed after conciliation
- bind phase-baseline and domain-specific pills to active tasks by applicability
- make the "pills are not 1:1 with tasks" correction explicit in guidance
- keep board routing minimal while task-local bindings carry domain-specific context

## Suggested Pills

- `desk/contexts/pill-001-task-closure-commit.md`
- `desk/contexts/pill-005-subagent-execution.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md`
- `desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md`

## Done When

- active tasks bind the reusable pills they actually need
- any missing reusable pill from the conciliation pass exists
- the many-to-many pill model is stated explicitly in guidance
- validations pass and the task closes with its own commit
