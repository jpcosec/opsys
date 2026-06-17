# Add artifact edit command

ID: task-add-artifact-edit-command
Status: active
Priority: medium

## Goal

Allow users to update modeled artifact fields from the CLI instead of manual file edits.

## Scope

- Design an `edit` command grammar for task, pill, and other modeled artifacts.
- Prefer SLDB field update operations where available.
- Cover fields needed for task progress, including goal, scope, and implementation path.

## Pills

- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-004-opsys-boundary.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`

## Source Inbox Notes

- `20260529-004404-suggestion-feature-edit-command.md`

## Done When

- A user can edit core task fields through a command that preserves modeled document structure.
- The command does not reimplement SLDB field behavior inside deskops when an SLDB path exists.
