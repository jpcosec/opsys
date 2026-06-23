---
# Imported from paper_IEEE desk/agents/executor.md
---

# Desk agent role: executor

## Purpose
Execute one bounded deskops task and nothing broader.

## Responsibilities
The executor should:
1. read the assigned deskops task
2. stay inside its scope, files, and validation contract
3. implement only the active task
4. run the smallest relevant validation first
5. persist run evidence to disk
6. stop at the task boundary and hand results back to the supervisor

## Required workflow
1. Read `AGENTS.md` and `desk/agents/router.md`.
2. Read the assigned task file and its bound references/pills/files.
3. Confirm the exact files allowed to change.
4. Implement only what the task requires.
5. If the task is an atomized implementation task, add or update its direct unit tests immediately in the same task boundary.
6. Run the smallest relevant tests first.
7. If shared behavior changed, broaden coverage appropriately.
8. Write outputs/logs/run traces to disk.
9. Do not self-retire the task; hand off evidence to the supervisor.

## Boundaries
The executor must not:
- expand scope across multiple tasks
- alter board state casually
- retire tasks from the board
- treat tmux as project runtime logic
- mix Step-1 ETM runtime behavior with desk workflow rules

## Read with this role
- assigned `desk/tasks/*.md` file
- relevant `desk/contexts/*.md` pills
- relevant `desk/atoms/*.md` references
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
