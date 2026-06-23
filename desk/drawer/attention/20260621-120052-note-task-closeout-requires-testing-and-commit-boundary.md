# Note: task closeout requires testing and a commit boundary

## Rule
A deskops task is not truly ready for closure merely because code was written.

A task is ready for retirement only when:
1. the scoped implementation exists
2. the relevant tests pass
3. closeout evidence is written to disk
4. the change is ready to commit
5. the result is secured by a commit boundary

## Why the commit boundary matters
The commit boundary is a key correction surface. It provides:
- rollback
- auditability
- bounded review
- safe recovery if a subagent or worker made a bad change

Without a commit boundary, "done" is too weak for safe supervised workflow.

## Required retirement order
The safe order is:
1. select task from the board
2. execute it in a task-scoped tmux subagent lane
3. test it
4. perform closeout ritual
5. ensure the change is ready to commit
6. secure the change behind a commit boundary
7. only then retire the task from active planning surfaces
   - delete the task file
   - remove the task entry from the board

## Operational implication
Passing tests alone is necessary but not sufficient.
A tested result should not be removed from the deskops task/board surfaces until it is also commit-bounded.

## Supervisor interpretation
The supervisor should treat commit readiness as a required gate for task retirement, not as optional post-processing.
