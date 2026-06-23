# Note: current workflow invariants

## Purpose
Capture the current workflow rules in short operational form without repeating the longer historical summary.

## Workflow invariants

### 1. `AGENTS.md` is the entry router
Start from `AGENTS.md`, then choose the correct desk role.

### 2. Choose exactly one desk role before acting
- supervisor = route, monitor, sync, close out, retire
- executor = execute one bounded task only

Relevant files:
- `desk/agents/router.md`
- `desk/agents/supervisor.md`
- `desk/agents/executor.md`

### 3. `deskops` is the workflow source of truth
Use desk artifacts for planning and execution state rather than relying on hidden chat context.

Primary surfaces:
- boards
- tasks
- pills
- atoms
- inbox notes

### 4. One task at a time
Execution should stay inside one bounded deskops task.
Do not drift across multiple tasks in one uncontrolled burst.

### 5. One task-scoped tmux lane/session per executing task
`tmux` is an external execution/supervision workbench.
It is not ETM runtime logic.

### 6. Runtime and desk workflow must stay separate
Keep desk workflow concerns out of:
- `agents/etm_specialist/*`
- ETM runtime contracts
- ADK runtime semantics

Keep ETM runtime concerns out of desk workflow role files unless the reference is only for routing or boundary clarification.

### 7. Task files contain only task-local information
A task file should describe:
- the task goal
- the task scope
- the task validation
- task-local repo-sync/evidence notes

A task file should not become a container for global workflow policy.

### 8. Workflow policy belongs in workflow files
Global workflow rules belong in files such as:
- `desk/agents/*.md`
- `desk/rituals/*.md`
- workflow-focused inbox notes

### 9. A task is a work objective, not a workflow phase
A desk task should describe a bounded work objective such as:
- implement something
- investigate something
- document something
- define something
- audit something

A desk task should not merely restate a workflow phase such as:
- commit something
- close something
- retire something

Testing belongs to closeout by default unless the actual deliverable of the task is itself a test artifact, testing surface, or testing specification.

### 10. Atomized implementation tasks should include direct unit tests
If a task implements a bounded component or behavior, its direct unit tests should be added or updated inside the same task boundary.

Preferred order:
1. implement the bounded task
2. add/update direct unit tests
3. run the smallest relevant tests immediately
4. persist evidence
5. hand back for closeout/retirement flow

### 11. Run the smallest relevant validation first
Testing should begin with the smallest meaningful check.
Broaden only when shared behavior changed.

### 12. A task is not retireable just because code exists
A task becomes retireable only when:
1. scoped implementation exists
2. relevant tests pass
3. closeout evidence exists on disk
4. board/task truth is synced
5. the result is ready to commit
6. the result is secured by a commit boundary

Only after that should the task be removed from active planning surfaces.

### 13. Chat is not the durable planning layer
If workflow truth matters, write it into desk artifacts.
Do not rely on transient conversation state as the sole source of operational truth.

## Related artifacts
- `AGENTS.md`
- `desk/agents/router.md`
- `desk/agents/supervisor.md`
- `desk/agents/executor.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/inbox/20260621-113406-note-tmux-usage-for-development-and-testing-only.md`
- `desk/inbox/20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md`
- `desk/inbox/20260621-120503-note-etm-runtime-must-stay-separate-from-desk-orchestration.md`
- `desk/inbox/20260621-160450-note-workflow-summary-so-far.md`
