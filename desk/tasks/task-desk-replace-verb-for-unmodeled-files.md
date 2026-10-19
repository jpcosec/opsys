---
id: task-desk-replace-verb-for-unmodeled-files
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
- deskops/cli/commands/desk.py
- deskops/cli/registry.py
- tests/test_desk_replace.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# `deskops desk replace` edits unmodeled desk files through the CLI with an exact text replacement

## Rationale

_Explain why this task exists or the business driver behind it._

On 2026-10-18, while auditing the desk for stale material, 37 still-valid but outdated files had no edit verb. They are drawer READMEs, features, issue bodies, questions, rituals, stress-tests, use-cases, the drawer Board, desk/atoms/tag-namespaces.yaml, and the body of a RoleDoc. The owner wants every desk change made through the deskops CLI, but `deskops edit` only reaches modeled fields of supported subjects.

## Goal

_Describe the concrete result this task must produce._

`deskops desk replace <path> --old <text> --new <text> [--count N] --root <repo>` replaces an exact substring in one file under desk/. By default the substring must occur exactly once, or exactly N times with --count. Otherwise the command refuses and the file stays untouched. A store-tracked document is re-tracked after the write. The command prints the path and the number of replacements.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/cli/commands/desk.py (or a new module) for a `desk replace` subcommand, the registry entry (mutates), the help goldens, and tests. Re-tracking goes through deskops/doc_io.py. A document that `deskops edit` can reach (task, pill, ritual, board, atom, materialization, repository, inbox-note, faq-doc, step) is refused with a pointer to `deskops edit`. Out of scope: regex replacement.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Resolve the path under desk/. 2. Refuse files whose path maps to an edit subject (desk/tasks, desk/contexts, desk/rituals, desk/atoms/**/*.md, desk/materializations, desk/registry, desk/inbox, desk/faq, desk/steps), but allow desk/drawer/** (features, use-cases, stress-tests, questions, README, Board), desk/atoms/tag-namespaces.yaml and desk/roles. 3. Count occurrences, refuse on a mismatch, and write. 4. If the file is tracked (sldb.api doc_status), re-track it through doc_io so stores check stays PASS. 5. Tests cover an unmodeled drawer file, a missing old text, an ambiguous count, a tracked RoleDoc that stays PASS, and a refusal for a pill.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_desk_replace.py tests/test_command_registry.py tests/test_output_goldens.py tests/test_cli_grammar.py tests/test_cli.py -q
- python -m pytest tests -q

## Done When

_Name the observable condition that makes the task complete._

The tests pass and `pytest tests` is green.
