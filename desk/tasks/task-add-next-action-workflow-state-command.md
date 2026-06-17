# Add next-action workflow state command

ID: task-add-next-action-workflow-state-command
Status: active
Priority: high

## Goal

Add a command that answers “what should I do?” from the current workflow state, so agents follow explicit next steps instead of guessing.

## Scope

- Define a persistent workflow state machine for deskops task execution.
- Store the machine in a durable spec or modeled document that can be versioned.
- Add a CLI command such as `deskops what-should-i-do` or `deskops next`.
- Return the next valid actions for the current desk state, including required rituals, pills, and validation gates.
- Render the workflow state machine as a graph projection.

## Pills

- `desk/contexts/pill-003-capture-cli-gaps.md`
- `desk/contexts/pill-004-opsys-boundary.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/contexts/pill-009-source-file-graph-traceability.md`
- `desk/contexts/pill-010-graph-runtime-output-policy.md`

## Related Drawer Work

- `desk/drawer/tasks/task-make-task-lifecycle-runnable-end-to-end.md`
- `desk/drawer/tasks/task-design-operational-cli-grammar.md`
- `desk/drawer/features/doc-materialization-pipeline.md`

## Done When

- The workflow state machine is stored in a durable source file.
- The CLI lists the next valid action from the current desk state.
- A graph view can be generated from the same source of truth.
