---
id: task-closeout-retire-legacy-resolved-tasks
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
files:
- deskops/services/closure.py
- deskops/cli/commands/closeout.py
- deskops/cli/registry.py
- tests/test_closeout.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops closeout retire` removes a task that was already resolved before the ritual lifecycle

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18 while bringing its desk to zero. graph_ui desk/tasks/001..006 are pre-lifecycle tasks: `status: resolved`, `current_node` empty, and the commit that resolved each one in references (3900ad4, ff85428, ...). `closeout commit --no-run` demands the evidence gates. Tried on a copy of graph_ui: "missing_tests_evidence" and "missing_atom_or_materialization_link". `closeout supersede` would record them as abandoned, which is false. Their files stay forever, unlike tasks closed by closeout.

## Goal

_Describe the concrete result this task must produce._

`deskops closeout retire --task <id> --reason <text> --ref <commit> [--ref ...] --root <repo>` removes a task whose status is already resolved, closed, done or complete, in one commit with trailers `Closeout-Mode: legacy-resolved`, `Closeout-Reason` and `Closeout-Ref`. The ref must be a commit that is HEAD or an ancestor. The command removes the task from the Board if it is routed there, folds the index line with mode legacy-resolved into the commit, and refuses any task whose status is not resolved.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/services/closure.py (close_retired, reusing _close the same way close_superseded does), deskops/cli/commands/closeout.py, deskops/cli/registry.py, the closeout help goldens, tests/test_closeout.py, tests/test_command_registry.py, and one sentence in desk/rituals/closeout.md written through `deskops edit ritual closeout`. Out of scope: migrating other repos' legacy tasks, which their owners run.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Mirror close_superseded. Validate refs as commits only, require a resolved-family status, do not rewrite the status, and set route and mode to legacy-resolved. 2. Register `closeout retire` with required --task, --reason and repeatable --ref. 3. Tests cover the happy path on a legacy task (no frontmatter lifecycle, `status: resolved`), a refusal for an active task, a refusal for an unresolvable ref (tree unchanged), and a clean tree afterwards. 4. Update the help goldens with --update-golden.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_closeout.py tests/test_command_registry.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The new tests pass, an active task is refused with the tree unchanged, and `pytest tests` is green.
