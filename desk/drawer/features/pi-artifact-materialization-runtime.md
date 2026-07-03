---
id: feature-pi-artifact-materialization-runtime
status: draft
created: 2026-07-02
tags:
- topic:pi
- topic:subagents
- topic:chains
- topic:system-prompts
- topic:materialization
- topic:workflow-runtime
- topic:proposal
---

# Pi artifact materialization runtime

## Purpose

Define a deskops-native plan for reusing existing desk artifacts as the source of truth for Pi runtime behavior.

The goal is not to create a second workflow system inside `.pi/`. The goal is to materialize already-modeled deskops artifacts into Pi-native runtime artifacts:

- roles and role-like workflow surfaces become agent `systemPrompt`s
- rituals and routines become Pi chains and hookable execution sequences
- pills become runtime guardrails and injected task constraints
- atoms become durable grounding context for agent bundles
- board/task state remains authoritative in `desk/` and is only read by Pi runtime layers

This feature should preserve the current deskops boundary:

- deskops owns workflow semantics, routing, phases, gates, and knowledge lifetimes
- sldb owns structured document operations
- Pi owns execution personas and orchestration materializations only

## Why

The repository already contains a substantial workflow model in `desk/`:

- rituals define gated execution/testing/closeout/phase behavior
- routines define procedural decomposition and task flow structure
- atoms define durable knowledge and architecture rulings
- pills define reusable transitional execution truths
- drawer features already describe supervisor/executor roles and workflow automation directions

Today, much of that intelligence exists as desk artifacts plus repo-local skills. Pi can already run subagents, define custom agents, and save chains, but the runtime layer is not yet systematically derived from deskops artifacts.

Without a derivation layer, there are three risks:

1. Pi prompts and chains drift from deskops rituals.
2. Agent personas remain underspecified and vary per prompt.
3. Execution orchestration is re-authored manually instead of reused from existing deskops models.

This proposal addresses those risks by making Pi a projection/runtime for deskops rather than a competing source of truth.

## Core thesis

Deskops should treat Pi artifacts the same way it treats other human/runtime projections:

- atoms -> docs/materializations for humans
- structured diagram specs -> rendered diagrams
- workflow semantics -> CLI surfaces and routines
- workflow role/routine semantics -> Pi agents, system prompts, chains, and hook plans

The direction of derivation matters:

- **good**: desk artifact -> generated or synchronized Pi runtime artifact
- **bad**: hand-maintained Pi artifact that silently diverges from desk meaning

## Source artifacts to reuse

### Roles / agent-role documents

Candidate sources:

- `.agents/skills/workflow-supervisor/SKILL.md`
- `.agents/skills/workflow-executor/SKILL.md`
- `.agents/skills/workflow-tester/SKILL.md`
- `desk/drawer/features/supervisor.md`
- `desk/drawer/features/executor.md`
- `desk/drawer/features/router.md`

These already encode role boundaries, responsibilities, and anti-patterns. They should inform Pi custom agent personas.

### Rituals

Primary sources:

- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/rituals/phase.md`

These define the gate sequence that runtime chains should respect.

### Routines

Primary sources:

- `desk/routines/` task routines and routine docs

These provide the more operational decomposition that can drive executable sequencing and hooks.

### Pills

Primary sources:

- `desk/contexts/`
- especially board-routed and task-bound pills

These should become injected constraints and validation guardrails inside agent tasks.

### Atoms

Primary sources:

- `desk/atoms/workflow-model/`
- `desk/atoms/knowledge-model/`

These should be used as durable grounding context for the agents/chains that need stable rules, especially around boundaries and lifecycle rules.

## Non-goals

- Do not move workflow truth out of `desk/` into `.pi/`.
- Do not make Pi chains authoritative for task routing or closeout semantics.
- Do not duplicate deskops document models as bespoke Pi config.
- Do not force all desk work through Pi; deterministic CLI/routine/hook flows should remain local when no semantic agent is required.
- Do not let generated Pi artifacts become hand-edited without a reconciliation path.
- Do not weaken the deskops/sldb boundary by letting Pi bypass structured document operations.

## Target mapping

| Deskops source | Pi runtime materialization | Notes |
|---|---|---|
| role contract / role skill | custom agent `systemPrompt` | persona, boundaries, allowed decision scope |
| ritual | chain template / phase-specific orchestration | human-readable ritual remains canonical |
| routine | executable chain step order and hook triggers | machine-runnable projection |
| hook / operator semantics | chain transitions and explicit follow-up triggers | do not invent parallel semantics |
| task doc | runtime input payload | current task remains in `desk/tasks/` |
| board | task routing source | Pi reads, never owns routing |
| pill | prompt guardrail / validation clause | inject `when/where/how_not` as runtime obligations |
| atom | durable grounding context | selected, not bulk-injected |
| test target / validation target | chain validation step inputs | should remain explicit and bounded |

## Deliverable shape

The long-term deliverable is a reproducible projection layer with these surfaces:

1. **role-to-agent materialization**
   - generate or sync Pi custom agents from deskops role sources
   - stable `systemPrompt`s with explicit role boundaries

2. **ritual/routine-to-chain materialization**
   - generate or sync Pi chains from deskops ritual/routine sources
   - preserve deskops gating and handoff semantics

3. **task bundle assembly for subagents**
   - resolve board, task, pills, atoms, files, tests, and validation targets
   - produce a compact bundle suitable for a clean subagent context

4. **hook-aware orchestration contracts**
   - define where deskops hooks stop and Pi orchestration begins
   - support agent-only steps without moving deterministic state logic into Pi

5. **drift detection**
   - identify when generated Pi artifacts diverge from source desk artifacts
   - fail review or warn before stale runtime instructions remain in use

## Detailed plan

## Phase 1 - Inventory and canonical mapping

### Objective

Make the source-to-target mapping explicit before building anything.

### Steps

1. Inventory every desk artifact family that has runtime implications:
   - rituals
n   - routines
   - hooks/operators/primitives if already modeled
   - role skills and drawer role documents
   - pills
   - atoms relevant to workflow runtime

2. For each source artifact family, classify:
   - canonical source path
   - stable fields available today
   - missing structure that blocks materialization
   - whether the materialization target is agent prompt, chain step, hook trigger, or task bundle data

3. Write one explicit projection contract document that states:
   - what is canonical
   - what is derived
   - whether the derived artifact is generated, synced, or advisory only
   - who may edit each side

4. Resolve naming rules for Pi artifacts:
   - agent names
   - chain names
   - package/runtime naming
   - file locations under `.pi/agents/` and `.pi/chains/`

5. Define precedence rules:
   - desk sources always override stale Pi artifacts
   - project-local Pi artifacts derived from deskops win over builtins
   - user-scoped Pi overrides are advisory but must not silently invalidate deskops role invariants

### Outputs

- one mapping spec in drawer
- one inventory table of candidate source artifacts
- one naming/precedence convention

### Open questions

- should projection read directly from markdown docs, from SLDB model payloads, or from both?
- which sources are mature enough to be materialized now versus later?

## Phase 2 - Role materialization into agent system prompts

### Objective

Turn existing role definitions into deterministic Pi personas.

### Steps

1. Identify the canonical role source for each runtime role:
   - supervisor
   - executor
   - tester
   - optional router / reviewer / cold-review roles

2. Normalize each role definition into a prompt contract with sections like:
   - identity
   - purpose
   - non-negotiables
   - allowed actions
   - forbidden actions
   - required reads / recovery
   - handoff expectations
   - evidence expectations
   - escalation rules

3. Decide whether role prompts are:
   - generated directly from desk role docs, or
   - generated from an intermediate structured role spec derived from those docs

4. Create project-local custom agents for the minimal set:
   - `deskops.supervisor`
   - `deskops.executor`
   - `deskops.tester`
   - `deskops.cold-reviewer` or equivalent review-only role

5. Encode repo invariants into each `systemPrompt`:
   - desk is source of truth
   - use board selector `Board`
   - one bounded task at a time where applicable
   - do not self-retire outside closeout rules
   - use SLDB for tracked structured docs
   - respect evidence and validation contracts

6. Decide which repo-local skills remain loaded in addition to the role prompt:
   - role prompt should define persona
   - skill should provide supporting procedure and references
   - avoid duplicating the same instructions in both places without a sync rule

7. Add a role prompt review checklist:
   - does it preserve desk semantics?
   - does it overfit to one task shape?
   - does it keep deterministic work out of the role when not needed?

### Outputs

- first-pass role prompt schema
- minimal custom agent set
- review checklist for role prompts

### Risks

- prompt drift from the desk role source
- repeated prose copied across prompts without synchronization

## Phase 3 - Ritual and routine materialization into chains

### Objective

Translate desk execution semantics into reusable Pi chains without moving authority away from `desk/`.

### Steps

1. Identify the smallest useful chain slices:
   - execution preflight
   - bounded execution handoff
   - testing handoff
   - closeout-readiness audit
   - optional phase-level validation/reconciliation support

2. Map ritual steps to chain phases:
   - `execution.md` -> preflight + ambiguity review + execution handoff
   - `testing.md` -> contract validation + targeted test pass
   - `closeout.md` -> closeout readiness review, not necessarily full deterministic closeout
   - `phase.md` -> integration validation and pill reconciliation support

3. Use routines where they are more operational than rituals:
   - derive exact chain sequencing from routine topology when available
   - use ritual docs to preserve purpose and gate meaning

4. Decide the runtime boundary for each chain step:
   - Pi semantic step
   - deskops deterministic CLI step
   - parent-session synthesis step

5. Design the first chain set:
   - `task-preflight`
   - `task-execution-lane`
   - `task-testing-handoff`
   - `task-closeout-readiness`
   - later: `phase-validation-and-reconciliation`

6. For each chain, define:
   - required inputs from deskops
   - which role agent runs each step
   - what artifact files get written
   - whether the step is read-only or may write
   - whether context is fresh or forked
   - what counts as success/failure

7. Keep deterministic actions out of agent chains when they belong in deskops commands:
   - board edits
   - tracked-doc mutations through SLDB
   - formal closeout cleanup
   - graph/store checks

8. Define how hooks and chains relate:
   - chains can be one runtime implementation target for semantic handoff points
   - hooks remain the better home for deterministic trigger semantics if/when modeled locally
   - avoid making Pi chains emulate a full local event engine if deskops should own that logic

### Outputs

- initial chain catalog
- per-chain input/output contract
- explicit chain-vs-hook boundary note

### Risks

- chains becoming hidden workflow logic instead of visible materializations
- over-encoding deterministic deskops steps into Pi prompts

## Phase 4 - Task bundle assembly and context injection

### Objective

Make clean subagent launches consume the exact deskops bundle they need.

### Steps

1. Define a task bundle schema assembled from desk artifacts:
   - board snapshot
   - task doc
   - current routine/ritual stage
   - bound pills
   - linked atoms
   - allowed files
   - validation targets
   - relevant graph/store diagnostics when needed

2. Formalize how pills become runtime instructions:
   - `what` -> constraint summary
   - `when` -> applicability clause
   - `where` -> touched-surface clause
   - `how_not` -> negative test / guardrail obligation

3. Formalize how atoms enter runtime context:
   - only linked or selected atoms
   - summarize or reference rather than bulk-dump everything
   - preserve stable rulings and boundaries

4. Define the bundle builder source:
   - direct deskops CLI output
   - structured SLDB extraction
   - or a new deskops command that emits a task bundle JSON/markdown artifact

5. Add an evidence bundle convention for subagent runs:
   - run directory
   - board/task/next/graph/git-status snapshots
   - result summary
   - validation output
   - review findings when applicable

6. Ensure subagents do not need to rediscover the codebase broadly when the task has already declared scope.

### Outputs

- task bundle schema
- pill-to-runtime translation rules
- atom selection rules
- proposal for a bundle-emitting command if needed

### Risks

- overstuffed bundles that recreate large-context problems
- under-specified bundles that force agents to roam again

## Phase 5 - Drift detection and synchronization

### Objective

Prevent desk/Pi divergence.

### Steps

1. Decide synchronization mode for each Pi artifact type:
   - generated on demand
   - generated and committed
   - checked but not written
   - manually written with drift audit

2. Add provenance metadata to Pi artifacts:
   - source ritual/role paths
   - generation timestamp
   - source digest/hash
   - generation command/version

3. Define drift checks:
   - source changed since last materialization
   - Pi artifact edited manually after generation
   - required source sections missing from prompt/chain

4. Add a review/report command concept:
   - `deskops pi drift` or equivalent future slice
   - should report stale agents/chains and missing projections

5. Decide CI posture:
   - warn only at first
   - later fail if committed derived artifacts are stale

### Outputs

- provenance metadata convention
- drift-check spec
- CLI/reporting proposal

### Risks

- stale runtime prompts surviving after desk ritual changes
- generated artifacts edited manually without rebase path

## Phase 6 - Minimal runnable slice

### Objective

Ship one small end-to-end example proving the architecture.

### Candidate slice

Use the execution ritual and executor role as the first projection pair.

### Steps

1. Create one deskops executor custom agent from current role sources.
2. Create one `task-preflight` or `execution-preflight` chain from `desk/rituals/execution.md`.
3. Feed it a task bundle assembled from a real active task.
4. Verify that:
   - the chain respects role boundaries
   - the bundle captures the right pills/atoms/files/tests
   - the output is useful without becoming a second source of truth
5. Record what parts had to be improvised because source artifacts were not yet structured enough.
6. Convert those gaps into explicit drawer issues or active tasks.

### Success criteria

- one real deskops task can be launched through the materialized Pi runtime with less ad hoc prompting
- the role/persona is more stable than with generic builtin agents
- the chain reflects the ritual gates instead of bypassing them
- no deskops truth had to move into `.pi/` manually

## Phase 7 - Extend to testing and supervisor flows

### Objective

Broaden from the first runnable slice to a coherent runtime set.

### Steps

1. Materialize tester role and testing handoff chain.
2. Materialize supervisor role and task-dispatch chain.
3. Add a closeout-readiness reviewer/auditor chain that checks evidence before human/CLI closeout.
4. Compare whether phase-level work belongs in:
   - Pi chain orchestration
   - deskops local hook/routine engine
   - or a hybrid where Pi only handles semantic review portions

### Outputs

- coherent minimal runtime suite for supervisor/executor/tester
- explicit note on which lifecycle parts remain local-only

## Phase 8 - Align with workflow engine and semantic adapter proposals

### Objective

Make sure this Pi projection plan complements, rather than conflicts with, other deferred architecture work.

### Relevant drawer items

- `desk/drawer/features/workflow-execution-engine.md`
- `desk/drawer/features/semantic-execution-adapter.md`
- `desk/drawer/issues/issue-implement-task-scoped-subagent-lanes.md`
- `desk/drawer/issues/issue-inject-files-and-atoms-into-subagent-task-context.md`

### Alignment tasks

1. Compare this proposal with the workflow engine proposal:
   - identify which transitions should stay deterministic and local
   - identify which transitions are semantic and suitable for Pi chains

2. Compare this proposal with the semantic execution adapter proposal:
   - Pi may be the first local adapter/runtime, not necessarily the only one
   - event contracts and context bundles should stay generic enough to support non-Pi adapters later

3. Reconcile naming and architecture:
   - is Pi materialization a feature of deskops core, a package, or a separate adapter package?
   - should generated `.pi/` artifacts live in the repo, be cached, or be emitted transiently?

4. Ensure task-scoped run artifact conventions stay compatible with existing `runs/subagents/` expectations.

### Outputs

- compatibility note against existing drawer proposals
- list of conflicts, overlaps, and merge opportunities

## Decision points

Before implementation, these decisions need explicit answers:

1. **Canonical source format**
   - markdown docs as-is
   - SLDB extracted payloads
   - intermediate structured spec

2. **Generation mode**
   - committed generated artifacts
   - on-demand materialization
   - hybrid with drift checks

3. **Runtime location**
   - `.pi/agents/` and `.pi/chains/` inside the repo
   - generated temp artifacts outside the repo
   - dedicated package that exposes them

4. **Boundary with deterministic automation**
   - which lifecycle parts belong in Pi chains
   - which belong in deskops local hooks/routines/CLI only

5. **Prompt/source synchronization**
   - how role/systemPrompt drift is detected and repaired

## Suggested first implementation tasks

The proposal is too broad for one task. A safe atomized follow-up sequence would be:

1. write the projection contract spec
2. define the role prompt schema
3. materialize the executor role into one custom agent
4. define the task bundle schema
5. materialize one execution-preflight chain
6. run a drift check review between source ritual and chain
7. decide chain/hook boundary for later automation

## Validation strategy

### Documentation/projection validation

- compare generated agent prompts against source role documents
- compare generated chains against ritual/routine steps
- review for missing gate semantics or duplicated logic

### Runtime validation

- launch one real preflight chain against a bounded task
- verify the subagent receives the intended bundle
- confirm evidence artifacts are produced
- confirm the role does not violate its boundaries

### Drift validation

- mutate a ritual source and confirm drift is reported
- mutate a generated Pi artifact and confirm provenance mismatch is reported

## Risks and failure modes

### 1. Parallel truth systems

If `.pi/agents` and `.pi/chains` become manually curated without provenance, deskops will gain a shadow workflow model.

### 2. Prompt overgeneration

If role prompts absorb too much ritual detail, prompts become bloated and fragile instead of stable personas.

### 3. Loss of deterministic boundaries

If chains start performing work that belongs in deskops local automation, Pi becomes a replacement for the workflow engine rather than a semantic runtime.

### 4. Weak source structure

Some existing desk artifacts may be rich conceptually but not structured enough yet for reliable prompt/chain generation.

### 5. Bundle overload

Injecting too many pills/atoms/files into every run could defeat the clean-subagent goal.

## Heuristics for success

This direction is working if, after the first slices:

- agents need less ad hoc steering
- chains match ritual gates more closely than manual prompts do
- desk remains the obvious source of truth
- runtime drift becomes visible instead of implicit
- adding a new role or ritual mostly means editing desk artifacts, not rewriting Pi config by hand

## Recommended next document(s)

After this plan, the next drawer docs should likely be:

1. `projection-contract.md` — the canonical source/derived artifact contract
2. `role-prompt-schema.md` — normalized sections for generated/system prompts
3. `task-bundle-schema.md` — exact context payload for clean subagents
4. `chain-hook-boundary.md` — semantic runtime vs deterministic local automation

## Summary

The right Pi adoption path for deskops is not to invent new workflow semantics in Pi. It is to materialize existing deskops artifacts into Pi-native runtime surfaces.

That means:

- roles -> system prompts
- rituals/routines -> chains and runtime hook plans
- pills -> guardrails and validation clauses
- atoms -> durable grounding context
- desk -> source of truth

A small, provable first slice should materialize one role and one ritual-derived chain against a real bounded task, then use the result to decide how far projection should go and what source structure still needs to be formalized first.
