---
id: task-edit-keeps-text-values-literal
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

# `deskops edit` keeps text field values literal

## Rationale

_Explain why this task exists or the business driver behind it._

Reported by graph-ui-59 on 2026-10-18. `edit` parses every value as YAML. For text fields that folds multi-line input (a numbered list collapses into one line), and a value starting with `**` fails with a YAML alias error when the field is `str | None` (only plain `str` had a raw fallback). graph-ui-59 worked around it with `json.dumps(text)`.

## Goal

_Describe the concrete result this task must produce._

Text fields (`str` and `str | None`) take the edit value as written; a JSON string literal is still decoded; list and other typed fields keep YAML/JSON parsing.

## Scope

_State what is in scope and what is out of scope._

In scope: `_parse_field_value` in deskops/operations.py and a CLI test. Out of scope: a `--from-file` option.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. For `str` / `str | None` annotations return the raw value, decoding it only when it is a JSON string literal starting with `"`. 2. Other annotations go through `parse_data_value` as before. 3. Test multi-line, `**bold`, and a quoted value.

## Validation

_List the checks required before this task can close._

- pytest tests/test_cli.py
- pytest tests

## Done When

_Name the observable condition that makes the task complete._

The test fails on the unfixed code and passes here, and `pytest tests` is green.
