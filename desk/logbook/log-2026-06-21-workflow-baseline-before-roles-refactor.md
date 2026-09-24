# Workflow baseline before the desk/roles refactor

Date: 2026-06-21 (recorded), merged 2026-09-24
Scope: deskops central workflow harness
Triggered By: drawer review — three attention notes merged into one entry

## Why this entry exists

Three notes captured the workflow state of June 2026: a summary of where the
harness was, the invariants in force, and the checklist a task had to satisfy to
be safe to hand to a subagent. They were merged here during a drawer review.

Most of what they assert is still the law of this repo, and lives as atoms and
pills now (`atom-workflow-role-model-routing`, `atom-agents-read-by-decision-need`,
`atom-tasks-enable-zero-context-subagents`, `atom-clean-subagent-ambiguity-review`,
`atom-clean-agents-start-from-minimum-workflow-set`). What follows is the
historical record, including the parts that the refactor superseded: it names
`desk/agents/*`, ETM runtime contracts and ADK semantics, none of which this repo
still has. Roles live in `desk/roles/` and the runtime is here.

## Superseded in this record

- `desk/agents/router.md`, `desk/agents/supervisor.md`, `desk/agents/executor.md`
  became `desk/roles/deskops-*.md`, tracked RoleDocs whose agent files are
  materializations.
- The ETM/ADK runtime boundary is gone from this repo.
- tmux as "the execution workbench" is being replaced by the Herdr runtime.

---

## Appendix A — workflow summary (2026-06)

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

---

## Appendix B — current workflow invariants (2026-06)

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

---

## Appendix C — subagent-ready task standard checklist (2026-06)

# Note: 100% subagent-ready task standard checklist

## Purpose
Define the minimum standard a desk task must meet before it is considered fully ready for blind subagent execution without hidden chat context.

This checklist is intentionally strict.
A task should not be called subagent-ready unless it passes every required section.

## Pass/fail rule
A task is **100% subagent-ready** only if:
- every **required** section below passes,
- no blocking ambiguity remains,
- and the executor could act from the task artifact plus its bound references/files/pills alone.

If any required item fails, the task is **not** 100% ready.

---

## Section A. Task identity and bounded purpose

### Required
- [ ] The task has a unique task file under `desk/tasks/`.
- [ ] The task title names one bounded responsibility.
- [ ] The task describes a bounded work objective, not merely a workflow phase.
- [ ] The goal states a concrete result, not a vague aspiration.
- [ ] The scope clearly states what is in scope.
- [ ] The scope clearly states what is out of scope.
- [ ] The task does not bundle multiple unrelated deliverables.
- [ ] The task can plausibly produce one coherent commit boundary.

### Clarification
Valid task types include work such as:
- implementing something
- investigating something
- documenting something
- defining something
- auditing something
- creating a reusable test artifact or testing specification

By default, the following are not standalone task types because they are workflow/closeout phases:
- committing
- closing out
- retiring
- merely running tests on already-bounded work

Testing may still be a valid task when the deliverable is itself a real artifact such as:
- an end-to-end test file
- a conversational test surface
- a testing strategy/specification
- a reusable regression harness

### Fail examples
- "Improve ETM agent"
- "Do testing and workflow and docs"
- a task that mixes runtime implementation, board cleanup, and operational policy
- a task whose only objective is "commit the work"
- a task whose only objective is "run tests" rather than create a test artifact

---

## Section B. Task-local content only

### Required
- [ ] The task file contains only task-local information.
- [ ] The task file does not define global workflow policy.
- [ ] The task file does not contain supervisor/executor doctrine that belongs in `desk/agents/*`.
- [ ] The task file does not contain ritual text that belongs in `desk/rituals/*`.
- [ ] The task file does not preserve deleted/legacy planning surfaces "for history".

### Fail examples
- task says how all tasks should be tested
- task explains retirement policy for the whole workflow
- task keeps historical alternatives that should live only in Git

---

## Section C. Dependency clarity

### Required
- [ ] `depends_on` includes the real prerequisite tasks.
- [ ] The task does not depend on deleted or legacy tasks.
- [ ] The task does not rely on unstated sequencing hidden in chat.
- [ ] If another task must finish first, that dependency is explicit.

### Fail examples
- task assumes schema exists but does not depend on schema task
- task depends on a removed umbrella task

---

## Section D. Reference sufficiency (stable knowledge grounding)

### Required
- [ ] The task binds the atoms needed to understand the domain/business/architecture rule set.
- [ ] The task binds enough references to explain why the task exists and what good output means.
- [ ] The task does not rely on memory of prior conversation for core conceptual grounding.
- [ ] References are relevant to the task, not just loosely related.

### Heuristic
A deterministic low-level task may need only a few references.
A boundary-sensitive or audit-like task usually needs more.

### Fail examples
- conversational test task without Step-1 boundary references
- readiness audit task without provenance or validation references

---

## Section E. File sufficiency (concrete work surface)

### Required
- [ ] `files` names the actual concrete surfaces the executor must read or change.
- [ ] The main implementation or review target is explicitly listed.
- [ ] The relevant tests are explicitly listed when the task is implementation-facing.
- [ ] The relevant fixtures are explicitly listed when the task is fixture-backed.
- [ ] The task does not rely on the executor discovering critical files by search.
- [ ] The file set is sufficient to complete the task without hidden repo knowledge.

### Heuristic
If the executor would need to ask "which file am I supposed to use?" then the task is not ready.

### Fail examples
- workflow task without the workflow test file
- conversational test task without fixture files or expected output file
- readiness audit task without evidence-producing scripts/tests

---

## Section F. Pill sufficiency (transitionary operational context)

### Required
- [ ] The task binds the pills needed for current operational guardrails.
- [ ] Pills are used for transitionary context, not as a substitute for atoms or files.
- [ ] The task includes pills for sensitive boundaries when needed.
- [ ] The task does not omit a critical guardrail that would otherwise only exist in chat.

### Typical pill needs
- Step-1 vs Step-2 separation
- expert-model-first evaluation
- provenance/evidence preservation
- deterministic validation around LLM judgment
- operational readiness/reproducibility

### Fail examples
- payload-validation task without provenance/deterministic-validation pills
- conversational task without Step-1 boundary pill

---

## Section G. Validation quality

### Required
- [ ] The validation section is explicit and task-specific.
- [ ] Validation criteria are observable, not hand-wavy.
- [ ] Validation includes failure behavior when relevant.
- [ ] Validation can be checked by another reviewer.
- [ ] Validation matches the actual files and outputs bound in the task.

### Strong validation examples
- known expert model loads
- missing context fails explicitly
- payload rejects Step-2 leakage
- workflow runs known fixture path

### Weak validation examples
- "works correctly"
- "looks good"
- "review results"

---

## Section H. Testability and immediate testing path

### Required for implementation tasks
- [ ] The task can be tested immediately after implementation.
- [ ] The direct test surface is bound in the task.
- [ ] The smallest relevant test path is obvious.
- [ ] If the task changes shared behavior, the likely broadened test surface is inferable from the bound files.
- [ ] The task does not postpone its first direct tests into another generic task.

### Fail examples
- implement tool now, write first tests later elsewhere
- add workflow behavior but no workflow test file is bound

---

## Section I. Fixture and evidence sufficiency

### Required when applicable
- [ ] If the task is fixture-backed, the fixture files are bound explicitly.
- [ ] If the task expects review against known output, the expected output file is bound explicitly.
- [ ] If the task is audit/readiness oriented, the evidence-producing scripts/tests are bound explicitly.
- [ ] The task can produce or inspect evidence without hidden lookup steps.

### Fail examples
- golden-path task without expected payload fixture
- readiness audit without connectivity or smoke evidence surfaces

---

## Section J. Boundary clarity

### Required
- [ ] The task does not cross Step-1 ETM and Step-2 ASI responsibilities unless that crossing is explicitly the task.
- [ ] The task does not mix desk workflow logic with ETM runtime logic.
- [ ] The task keeps runtime surfaces under `agents/etm_specialist/*` and workflow policy under `desk/*`.
- [ ] Non-goals are explicit when a boundary is easy to violate.

### Fail examples
- ETM task that drifts into diagnosis generation
- runtime task that starts describing tmux orchestration behavior

---

## Section K. Ambiguity check

### Required
- [ ] A blind executor would know what to read first.
- [ ] A blind executor would know what file(s) to modify or inspect.
- [ ] A blind executor would know how to test the result.
- [ ] A blind executor would know what evidence to persist.
- [ ] A blind executor would know what "done" means.

### Hard rule
If a reasonable executor would need to ask a clarifying question before starting, the task is not 100% ready.

---

## Section L. Legacy/duplication check

### Required
- [ ] No parallel legacy task competes with this one.
- [ ] No deleted or superseded planning surface is still referenced.
- [ ] The board/task set gives one clear execution contract for this work.

### Fail examples
- both an umbrella task and a finer-grained task claim the same scope
- spec still points to deleted task IDs

---

## Section M. Current repo-sync truthfulness

### Required
- [ ] The repo-sync note reflects current reality.
- [ ] The note distinguishes implemented work from remaining gaps.
- [ ] The note does not smuggle workflow policy into task-local text.
- [ ] The note references actual evidence surfaces when claiming progress.

### Fail examples
- task says it is implemented when file/test surfaces do not support that claim
- repo-sync note uses workflow doctrine instead of task-local status

---

## Scoring recommendation
Use strict pass/fail first.
If a lightweight score is still useful, evaluate each section as:
- pass
- partial
- fail

But only tasks with **all required sections = pass** should be called:
- **100% subagent-ready**

---

## Fast evaluation template
Use this when auditing a task:

- Task: `...`
- A. Identity and purpose: pass / partial / fail
- B. Task-local content only: pass / partial / fail
- C. Dependency clarity: pass / partial / fail
- D. Reference sufficiency: pass / partial / fail
- E. File sufficiency: pass / partial / fail
- F. Pill sufficiency: pass / partial / fail
- G. Validation quality: pass / partial / fail
- H. Testability and immediate testing path: pass / partial / fail
- I. Fixture and evidence sufficiency: pass / partial / fail
- J. Boundary clarity: pass / partial / fail
- K. Ambiguity check: pass / partial / fail
- L. Legacy/duplication check: pass / partial / fail
- M. Repo-sync truthfulness: pass / partial / fail
- Final verdict: 100% ready / not 100% ready
- Required fixes before routing: `...`

## Related artifacts
- `AGENTS.md`
- `desk/agents/router.md`
- `desk/agents/supervisor.md`
- `desk/agents/executor.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/inbox/20260621-160930-note-current-workflow-invariants.md`

---

## Appendix D — 20260621-120052-note-task-closeout-requires-testing-and-commit-boundary.md

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


---

## Appendix D — 20260621-034212-suggestion-clarify-atoms-vs-pills-and-knowledge-flow-in-deskops-docs.md

---
kind: suggestion
sender_project: paper_IEEE
created_at: 2026-06-21T03:42:12
status: open
---

# Clarify atoms vs pills and knowledge flow in deskops docs

Deskops documentation/help should explicitly explain the knowledge hierarchy and intended flow between atoms, context pills, specs/docs, code, and testing. Current help makes artifact types visible, but it does not make the epistemic model sufficiently clear. Required clarifications: (1) atoms are the baseline stabilized knowledge substrate for project purpose, business rules, domain theory, tooling, code patterns, and testing strategies; (2) context pills are transitionary operational context for subagents and task-phase guidance; (3) avoid duplicating stable knowledge between pills and atoms; (4) tasks should bind enough atoms, files, and pills to enable autonomous execution with minimal hidden chat context; (5) preferred flow is pills -> atoms -> specs/docs -> code -> testing. Suggested surfaces to improve: deskops

Workflow-domain CLI built on top of sldb.

What it manages:
- repo-local desk workspaces
- global and local sldb bootstrap flows
- workflow models such as tasks, boards, pills, rituals, inbox notes, and repository registrations

First-use commands:
- deskops bootstrap
- deskops init .

Useful commands:
- deskops faq
- deskops inbox
- deskops promote
- deskops repo register, quickstart/help docs, and any first-use FAQ material.

