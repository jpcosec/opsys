---
id: task-rewrites-refuse-to-erase-undeclared-sections
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
- deskops/operations.py
- tests/test_cli.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Document rewrites refuse to erase sections the model does not declare

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. Since b4517c0 (TaskDoc `extra: ignore`), `deskops edit task <t> <field> <v>`, `advance` and `bind` re-render the whole document from its extracted payload, so any `## ...` heading the template does not declare (for example `## Out of scope`) is silently dropped. `sldb stores check` reports those as structural noise; deskops erased them without a warning. This repo has 10 such documents (atoms and RoleDocs).

## Goal

_Describe the concrete result this task must produce._

`_write_doc` refuses to rewrite an existing document when the rewrite would erase an undeclared heading, names the headings, and leaves the file unchanged.

## Scope

_State what is in scope and what is out of scope._

In scope: deskops/operations.py `_write_doc` using sldb's `find_structural_noise` (sldb >= 0.1.10), and a regression test. A heading that a field carries and the render keeps does not count. Out of scope: migrating undeclared sections into fields (`desk update`), and sldb's own write paths.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. In `_write_doc`, after the unreadable-field guard, compute `find_structural_noise(model, existing)` and keep the headings missing from the rendered text. 2. Raise ValueError listing them. 3. Test: a task with a hand-written `## Out of scope` section; `edit task` exits non-zero, the message names the heading, and the file is byte-identical.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The regression test fails on the unfixed code and passes here, and `pytest tests` is green.
