# UC-05: Routine work — ticking off tasks

The user has a task board with work items. They want to pick something up, work on it, and mark progress.

**Interaction flow:**

1. `deskops list` → sees available tasks with status and phase
2. `deskops show desk-042` → reads the task details
3. Starts working: `deskops advance desk-042 --to in_progress`
4. Finishes implementation: commits, then `deskops advance desk-042 --to review`
5. After review passes: `deskops advance desk-042 --to done`

**What this user is trying to do:**
Track progress without leaving the terminal. They want the task board to reflect reality with minimal overhead.

**When this breaks:**
- `list` shows tasks in a confusing order or missing context
- `advance` lets them skip phases that shouldn't be skippable (phase gate violation)
- `show` buries the important info in noise
- State gets out of sync with git (task says done but nothing committed)
- Multiple users advance the same task → conflict
