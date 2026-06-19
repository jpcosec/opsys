# Enforce pill-to-atom knowledge graduation during task closeout

ID: task-enforce-pill-to-atom-knowledge-graduation
Status: deferred
Priority: high

## Goal

Make task closeout verify that durable knowledge discovered through pills is promoted into atoms before transient execution context is deleted.

## Scope

- define how closeout distinguishes transitional pill context from durable residue
- require pill audit during closeout for bugfix, feature, and migration tasks
- record or verify atom updates when a task refined project rulings or reusable patterns
- avoid forcing atom updates when a pill only routed already-existing knowledge
- integrate the rule with task deletion, pill cleanup, and closeout evidence

## Done When

- The workflow has an explicit closeout rule for graduating durable pill knowledge into atoms.
- Tasks that create or refine durable rulings cannot close without either updating atoms or recording why no atom change was needed.
- Pill cleanup no longer risks deleting stabilized knowledge before it reaches the atom base.

## Suggested Pills

- `desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md`
- `desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
