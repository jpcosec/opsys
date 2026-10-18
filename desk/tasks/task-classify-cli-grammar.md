---
id: task-classify-cli-grammar
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
- tests/test_cli_grammar.py
task_type: implementation
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Classify the CLI grammar by workflow noun

## Rationale

_Explain why this task exists or the business driver behind it._

The CLI exposes model CRUD, operational workflow commands, and transitional commands in one flat
namespace. There is no test or artifact that states which nouns are intentional public workflow
surfaces, so future commands can drift into exposing models just because they exist.

## Goal

_Describe the concrete result this task must produce._

Record one explicit top-level noun classification and enforce it with a test, without removing or
renaming any command.

## Scope

_State what is in scope and what is out of scope._

In scope: one classification constant and one test. Out of scope: parser changes, command removal,
deprecations, and per-subcommand classification.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Create `tests/test_cli_grammar.py` with `TOP_LEVEL_GRAMMAR`:
   - `operational`: `next`, `advance`, `closeout`, `promote`, `bind`, `message`, `inbox`, `graph`,
     `drift`, `runtime`, `drawer`, `issue`
   - `model_crud`: `add`, `edit`, `list`, `show`
   - `admin`: `about`, `doctor`, `status`, `faq`, `bootstrap`, `init`, `repo`, `desk`
   - `mixed`: `atoms`
   - `transitional`: `materialize`
2. Test that every top-level path in `command_registry()` appears in exactly one category and that
   the category keys have no extra nouns.
3. Test that `mutates` commands are not classified as `model_crud` only by accident: assert
   `("next",)` and `("show",)` are non-mutating, and `("advance",)` and `("closeout",)` are
   mutating, as a guard on the operational category.
4. Do not edit `deskops/cli/registry.py`. If the test exposes a missing noun, add it to the mapping
   rather than changing the CLI.

## Validation

_List the checks required before this task can close._

- python -m pytest tests/test_cli_grammar.py -q
- python -m pytest tests/test_command_registry.py -q
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

The top-level CLI nouns are classified once, the test fails on an unclassified new noun, and no
command behavior changes.
