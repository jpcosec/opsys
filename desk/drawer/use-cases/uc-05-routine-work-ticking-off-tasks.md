# UC-05: Task lifecycle — moving through rituals

The user has a task board with work items. They want to pick something up, work on it, and mark progress.

**Interaction flow:**

1. `deskops list tasks` → sees available tasks with status and phase
2. `deskops show task <id>` → reads the task details
3. `deskops next <id>` → sees the next valid action
4. Starts working: `deskops advance task <id>`
5. Finishes implementation: `deskops closeout verify --task <id>`
6. After verification passes: `deskops closeout commit --task <id> --no-run --reason "..."`

**What this user is trying to do:**
Track progress without leaving the terminal. They want the task board to reflect reality with minimal overhead.

**When this breaks:**
- `list` shows tasks in a confusing order or missing context
- `advance` lets them skip phases that shouldn't be skippable (phase gate violation)
- `show` buries the important info in noise
- State gets out of sync with git (task says done but nothing committed)
- Multiple users advance the same task → conflict
