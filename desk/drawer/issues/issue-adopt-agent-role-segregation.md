# Adopt agent role segregation (Supervisor vs Executor)

## Kind

feature

## Status

open

## Problem

Currently, `AGENTS.md` often serves as a monolithic policy dump, leading to conflicting agent behaviors where an agent might try to plan, route, execute, and evaluate simultaneously. This lack of role segregation creates "free-running" implementers that drift across task boundaries and mix orchestration with execution.

In successful implementations (like the IEEE tutoring paper desk), splitting responsibilities into distinct operational personas provides much better control and prevents hallucination.

## Desired Outcome

Refactor the agent onboarding and execution model to explicitly separate roles:
- **Router** (`AGENTS.md`): Purely directs the incoming agent to adopt a specific operational role based on context.
- **Supervisor** (`desk/roles/deskops-supervisor.md`): Handles planning, routing tasks, launching subagents, monitoring testing, syncing the board, and enforcing closeout rituals.
- **Executor** (`desk/roles/deskops-executor.md`): Operates blindly on exactly *one* bounded task at a time, writes the code/tests, persists run traces, and stops exactly at the task boundary.

## Questions

- How do we enforce that an agent explicitly adopts a role before acting?
- Should `deskops` CLI commands be role-aware (e.g., `deskops supervisor run`)?
- How do we migrate existing monolithic `AGENTS.md` files in other repositories?

## Follow-Up Shape

- Rewrite `AGENTS.md` to be a pure router.
- Create default `desk/roles/deskops-supervisor.md` and `desk/roles/deskops-executor.md` templates in the deskops scaffold.
- Update the operator manual to reflect role-based workflow.

## Related Atoms

- atom-clean-agents-start-from-minimum-workflow-set
- atom-phase-gates-prevent-agent-skipping
