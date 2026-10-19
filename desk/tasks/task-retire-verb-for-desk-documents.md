---
id: task-retire-verb-for-desk-documents
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/retire.py
- deskops/cli/commands/retire.py
- deskops/cli/registry.py
- tests/test_retire_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops retire` removes an obsolete desk document with its reason and refs

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18 the owner asked to clear old and legacy material out of the desk through the deskops CLI, leaving the trace in git. Several kinds of document already have a verb: tasks use closeout, issues use issue close, atoms use atoms delete, drawer entries use drawer remove, and registry entries use repo remove. Pills in desk/contexts, inbox notes, steps, roles, runtimes, faq, logbook, materializations and legacy non-document files under desk/ have none, so the only way to retire one is deleting it by hand.

## Goal

_Describe the concrete result this task must produce._

`deskops retire <path> --reason <text> --ref <commit-or-path> [--ref ...] [--force] --root <repo>` deletes one file under desk/ and untracks it from the store if tracked, in one DocTransaction, then prints the path, reason and refs. It refuses when other desk/docs files still reference it, listing them, unless --force is given. It refuses kinds that have their own verb, naming that verb: tasks in desk/tasks, drawer entries, atoms, and registry entries.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/services/retire.py, deskops/cli/commands/retire.py, a registry entry (mutates=True), help goldens, and tests/test_retire_cli.py. Out of scope: committing. The supervisor commits each batch with the reasons in the message.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Resolve the path relative to the root and require it to be under desk/. 2. Refuse desk/tasks/task-*.md, desk/drawer/**, desk/atoms/**/*.md and desk/registry/*.md, naming the dedicated verb. 3. Look for inbound references to its relative path or stem in desk/**/*.md, docs/**/*.md, README.md and AGENTS.md, excluding the file itself, and refuse if any are found unless --force. 4. Require a non-empty reason and at least one ref that resolves as an ancestor commit or an existing path. 5. Delete through DocTransaction.delete, which also untracks. 6. Tests cover a tracked pill retired cleanly, a refusal on inbound references and --force, a refusal for a task naming closeout, an unresolvable ref, and a non-markdown leftover file.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_retire_cli.py tests/test_command_registry.py tests/test_output_goldens.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The tests pass and `pytest tests` is green.
