# Enforce task-local vs global policy separation

## Kind

feature

## Status

open

## Problem

Global workflow rules (how to test, how to close a task, general constraints) often leak into individual task files (`desk/tasks/task-*.md`). This pollutes task scope, creates redundancy, and makes global policy updates difficult because rules are scattered across transient task definitions.

## Desired Outcome

Enforce a strict content boundary:
- **Task files (`task-*.md`)**: Must contain *only* task-local information (the specific goal, scope, localized validation target, and local evidence/repo-sync notes).
- **Workflow files**: Global rules must live exclusively in `desk/rituals/` or `desk/agents/` and must be referenced, not duplicated.

## Questions

- Can we build a linter or drift check to detect when a task file starts accumulating global policy jargon?
- How do we make referencing global policies ergonomic so task creators don't feel the need to copy-paste?
- What is the exact taxonomy of a perfectly scoped task file?

## Follow-Up Shape

- Update the task template and scaffolding routines to strip out any global policy placeholders.
- Add guidance in the operator manual about keeping task files local.
- Create a drift check routine to scan tasks for policy leakage.

## Related Atoms

- atom-tasks-enable-zero-context-subagents
- atom-workflow-vocabulary-separates-knowledge-and-work
