FILE:desk/tasks/task-scion-autonomy-coordinator-contract.md
---
sldb:
  by: agent
  at: '2026-11-10T14:46:35Z'
  authority: generated
  via: update_document
id: task-scion-autonomy-coordinator-contract
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- e58ee061
- tests/test_scion_runtime.py
depends_on:
- task-scion-autonomy-review-status
pills: []
files:
- deskops/runtime/scion.py
- deskops/cli/registry.py
- deskops/cli/commands/runtime.py
- desk/roles/deskops-supervisor.md
- desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
- tests/test_scion_runtime.py
- tests/fixtures/golden/help
- docs/operator-manual.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-scion-autonomy-coordinator-contract.md
---

# Scion autonomy: consistent coordinator and tester contract

## Rationale

_Explain why this task exists or the business driver behind it._

Not provided.

## Goal

_Describe the concrete result this task must produce._

One coherent source contract makes Scion coordinator recover configured current state, progress routine authorized work, select reviewed ready unowned tasks, dispatch fresh executor/tester and reconcile closeout before continuing.

## Scope

_State what is in scope and what is out of scope._

Role source, generated Scion modes/prompts and command examples, explicit runtime context and durable atoms/docs. No replacement lifecycle engine, automatic policy decisions, pi-subagents or unrelated CC tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Source contract: correct RoleDoc via SLDB, permitting modeled workflow CLI mutations but no implementation by supervisor. Ordinary implementation questions answered from task/source evidence; escalate only unresolved owner decisions, actual ownership conflicts or external credentials/permissions. Never rerun an accepted review with unchanged input; bound technical retries and report precise blockers instead of broad diagnostic loops. Add optional --context-file JSON to existing runtime template command (and matching generator context kwarg); context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project. Emit DESKOPS_DESK_ROOT, DESKOPS_SOURCE_ROOT, DESKOPS_SLDB_SOURCE_ROOT, DESKOPS_WORKSPACE_ROOT, DESKOPS_SCION_PROJECT and PYTHONPATH plus a supported volume source=workspace_root target=workspace_root. No secrets in context. Preserve no-context behavior. Include tester mode in existing --mode choices, auto-detect tester RoleDoc, and separate tester scope/completion instructions. Coordinator recovers this configured current desk/tools, checks canonical/dirty state, board DAG/review gates and existing ownership (labels/RunDoc/worktrees), skips blocked/owned tasks, selects one reviewed ready leaf. Deterministic task+contract-derived agent names and task/role labels: write run intent BEFORE start and reconcile existing matching Scion child before any new start; duplicate-name protection stays Scion native, not a new scheduler/registry. Explicit --project, --workspace, --type, --harness-auth api-key, --non-interactive and correct subcommand --root flags in examples. Executor -> independent tester -> coordinator validates evidence -> deskops closeout -> reconcile phase -> recover/select again. Failed tester cannot close; request bounded correction and fresh test. Waiting-for-child uses Scion blocked/completion notifications (already subscribed); only real human decisions ask_user. Capture source atom before operator docs, generate from source, test YAML/modes/context and actual command examples; runtime task supplies hooks/bootstrap and unattended integration. Concrete interface choices: project is a nonempty Scion slug or UUID (not a filesystem path); mode literal is tester. Context JSON requires all five named keys; reject missing/unknown/invalid/relative/out-of-workspace paths before generation, no partial defaults; omitted --context-file preserves existing behavior. sldb_root already names its src directory. PYTHONPATH is source_root + os.pathsep + sldb_root, without inherited stale paths. Existing role model preferences never override explicit configured harness/model alias. Bound technical retries to 2 per unchanged input and implementation correction/test cycles to 2 per task contract; if still failing persist exact blocker, do not ask owner for facts already in sources. Run intent is the existing RunDoc with in_progress outcome in the assigned run_dir, explicitly intent not proof of start. Deterministic child identity: role-specific prefix deskops-e or deskops-t plus first 12 hex of SHA256(task_id + NUL + contract_sha256 + NUL + role); labels deskops.task_id, deskops.contract_sha256, deskops.role. Reconcile exact project+name+labels and RunDoc before start; conflicting ownership blocks that task only. Matching running child is observed, stopped child resumed, completed child reviewed; never launch duplicate. Independent testers use role-deskops-tester/--mode tester and a distinct role identity. Scope also includes deskops/cli/commands/runtime.py to load/pass context-file; test helpers may be added in runtime/scion.py but no replacement scheduler or lifecycle engine.

## Validation

_List the checks required before this task can close._

- pytest tests/test_scion_runtime.py
- affected CLI help/output goldens if tester mode adds a choice
- real unattended coordinator -> executor -> independent tester -> closeout/continue integration

## Done When

_Name the observable condition that makes the task complete._

No source/installed instruction contradiction; tester materialization correct; routine questions not blanket ask_user; dispatch checks readiness/ownership and restart identity. Focused tests pass and live integrated experiment demonstrates the loop without parent prompts.


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


FILE:desk/drawer/tasks/task-scion-autonomy-coordinator-contract.md
# Scion autonomy: consistent coordinator/executor/tester contract

Owner authorization 2026-11-10: make the system recover a current desk, choose an
authorized ready unowned task, review it, dispatch, independently test, close and
continue without handholding. Scion owns runtime; DeskOps owns task gates. No
pi-subagents or second runtime scheduler.

Fix the source RoleDoc and generated Scion instructions, not only installed files.
Resolve the conflict between read-only bash and workflow mutation/closeout duties.
Permit routine clarifications from task/source evidence; escalate only unresolved
owner decisions, conflicting authorization or actual ownership conflicts.
Read configured current desk and tool source, use exact CLI syntax and explicit
project/auth/workspace when dispatching. Check current review/dependency/phase
gates and ownership before dispatch; skip blocked/owned tasks and consider the
remaining ready ones. Persist/reconcile stable run identity before dispatch so a
restart does not create a duplicate. Require separate tester and explicit failed
validation recovery. Finish the current phase gate before selecting another.

Bounded deliverable: coherent role/template contract, including tester templates
and executable command examples. Do not replace the lifecycle engine or introduce
a broad new framework. Code enforcement beyond existing gates must be explicit,
not claimed from prose tests. Capture durable rules in atoms before docs.

Files: deskops/runtime/scion.py, deskops/cli/registry.py if tester mode requires it,
desk/roles/deskops-supervisor.md, relevant new atom(s), tests/test_scion_runtime.py,
relevant CLI help golden if needed, docs/operator-manual.md, CHANGELOG.md.
Validation: focused template/runtime tests and real unattended integration after
the runtime bridge is installed. Depends on review-status correction.


FILE:desk/roles/deskops-supervisor.md
---
id: role-deskops-supervisor
name: deskops-supervisor
description: Use when acting as the desk workflow supervisor in this repository. Recover
  state from Board.md, choose or confirm the active task, dispatch bounded execution,
  inspect evidence, update routing truthfully, and enforce commit-boundary closeout.
kind: pi
model: anthropic/claude-opus-4-8
fallback_models:
- openai-codex/gpt-5.4
tools:
- read
- grep
- find
- ls
- bash
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Workflow Supervisor

Use this skill when your role is **supervisor**.

## Non-negotiables

- The real board is `desk/tasks/Board.md` with selector `Board`.
- Supervisor routes and reviews; it should not silently become the executor.
- Keep routing truthful.
- Require evidence, validation, and a commit boundary before retirement.

## Model binding

- anthropic/claude-opus-4-8 (canonical; routing and review need long context and reliable instruction-following). Fallback: openai-codex/gpt-5.4.

## Hard boundaries (tool-enforced)

- Installed agent runs with tool allowlist `read, grep, find, ls, bash`; no `edit`/`write`.
- `bash` is for read-side CLI only: `deskops`, `sldb`, `git status/log/diff`, `pytest`. Never edit files through shell redirection or scripts.
- Review happens on the evidence surface: `runs/subagents/<run-dir>/`.

## Recovery

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

## Supervisor duties

- recover active board state
- choose or confirm the active task
- verify scope, files, references, and pills
- dispatch one bounded executor lane when implementation is needed
- inspect run evidence and validation evidence
- update board state truthfully
- enforce commit-boundary closeout

## Role lock check

Before any action that looks like implementation, ask:

1. Am I still acting as supervisor?
2. Is this implementation work for an active task?
3. Should this be done by an executor lane instead?

If yes, dispatch instead of implementing inline.

## Dispatch guidance

Prefer bounded execution with explicit instructions such as:

- recover board and task state first
- operate only within task scope
- persist run evidence under `runs/subagents/`
- run the smallest relevant validation first
- do not self-retire the task

## Evidence expectations

Inspect at least:

- `board.txt`
- `task.txt`
- `next.txt`
- `graph.txt`
- `git-status.txt`
- `result-summary.md` with `run_id`, child `session` path, and `session_sha256`
- `validation.log` when applicable

A green exit code alone is not enough.

## Closeout checklist

Do not retire unless all are true:

- implementation exists
- relevant tests pass
- graph is clean or understood
- board state is correct
- evidence exists on disk
- the closing commit was created via `deskops closeout commit` (trailers present, `index.jsonl` updated)

## Anti-patterns

Do not:

- implement active-task changes inline while claiming to be supervisor
- accept missing validation evidence
- leave stale routing on the board
- retire work without the final commit gate


FILE:desk/roles/deskops-tester.md
---
id: role-deskops-tester
name: deskops-tester
description: Use when acting as the tester for one bounded deskops task in this repository.
  Recover board and task state, verify the execution handoff, translate task and pill
  guardrails into concrete checks, run the smallest relevant validation first, and
  hand off to closeout without changing routing or implementation scope.
kind: pi
model: openrouter/nvidia/nemotron-3-super-120b-a12b:free
fallback_models:
- openrouter/openai/gpt-oss-20b:free
tools:
- read
- grep
- find
- ls
- bash
system_prompt_mode: replace
inherit_project_context: true
inherit_skills: true
default_context: fresh
---

# Workflow Tester

Use this skill when your role is **tester**.

## Non-negotiables

- Test one bounded task only.
- Recover board and task state before validation.
- Confirm the execution handoff names the intended contract, touched surfaces, and guardrails to prove.
- Run the smallest relevant validation first.
- Do not silently expand into implementation or closeout work.
- Persist validation evidence on disk for non-trivial work.

## Model binding

- Primary: `openrouter/nvidia/nemotron-3-super-120b-a12b:free`.
- Fallback: `openrouter/openai/gpt-oss-20b:free`.
- Free models are deliberately used here; if quality proves insufficient, revisit the binding rather than silently inheriting the default model.

## Hard boundaries (tool-enforced)

- Installed agent runs with tool allowlist `read, grep, find, ls, bash`; no `edit`/`write`.
- `bash` is for `deskops`, `sldb`, `git status/log/diff`, and `pytest` only.
- Never fix failing code or author tests. Report missing/stale tests and failures in `result-summary.md` and hand back to the executor; test authorship belongs to the executor.
- Annotations go to `runs/subagents/<run-dir>-testing/`. Do not hand off in chat only.

## Recovery

```bash
deskops show board Board --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

Read as needed:

- `AGENTS.md`
- `desk/rituals/testing.md`
- `desk/rituals/closeout.md`
- `.opencode/skills/use-deskops/SKILL.md`
- `.opencode/skills/use-sldb/SKILL.md` when tracked structured docs or models are involved

## Tester duties

- confirm the incoming contract and guardrails
- inspect whether existing tests are stale or encode obsolete behavior
- translate pills and task constraints into assertions, especially failure cases
- run focused validation first, then broaden only if shared behavior changed
- record evidence for handoff to closeout

## Evidence snapshot pattern

```bash
TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="runs/subagents/$TS-<task-id>-testing"
mkdir -p "$RUN_DIR"

deskops show board Board --root . > "$RUN_DIR/board.txt"
deskops show task <task-id> --root . > "$RUN_DIR/task.txt"
deskops next <task-id> --root . > "$RUN_DIR/next.txt"
deskops graph missing --root . > "$RUN_DIR/graph.txt"
git status --short --branch > "$RUN_DIR/git-status.txt"
```

Save validation output, for example:

```bash
pytest tests/<targeted-scope> -q | tee "$RUN_DIR/validation.log"
```

## Validation discipline

Default order:

1. task-specific or narrowly targeted tests
2. boundary or negative tests implied by `how_not`
3. broader shared validation only when the change affects shared behavior

Examples:

```bash
pytest tests/<targeted-scope> -q
pytest
sldb stores check --store .sldb
```

## Required outputs

- `board.txt`
- `task.txt`
- `next.txt`
- `graph.txt`
- `git-status.txt`
- `validation.log` when validation was run
- `result-summary.md` with `run_id`, child `session` path, and `session_sha256`

## Handoff contract

The result summary should state at least:

- task id
- role = tester
- run id, session path, and session sha256
- validations run
- pass/fail status
- guardrails proven
- stale or missing tests found
- follow-up needed before closeout

## Anti-patterns

Do not:

- treat stale tests as proof
- skip negative or boundary cases just to get green output
- mutate board routing from the testing lane
- self-retire the task
- perform unrelated implementation while claiming to test


FILE:deskops/runtime/scion.py
"""Project a RoleDoc + its RuntimeProfileDoc onto a Scion agent template.

Scion (github.com/GoogleCloudPlatform/scion) launches an agent from a
*template* directory: ``scion-agent.yaml`` plus the prose files it points at
(``system-prompt.md``, ``agents.md``). A template describes the job, never the
environment: the harness-config decides image, auth and concrete model, and
the template only carries a portable model *size alias*.

This module is the Scion counterpart of ``materializers.roles`` (pi agent
files): the RoleDoc stays the tracked source and the template is a
materialization. Pure except for the two writers at the bottom; it never
calls ``scion``. Dispatch (``scion start``) is the supervisor's gesture.

Nothing is dropped silently: every RoleDoc setting the template cannot carry
is written into ``scion-agent.yaml`` as a comment that names the setting and
why it was left out.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re
from typing import Any

from deskops import doc_access
from deskops.materializers.roles import iter_role_doc_paths, load_role_doc
from deskops.materializers.runtime_profiles import build_agent_spec_args, load_runtime_profiles
from deskops.models import RunDoc

#: RuntimeProfileDoc.kind -> Scion harness-config name. Only ``claude`` and
#: ``gemini`` ship installed; the rest need ``scion harness-config install``
#: (``pi`` needs a bundle of our own; see the scion fork's desk).
HARNESS_BY_KIND: dict[str, str] = {
    "claude": "claude",
    "codex": "codex",
    "antigravity": "antigravity",
    "gemini": "gemini",
    "opencode": "opencode",
    "pi": "pi",
}

#: Scion's portable model size aliases (``local/templates.md``).
MODEL_SIZE_ALIASES: tuple[str, ...] = ("small", "medium", "large", "extra-large")

#: ``medium`` by default: the owner's rule is that subagents never run on the
#: largest tier. Pass ``model_alias`` to change it per template.
DEFAULT_MODEL_ALIAS = "medium"
DEFAULT_MAX_TURNS = 200
DEFAULT_MAX_DURATION = "2h"
#: A coordinator waits blocked on its children and Scion counts that idle time,
#: so the executor's limit would kill it mid-review.
COORDINATOR_MAX_TURNS = 1000
COORDINATOR_MAX_DURATION = "24h"

#: Without this the Hub picks whichever credential it finds; a stale
#: ``CLAUDE_AUTH`` file beats a project token and the agent is not logged in.
HARNESS_AUTH: dict[str, str] = {"claude": "oauth-token"}

TEMPLATE_FILES: tuple[str, ...] = ("scion-agent.yaml", "system-prompt.md", "agents.md")


def pick_harness_config(runtime_kind: str) -> str:
    """Scion harness-config name for a RuntimeProfileDoc kind."""
    try:
        return HARNESS_BY_KIND[runtime_kind]
    except KeyError as exc:
        known = ", ".join(sorted(HARNESS_BY_KIND))
        raise ValueError(f"no Scion harness-config is known for runtime kind '{runtime_kind}' (known: {known})") from exc


def find_role_doc(root: Path, role_id: str) -> tuple[Path, dict[str, Any]]:
    """Locate a tracked RoleDoc by ``id`` or ``name`` (``role-x`` and ``x`` both resolve)."""
    wanted = {role_id, f"role-{role_id}"}
    for path in iter_role_doc_paths(root):
        role_doc = load_role_doc(path)
        if role_doc.get("id") in wanted or role_doc.get("name") in wanted:
            return path, role_doc
    raise ValueError(f"no RoleDoc with id or name '{role_id}' under {root / 'desk' / 'roles'}")


def template_dir_for(root: Path, role_doc: dict[str, Any], out_dir: Path | None = None) -> Path:
    """Default destination: ``<root>/.scion/templates/<role-name>/`` (a Scion project template)."""
    if out_dir is not None:
        return out_dir
    name = str(role_doc.get("name") or role_doc.get("id") or "").strip()
    if not name:
        raise ValueError("Role doc is missing a name")
    return root / ".scion" / "templates" / name


def _yaml_scalar(value: Any) -> str:
    """One-line YAML for a scalar or list: JSON is a YAML subset, and it never wraps."""
    return json.dumps(value, ensure_ascii=False)


def _command_args(role_doc: dict[str, Any], profile: dict[str, Any]) -> list[str]:
    """Role settings that only exist as CLI flags (today: ``tools``).

    Model and system prompt have template fields of their own, the session is
    Scion's, and the profile's ``extra_args`` describe a non-interactive
    invocation (``--print``) that Scion must not inherit. What is left is the
    tools vocabulary, folded through the profile's own flag.
    """
    stripped = dict(profile)
    stripped.update(model_flag="", fallback_models_flag="", system_prompt_flag="", session_flag="", extra_args=[])
    return list(build_agent_spec_args(role_doc, stripped))


def scion_template_files(
    role_doc: dict[str, Any],
    profile: dict[str, Any],
    *,
    harness: str,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    source: str | None = None,
    mode: str | None = None,
) -> dict[str, str]:
    """Render the three template files as ``{filename: text}``.

    ``source`` is a human-readable provenance line (role path + runtime path)
    written at the top of ``scion-agent.yaml``. ``mode`` picks the
    ``agents.md``: ``executor`` (one bounded task) or ``coordinator`` (owns a
    desk); by default a role whose name says supervisor/coordinator gets the
    coordinator instructions.
    """
    if mode not in (None, "executor", "coordinator"):
        raise ValueError(f"mode must be executor or coordinator, got '{mode}'")
    if model_alias not in MODEL_SIZE_ALIASES:
        raise ValueError(f"model alias must be one of {MODEL_SIZE_ALIASES}, got '{model_alias}'")
    if harness not in HARNESS_BY_KIND.values():
        raise ValueError(f"unknown Scion harness-config '{harness}' (known: {', '.join(sorted(set(HARNESS_BY_KIND.values())))})")

    role_name = str(role_doc.get("name") or role_doc.get("id") or "role")
    resolved_mode = mode or ("coordinator" if "supervisor" in role_name or "coordinator" in role_name else "executor")
    description = str(role_doc.get("description") or "").strip()
    body = str(role_doc.get("body") or "").strip()
    unsupported = set(profile.get("unsupported_role_fields") or [])

    lines: list[str] = []
    lines.append(f"# Generated by `deskops runtime template {role_doc.get('id') or role_name} --harness {harness}`.")
    if source:
        lines.append(f"# Source: {source}")
    lines.append("# Edit the RoleDoc / RuntimeProfileDoc and regenerate; do not edit this file by hand.")
    lines.append('schema_version: "1"')
    lines.append(f"description: {_yaml_scalar(description or role_name)}")
    lines.append("agent_instructions: agents.md")
    lines.append("system_prompt: system-prompt.md")
    lines.append(f"default_harness_config: {harness}")

    concrete_model = role_doc.get("model")
    if concrete_model:
        lines.append(
            f"# RoleDoc.model is {_yaml_scalar(concrete_model)}. A template carries a portable size alias; "
            f"the harness-config '{harness}' resolves it to a concrete model (Scion local/templates.md)."
        )
    lines.append(f"model: {model_alias}")
    if harness in HARNESS_AUTH:
        lines.append(f"auth_selectedType: {HARNESS_AUTH[harness]}")
    coordinator = resolved_mode == "coordinator"
    lines.append(f"max_turns: {COORDINATOR_MAX_TURNS if coordinator else DEFAULT_MAX_TURNS}")
    lines.append(f"max_duration: {COORDINATOR_MAX_DURATION if coordinator else DEFAULT_MAX_DURATION}")

    command_args = _command_args(role_doc, profile)
    if command_args:
        lines.append("# RoleDoc.tools, folded through the runtime profile's tools flag:")
        lines.append(f"command_args: {_yaml_scalar(command_args)}")

    omitted: list[str] = []
    fallback_models = role_doc.get("fallback_models") or []
    if fallback_models:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "fallback_models" in unsupported
            else "a Scion template has no field for it"
        )
        omitted.append(f"fallback_models: {_yaml_scalar(list(fallback_models))}  ({reason})")
    tools = role_doc.get("tools") or []
    if tools and not command_args:
        reason = (
            f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' lists it in unsupported_role_fields"
            if "tools" in unsupported
            else f"RuntimeProfileDoc '{profile.get('id') or profile.get('kind')}' declares no tools_flag"
        )
        omitted.append(f"tools: {_yaml_scalar(list(tools))}  ({reason})")
    for key in ("system_prompt_mode", "inherit_project_context", "inherit_skills", "default_context"):
        if key in role_doc and role_doc.get(key) not in (None, ""):
            omitted.append(f"{key}: {_yaml_scalar(role_doc[key])}  (pi agent setting; Scion templates have no equivalent)")
    if omitted:
        lines.append("# Omitted on purpose (nothing is dropped silently):")
        lines.extend(f"#   {item}" for item in omitted)

    agent_yaml = "\n".join(lines) + "\n"
    system_prompt = (body or f"# {role_name}") + "\n"
    if resolved_mode == "coordinator":
        agents_md = _render_coordinator_agents_md(role_name, harness, task_repo)
    else:
        agents_md = _render_agents_md(role_name, harness, task_repo)
    return {"scion-agent.yaml": agent_yaml, "system-prompt.md": system_prompt, "agents.md": agents_md}


def _render_coordinator_agents_md(role_name: str, harness: str, task_repo: str | None) -> str:
    """Instructions for the long-lived agent that owns one desk.

    One coordinator per desk is the shape the owner chose (2026-10-29): it is
    the only writer of that ``desk/``, it dispatches short-lived executors
    through ``scion start``, waits blocked, reviews their evidence and closes.
    What needs the owner is never decided here.
    """
    repo = task_repo or "<repo>"
    return (
        f"# {role_name}: coordinator of the `{repo}` desk on Scion ({harness})\n"
        "\n"
        "You are the long-lived coordinator of ONE desk. The desk, not your memory, holds the state; every time you\n"
        "wake up, read it again. You are the only agent that writes `/workspace/" + repo + "/desk/`.\n"
        "\n"
        "## Each time you wake up\n"
        "\n"
        "```bash\n"
        f"cd /workspace/{repo}\n"
        "deskops show board Board --root .          # active tasks and their nodes\n"
        "deskops message list --root .              # inbox: incoming notes\n"
        "scion list                                 # executors you already dispatched\n"
        "git status --short --branch\n"
        "```\n"
        "\n"
        "## What you do\n"
        "\n"
        "1. **Triage the inbox.** Informational or duplicate -> `deskops message ack`. Bounded work for this repo ->\n"
        "   `deskops promote inbox-to-drawer-task`, then `deskops add task --from-drawer ...` when it is next.\n"
        "   Work for another repo -> `deskops message send --to <repo>`. A decision only the owner can make ->\n"
        "   leave the note open and say so with `sciontool status ask_user \"<the question>\"`.\n"
        "2. **Dispatch one executor per active task that has none.** Build the prompt from `deskops show task <id>`:\n"
        "   the task id, the repo, what to verify or implement, the validation command, the evidence files, and the\n"
        "   three prohibitions (no desk/ writes, no closeout, no commits unless the task says so). Then:\n"
        "   `scion start " + repo + "-<short-slug> \"<prompt>\" --type deskops-executor` and record it:\n"
        "   `deskops runtime template role-deskops-executor --harness " + harness + " --root /workspace/deskops --out /tmp/t"
        " --task <id> --agent " + repo + "-<short-slug> --task-root /workspace/" + repo + "`.\n"
        "3. **One executor per repository at a time.** Agents share the checkout; two writers on the same repo\n"
        "   collide in git. Different repositories may run in parallel.\n"
        "4. **Wait properly.** After dispatching: `sciontool status blocked \"waiting on <agent>\"`. Scion wakes you\n"
        "   when the child completes, stalls or asks for input. Do not poll in a loop.\n"
        "5. **Review before closing.** Read `runs/subagents/<run>/result-summary.md` and `validation.log`; re-run the\n"
        "   task's validation yourself; check `git status` shows only what the task scoped. Then\n"
        "   `deskops advance task <id>` through its gates and `deskops closeout commit --task <id> --run-dir <run>\n"
        "   --paths <files>`. If evidence is missing, message the executor or dispatch a new one; never fabricate it.\n"
        "   Then `scion stop <agent>`: an executor that reported completed keeps its container alive until stopped,\n"
        "   and Scion counts that idle time against its duration limit.\n"
        "6. **Do not push.** Commits stay local; the owner pushes. Report what you committed.\n"
        "7. **Report.** When the desk has nothing dispatchable left, `sciontool status task_completed \"<one-line summary>\"`.\n"
        "\n"
        "## Never\n"
        "\n"
        "- Never edit a tracked desk document by hand; always the `deskops` / `sldb` CLIs (`--help` first).\n"
        "- Never write outside `/workspace/" + repo + "` except `runs/` evidence and inbox notes sent through `deskops message send`.\n"
        "- Never decide for the owner: releases, policy, model design, anything a note marks as theirs.\n"
        "- Never answer an executor's question on the owner's behalf; surface it.\n"
    )


def _render_agents_md(role_name: str, harness: str, task_repo: str | None) -> str:
    repo_line = (
        f"- Your task lives in the repository `{task_repo}` under `/workspace`. Write only there."
        if task_repo
        else "- Your task names its repository under `/workspace`. Write only there; the other repositories are context."
    )
    return (
        f"# {role_name} on Scion ({harness})\n"
        "\n"
        "You are a deskops executor running as a Scion agent. The desk, not your memory, holds the state.\n"
        "\n"
        "## Scope\n"
        "\n"
        f"{repo_line}\n"
        "- One bounded task. Do not route the board, touch other tasks, or close the task yourself.\n"
        "- The CLIs are `deskops` and `sldb`; learn them with `--help`. Never edit a tracked desk document by hand.\n"
        "\n"
        "## Recover state first\n"
        "\n"
        "```bash\n"
        "deskops show board Board --root <repo>\n"
        "deskops show task <task-id> --root <repo>\n"
        "deskops next <task-id> --root <repo>\n"
        "git -C <repo> status --short --branch\n"
        "```\n"
        "\n"
        "## Evidence\n"
        "\n"
        "Make `<repo>/runs/subagents/<YYYYMMDD-HHMMSS>-<task-id>/` first and snapshot the state you start from;\n"
        "`deskops closeout commit --run-dir` refuses a run dir without `board.txt` and `git-status.txt`:\n"
        "\n"
        "```bash\n"
        "RUN_DIR=<repo>/runs/subagents/$(date +%Y%m%d-%H%M%S)-<task-id>; mkdir -p \"$RUN_DIR\"\n"
        "deskops show board Board --root <repo> > \"$RUN_DIR/board.txt\"\n"
        "deskops show task <task-id> --root <repo> > \"$RUN_DIR/task.txt\"\n"
        "deskops next <task-id> --root <repo> > \"$RUN_DIR/next.txt\"\n"
        "git -C <repo> status --short --branch > \"$RUN_DIR/git-status.txt\"\n"
        "```\n"
        "\n"
        "- Then `validation.log` (the exact command and its exit code) and `result-summary.md`.\n"
        "- `result-summary.md` is the handoff: what you did, what you ran, what the supervisor must review.\n"
        "- Run the smallest relevant validation first.\n"
        "\n"
        "## When done\n"
        "\n"
        "- Leave the working tree committed or clearly described in `result-summary.md`; do not run `deskops closeout`.\n"
        "- Say you are done with `sciontool status task_completed \"<one-line summary>\"`: Scion wakes the coordinator\n"
        "  on that status, not on `blocked`.\n"
    )


def materialize_scion_template(
    root: Path,
    role_id: str,
    *,
    harness: str | None = None,
    out_dir: Path | None = None,
    model_alias: str = DEFAULT_MODEL_ALIAS,
    task_repo: str | None = None,
    mode: str | None = None,
) -> Path:
    """Write the template for ``role_id`` and return its directory.

    The runtime profile is the one matching the role's ``kind`` unless
    ``harness`` names another installed kind; ``harness`` also decides
    ``default_harness_config``.
    """
    role_path, role_doc = find_role_doc(root, role_id)
    profiles = load_runtime_profiles(root)
    kind = harness or str(role_doc.get("kind") or "")
    profile = profiles.get(kind) or profiles.get(str(role_doc.get("kind") or ""))
    if profile is None:
        raise ValueError(f"no RuntimeProfileDoc for kind '{kind}' under {root / 'desk' / 'runtimes'}")
    harness_name = pick_harness_config(kind)
    source = f"{role_path.relative_to(root).as_posix()} + desk/runtimes/{profile.get('id', kind)}.md"
    files = scion_template_files(
        role_doc, profile, harness=harness_name, model_alias=model_alias, task_repo=task_repo, source=source, mode=mode
    )
    target = template_dir_for(root, role_doc, out_dir)
    target.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (target / name).write_text(text, encoding="utf-8")
    return target


_SLUG_RE = re.compile(r"[^a-z0-9]+")


def _slug(value: str) -> str:
    return _SLUG_RE.sub("-", value.lower()).strip("-")


def record_scion_run(
    root: Path,
    *,
    task_id: str,
    role_id: str,
    kind: str,
    agent_slug: str,
    run_dir: str | None = None,
    outcome: str = "in_progress",
    summary: str = "",
) -> Path:
    """Write (and track, when the root has a store) a RunDoc for one Scion dispatch.

    The RunDoc lives at ``<run_dir>/run.md`` so the evidence directory and its
    record travel together. ``session_path`` carries ``scion://agent/<slug>``:
    the transcript is Scion's (``scion logs <slug>``), copied into ``run_dir``
    by the supervisor at closeout.
    """
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    run_dir = run_dir or f"runs/subagents/{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{_slug(task_id)}"
    run_id = f"run-{_slug(agent_slug)}"
    payload = {
        "id": run_id,
        "title": f"Scion agent {agent_slug} on {task_id}",
        "summary": summary or f"Dispatched with `scion start {agent_slug}` from role {role_id} ({kind}).",
        "task_id": task_id,
        "role_id": role_id,
        "kind": kind,
        "run_dir": run_dir,
        "herdr_pane_id": "",
        "session_path": f"scion://agent/{agent_slug}",
        "session_sha256": "",
        "started_at": now,
        "ended_at": "" if outcome == "in_progress" else now,
        "outcome": outcome,
        "commit_sha": "",
        "tags": ["system:deskops", "runtime:scion"],
    }
    path = root / Path(run_dir) / "run.md"
    if path.exists():
        doc_access.write_doc(root, path, RunDoc, payload)
    else:
        doc_access.create_doc(root, path, RunDoc, payload, run_id)
    return path


FILE:tests/test_scion_runtime.py
"""RoleDoc + RuntimeProfileDoc -> Scion agent template, against this repo's real desk."""

from __future__ import annotations

from pathlib import Path
import re
import sys

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
SLDB_SRC = ROOT.parent / "sldb" / "src"
if str(SLDB_SRC) not in sys.path:
    sys.path.insert(0, str(SLDB_SRC))

from deskops.cli.main import main
from deskops.materializers.runtime_profiles import load_runtime_profiles
from deskops.models import RunDoc
from deskops.runtime.scion import (
    TEMPLATE_FILES,
    find_role_doc,
    materialize_scion_template,
    pick_harness_config,
    record_scion_run,
    scion_template_files,
)
from sldb.runtime.validation import extract_model_data


@pytest.fixture(scope="module")
def executor() -> dict:
    _, role_doc = find_role_doc(ROOT, "role-deskops-executor")
    return role_doc


@pytest.fixture(scope="module")
def profiles() -> dict[str, dict]:
    return load_runtime_profiles(ROOT)


def test_harness_for_every_tracked_runtime_kind(profiles: dict[str, dict]) -> None:
    for kind in profiles:
        assert pick_harness_config(kind)
    with pytest.raises(ValueError, match="no Scion harness-config"):
        pick_harness_config("emacs")


def test_find_role_doc_accepts_id_and_name() -> None:
    by_id = find_role_doc(ROOT, "role-deskops-executor")[1]
    by_name = find_role_doc(ROOT, "deskops-executor")[1]
    assert by_id == by_name
    with pytest.raises(ValueError, match="no RoleDoc"):
        find_role_doc(ROOT, "role-nobody")


def test_claude_template_is_portable_and_loud_about_omissions(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["claude"], harness="claude", source="desk/roles/x.md")
    assert set(files) == set(TEMPLATE_FILES)

    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["schema_version"] == "1"
    assert agent["default_harness_config"] == "claude"
    assert agent["model"] == "medium"  # size alias, never the concrete RoleDoc model
    assert agent["auth_selectedType"] == "oauth-token"  # never left to whatever credential the Hub finds
    assert agent["agent_instructions"] == "agents.md"
    assert agent["system_prompt"] == "system-prompt.md"
    assert agent["max_turns"] and agent["max_duration"]
    assert "image" not in agent  # environment keys belong to the harness-config

    text = files["scion-agent.yaml"]
    assert "# Source: desk/roles/x.md" in text
    assert executor["model"] in text  # the concrete model is named in a comment
    assert "fallback_models" in text and "unsupported_role_fields" in text  # dropped, but said so
    assert files["system-prompt.md"].strip() == executor["body"].strip()
    assert "Write only there" in files["agents.md"]
    assert "deskops closeout" in files["agents.md"]


def test_pi_template_targets_the_pi_harness_config(executor: dict, profiles: dict[str, dict]) -> None:
    files = scion_template_files(executor, profiles["pi"], harness="pi", model_alias="small", task_repo="sldb")
    agent = yaml.safe_load(files["scion-agent.yaml"])
    assert agent["default_harness_config"] == "pi"
    assert agent["model"] == "small"
    assert "auth_selectedType" not in agent
    assert "repository `sldb`" in files["agents.md"]


def test_supervisor_role_gets_coordinator_instructions(profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    files = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    agents = files["agents.md"]
    assert "coordinator of the `deskops` desk" in agents
    assert "One executor per repository at a time" in agents
    assert "Do not push" in agents and "Never decide for the owner" in agents
    # the executor text is not in it, and an explicit mode overrides the name
    assert "You are a deskops executor" not in agents
    forced = scion_template_files(supervisor, profiles["claude"], harness="claude", mode="executor")
    assert "You are a deskops executor" in forced["agents.md"]
    with pytest.raises(ValueError, match="mode must be"):
        scion_template_files(supervisor, profiles["claude"], harness="claude", mode="boss")


def test_statuses_are_ones_sciontool_has_and_wake_the_coordinator(executor: dict, profiles: dict[str, dict]) -> None:
    _, supervisor = find_role_doc(ROOT, "role-deskops-supervisor")
    coordinator = scion_template_files(supervisor, profiles["claude"], harness="claude", task_repo="deskops")
    worker = scion_template_files(executor, profiles["claude"], harness="claude", task_repo="deskops")
    for text in (coordinator["agents.md"], worker["agents.md"]):
        statuses = set(re.findall(r"sciontool status (\w+)", text))
        assert statuses <= {"ask_user", "blocked", "task_completed"}, statuses
    assert "sciontool status task_completed" in worker["agents.md"]  # blocked would not wake the coordinator

    # A coordinator idles blocked on its children; the executor's limit would kill it.
    assert yaml.safe_load(coordinator["scion-agent.yaml"])["max_duration"] == "24h"
    assert yaml.safe_load(worker["scion-agent.yaml"])["max_duration"] == "2h"


def test_tools_fold_into_command_args_when_the_profile_has_a_flag(profiles: dict[str, dict]) -> None:
    role = {"id": "role-x", "name": "x", "description": "d", "kind": "claude", "model": "", "tools": ["Read", "Bash"], "body": "# x"}
    agent = yaml.safe_load(scion_template_files(role, profiles["claude"], harness="claude")["scion-agent.yaml"])
    assert agent["command_args"] == ["--allowedTools", "Read", "--allowedTools", "Bash"]


def test_bad_alias_and_bad_harness_are_refused(executor: dict, profiles: dict[str, dict]) -> None:
    with pytest.raises(ValueError, match="model alias"):
        scion_template_files(executor, profiles["claude"], harness="claude", model_alias="huge")
    with pytest.raises(ValueError, match="unknown Scion harness-config"):
        scion_template_files(executor, profiles["claude"], harness="emacs")


def test_materialize_writes_the_three_files(tmp_path: Path) -> None:
    target = materialize_scion_template(ROOT, "deskops-executor", harness="claude", out_dir=tmp_path / "t")
    assert target == tmp_path / "t"
    assert sorted(p.name for p in target.iterdir()) == sorted(TEMPLATE_FILES)
    assert "Source: desk/roles/deskops-executor.md + desk/runtimes/runtime-claude.md" in (target / "scion-agent.yaml").read_text()


def test_cli_runtime_template(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude", "--out", str(tmp_path / "t")])
    out = capsys.readouterr().out
    assert code == 0, out
    assert "Scion template:" in out and "scion start" in out
    assert (tmp_path / "t" / "scion-agent.yaml").exists()


def test_cli_task_root_puts_the_rundoc_next_to_the_task(tmp_path: Path, capsys) -> None:
    task_root = tmp_path / "other-repo"
    task_root.mkdir()
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-x", "--task-root", str(task_root),
    ])
    out = capsys.readouterr().out
    assert code == 0, out
    runs = list((task_root / "runs" / "subagents").glob("*-task-x/run.md"))
    assert len(runs) == 1, out

    # An agent that already made its own evidence dir: the RunDoc points there.
    code = main([
        "runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--harness", "claude",
        "--out", str(tmp_path / "t"), "--task", "task-x", "--agent", "agent-y", "--task-root", str(task_root),
        "--run-dir", "runs/subagents/20261029-000000-task-x",
    ])
    assert code == 0, capsys.readouterr().out
    doc = extract_model_data(RunDoc, (task_root / "runs/subagents/20261029-000000-task-x/run.md").read_text(encoding="utf-8"))
    assert doc["run_dir"] == "runs/subagents/20261029-000000-task-x" and doc["id"] == "run-agent-y"
    assert not list((ROOT / "runs" / "subagents").glob("*-task-x"))  # nothing written into the roles' repo
    assert extract_model_data(RunDoc, runs[0].read_text(encoding="utf-8"))["id"] == "run-agent-x"


def test_cli_task_without_agent_is_an_error(tmp_path: Path, capsys) -> None:
    code = main(["runtime", "template", "role-deskops-executor", "--root", str(ROOT), "--out", str(tmp_path / "t"), "--task", "task-x"])
    captured = capsys.readouterr()
    assert code != 0
    assert "--task and --agent go together" in captured.out + captured.err


def test_record_scion_run_writes_a_rundoc_that_roundtrips(tmp_path: Path) -> None:
    path = record_scion_run(
        tmp_path,
        task_id="task-close-serve",
        role_id="role-deskops-executor",
        kind="claude",
        agent_slug="sldb-close-serve",
        run_dir="runs/subagents/20261029-000000-task-close-serve",
    )
    assert path == tmp_path / "runs/subagents/20261029-000000-task-close-serve/run.md"
    data = extract_model_data(RunDoc, path.read_text(encoding="utf-8"))
    assert data["id"] == "run-sldb-close-serve"
    assert data["task_id"] == "task-close-serve"
    assert data["session_path"] == "scion://agent/sldb-close-serve"
    assert data["outcome"] == "in_progress" and data["ended_at"] == ""
    assert data["tags"] == ["system:deskops", "runtime:scion"]
