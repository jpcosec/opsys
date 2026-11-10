FILE:desk/tasks/task-scion-autonomy-review-status.md
---
sldb:
  by: agent
  at: '2026-11-10T14:29:08Z'
  authority: generated
  via: create_document
id: task-scion-autonomy-review-status
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- e58ee061
- tests/test_review_command.py
depends_on: []
pills: []
files:
- deskops/services/review.py
- tests/test_review_command.py
- desk/atoms/workflow-model/atom-review-status-preserves-current-dispositions.md
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-review-status.md
---

# Scion autonomy: preserve current accepted review status

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

Current accepted/rejected reviews are reported truthfully for the current exact input, preventing false technical failures and review loops.

## Scope

_State what is in scope and what is out of scope._

Only review status classification, its tests and atom-backed documentation; no lifecycle gates, model or CLI grammar changes. Independent runtime-readiness leaf of the autonomy repair phase.

## Implementation Path

_Outline the expected implementation route or affected surface._

Read task and routed workflow; fresh task-only and cold review; classify matching hash accepted > rejected > pending(reviewed) > incomplete(technical_failure), stale when only other inputs, missing when none. Keep all receipts. Add real isolated-desk status CLI regressions, source atom then docs.

## Validation

_List the checks required before this task can close._

- pytest tests/test_review_command.py
- actual isolated review status after accepted disposition
- pytest at integration

## Done When

_Name the observable condition that makes the task complete._

Current accepted disposition survives status and older rejected/stale receipts do not mask it; input changes report stale; existing pending and technical failure contracts remain; tests and closeout evidence pass.


FILE:AGENTS.md
# Agent Onboarding

This file is the first stop for agents working in this repository. It is a routing document, not the full operator manual.

## Startup Route

Read in this order before changing files:

1. `README.md` for repository purpose, install flow, and tool boundaries.
2. `docs/faq.md` for first-use CLI orientation.
3. `desk/tasks/Board.md` for active routing, board pills, and rituals.
4. The board-routed pills under `desk/contexts/` that match the task.
5. `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, and `desk/rituals/closeout.md` for board/phase and task gates.
6. Relevant atoms under `desk/atoms/`, preferably found through `sldb find` or graph commands rather than raw scanning.

If the active board does not route a task, do not treat fixture-looking files in `desk/tasks/` as real work by default. Use `desk/drawer/tasks/Board.md` for deferred backlog; a drawer item becomes active work only when someone authors the task with `deskops add task --from-drawer <selector> ...`, declaring its closeout evidence (`--task-type` or `--evidence`).

## Skill Route

Load the global surface skill that matches the work before changing files. Workflow roles such as supervisor, executor, and tester are system-prompt concerns, not repo-local skills:

- `use-deskops` for `desk/` surfaces, tasks, drawer work, pills, rituals, the lifecycle graph, repo registry, and workflow operations.
- `use-sldb` for `StructuredNLDoc` models, reversible Markdown markers, `.sldb` stores, document tracking, model registration, rendering, extraction, or field operations. The authoritative global Pi skill lives in the sibling `../sldb/.pi/skills/use-sldb/`.
- `use-kgdb` for graph contracts, graph snapshots, nodes, edges, provenance, `deskops graph build`, `deskops graph missing`, or graph runtime validation.
- `use-spec2viz` for diagram specs, Mermaid/projection outputs, and generated diagram surfaces under `docs/diagrams/`.
- `customize-opencode` only for opencode configuration, `.opencode/` agents, skills, plugins, MCP servers, permissions, or `AGENTS.md`/opencode routing changes.

For Pi in this repo, prefer the project skills under `.pi/skills/`.

## Core Boundaries

- `deskops/` contains Python implementation code.
- `desk/` contains workflow document data: tasks, pills, rituals, atoms, inbox notes, drawer items, and the lifecycle graph (`desk/lifecycle/`).
- SLDB owns structured Markdown infrastructure, model contracts, reversible templates, stores, field queries, and safe document edits.
- KGDB owns graph contracts and graph runtime validation.
- Spec2viz owns structured diagram sources and generated diagram projections.

Docs are human-facing materializations of atoms, not the durable source of truth by themselves. When adding or changing a substantive rule in `docs/`, first capture it in one or more atoms under `desk/atoms/`, then make the doc reflect those atoms.

Do not add desk-local field documents to duplicate SLDB field behavior. If an expected SLDB path fails, capture the gap in the sibling `sldb` repo inbox first, then route an explicit desk task before building a deskops workaround.

## Working Rules

- Start with ambiguity review. If a task would require improvisation, record or resolve the ambiguity before implementation.
- New unrouted repo-local project work starts in `desk/drawer/tasks/`, not `desk/inbox/`. Reserve inbox for incoming notes, unclear external input, or cross-repo intake.
- Commit the drawer task creation before authoring the active task. Commit the authored task (`deskops add task --from-drawer ...`) before implementation.
- Keep one coherent deliverable per task.
- Treat active work as a dependency graph: tasks are atomic units, phases are the current horizontal layer of non-overlapping ready tasks, and the next phase does not begin until the current phase passes its closeout ritual.
- For active desk tasks, run the execution-ritual fresh-context subagent review before implementation. Each task should execute in its own fresh subagent context bundle: the task doc, routed instructions, bound pills, linked atoms, linked files, and validation targets. Use additional subagents for broad exploration when the task is non-trivial.
- Correction: pills are not 1:1 with tasks.
- Treat pills as reusable atomic truths, not one-to-one task artifacts.
- Bind relevant pills by checking `when`, `where`, and `how_not`, not just titles.
- Do not skip from implementation to closeout. Pass execution, testing, and closeout gates explicitly.
- Keep changes small and scoped. Do not clean unrelated dirty worktree changes.
- For mutating CLI exploration or UX testing, write to a disposable sandbox desk such as `.tmp/deskops-cli-test`, not the repo's real `desk/`, unless the task is intentionally changing the tracked desk.
- Every closed task ends with its own atomic commit, made by `deskops closeout commit` after `closeout verify` checks exactly the evidence the task declared at creation (printed as declared X; found Y). `closeout supersede` and `closeout retire` are the closes for a vanished subject or a pre-lifecycle resolution.
- When every task in a phase is closed, run the phase ritual: execute shared integration validation, reconcile pills, capture newly discovered work, and make the phase-closing commit before starting the next phase.

## Validation

Minimum validation for code changes:

```bash
pytest
```

For CLI changes, also run the affected command directly, for example:

```bash
python -m deskops --help
deskops faq
```

For graph or store work, prefer semantic checks:

```bash
sldb stores check --store .sldb
deskops graph missing
```

## Selected Source Documents

- `README.md`
- `docs/quickstart.md`
- `docs/operator-manual.md`
- `docs/faq.md`
- `docs/atoms.md`
- `docs/workflow-policy-reference.md`
- `docs/how-to-test-ux-cli.md`
- `.pi/skills/use-deskops/SKILL.md`
- `../sldb/.pi/skills/use-sldb/SKILL.md`
- `docs/agent-system-prompts/README.md`
- `.opencode/skills/use-deskops/SKILL.md` (parallel copy)
- `.opencode/skills/use-sldb/SKILL.md` (parallel copy)
- `desk/tasks/Board.md`
- `desk/drawer/tasks/Board.md`
- `desk/rituals/phase.md`
- `desk/rituals/execution.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `desk/contexts/pill-001-task-closure-commit.md`
- `desk/contexts/pill-005-subagent-execution.md`
- `desk/contexts/pill-007-phase-gated-task-flow.md`
- `desk/atoms/workflow-model/atom-first-safe-action-follows-read-route.md`
- `desk/atoms/workflow-model/atom-clean-agents-start-from-minimum-workflow-set.md`
- `desk/atoms/workflow-model/atom-agents-read-by-decision-need.md`
- `desk/atoms/workflow-model/atom-agents-read-through-semantic-tools.md`
- `desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md`
- `desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md`
- `desk/atoms/workflow-model/atom-phase-gates-prevent-agent-skipping.md`
- `desk/atoms/workflow-model/atom-docs-are-human-facing-atom-materializations.md`
- `desk/atoms/workflow-model/atom-cli-mutation-testing-uses-sandbox-desk-roots.md`
- `desk/atoms/atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly.md`

The end-to-end manual is `docs/operator-manual.md`; `docs/quickstart.md` is the shortest walkthrough.


FILE:desk/tasks/Board.md
---
sldb:
  by: agent
  at: '2026-11-10T14:30:19Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-cc33a-recibos-de-evidencia-closeout-verify-escribe-reviewdoc-kind-evidence-y-queda-como-orquestador.md
- desk/tasks/task-rendimiento-cada-comando-cli-tarda-30-s-desde-cc32-cc35b.md
- desk/tasks/task-cc33c-grafo-graph-y-drift-leen-sldb-graph-project-gd21-se-borran-la-construcción-propia-y-sus-rglob.md
- desk/tasks/task-cc35d-tags-y-reemplazo-namespaces-domain-tree-y-desk-replace-por-la-api-de-sldb-gd27-gd22.md
- desk/tasks/task-scion-autonomy-review-status.md
- desk/tasks/task-scion-autonomy-coordinator-contract.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- context-review
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- CC33a: Recibos de evidencia - closeout verify escribe ReviewDoc kind evidence y queda como orquestador [draft] - deskops closeout verify corre los productores de hechos de git y archivos y escribe, por cada kind de evidencia verificado, un ReviewDoc kind evidence (fact, value, verdict accepted o rejected, subject anclado al contrato de la tarea), sin duplicar recibos en una verificación repetida sin cambios. verify_task_closeout queda como orquestador y devuelve el mismo envelope que hoy. El gate de cierre todavía no cambia: lo cambia CC33b.
- rendimiento: cada comando CLI tarda ~30 s desde CC32/CC35b [draft] - Se mide, se escribe la causa raíz y se arregla donde viva. Cada comando de deskops (show task, advance) vuelve a un tiempo del orden de antes de CC32, y test_activation_rules y test_lifecycle_end_to_end vuelven a quedar por debajo de ~90 s por archivo.
- CC33c: Grafo - graph y drift leen sldb graph project (GD21); se borran la construcción propia y sus rglob [draft] - deskops graph build|neighbors|missing|reflect y drift leen el grafo de proyecto de sldb (GD21) con la configuración de desk_graph.py; se borran snapshot.py como construcción propia, el rglob de checks.py y los de self_reflection.py; neighbors y missing dan lo mismo que el oráculo v1 y después tests/graph_oracle_v1/ se borra.
- CC35d: Tags y reemplazo - namespaces, domain tree y desk replace por la API de sldb (GD27, GD22) [draft] - tag-namespaces.yaml se sincroniza al store por la API de sldb; require_domain_parents y DomainTree.check/tree pasan a la validación y tag_tree de GD27; axis_folder_relpath pasa a tag_folder; services/replace.py pasa a sldb replace_text con la misma guarda de conteo.
- Scion autonomy: preserve current accepted review status [draft] - Current accepted/rejected reviews are reported truthfully for the current exact input, preventing false technical failures and review loops.
- Scion autonomy: consistent coordinator and tester contract [draft] - One coherent source contract makes Scion coordinator recover configured current state, progress routine authorized work, select reviewed ready unowned tasks, dispatch fresh executor/tester and reconcile closeout before continuing.


FILE:desk/rituals/execution.md
---
sldb:
  by: agent
  at: '2026-11-09T19:13:53Z'
  authority: generated
  via: save_document_payload
# ritual-xxx
id: ritual-execution
# Ordered prose steps; not document references
steps:
- 1. Confirm the current phase is explicit and that this task belongs to the ready
  dependency layer being executed.
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- '1. Run cheap TaskDoc-only preflight under [ritual-context-review](context-review.md)
  in a fresh ephemeral no-tools process: restate objective, list ambiguities and give
  a detailed non-executing dry-run.'
- 1. Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
- 1. Pass the preflight only when the reformulation reproduces the task intent closely
  enough to execute without guesswork; if the subagent reports any ambiguity or misses
  the intended work, fix the TaskDoc before dispatching any Executor.
- '1. Run a separate cheap cold-bundle coverage review under [ritual-context-review](context-review.md):
  explicitly supply task, routed instructions/rituals, bound pills, linked atoms/files
  and validation. Require reformulation, ambiguities and detailed dry-run; no commands
  or source edits.'
- 1. The coordinator compares both outputs with owner intent. Fix the written brief,
  split oversized nodes and retry changed input in a new isolated process. Resolve
  cold-review findings before implementation; unresolved ambiguity blocks dispatch.
- 1. Sweep the board-routed pills and any task-local pills against the task scope,
  touched files, implementation path, and planned validation.
- 1. Bind every pill whose `when`, `where`, or `how_not` matches a plausible part
  of the task.
- 1. If a risky ambiguity is still uncovered, create or update a pill before implementation
  instead of proceeding on implicit assumptions.
- 1. Do not start implementation until the initialization gate confirms atomization,
  preflight comprehension, cold review, and pill coverage.
- '1. Activate the task with `deskops advance task <id>`: the task type''s activation
  RuleDoc (`desk/lifecycle/rule-activation-<type>.md`) requires its review receipts
  accepted and intact and its dependencies closed. Receipts come from `deskops review
  preflight|bundle` or `deskops review record --kind reproduction|goldens|owner`,
  each disposed with `deskops review dispose`; a blocked advance, `deskops show task
  <id>` and `deskops next <id>` name the clause that fails.'
- 1. Implement only the changes required for the active task.
- 1. Keep scope tight and avoid unrelated fixes.
- 1. Prepare validation before calling the work complete.
- 1. Exit execution only by opening a handoff to testing that names the intended contract,
  relevant tests, and pill guardrails that must be proven.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:execution
---

# Execution ritual for active desk tasks

## Purpose

_Explain why this ritual exists._

Carry one active desk task through scoped implementation inside an explicit phase with task and pill binding, including a zero-context TaskDoc comprehension gate and a fresh-context coverage check strong enough to catch missing guardrails before implementation starts. Apply the [context-review ritual](context-review.md) as the cheap non-executing brief-quality gate; expert review, Executor work and independent Tester validation remain distinct.

## Trigger

_State when this ritual should start._

Start when a desk task becomes the current execution target.

## Preconditions

_List the conditions that must hold before running the ritual._

- The task exists in desk/tasks.
- The current phase or ready dependency layer is explicit.
- Dependencies are explicit.
- Required pills exist.
- The board routes the task as active.
- The active board pills are visible to the executor.
- The initialization gate is still open.
- The TaskDoc is specific enough for a fresh-context subagent to restate the work without guessing.
- Required root/package/leaf and dependency-interface reviews have passed the coordinator comparison under [ritual-context-review](context-review.md).

## Validation

_List the checks that prove the ritual was performed correctly._

- The active task is explicit.
- A cheap isolated reviewer completed TaskDoc-only preflight before Executor dispatch; provider/model/profile, exact input/hash, output and coordinator disposition are traceable under ritual-context-review.
- The preflight reformulation was stored at `runs/subagents/<run-dir>/preflight.md`.
- The preflight passed only because the subagent's reformulation reproduced the intended work and surfaced no unresolved ambiguity.
- A separate cheap isolated cold-bundle reviewer completed comprehension and guardrail coverage; expert council review does not satisfy either cheap gate.
- Required pills are named in the task.
- Cold-review ambiguities were resolved in the written contract and rerun when affected input changed; no unresolved finding was merely recorded as permission to execute.
- Each changed surface is either covered by a named pill or explicitly judged to need no pill.
- No active board pill was skipped just because it looked generic or already familiar.
- Implementation did not start before the initialization gate was satisfied.
- Changes stay within task scope.
- The work is ready for testing and has an explicit testing handoff.

## Failure Modes

_List common mistakes this ritual prevents._

- Working without an active task doc.
- Mixing unrelated concerns into one task.
- Skipping the zero-context TaskDoc comprehension gate and dispatching an Executor anyway.
- Letting the preflight pass even though the reformulation missed intent or reported ambiguity.
- Skipping the fresh-context subagent review and relying only on the primary executor's familiarity.
- Skipping pill binding when ambiguity still exists.
- Treating the task's `## Pills` list as a formality instead of a coverage checklist.
- Binding only the most obvious pill while ignoring pills implied by `when`, `where`, or `how_not`.
- Starting code changes before the initialization gate is closed.
- Handing work to closeout directly from execution without a testing gate.
- Using expert approval, a verdict token, reviewer execution, or implementation tests as a substitute for cheap non-executing comprehension.

## Completion

_Describe what completion looks like._

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.


FILE:desk/rituals/testing.md
---
# ritual-xxx
id: ritual-testing
# List of step-xxx paths
steps:
- 1. Confirm the incoming handoff names the intended contract, touched surfaces, and
  pill guardrails to prove.
- 1. Check whether existing tests are stale or encode obsolete behavior.
- 1. Translate the bound pills into concrete assertions, especially the failure cases
  implied by `how_not`.
- 1. Add or update tests for the intended contract.
- 1. Run the smallest relevant test scope first.
- 1. Run broader validation when the task changes shared behavior.
- 1. Do not proceed to closeout while relevant tests fail.
- 1. Exit testing only by opening a closeout handoff that confirms passing evidence
  for the contract and the bound pills.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:testing
---

# Testing ritual for desk task closure

## Purpose

_Explain why this ritual exists._

Verify the intended task behavior with the right test scope before a task can close, while leaving shared integration or end-to-end proof for phase closeout.

## Trigger

_State when this ritual should start._

Run after implementation changes and before closeout.

## Preconditions

_List the conditions that must hold before running the ritual._

- The intended behavior is clear.
- Relevant tests or test locations are known.
- Bound pills and their guardrails are known.
- The execution-to-testing handoff gate is explicit.

## Validation

_List the checks that prove the ritual was performed correctly._

- The intended behavior is covered.
- Bound pill guardrails are covered directly by tests or by an explicit validation step.
- The relevant tests pass.
- No known failure was ignored to force completion.
- Closeout receives an explicit green handoff rather than an informal claim that the task is done.

## Failure Modes

_List common mistakes this ritual prevents._

- Treating stale tests as truth.
- Skipping tests to move faster.
- Closing with failing relevant tests.
- Passing contract tests while leaving a bound pill's `how_not` path unchecked.
- Letting work skip from execution to closeout without a testing gate.

## Completion

_Describe what completion looks like._

The task has trustworthy test evidence and can proceed to closeout, with any broader cross-task validation obligations handed forward to the phase ritual.


FILE:desk/rituals/closeout.md
---
# ritual-xxx
id: ritual-closeout
# Ordered prose steps; not document references
steps:
- 1. Confirm the incoming handoff includes passing evidence for the contract, validations,
  and bound pills.
- 1. Invalidate or fix stale tests if they no longer prove the intended behavior.
- 1. Run the required validation commands and confirm they pass.
- 1. Run `deskops closeout verify --task <id>` and require all reported gates to pass
  before the tool-made commit.
- '1. Check that verify reports ''esta tarea declaró X; encontré Y'' and that Y covers
  X: closeout verifies only the evidence the task declared in `closeout_evidence`
  (tests, commit, atom, materialization, document, external), and a task created without
  it is gated as code and raises an alert. Read every alert; a `.py` change on a task
  that declared no tests is not blocked, but it is never silent.'
- 1. Confirm the task satisfied each bound pill and that no matching board-routed
  pill was missed during execution.
- 1. If the task bound pills, check whether the task `references` list already points
  to an atom that captures any durable residue; tasks with no bound pills pass this
  check trivially.
- 1. If verify reports a changed file with no live atom/materialization link, route
  that gap into an explicit follow-up reference before closing.
- 1. If verify reports a rendered artifact with a sibling source but no declared `source_atoms`
  or `provenance`, fix the artifact metadata before closing.
- 1. Remove stale context docs that are no longer needed.
- '1. Leave removal and untracking to deskops closeout commit: it removes the task
  from the Board, untracks it, and deletes the bundle in the closing commit. Do not
  delete or untrack by hand first.'
- 1. If the task's subject no longer exists, close it with `deskops closeout supersede`,
  naming a reason and at least one resolvable ref, and stop here instead of running
  the closeout commit.
- 1. Close the task with `deskops closeout commit` as the one entry point and the
  mandatory final gate.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:closeout
---

# Closeout ritual for tracked desk tasks

## Purpose

_Explain why this ritual exists._

Close a desk task only after tests, board cleanup, store cleanup when needed, and a dedicated closing commit, while leaving shared integration, pill reconciliation, and next-phase preparation to the phase ritual. `deskops closeout commit` is the one closure entry point: it runs the closeout gates, removes the task from the Board, removes the bundle, makes exactly one commit with the route's trailers, and records the index entry. `deskops advance` does not close tasks. `deskops closeout supersede` is the only way to close a task whose subject no longer exists: it records `superseded` and the stated reason instead of pretending the work was done. `deskops closeout retire` removes a task that was already resolved before the ritual lifecycle (status resolved, closed, done or complete), naming the commit that resolved it, so legacy history leaves desk/tasks without passing through evidence gates it predates. When a closed task was never committed, the closeout first records its body in one commit (`desk: registra <task stem>`, with `Task-Id` and `Closeout-Mode: record` trailers) before the closing commit removes it, so the task's rationale, goal, scope, validation, and done-when stay in git history. The evidence that closes a task is declared when the task is created (`closeout_evidence`, set with `deskops add task --evidence` or filled from `--task-type`; owner decision of 2026-10-29), and closeout verifies exactly that: the same evidence cannot be demanded of every task. See atom-closeout-evidence-is-declared-at-task-creation-and-verified-exactly.

## Trigger

_State when this ritual should start._

Start when the implementation work for a task is complete.

## Preconditions

_List the conditions that must hold before running the ritual._

- Relevant tests pass.
- Bound pill obligations were checked during testing.
- If the task bound one or more pills, closeout reviewed whether any durable pill residue now needs an atom reference in the task `references` list.
- The testing-to-closeout handoff gate is explicit.
- Any stale context docs are ready to be removed.
- The closing change is ready to commit.
- For a superseded task, the reason states that the subject no longer exists and the ref resolves to an ancestor commit or an existing path.

## Validation

_List the checks that prove the ritual was performed correctly._

- The task is gone from desk/tasks.
- The board no longer routes the task.
- No bound pill is left unmet or unverified.
- Tasks with bound pills either reference an atom in `references` or explicitly affirm that no durable pill knowledge needed graduation.
- `deskops closeout verify --task <id>` passes before the tool-made closeout commit.
- Verify reports the evidence the task declared in `closeout_evidence` and what it found ('esta tarea declaró X; encontré Y'): resolvable test evidence when tests is declared, a resolvable ancestor commit when commit is declared, changed-file atom/materialization coverage (or a routed follow-up when coverage is not live yet) when atom or materialization is declared, an existing document when document is declared, and an http(s) URL in `references` when external is declared.
- A `.py` change on a task that did not declare tests, or a task with no `closeout_evidence` (gated as code), is reported as a visible alert and does not block closeout.
- Changed generated artifacts with a sibling source declare `source_atoms` or `provenance` so the source relation is explicit.
- The local store stays consistent after untracking.
- `deskops closeout commit` made exactly one closing commit, with the route's trailers, and recorded its index entry.
- The task was not treated as closed before the final commit gate.
- A superseded task was closed with `deskops closeout supersede`, not with a closeout commit that claims completed work.
- The superseded closing commit carries `Closeout-Mode: superseded`, `Closeout-Reason`, and `Closeout-Ref` trailers.

## Failure Modes

_List common mistakes this ritual prevents._

- Deleting the task before the closing commit exists.
- Leaving a stale tracked document in the store.
- Calling a task closed while tests still fail.
- Closing from green tests alone without checking pill coverage.
- Removing a pill-bound task without checking whether its durable residue should now point at an atom.
- Treating board cleanup or task deletion as equivalent to the final commit gate.
- Closing a task whose subject was removed as if the work had been done.
- Running `deskops closeout supersede` without a reason or a resolvable ref.
- Demanding the same evidence from every task: a docs, spec or external task is not blocked for lacking tests, and a code task cannot skip them by declaring nothing.

## Completion

_Describe what completion looks like._

The task has left the active workspace and its closure is recorded by its own git commit. If it was the last open task in the current phase, the board must still pass through phase closeout before the next phase begins.


FILE:desk/rituals/context-review.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:18Z'
  authority: generated
  via: create_document
# ritual-xxx
id: ritual-context-review
# Ordered prose steps; not document references
steps:
- '1. Map the multilevel DAG: root, packages, leaves and dependency edges. Start with
  the question at the current node; review every node and its edges, not only the
  root.'
- '2. Save input.md as an explicit concatenation of FILE:<path> headers and UTF-8
  texts in documented order. Hash the exact saved bytes with SHA-256, without additional
  normalization. Evidence directory: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/.'
- '3. Launch a new ephemeral process for each attempt. On this machine the verified
  profile is: pi --provider deepseek --model deepseek-flash --thinking low --offline
  --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates
  --no-tools --system-prompt <reviewer-role> --print @<input.md>. Save the command,
  provider/model/profile and reason for cheap selection. No --continue or --resume.
  Record isolation flags and supplied input as operational evidence; this does not
  assert knowledge of provider internal memory.'
- '4. Instruct the non-executing reviewer to restate the objective and scope, enumerate
  ambiguities and produce a detailed dry-run: which supplied sources it would read,
  proposed edits, dependency/interface implications, commands it would run later and
  expected validation outcomes. It may name commands but must not run them, inspect
  unsupplied sources or edit files.'
- 5. Save output and coordinator comparison with owner intent, including missing guardrails,
  required textual corrections and disposition. A word such as APTO is never sufficient.
  Keep transport/quota/unavailable-model failures separately from comprehension findings;
  stop or retry an available cheap model with explicit reason, without expert rescue.
- 6. Use misunderstandings as feedback on the brief. Correct its text; split oversized
  or ambiguous nodes recursively into coherent children and explicit dependency edges.
  Review root, packages and all leaves, plus contracts across edges. Do not execute
  while ambiguity remains unresolved.
- 7. Retry the revised explicit input in a new process, with no prior review or oral
  fixes injected. A new input or changed dependency contract invalidates affected
  reviews, including dependent nodes whose supplied contract changed; unrelated typos
  do not revoke every review. Preserve previous attempts for traceability.
- '8. Before Executor dispatch, run two separate cheap roles under this protocol:
  TaskDoc-only preflight (save reformulation also at runs/subagents/<run-dir>/preflight.md),
  then cold-bundle coverage using TaskDoc, routed instructions/rituals, bound pills,
  linked atoms/files and validation targets supplied explicitly. The coordinator accepts
  both comparisons before dispatch.'
- 9. Only reviewed ready leaves may enter the execution ritual. Expert council review
  of design, an Executor implementation and a fresh independent Tester are separate
  gates; none substitutes for cheap comprehension or human product decisions.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:context-review
---

# Cheap recursive zero-context brief review

## Purpose

_Explain why this ritual exists._

Test whether a cheap isolated reviewer understands the written question before planning, promotion or execution. Durable rule: [source atom](../atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md). This ritual is a documentary gate; it adds no lifecycle state or runtime enforcement.

## Trigger

_State when this ritual should start._

Run while drafting or revising a plan, root, package or leaf, before promotion or execution and again when its explicit input or dependency contract changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The coordinator names the node, exact versioned brief, explicit dependencies/interfaces and expected intent. Large nodes can still be drafts; they need not be promoted to receive review.
- The supplied context is minimal: exact brief plus only necessary explicitly supplied references, with a documented order and paths. No chat history, previous outputs, oral corrections, persistent memory or automatically loaded context/skills.
- A cheap available provider/model is selected with a recorded reason and profile. Do not claim global minimum price without measurement; do not replace a failed cheap reviewer with an expert to obtain approval.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every required root/package/leaf review has exact input/hash, provider/model/profile and selection reason, command/isolation evidence, reformulation, ambiguities, detailed non-executing dry-run, coordinator comparison and required changes.
- The coordinator compares understanding with intent rather than accepting a verdict token; no unresolved ambiguity remains before execution.
- Each attempt used a new process without history, memory, automatic skills/context or reviewer tools. TaskDoc-only and cold-bundle evidence remain separate.
- Changed node inputs and dependency contracts invalidate the affected reviews; review coverage is explicit by node/revision, never inferred from council approval or plan structure.

## Failure Modes

_List common mistakes this ritual prevents._

- Asking an expert council to compensate for an unclear brief, or treating APTO/structural PASS as comprehension or execution authorization.
- Reviewing only the root or whole large DAG and claiming every descendant passed.
- Letting a reviewer execute the dry-run or loading implicit chat history, skills, memory or previous corrections.
- Retrying in the same session, fabricating node evidence, or marking pending reviews approved.
- Confusing transport/quota failures with ambiguous intent, or replacing cheap review with execution/testing.

## Completion

_Describe what completion looks like._

For the reviewed node/version, the coordinator has accepted a faithful reformulation and detailed dry-run with no unresolved ambiguity; all required descendant and interface reviews are traceable. This proves brief comprehension only. Promotion, execution, independent testing, product decisions and closeout retain their own gates.


FILE:desk/contexts/pill-005-subagent-execution.md
---
# pill-xxx
id: pill-005
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:pattern
- topic:subagents
- topic:execution
---

# Pattern: execute active tasks through fresh subagents

## What

_Define the context or guardrail this pill carries._

Use one fresh subagent as the normal execution surface for each active task, with the primary session acting as coordinator, integrator, and final verifier.

## Why

_Explain why this context matters for safe execution._

Fresh task-specific contexts reduce context overload, make ambiguity easier to spot, and keep execution aligned with the task's actual bundle of files, pills, atoms, and validations instead of leaked memory from earlier work.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever an active task enters execution, especially when the board contains multiple parallel-ready tasks in the same phase.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/execution.md`, `desk/rituals/phase.md`, active task execution, and any workflow tooling that launches or simulates subagent work.

## How

_Describe the correct way to apply this guidance._

Give each task its own clean execution bundle: the task doc, routed instructions, bound pills, linked atoms, linked files, and validation targets. Let the primary session coordinate handoffs, integration, and final verification across tasks and phases.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not carry multiple unrelated tasks through one long-lived context. Do not let subagent outputs bypass the task's own validation, closeout, and commit workflow.


FILE:desk/drawer/tasks/task-scion-autonomy-review-status.md
# Scion autonomy: review status preserves current dispositions

Owner authorization 2026-11-10: iterate with bots and fix DeskOps/Scion to operate
without manual prompting between normal workflow steps.

First leaf: ReviewService._state_for_key currently ignores disposed accepted and
rejected receipts, reporting technical failure/stale and provoking review loops.
Filter by current exact input hash first. Report accepted if any current accepted
receipt exists (same existential condition as lifecycle); else rejected if any
current rejected, reviewed for current pending, technical_failure for current
incomplete. With records but no current hash report stale; with no records missing.
Preserve all receipts and run provenance; change no gate, model or CLI grammar.
Capture this durable contract in an atom and reflect it in operator-manual.md.
Regression tests must use real modeled receipts/status CLI with isolated desks.

Files: deskops/services/review.py, tests/test_review_command.py, a relevant new
atom under desk/atoms/workflow-model/, docs/operator-manual.md, CHANGELOG.md.
Validation: affected pytest, actual review status before/after accepted disposition,
full pytest at integration, declared exact closeout evidence and atomic commit.


FILE:deskops/services/review.py
"""Cold context review service behind ``deskops review`` (GC03).

This replaces the two governed ``context_review.py`` scripts with a CLI command
(plan gates-por-tipo, D10). Every run writes the evidence the ritual asks for
under ``runs/subagents/<run>/context-review/<key>/<input sha256>/attempt-N/``
(``input.md``, ``manifest.json``, ``output.md``, ``stderr.log``, ``receipt.json``)
and one ``ReviewDoc`` receipt under ``desk/reviews/``.

Modes:
  node <plan-dir> [IDS...]   review drawer dag.yaml nodes (contract + neighbours + gates)
  preflight <task>           TaskDoc-only review before dispatch
  bundle <task>              cold bundle: TaskDoc + routed rituals + pills + atoms + files + validation
  status [task | plan-dir]   compare current inputs with recorded reviews; no model call
  dispose <review-id>        write the verdict on one pending receipt
  record <task> --kind K     reproduction/goldens/owner receipt from operator evidence; no model call

Caps (owner, D9): an unchanged input is not reviewed again; ``--max-attempts``
(default 2) refuses another *good* attempt on the same key unless ``--force`` with
``--reason``. Transport failures (non-zero exit, timeout, or output without the
``REFORMULACION`` section) do not count against the cap and are recorded as
``technical_ok: false`` with a ``verdict: incomplete`` / ``reason: technical``
receipt, kept separate from comprehension findings (ritual step 5).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import yaml
from sldb.api.stores.doc_status import doc_status
from sldb.runtime.validation import extract_model_data

from deskops import doc_access
from deskops.config import DeskConfig
from deskops.errors import DomainError
from deskops.errors import UsageError
from deskops.models import ReviewDoc
from deskops.models import RuntimeProfileDoc
from deskops.models import TaskDoc
from deskops.models import BoardDoc


# The verified reviewer profile from desk/rituals/context-review.md step 3 (D4).
SYSTEM = (
    "Revisor barato aislado de un encargo de planificación. Trabajas solo con el input explícito: "
    "sin herramientas, historial ni otras fuentes. No ejecutas nada. Responde en español con estas "
    "secciones exactas: REFORMULACION (propósito, resultado, repo, límites), AMBIGUEDADES (numeradas, "
    'cada una con cita textual del input y qué obligaría a inventar; escribe "ninguna" si no hay), '
    "DRY-RUN (lecturas, cambios previstos, dependencias y validaciones futuras, sin ejecutar), "
    "FUTURO (lo que produce otro nodo o decide un humano, no ambigüedad). "
    "REFORMULACION describe el encargo del nodo, no esta revisión. DRY-RUN describe cómo lo ejecutaría "
    "un ejecutor futuro, hipotéticamente y sin ejecutar nada. Si el nodo es un agregado o paquete no "
    "ejecutable, dilo y además recorre cómo lo cumplen sus hijos, qué transfiere cada uno al siguiente "
    "y cómo se valida el resultado conjunto. Máximo 350 palabras."
)
SELECTION = "deepseek-flash: perfil barato verificado en esta máquina por ritual-context-review (D4)"
MODEL = "deepseek/deepseek-flash"
DEFAULT_ENGINE = "runtime-pi-deepseek-flash"
TIMEOUT = 900
# Receipts ``deskops review record`` writes by hand (no model call); the others come from their command.
# Kinds an operator records by hand. ``preflight`` and ``bundle`` also come from their own
# model review; a hand-recorded one keeps ``engine: human`` so it never reads as a model review.
RECORD_KINDS = ("reproduction", "goldens", "owner", "preflight", "bundle")

# Recorded by hand, ``preflight`` and ``bundle`` name their operator (``--operator``) and say
# why no model reviewed them; they are for desks without a model (CI scenarios, the quickstart),
# not a substitute for ``deskops review preflight|bundle`` on a real desk.
HUMAN_REVIEW_KINDS = ("preflight", "bundle")
NO_MODEL_REASON = "no model available"

KEEP = (
    "id",
    "title",
    "kind",
    "owner_repo",
    "node_role",
    "parent_id",
    "children",
    "scope",
    "acceptance",
    "output_scope",
    "depends_on",
    "requires",
)
BASE = ["context-review-guide.md", "brief.md", "alcance.md", "decisiones.md"]


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def _coerce_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


class Bundle:
    """Accumulates the explicit input.md parts and their per-source hashes."""

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.sources: list[dict[str, Any]] = []
        self.omitted: list[dict[str, Any]] = []

    def add(self, path: str, text: str, projection: str = "whole_file") -> None:
        self.parts.append(f"FILE:{path}\n{text.rstrip()}\n")
        self.sources.append({"path": path, "sha256": _sha(text.encode()), "projection": projection})

    def omit(self, path: str, reason: str, size: int | None = None) -> None:
        record: dict[str, Any] = {"path": path, "reason": reason}
        if size is not None:
            record["size"] = size
        self.omitted.append(record)

    def close(self, instruction: str) -> bytes:
        self.parts.append(f"FILE:instruccion\n{instruction}\n")
        return "".join(part + "\n" for part in self.parts).encode()


def _technical_ok(attempt_dir: Path) -> bool:
    receipt = attempt_dir / "receipt.json"
    if not receipt.exists():
        return False
    try:
        return bool(json.loads(receipt.read_text(encoding="utf-8")).get("technical_ok"))
    except Exception:
        return False


class ReviewService:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.desk_root = self.root / "desk"

    # ------------------------------------------------------------------ paths
    def _reviews_dir(self) -> Path:
        return self.desk_root / "reviews"

    def _evidence_root(self, run_name: str) -> Path:
        return self.root / "runs" / "subagents" / run_name / "context-review"

    def _key_attempts(self, key: str) -> list[Path]:
        base = self.root / "runs" / "subagents"
        if not base.exists():
            return []
        return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))

    def _identity(self) -> str:
        identity = (DeskConfig.load(self.desk_root).project_identity or "").strip()
        if identity and identity != "unknown-project":
            return identity
        return self.root.name

    # ------------------------------------------------------------------ engine
    def _load_engine(self, engine_id: str) -> dict[str, Any]:
        directory = self.desk_root / "runtimes"
        for path in sorted(directory.glob("*.md")) if directory.exists() else []:
            try:
                data = extract_model_data(RuntimeProfileDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("id") == engine_id or path.stem == engine_id:
                return data
        raise DomainError(
            f"RuntimeProfileDoc '{engine_id}' not found under {directory}; "
            f"seed it with `deskops init` / `deskops desk update --apply` or write it by hand."
        )

    def _argv(self, engine: dict[str, Any], input_path: Path) -> list[str]:
        argv = [str(engine.get("binary") or "pi")]
        argv += [str(item) for item in (engine.get("extra_args") or [])]
        if engine.get("system_prompt_flag") and engine.get("system_prompt"):
            argv += [str(engine["system_prompt_flag"]), str(engine["system_prompt"])]
        argv.append(f"@{input_path}")
        return argv

    # ------------------------------------------------------------------ tasks
    def _task_path(self, task_id: str) -> Path:
        tasks_dir = self.desk_root / "tasks"
        try:
            return doc_access.resolve_document(self.root, tasks_dir, task_id, "task", recursive=False)
        except FileNotFoundError:
            raise DomainError(f"Task '{task_id}' not found under {tasks_dir}") from None

    def _resolve_task(self, selector: str) -> tuple[Path, str]:
        """The task file a selector names and the task's full id (its frontmatter ``id``, else the
        file stem). Receipts are keyed and anchored on that id, never on the selector as typed:
        ``task-cc37`` would otherwise give ``doc:<Model>:task-cc37``, a subject no rule matches."""
        task_path = self._task_path(selector)
        task_id = str(self._task_payload(task_path).get("id") or "").strip() or task_path.stem
        return task_path, task_id

    def _task_model(self, task_path: Path) -> str:
        store = self.root / ".sldb"
        if not store.exists():
            return "TaskDoc"
        try:
            status = doc_status(store, task_path.relative_to(self.root).as_posix())
        except Exception:
            return "TaskDoc"
        return status.model or "TaskDoc" if status.exists else "TaskDoc"

    def _task_payload(self, task_path: Path) -> dict[str, Any]:
        return extract_model_data(TaskDoc, task_path.read_text(encoding="utf-8"))

    # ------------------------------------------------------------------ bundle
    def _preflight_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))
        instruction = (
            f"Preflight solo-TaskDoc de la tarea {task_id}: reformula el encargo tal como lo leería "
            "un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y "
            "da el DRY-RUN sin ejecutar nada. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _resolve_pill(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        try:
            return doc_access.resolve_document(self.root, self.desk_root / "contexts", ref, "pill")
        except (FileNotFoundError, ValueError):
            return None

    def _resolve_atom(self, ref: str) -> Path | None:
        ref = ref.strip()
        if not ref:
            return None
        candidate = Path(ref)
        if not candidate.is_absolute():
            candidate = self.root / candidate
        if candidate.is_file():
            return candidate
        atom_id = ref.removeprefix("atom:")
        matches = [path for path in (self.desk_root / "atoms").rglob("*.md") if path.stem == atom_id]
        if len(matches) == 1:
            return matches[0]
        return None

    def _bundle_input(self, task_path: Path, task_id: str) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        payload = self._task_payload(task_path)

        # 1. TaskDoc
        rel = task_path.relative_to(self.root).as_posix()
        bundle.add(rel, task_path.read_text(encoding="utf-8"))

        # 2. Rituals routed by the Board (desk/tasks/Board.md), in order.
        board_path = self.desk_root / "tasks" / "Board.md"
        rituals: list[str] = []
        if board_path.is_file():
            try:
                board = extract_model_data(BoardDoc, board_path.read_text(encoding="utf-8"))
                rituals = [str(item) for item in (board.get("rituals") or [])]
            except Exception:
                rituals = []
        if rituals:
            for ritual_ref in rituals:
                ritual_path = Path(ritual_ref)
                if not ritual_path.is_absolute():
                    ritual_path = self.root / ritual_path
                if ritual_path.is_file():
                    bundle.add(ritual_path.relative_to(self.root).as_posix(), ritual_path.read_text(encoding="utf-8"))
                else:
                    bundle.omit(ritual_ref, "missing")
        else:
            bundle.omit("desk/tasks/Board.md rituals", "missing")

        # 3. Bound pills (TaskDoc.pills), in order.
        for pill_ref in _coerce_list(payload.get("pills")):
            pill_path = self._resolve_pill(pill_ref)
            if pill_path is not None:
                bundle.add(pill_path.relative_to(self.root).as_posix(), pill_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(pill_ref, "unresolved")

        # 4. Bound atoms (TaskDoc.atoms), in order.
        for atom_ref in _coerce_list(payload.get("atoms")):
            atom_path = self._resolve_atom(atom_ref)
            if atom_path is not None:
                bundle.add(atom_path.relative_to(self.root).as_posix(), atom_path.read_text(encoding="utf-8"))
            else:
                bundle.omit(atom_ref, "unresolved")

        # 5. Files the TaskDoc names, under 60 KB, files only, present.
        for file_ref in _coerce_list(payload.get("files")):
            file_path = Path(file_ref)
            if not file_path.is_absolute():
                file_path = self.root / file_path
            if not file_path.exists():
                bundle.omit(file_ref, "missing")
                continue
            if file_path.is_dir():
                bundle.omit(file_ref, "directory")
                continue
            size = file_path.stat().st_size
            if size >= 60_000:
                bundle.omit(file_ref, "size>=60000", size=size)
                continue
            bundle.add(file_ref, file_path.read_text(encoding="utf-8", errors="replace"))

        # 6. The TaskDoc validation section as the instruction.
        validation = _coerce_list(payload.get("validation"))
        validation_text = "\n".join(f"- {item}" for item in validation) if validation else "(sin validación declarada)"
        instruction = (
            f"Cold-bundle de la tarea {task_id}: con el TaskDoc, los rituales enrutados por el Board, "
            "las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el "
            "encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. "
            "No ejecutes nada.\n\nSección de validación del TaskDoc:\n" + validation_text
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    # ------------------------------------------------------------------ node
    def _load_dag(self, plan_dir: Path) -> tuple[dict, dict]:
        dag_path = plan_dir / "dag.yaml"
        if not dag_path.is_file():
            raise DomainError(f"No dag.yaml in plan directory {plan_dir}")
        try:
            dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise DomainError(f"Could not parse {dag_path}: {exc}") from exc
        nodes: dict[str, dict] = {}
        for task in dag.get("tasks") or []:
            nodes[task["id"]] = task
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            nodes[package["id"]] = package
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            nodes[root["id"]] = root
        return dag, nodes

    def _plan_nodes(self, dag: dict) -> list[str]:
        order: list[str] = []
        root = (dag.get("hierarchy") or {}).get("root")
        if root:
            order.append(root["id"])
        for package in (dag.get("hierarchy") or {}).get("packages") or []:
            order.append(package["id"])
        for task in dag.get("tasks") or []:
            order.append(task["id"])
        return list(dict.fromkeys(order))

    @staticmethod
    def _contract(node: dict) -> dict:
        return {key: node[key] for key in KEEP if key in node}

    @staticmethod
    def _neighbours(dag: dict, nodes: dict, node: dict) -> tuple[list[dict], dict]:
        tasks = {task["id"]: task for task in dag.get("tasks") or []}
        packages = {package["id"] for package in (dag.get("hierarchy") or {}).get("packages") or []}
        node_id = node["id"]
        if node_id == "ROOT":
            ids = list(node.get("children") or [])
        elif node_id in packages:
            ids = list(node.get("children") or [])
            inside = set(ids)
            for child in ids[:]:
                ids += [x for x in (tasks.get(child) or {}).get("depends_on") or [] if x not in inside]
        else:
            ids = list(node.get("depends_on") or [])
            ids += [task["id"] for task in (dag.get("tasks") or []) if node_id in (task.get("depends_on") or [])]
            ids += [node.get("parent_id") or ""]
        ids = list(dict.fromkeys(item for item in ids if item and item != node_id))
        gates_ids = list(node.get("requires") or [])
        gates_ids += [
            gate for gate, value in (dag.get("gates") or {}).items()
            if isinstance(value, dict) and value.get("produced_by") == node_id
        ]
        gates_ids += [
            gate for gate in (dag.get("gates") or {}) if gate in str(ReviewService._contract(node))
        ]
        return [nodes[item] for item in ids if item in nodes], {
            gate: (dag.get("gates") or {})[gate] for gate in dict.fromkeys(gates_ids) if gate in (dag.get("gates") or {})
        }

    def _node_input(self, plan_dir: Path, dag: dict, nodes: dict, node: dict) -> tuple[bytes, list[dict], list[dict]]:
        bundle = Bundle()
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        for rel in BASE:
            source = plan_dir / rel
            if source.is_file():
                bundle.add(f"{plan_rel}/{rel}", source.read_text(encoding="utf-8"))
            else:
                bundle.omit(f"{plan_rel}/{rel}", "missing")

        node_id = node["id"]
        bundle.add(f"{plan_rel}/dag.yaml#node:{node_id}", yaml.safe_dump(self._contract(node), allow_unicode=True, sort_keys=False), "node_contract")
        neighbours, gates = self._neighbours(dag, nodes, node)
        for neighbour in neighbours:
            bundle.add(f"{plan_rel}/dag.yaml#edge:{neighbour['id']}", yaml.safe_dump(self._contract(neighbour), allow_unicode=True, sort_keys=False), "edge_contract")
        if gates:
            bundle.add(f"{plan_rel}/dag.yaml#gates", yaml.safe_dump(gates, allow_unicode=True, sort_keys=False), "gate_contracts")

        is_aggregate = node_id == "ROOT" or node_id.startswith("PK")
        instruction = (
            f"Revisa el nodo {node_id} siguiendo context-review-guide.md. "
            + (
                "Es un agregado: reformula el resultado sustantivo del paquete y da un DRY-RUN hipotético de "
                "sus hijos en orden, con entradas y salidas entre ellos y la validación conjunta. "
                if is_aggregate
                else ""
            )
            + "Los bloques edge son contratos de vecinos; no los revises. No ejecutes nada."
        )
        return bundle.close(instruction), bundle.sources, bundle.omitted

    def _find_plan_dir(self, plan_id: str) -> Path | None:
        plans_root = self.desk_root / "drawer" / "plans"
        if not plans_root.exists():
            return None
        for dag_path in sorted(plans_root.rglob("dag.yaml")):
            try:
                dag = yaml.safe_load(dag_path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(dag, dict) and dag.get("id") == plan_id:
                return dag_path.parent
        return None

    # ------------------------------------------------------------------ caps
    def _next_attempt_dir(
        self,
        run_name: str,
        key: str,
        input_sha256: str,
        max_attempts: int,
        force: bool,
    ) -> Path | None:
        attempts = self._key_attempts(key)
        prior = [attempt for attempt in attempts if attempt.parent.name == input_sha256]
        if prior and any(_technical_ok(attempt) for attempt in prior) and not force:
            return None  # unchanged input already reviewed
        good = sum(1 for attempt in attempts if _technical_ok(attempt))
        if not prior and good >= max_attempts and not force:
            raise DomainError(
                f"{key}: {good} intentos ya; tope --max-attempts {max_attempts} "
                "(usa --force con --reason si el input cambió de verdad)"
            )
        out = self._evidence_root(run_name) / key / input_sha256 / f"attempt-{len(prior) + 1}"
        out.mkdir(parents=True, exist_ok=True)
        return out

    # ------------------------------------------------------------------ run
    def _run_one(
        self,
        *,
        run_name: str,
        key: str,
        input_data: bytes,
        sources: list[dict],
        omitted: list[dict],
        engine_id: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
        kind: str,
        subject: str,
        subject_ref: str,
        node_id: str | None,
        plan_id: str | None = None,
    ) -> dict[str, Any]:
        input_sha256 = _sha(input_data)
        attempt_dir = self._next_attempt_dir(run_name, key, input_sha256, max_attempts, force)
        if attempt_dir is None:
            return {"key": key, "state": "unchanged", "input_sha256": input_sha256}

        (attempt_dir / "input.md").write_bytes(input_data)
        engine = self._load_engine(engine_id)
        argv = self._argv(engine, attempt_dir / "input.md")
        start = _now()
        try:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
            stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired as exc:
            detail = ""
            if isinstance(getattr(exc, "stderr", None), bytes):
                detail = exc.stderr.decode(errors="replace")
            elif isinstance(getattr(exc, "stderr", None), str):
                detail = exc.stderr or ""
            stdout, stderr, returncode = "", f"timeout after {timeout}s\n{detail}", None
        end = _now()

        (attempt_dir / "output.md").write_text(stdout, encoding="utf-8")
        (attempt_dir / "stderr.log").write_text(stderr, encoding="utf-8")
        technical_ok = returncode == 0 and "REFORMULACION" in stdout

        manifest: dict[str, Any] = {
            "key": key,
            "input_sha256": input_sha256,
            "argv": argv,
            "model": MODEL,
            "profile": engine_id,
            "selection_reason": SELECTION,
            "sources": sources,
            "omitted_sources": omitted,
            "started": start,
            "finished": end,
        }
        if force and reason:
            manifest["retry_reason"] = reason
        (attempt_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        receipt: dict[str, Any] = {
            "key": key,
            "technical_ok": technical_ok,
            "returncode": returncode,
            "input_sha256": input_sha256,
            "output_sha256": _sha(stdout.encode()),
            "start": start,
            "end": end,
        }
        (attempt_dir / "receipt.json").write_text(
            json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        run_dir = attempt_dir.relative_to(self.root).as_posix()
        if technical_ok:
            verdict = "pending"
            review_reason = reason if force else ""
        else:
            verdict = "incomplete"
            review_reason = "technical"

        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref=subject_ref,
            engine=engine_id,
            run_dir=run_dir,
            input_sha256=input_sha256,
            output_sha256=receipt["output_sha256"],
            verdict=verdict,
            reason=review_reason,
            node_id=node_id,
            plan_id=plan_id,
        )

        return {
            "key": key,
            "state": "reviewed" if technical_ok else "technical_failure",
            "input_sha256": input_sha256,
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "run_dir": run_dir,
            "technical_ok": technical_ok,
        }

    def _next_review_number(self, review_dir: Path, kind: str, node: bool) -> int:
        if not review_dir.exists():
            return 1
        prefix = "node-" if node else f"{kind}-"
        matches = [path for path in review_dir.glob(f"{prefix}*.md") if path.stem.startswith(prefix)]
        return len(matches) + 1

    def _write_review(
        self,
        *,
        kind: str,
        subject: str,
        subject_ref: str,
        engine: str,
        run_dir: str,
        input_sha256: str,
        output_sha256: str,
        verdict: str,
        reason: str,
        node_id: str | None,
        plan_id: str | None = None,
        summary: str | None = None,
        actor: str | None = None,
        title: str | None = None,
    ) -> tuple[str, Path]:
        if node_id is not None:
            node_lower = node_id.lower()
            plan_id = plan_id or (subject_ref.split("/dag.yaml#node:", 1)[0].rsplit("/", 1)[-1] if "/" in subject_ref else "")
            review_dir = self._reviews_dir() / f"{plan_id}-{node_lower}"
            n = self._next_review_number(review_dir, kind, node=True)
            review_id = f"review-{plan_id}-{node_lower}-node-{n}"
            title = title or f"Node review of {node_id}"
        else:
            task_id = subject.rsplit(":", 1)[-1].split("@", 1)[0]
            review_dir = self._reviews_dir() / task_id
            n = self._next_review_number(review_dir, kind, node=False)
            review_id = f"review-{task_id}-{kind}-{n}"
            title = title or f"{kind.capitalize()} review of {task_id}"

        path = review_dir / (f"node-{n}.md" if node_id is not None else f"{kind}-{n}.md")
        payload: dict[str, Any] = {
            "id": review_id,
            "title": title,
            "kind": kind,
            "subject": subject,
            "subject_ref": subject_ref,
            "engine": engine,
            "actor": actor or self._identity(),
            "run_dir": run_dir,
            "input_sha256": input_sha256,
            "output_sha256": output_sha256,
            "verdict": verdict,
            "reason": reason,
            "created_at": _now(),
            "disposed_at": "",
            "disposed_by": "",
            "summary": summary if summary is not None else f"{kind} review; engine {engine}; evidence under {run_dir}.",
            "disposition": "",
            "tags": ["workspace:desk"],
        }
        doc_access.create_doc(self.root, path, ReviewDoc, payload, review_id)
        return review_id, path

    # ------------------------------------------------------------------ record
    def record_receipt(
        self, task_id: str, kind: str, evidence: list[str], reason: str, operator: str | None = None
    ) -> dict[str, Any]:
        """A receipt the desk operator records without a model call (reproduction, goldens, owner,
        and preflight or bundle from operator evidence, always with ``engine: human``).

        Every ``evidence`` path must be an existing file inside the root; otherwise nothing is
        written. ``input_sha256`` hashes ``<path>\\n<content>\\n`` of each file, paths POSIX-relative
        to the root, sorted, without repeats (b1); empty without evidence. The verdict stays
        ``pending`` until ``deskops review dispose`` (r4).
        """
        if kind not in RECORD_KINDS:
            raise UsageError(
                f"--kind {kind} is not recorded by hand; use one of {', '.join(RECORD_KINDS)} "
                "(node comes from its own review command)"
            )
        if not (reason and reason.strip()):
            raise UsageError("--reason is required")
        operator = (operator or "").strip()
        if kind in HUMAN_REVIEW_KINDS and not operator:
            raise UsageError(
                f"--kind {kind} recorded by hand requires --operator <name>: the receipt names the "
                f"human who reviewed instead of a model ({NO_MODEL_REASON})"
            )
        paths: list[str] = []
        for raw in evidence:
            candidate = Path(raw)
            if not candidate.is_absolute():
                candidate = self.root / candidate
            resolved = candidate.resolve()
            if not resolved.is_relative_to(self.root) or not resolved.is_file():
                raise DomainError(f"evidence not found: {raw}")
            paths.append(resolved.relative_to(self.root).as_posix())
        paths = sorted(set(paths))
        if not paths and kind != "owner":
            raise UsageError(f"--kind {kind} requires at least one --evidence")

        task_path, task_id = self._resolve_task(task_id)
        subject = f"doc:{self._task_model(task_path)}:{task_id}"
        input_sha256 = ""
        if paths:
            data = b"".join(rel.encode() + b"\n" + (self.root / rel).read_bytes() + b"\n" for rel in paths)
            input_sha256 = _sha(data)
        actor = operator or self._identity()
        summary = f"{kind} receipt recorded by {actor}; evidence: {', '.join(paths) if paths else '(none)'}"
        title = None
        if kind in HUMAN_REVIEW_KINDS:
            summary = (
                f"{kind} receipt recorded by hand by operator {operator}, not by a model review "
                f"(engine human; {NO_MODEL_REASON}); evidence: {', '.join(paths)}"
            )
            title = f"{kind.capitalize()} receipt of {task_id} by operator {operator} ({NO_MODEL_REASON})"
        review_id, review_path = self._write_review(
            kind=kind,
            subject=subject,
            subject_ref="",
            engine="human",
            run_dir="",
            input_sha256=input_sha256,
            output_sha256="",
            verdict="pending",
            reason=reason,
            node_id=None,
            summary=summary,
            actor=actor,
            title=title,
        )
        return {
            "key": f"{task_id}/{kind}",
            "state": "recorded",
            "review_id": review_id,
            "review_path": review_path.relative_to(self.root).as_posix(),
            "evidence": paths,
            "input_sha256": input_sha256,
            "engine": "human",
            "operator": actor,
            "no_model_reason": NO_MODEL_REASON if kind in HUMAN_REVIEW_KINDS else "",
        }

    # ------------------------------------------------------------------ dispose
    def dispose(self, review_id: str, verdict: str, reason: str) -> dict[str, Any]:
        path = self._resolve_review_path(review_id)
        payload = doc_access.read_doc(path, ReviewDoc)
        if (payload.get("verdict") or "pending") != "pending":
            raise DomainError(f"Review '{review_id}' already has verdict '{payload.get('verdict')}'; only a pending review can be disposed.")
        payload["verdict"] = verdict
        payload["reason"] = reason
        payload["disposed_at"] = _now()
        payload["disposed_by"] = self._identity()
        payload["disposition"] = f"Verdict {verdict}: {reason}"
        doc_access.write_doc(self.root, path, ReviewDoc, payload)
        return {
            "review_id": review_id,
            "verdict": verdict,
            "reason": reason,
            "disposed_at": payload["disposed_at"],
            "disposed_by": payload["disposed_by"],
        }

    def _resolve_review_path(self, review_id: str) -> Path:
        reviews_dir = self._reviews_dir()
        matches: list[Path] = []
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                payload = extract_model_data(ReviewDoc, path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if payload.get("id") == review_id:
                matches.append(path)
        if not matches:
            raise DomainError(f"Review '{review_id}' not found under {reviews_dir}")
        if len(matches) > 1:
            names = ", ".join(str(path.relative_to(self.desk_root)) for path in matches)
            raise DomainError(f"Ambiguous review selector '{review_id}': {names}")
        return matches[0]

    # ------------------------------------------------------------------ status
    def _review_records(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        reviews_dir = self._reviews_dir()
        if not reviews_dir.exists():
            return records
        for path in sorted(reviews_dir.rglob("*.md")):
            try:
                records.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
            except Exception:
                continue
        return records

    def _state_for_key(self, key: str, input_data: bytes) -> dict[str, Any]:
        current_sha = _sha(input_data)
        records = [
            record
            for record in self._review_records()
            if self._record_key(record) == key
        ]
        pending = [record for record in records if record.get("verdict") == "pending"]
        if not records:
            return {"key": key, "state": "missing", "input_sha256": current_sha}
        if any(record.get("input_sha256") == current_sha for record in pending):
            return {"key": key, "state": "reviewed", "input_sha256": current_sha}
        if pending:
            return {"key": key, "state": "stale", "input_sha256": current_sha}
        return {"key": key, "state": "technical_failure", "input_sha256": current_sha}

    def _record_key(self, record: dict[str, Any]) -> str:
        subject = str(record.get("subject") or "")
        subject_ref = str(record.get("subject_ref") or "")
        kind = str(record.get("kind") or "")
        if subject:
            task_id = subject.rsplit(":", 1)[-1].split("@", 1)[0]
            return f"{task_id}/{kind}"
        if subject_ref:
            node_id = subject_ref.rsplit("#node:", 1)[-1]
            plan_path = subject_ref.split("#node:", 1)[0]
            plan_dir = Path(plan_path)
            if not plan_dir.is_absolute():
                plan_dir = self.root / plan_dir
            try:
                dag = yaml.safe_load((plan_dir / "dag.yaml").read_text(encoding="utf-8"))
                plan_id = dag["id"]
            except Exception:
                plan_id = plan_path.rsplit("/", 1)[-1]
            return f"{plan_id}/{node_id}"
        return f"unknown/{kind}"

    def status(self, target: str | None) -> list[dict[str, Any]]:
        if target:
            if self._is_plan_dir(target):
                return self._status_plan(target)
            return self._status_task(target)
        # No target: every key that has at least one ReviewDoc.
        keys: list[str] = []
        for record in self._review_records():
            key = self._record_key(record)
            if key not in keys and not key.startswith("unknown/"):
                keys.append(key)
        reports: list[dict[str, Any]] = []
        for key in keys:
            input_data = self._input_for_key(key)
            if input_data is None:
                reports.append({"key": key, "state": "missing", "input_sha256": ""})
            else:
                reports.append(self._state_for_key(key, input_data))
        return reports

    def _is_plan_dir(self, target: str) -> bool:
        plan_dir = Path(target)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        return (plan_dir / "dag.yaml").is_file()

    def _status_task(self, task_id: str) -> list[dict[str, Any]]:
        task_path, task_id = self._resolve_task(task_id)
        reports: list[dict[str, Any]] = []
        for mode, builder in (
            ("preflight", self._preflight_input),
            ("bundle", self._bundle_input),
        ):
            input_data, _, _ = builder(task_path, task_id)
            reports.append(self._state_for_key(f"{task_id}/{mode}", input_data))
        return reports

    def _status_plan(self, plan_dir_str: str) -> list[dict[str, Any]]:
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        reports: list[dict[str, Any]] = []
        for node_id in self._plan_nodes(dag):
            node = nodes[node_id]
            input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
            reports.append(self._state_for_key(f"{dag['id']}/{node_id}", input_data))
        return reports

    def _input_for_key(self, key: str) -> bytes | None:
        if "/preflight" in key or "/bundle" in key:
            task_id, _, mode = key.rpartition("/")
            if mode not in {"preflight", "bundle"}:
                return None
            try:
                task_path = self._task_path(task_id)
            except DomainError:
                return None
            builder = self._preflight_input if mode == "preflight" else self._bundle_input
            input_data, _, _ = builder(task_path, task_id)
            return input_data
        # node key <plan-id>/<NODE>
        parts = key.split("/", 1)
        if len(parts) != 2:
            return None
        plan_id, node_id = parts
        plan_dir = self._find_plan_dir(plan_id)
        if plan_dir is None:
            return None
        dag, nodes = self._load_dag(plan_dir)
        node = nodes.get(node_id)
        if node is None:
            return None
        input_data, _, _ = self._node_input(plan_dir, dag, nodes, node)
        return input_data

    # ------------------------------------------------------------------ public run
    def run_task(
        self,
        mode: str,
        task_id: str,
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> dict[str, Any]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        task_path, task_id = self._resolve_task(task_id)
        model = self._task_model(task_path)
        subject = f"doc:{model}:{task_id}"
        builder = self._preflight_input if mode == "preflight" else self._bundle_input
        input_data, sources, omitted = builder(task_path, task_id)
        return self._run_one(
            run_name=run_name,
            key=f"{task_id}/{mode}",
            input_data=input_data,
            sources=sources,
            omitted=omitted,
            engine_id=engine,
            max_attempts=max_attempts,
            force=force,
            reason=reason,
            timeout=timeout,
            kind=mode,
            subject=subject,
            subject_ref="",
            node_id=None,
        )

    def run_nodes(
        self,
        plan_dir_str: str,
        ids: list[str],
        *,
        run_name: str,
        engine: str,
        max_attempts: int,
        force: bool,
        reason: str,
        timeout: int,
    ) -> list[dict[str, Any]]:
        if force and not (reason and reason.strip()):
            raise UsageError("--force requires --reason (recorded in manifest.json and the ReviewDoc)")
        plan_dir = Path(plan_dir_str)
        if not plan_dir.is_absolute():
            plan_dir = self.root / plan_dir
        dag, nodes = self._load_dag(plan_dir)
        plan_rel = plan_dir.relative_to(self.root).as_posix()
        selected = ids or self._plan_nodes(dag)
        reports: list[dict[str, Any]] = []
        for node_id in selected:
            if node_id not in nodes:
                raise DomainError(f"Unknown node '{node_id}' in {plan_dir / 'dag.yaml'}")
            node = nodes[node_id]
            input_data, sources, omitted = self._node_input(plan_dir, dag, nodes, node)
            reports.append(
                self._run_one(
                    run_name=run_name,
                    key=f"{dag['id']}/{node_id}",
                    input_data=input_data,
                    sources=sources,
                    omitted=omitted,
                    engine_id=engine,
                    max_attempts=max_attempts,
                    force=force,
                    reason=reason,
                    timeout=timeout,
                    kind="node",
                    subject="",
                    subject_ref=f"{plan_rel}/dag.yaml#node:{node_id}",
                    node_id=node_id,
                    plan_id=dag["id"],
                )
            )
        return reports


FILE:tests/test_review_command.py
"""GC03: ``deskops review`` — cold context reviews and their disposition.

Each test runs in a temporary desk with a fake ``pi`` executable placed first on
``PATH``. The fake prints a ``REFORMULACION`` section (or fails) and counts its
invocations, so no test ever calls the real model or touches the network.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from sldb.runtime.validation import extract_model_data

from deskops.models import ReviewDoc


ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, "-m", "deskops"]
PLAN_SRC = ROOT / "desk" / "drawer" / "plans" / "gates-por-tipo"


FAKE_PI = """#!/usr/bin/env python3
import os
import sys
import time

log = os.environ.get("FAKE_PI_LOG")
if log:
    with open(log, "a", encoding="utf-8") as handle:
        handle.write(" ".join(sys.argv[1:]) + "\\n")

mode = os.environ.get("FAKE_PI_MODE", "ok")
if mode == "fail":
    sys.exit(1)
if mode == "no-reformulacion":
    print("sin seccion")
    sys.exit(0)
if mode == "sleep":
    time.sleep(5)
    print("REFORMULACION\\nDRY-RUN: nada.")
    sys.exit(0)
print(
    "REFORMULACION\\n"
    "Propósito: revisar el encargo.\\n"
    "AMBIGUEDADES: ninguna.\\n"
    "DRY-RUN: leer, proponer, validar, sin ejecutar.\\n"
    "FUTURO: otro nodo o un humano."
)
sys.exit(0)
"""


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return env


def _run(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*argv], cwd=root, env=env or _env(), capture_output=True, text=True)


def _deskops(root: Path, *argv: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return _run(root, *CLI, *argv, "--root", str(root), env=env)


@pytest.fixture
def fake_pi(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    pi = bin_dir / "pi"
    pi.write_text(FAKE_PI, encoding="utf-8")
    pi.chmod(0o755)
    log = tmp_path / "pi.log"
    monkeypatch.setenv("FAKE_PI_LOG", str(log))
    monkeypatch.setenv("FAKE_PI_MODE", "ok")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    return bin_dir, log


def _pi_calls(log: Path) -> int:
    if not log.exists():
        return 0
    return len([line for line in log.read_text(encoding="utf-8").splitlines() if line.strip()])


def _add_task(root: Path, *, title: str = "X", task_type: str = "task.code") -> str:
    result = _deskops(
        root,
        "add",
        "task",
        "--title",
        title,
        "--goal",
        "review goal",
        "--scope",
        "review scope",
        "--validation",
        "pytest",
        "--task-type",
        task_type,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return f"task-{title.lower().replace(' ', '-')}"


def _attempt_dirs(root: Path, key: str) -> list[Path]:
    base = root / "runs" / "subagents"
    if not base.exists():
        return []
    return sorted(base.glob(f"*/context-review/{key}/*/attempt-*"))


def _review_docs(root: Path) -> list[dict]:
    reviews = root / "desk" / "reviews"
    if not reviews.exists():
        return []
    docs: list[dict] = []
    for path in sorted(reviews.rglob("*.md")):
        docs.append(extract_model_data(ReviewDoc, path.read_text(encoding="utf-8")))
    return docs


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_preflight_writes_attempt_evidence_and_receipt(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 1
    attempt = attempts[0]
    assert attempt.name == "attempt-1"
    for name in ("input.md", "manifest.json", "output.md", "stderr.log", "receipt.json"):
        assert (attempt / name).is_file(), name

    input_bytes = (attempt / "input.md").read_bytes()
    assert input_bytes.decode().startswith("FILE:desk/tasks/task-x.md\n")

    manifest = _json(attempt / "manifest.json")
    assert manifest["input_sha256"] == __import__("hashlib").sha256(input_bytes).hexdigest()
    assert manifest["sources"][0]["path"] == "desk/tasks/task-x.md"
    assert manifest["argv"][0] == "pi"
    assert manifest["argv"][-1].startswith("@")

    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is True
    assert receipt["returncode"] == 0
    assert receipt["input_sha256"] == manifest["input_sha256"]

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "pending"
    assert doc["subject"] == "doc:TaskCodeDoc:task-x"
    assert doc["run_dir"] == attempt.relative_to(root).as_posix()
    assert doc["input_sha256"] == manifest["input_sha256"]
    assert doc["output_sha256"] == receipt["output_sha256"]


def test_unchanged_second_run_is_reviewed_and_does_not_call_the_model(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    calls_after_first = _pi_calls(_log)
    assert calls_after_first == 1

    second = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert second.returncode == 0, second.stdout + second.stderr
    assert "unchanged" in second.stdout
    assert _pi_calls(_log) == calls_after_first
    assert len(_attempt_dirs(root, "task-x/preflight")) == 1

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    assert status.returncode == 0, status.stdout + status.stderr
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "reviewed"


def test_edited_goal_is_stale_and_next_run_uses_a_new_sha(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    first_sha = _attempt_dirs(root, "task-x/preflight")[0].parent.name

    edit = _deskops(root, "edit", "task", "task-x", "goal", "goal changed")
    assert edit.returncode == 0, edit.stdout + edit.stderr

    status = _deskops(root, "review", "status", "task-x", "--format", "json")
    payload = json.loads(status.stdout)
    preflight = next(item for item in payload if item["key"] == "task-x/preflight")
    assert preflight["state"] == "stale"

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    new_shas = {attempt.parent.name for attempt in attempts}
    assert first_sha in new_shas
    assert len(new_shas) == 2


def test_bundle_includes_rituals_pills_and_files_in_order(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    pill = _deskops(
        root,
        "add",
        "pill",
        "--title",
        "Guardrail",
        "--what",
        "keep layers clean",
        "--why",
        "safety",
        "--when",
        "always",
        "--where",
        "desk",
        "--how",
        "read first",
        "--how-not",
        "skip it",
    )
    assert pill.returncode == 0, pill.stdout + pill.stderr
    assert _deskops(root, "bind", "pill", "task-x", "pill-guardrail").returncode == 0

    doc = root / "docs" / "foo.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text("# Foo\nsmall file\n", encoding="utf-8")
    edit = _deskops(root, "edit", "task", "task-x", "files", '["docs/foo.md"]')
    assert edit.returncode == 0, edit.stdout + edit.stderr

    assert _deskops(root, "review", "bundle", "task-x", "--run", "test-run").returncode == 0

    attempt = _attempt_dirs(root, "task-x/bundle")[0]
    input_text = (attempt / "input.md").read_text(encoding="utf-8")
    file_headers = [line for line in input_text.splitlines() if line.startswith("FILE:")]
    assert file_headers[0] == "FILE:desk/tasks/task-x.md"
    assert "FILE:desk/rituals/phase.md" in file_headers
    assert "FILE:desk/rituals/execution.md" in file_headers
    assert "FILE:desk/rituals/testing.md" in file_headers
    assert "FILE:desk/rituals/closeout.md" in file_headers
    assert "FILE:desk/contexts/pill-guardrail.md" in file_headers
    assert "FILE:docs/foo.md" in file_headers
    assert file_headers[-1] == "FILE:instruccion"

    # Order: task, rituals, pill, file, instruction.
    ordered = [
        "FILE:desk/tasks/task-x.md",
        "FILE:desk/rituals/phase.md",
        "FILE:desk/rituals/execution.md",
        "FILE:desk/rituals/testing.md",
        "FILE:desk/rituals/closeout.md",
        "FILE:desk/contexts/pill-guardrail.md",
        "FILE:docs/foo.md",
        "FILE:instruccion",
    ]
    assert file_headers == ordered


def test_node_writes_one_review_doc_per_node(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)

    result = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    node_docs = [doc for doc in _review_docs(root) if doc["kind"] == "node"]
    node_ids = [doc["id"] for doc in node_docs]
    assert "review-deskops-gates-por-tipo-gc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-pc01-node-1" in node_ids
    assert "review-deskops-gates-por-tipo-root-node-1" in node_ids
    for doc in node_docs:
        assert doc["subject"] == ""
        assert doc["subject_ref"].startswith("desk/drawer/plans/gates-por-tipo/dag.yaml#node:")
        assert doc["verdict"] == "pending"


def test_dispose_writes_the_verdict_and_a_second_dispose_fails(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0

    disposed = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "accepted",
        "--reason",
        "looks right",
    )
    assert disposed.returncode == 0, disposed.stdout + disposed.stderr

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    doc = docs[0]
    assert doc["verdict"] == "accepted"
    assert doc["reason"] == "looks right"
    assert doc["disposed_at"]
    assert doc["disposed_by"]

    again = _deskops(
        root,
        "review",
        "dispose",
        "review-task-x-preflight-1",
        "--verdict",
        "rejected",
        "--reason",
        "changed my mind",
    )
    assert again.returncode == 1
    assert "already has verdict" in again.stdout


def test_third_good_attempt_on_the_same_key_fails_without_force(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path]
) -> None:
    root = lifecycle_desk
    plan_dir = root / "desk" / "drawer" / "plans" / "gates-por-tipo"
    shutil.copytree(PLAN_SRC, plan_dir)
    brief = plan_dir / "brief.md"
    log = fake_pi[1]

    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change one\n", encoding="utf-8")
    assert _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r").returncode == 0
    assert _pi_calls(log) == 2

    brief.write_text(brief.read_text(encoding="utf-8") + "\n# change two\n", encoding="utf-8")
    third = _deskops(root, "review", "node", "desk/drawer/plans/gates-por-tipo", "GC01", "--run", "r")
    assert third.returncode == 1
    assert "tope --max-attempts" in third.stdout
    assert _pi_calls(log) == 2


def test_transport_failure_leaves_technical_failure_and_incomplete(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "fail")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    receipt = _json(attempt / "receipt.json")
    assert receipt["technical_ok"] is False
    assert receipt["returncode"] == 1

    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert len(docs) == 1
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_output_without_reformulacion_is_a_transport_failure(
    lifecycle_desk: Path, fake_pi: tuple[Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")
    monkeypatch.setenv("FAKE_PI_MODE", "no-reformulacion")

    result = _deskops(root, "review", "preflight", "task-x", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr

    attempt = _attempt_dirs(root, "task-x/preflight")[0]
    assert _json(attempt / "receipt.json")["technical_ok"] is False
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-1"]
    assert docs[0]["verdict"] == "incomplete"
    assert docs[0]["reason"] == "technical"


def test_force_requires_reason(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    _add_task(root, title="X")

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--run", "test-run")
    assert result.returncode == 2
    assert "--force requires --reason" in result.stdout


def test_force_with_reason_retries_the_same_input(lifecycle_desk: Path, fake_pi: tuple[Path, Path]) -> None:
    root = lifecycle_desk
    log = fake_pi[1]
    _add_task(root, title="X")

    assert _deskops(root, "review", "preflight", "task-x", "--run", "test-run").returncode == 0
    assert _pi_calls(log) == 1

    result = _deskops(root, "review", "preflight", "task-x", "--force", "--reason", "again", "--run", "test-run")
    assert result.returncode == 0, result.stdout + result.stderr
    assert _pi_calls(log) == 2

    attempts = _attempt_dirs(root, "task-x/preflight")
    assert len(attempts) == 2
    manifest = _json(attempts[1] / "manifest.json")
    assert manifest["retry_reason"] == "again"
    docs = [doc for doc in _review_docs(root) if doc["id"] == "review-task-x-preflight-2"]
    assert len(docs) == 1
    assert docs[0]["reason"] == "again"


def test_init_and_desk_update_seed_the_deepseek_flash_profile_idempotently(
    tmp_path: Path,
) -> None:
    from deskops.cli.main import main

    root = tmp_path / "repo"
    root.mkdir()
    assert main(["init", str(root)]) == 0

    profile = root / "desk" / "runtimes" / "runtime-pi-deepseek-flash.md"
    assert profile.is_file()
    first = profile.read_text(encoding="utf-8")

    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == first

    # An existing profile is never overwritten.
    profile.write_text("# my own profile\n", encoding="utf-8")
    assert main(["desk", "update", "--apply", "--root", str(root)]) == 0
    assert profile.read_text(encoding="utf-8") == "# my own profile\n"
