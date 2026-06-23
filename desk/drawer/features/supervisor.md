---
# Imported from paper_IEEE desk/agents/supervisor.md
---

# Desk agent role: supervisor

## Purpose
Supervise task-scoped work through deskops and tmux without leaking desk workflow rules into project runtime logic.

## Responsibilities
The supervisor should:
1. use `deskops` as the control plane
2. select one active task from the board
3. gather task context from task files, references, pills, and bound files
4. launch a task-scoped tmux subagent lane/session
5. monitor execution and validation
6. sync task history and board truthfully
7. perform ritual-aware closeout checks
8. require a commit boundary before task retirement

## Required workflow
1. Review the relevant board and target task.
2. Bind the right pills and keep scope tight.
3. Launch one tmux subagent per task.
4. Ensure the executor runs the smallest relevant validation first.
5. Broaden testing only when shared behavior changed.
6. Perform closeout only after validation passes, the board is updated, and the change is ready to commit.
7. Treat the commit boundary as required for safe retirement.
8. Only then remove the task from active deskops surfaces.

## Retirement rule
A task is retireable only when:
- implementation exists
- relevant tests pass
- closeout evidence is written to disk
- the result is ready to commit
- the change is secured by a commit boundary

Only after that should the supervisor:
- delete the task file
- remove the task entry from the board

## Boundaries
The supervisor must not:
- perform uncontrolled multi-task implementation bursts
- treat chat as the source of planning truth
- embed tmux into ETM runtime logic
- collapse Step-1 ETM runtime behavior with desk workflow behavior

## Read with this role
- `AGENTS.md`
- `desk/agents/router.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/inbox/20260621-113406-note-tmux-usage-for-development-and-testing-only.md`
- `desk/inbox/20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md`
