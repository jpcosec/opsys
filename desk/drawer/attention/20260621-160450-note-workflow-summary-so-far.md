# Note: workflow summary so far

## Purpose
Record the workflow decisions, artifacts, and cleanups completed so far for desk-side execution, supervision, task atomization, testing order, and task retirement.

## What we established

### 1. `deskops` is the workflow control plane
We decided that ETM specialist planning should be managed through real deskops artifacts rather than only through chat or free-form prose.

Current planning surfaces include:
- `desk/tasks/board-etm-specialist-agent-in-adk.md`
- atomized `desk/tasks/task-*.md` files
- transitionary `desk/contexts/*.md` pills
- stable `desk/atoms/*.md` references

### 2. The operating role is supervisor, not free-running implementer
We clarified that the assistant should operate as a supervisor over bounded task execution.

That means:
- select one task from the board
- gather task context
- launch or route one task-scoped tmux subagent lane
- monitor execution and testing
- persist run evidence
- sync board/task truth
- perform closeout checks
- require a commit boundary before retirement

Role files were created to make this explicit:
- `desk/agents/router.md`
- `desk/agents/supervisor.md`
- `desk/agents/executor.md`

`AGENTS.md` was reworked into a router/entrypoint instead of a blended policy dump.

### 3. tmux is external orchestration only
We decided that tmux is allowed as a desk/development orchestration layer, but it must not become part of ETM runtime logic.

This means tmux belongs to:
- supervisor/executor workflow
- task-scoped runs
- test/development orchestration

It does not belong to:
- `agents/etm_specialist/*`
- ETM runtime semantics
- ADK runtime dependencies

Relevant artifacts:
- `specs/SPEC_TMUX_ASYNC_SUBAGENTS_ETM.md`
- `specs/SPEC_TMUX_DESKOPS_TASK_SUBAGENT_RUNNER.md`
- `scripts/start_etm_subagents_tmux.sh`
- `scripts/launch_deskops_tmux_subagent.sh`
- `scripts/build_deskops_task_context.py`
- `scripts/update_deskops_task_history.py`
- `desk/inbox/20260621-113406-note-tmux-usage-for-development-and-testing-only.md`

### 4. Task execution is one bounded task at a time
We established that each deskops task should be executed through a task-scoped lane/session and should not expand across unrelated work.

Executor expectations now include:
- read the task and its bound references/pills/files
- confirm allowed file surface
- implement only the active task
- run the smallest relevant validation first
- persist outputs/logs/run traces
- stop at the task boundary

### 5. Closeout is ritualized and evidence-backed
We read and accepted the ritual files as authoritative:
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`

We also recorded and enforced the rule that a task is not ready for retirement just because code exists.

A task becomes retireable only when:
1. scoped implementation exists
2. relevant tests pass
3. closeout evidence is written to disk
4. the change is ready to commit
5. the change is secured by a commit boundary

Relevant note:
- `desk/inbox/20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md`

### 6. Desk workflow must stay separate from ETM runtime logic
We clarified and documented the boundary between:
- desk-side orchestration and supervision
- project/runtime implementation

Desk workflow concerns include:
- deskops routing
- tmux subagent launch/monitoring
- supervisor/executor roles
- closeout rules
- commit-boundary retirement

Project/runtime concerns include:
- `agents/etm_specialist/agent.py`
- `agents/etm_specialist/tools.py`
- `agents/etm_specialist/workflow.py`
- runtime fixtures, contracts, and tests

Relevant note:
- `desk/inbox/20260621-120503-note-etm-runtime-must-stay-separate-from-desk-orchestration.md`

### 7. Atomization means bounded executable task units
We clarified that atomization is not merely splitting work into many small pieces.

A task is atomized enough when it is:
- bounded in scope
- executable with minimal hidden context
- linked to specific files, references, and pills
- directly testable
- closeable with a coherent commit boundary

The ETM board was already substantially atomized into separate concerns such as:
- connection tests
- expert-model loading
- context lookup
- segmentation/locator preservation
- notation normalization
- payload assembly/validation
- agent wiring
- workflow/state
- fixtures/golden path
- end-to-end tests
- conversational Step-1 tests
- readiness

### 8. Direct unit tests should happen inside each atomized implementation task
We refined the execution rule so that direct unit tests should be written and run immediately after implementing an atomized task, not postponed into a vague late testing phase.

Preferred order:
1. implement the bounded task
2. add or update its direct unit tests
3. run the smallest relevant tests immediately
4. commit the bounded change
5. move to the next task

This rule was placed in workflow surfaces, not task surfaces:
- `desk/agents/executor.md`
- `desk/rituals/execution.md`

### 9. Task files must contain only task-local information
We then tightened the layering rule further:
- task files should contain only task-local information
- workflow desk files should contain workflow policy only

This caused a cleanup pass where we removed workflow-policy leakage from ETM task files.

Examples of cleaned workflow surfaces:
- `desk/agents/executor.md`
- `desk/rituals/execution.md`

Examples of task-local cleanup:
- `desk/tasks/task-build-etm-cross-cutting-negative-tests.md`
- `desk/tasks/task-implement-etm-payload-assembly-and-validation-tool.md`

## Concrete workflow implementation already exercised
We did not only define the workflow; we also exercised it with real task-scoped runs.

Validated task-scoped tmux runs include:
- `runs/tmux-subagents/20260621-114745-task-implement-expert-model-loading-tool/`
- `runs/tmux-subagents/20260621-114950-task-implement-etm-connection-tests/`

These runs produced:
- disk artifacts
- task history updates
- inbox notes

## Recent workflow/desk commits
Workflow-related documentation and planning changes were secured with commit boundaries, including:
- `0c9cf0d docs: require per-task unit tests in atomized execution`
- `85b9113 docs: keep workflow rules out of task-specific ETM docs`
- `1341de8 docs: keep ETM task notes task-local`

## Current interpretation
The current workflow model is:
- use `AGENTS.md` as router
- choose supervisor or executor role explicitly
- treat `deskops` as the planning/control surface
- execute one deskops task per tmux lane/session
- keep runtime logic out of desk workflow files
- keep workflow rules out of task-local files
- test inside the atomized task when implementing
- require ritual-aware closeout plus commit boundary before retirement

## Remaining workflow discipline to preserve
Going forward, maintain these invariants:
- do not free-run across multiple tasks
- do not mix desk policy into ETM runtime code
- do not put global workflow rules into task files
- do not retire tasks before testing, evidence, and commit boundary
- do not treat chat as the planning source of truth when desk artifacts exist

## Related artifacts
- `AGENTS.md`
- `desk/agents/router.md`
- `desk/agents/supervisor.md`
- `desk/agents/executor.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/tasks/board-etm-specialist-agent-in-adk.md`
- `desk/inbox/20260621-113406-note-tmux-usage-for-development-and-testing-only.md`
- `desk/inbox/20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md`
- `desk/inbox/20260621-120503-note-etm-runtime-must-stay-separate-from-desk-orchestration.md`
