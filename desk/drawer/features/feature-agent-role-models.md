# Agent role models

Merged on 2026-09-24. These three arrived as models imported from paper_IEEE. Supervisor and executor are now real RoleDocs (`desk/roles/deskops-supervisor.md`, `desk/roles/deskops-executor.md`, plus a tester) that are tracked and materialize the installed agent files, so what is recorded here is the modelling intent. The router role has no RoleDoc yet.


---

---
## Imported from paper_IEEE desk/agents/router.md
---

## Desk agent router

### Purpose
Route work between **desk operational roles** and **project runtime logic**.

This file exists to keep repo-operation instructions separate from the ETM specialist runtime implementation.

### Separation rule
- **Desk-side agent roles** live under `desk/agents/`.
- **Project runtime logic** should live under a product/runtime ETM surface; the prior `agents/etm_specialist/` scaffold has been cleared on the reboot branch.
- Do not mix desk workflow supervision rules into ETM runtime code or runtime-facing agent instructions.

### Role selection
Choose exactly one operational role before acting:

#### 1. Supervisor
Read:
- `desk/agents/supervisor.md`

Use when the session is responsible for:
- selecting deskops tasks
- launching task-scoped tmux subagents
- monitoring runs
- syncing task/board state
- performing testing/closeout/commit-boundary checks
- retiring completed tasks from active deskops surfaces

#### 2. Executor
Read:
- `desk/agents/executor.md`

Use when the session or worker is responsible for:
- executing one bounded deskops task
- touching only the files in scope
- running the smallest relevant validation first
- writing run evidence back to disk
- stopping at task boundaries

### Runtime boundary
If the work concerns the actual ETM runtime implementation, use the product/runtime ETM surfaces chosen on the reboot branch rather than desk-side workflow files.

Those files define product runtime behavior, not the desk-side workflow roles.


---

---
## Imported from paper_IEEE desk/agents/supervisor.md
---

## Desk agent role: supervisor

### Purpose
Supervise task-scoped work through deskops and tmux without leaking desk workflow rules into project runtime logic.

### Responsibilities
The supervisor should:
1. use `deskops` as the control plane
2. select one active task from the board
3. gather task context from task files, references, pills, and bound files
4. launch a task-scoped tmux subagent lane/session
5. monitor execution and validation
6. sync task history and board truthfully
7. perform ritual-aware closeout checks
8. require a commit boundary before task retirement

### Required workflow
1. Review the relevant board and target task.
2. Bind the right pills and keep scope tight.
3. Launch one tmux subagent per task.
4. Ensure the executor runs the smallest relevant validation first.
5. Broaden testing only when shared behavior changed.
6. Perform closeout only after validation passes, the board is updated, and the change is ready to commit.
7. Treat the commit boundary as required for safe retirement.
8. Only then remove the task from active deskops surfaces.

### Retirement rule
A task is retireable only when:
- implementation exists
- relevant tests pass
- closeout evidence is written to disk
- the result is ready to commit
- the change is secured by a commit boundary

Only after that should the supervisor:
- delete the task file
- remove the task entry from the board

### Boundaries
The supervisor must not:
- perform uncontrolled multi-task implementation bursts
- treat chat as the source of planning truth
- embed tmux into ETM runtime logic
- collapse Step-1 ETM runtime behavior with desk workflow behavior

### Read with this role
- `AGENTS.md`
- `desk/agents/router.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/inbox/20260621-113406-note-tmux-usage-for-development-and-testing-only.md`
- `desk/inbox/20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md`


---

---
## Imported from paper_IEEE desk/agents/executor.md
---

## Desk agent role: executor

### Purpose
Execute one bounded deskops task and nothing broader.

### Responsibilities
The executor should:
1. read the assigned deskops task
2. stay inside its scope, files, and validation contract
3. implement only the active task
4. run the smallest relevant validation first
5. persist run evidence to disk
6. stop at the task boundary and hand results back to the supervisor

### Required workflow
1. Read `AGENTS.md` and `desk/agents/router.md`.
2. Read the assigned task file and its bound references/pills/files.
3. Confirm the exact files allowed to change.
4. Implement only what the task requires.
5. If the task is an atomized implementation task, add or update its direct unit tests immediately in the same task boundary.
6. Run the smallest relevant tests first.
7. If shared behavior changed, broaden coverage appropriately.
8. Write outputs/logs/run traces to disk.
9. Do not self-retire the task; hand off evidence to the supervisor.

### Boundaries
The executor must not:
- expand scope across multiple tasks
- alter board state casually
- retire tasks from the board
- treat tmux as project runtime logic
- mix Step-1 ETM runtime behavior with desk workflow rules

### Read with this role
- assigned `desk/tasks/*.md` file
- relevant `desk/contexts/*.md` pills
- relevant `desk/atoms/*.md` references
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
