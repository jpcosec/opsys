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
