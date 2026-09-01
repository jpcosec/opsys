# Prevent promotion from nesting structured source sections into active task fields

ID: task-prevent-promotion-from-nesting-structured-source-sections-into-active-task-fields
Status: deferred
Priority: medium

## Rationale

While dogfooding `task-make-task-lifecycle-runnable-from-intake-to-closeout`, an inbox note that already contained `## Goal` and `## Scope` headings produced a drawer task whose promoted active-task `## Scope` section embedded nested headings. That can make later active-task section extraction lose fields like `Validation` during `advance task`.

## Goal

Keep inbox-to-drawer-to-active promotion robust when the source note already uses structured headings.

## Scope

- reproduce the nested-heading promotion case from intake notes
- decide whether normalization belongs in inbox-to-drawer rendering or drawer-to-active extraction
- preserve operator-authored active-task sections after promotion
- add focused regression coverage

## Non-goals

- redesign the whole drawer-task markdown shape
- change the closeout evidence contract

## Validation

- `pytest tests/test_lifecycle_end_to_end.py -q`
- focused promotion regression test
