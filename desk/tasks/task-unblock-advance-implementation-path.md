# Unblock advance when implementation path is empty

ID: task-unblock-advance-implementation-path
Status: active
Priority: high

## Goal

Remove the task progression blocker caused by empty Implementation Path data.

## Scope

- Reproduce the `advance` failure on a task with empty Implementation Path.
- Decide whether `advance` should tolerate the empty field, prompt for it, or require an edit command first.
- Provide a CLI path to set the field if it remains required.

## Pills

- `desk/contexts/pill-002-test-real-cli-surfaces.md`
- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`

## Source Inbox Notes

- `20260529-004405-unclear-bug-progression-blocker-on-empty-implementation-path.md`

## Related Drawer Work

- `desk/drawer/tasks/task-make-task-lifecycle-runnable-end-to-end.md`
- `desk/tasks/task-add-artifact-edit-command.md`

## Done When

- `advance task` no longer dead-ends on an empty Implementation Path without a documented recovery path.
- Tests cover the chosen behavior.
