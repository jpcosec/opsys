# Add rationale capture with --why

ID: task-add-why-rationale-fields
Status: active
Priority: medium

## Goal

Let users capture creation rationale directly from the CLI.

## Scope

- Add a `--why` or equivalent rationale field to task and pill creation.
- Decide whether the field maps to existing document sections or requires model/template updates.
- Update help text and tests for task and pill creation.

## Pills

- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`

## Source Inbox Notes

- `20260529-004404-suggestion-feature-why-flag.md`

## Done When

- `deskops add task --why ...` and the pill equivalent preserve rationale in the generated document.
- Missing or empty rationale behavior is explicit.
