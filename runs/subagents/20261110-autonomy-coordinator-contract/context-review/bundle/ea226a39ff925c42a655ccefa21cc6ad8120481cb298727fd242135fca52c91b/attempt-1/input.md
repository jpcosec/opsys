FILE:desk/tasks/task-scion-autonomy-coordinator-contract.md
---
sldb:
  by: agent
  at: '2026-11-10T15:15:34Z'
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

Owner requires unattended authorized task progress; real coordinator stopped on source-policy conflicts, stale state and false review status.

## Goal

_Describe the concrete result this task must produce._

One coherent source contract makes Scion coordinator recover configured current state, progress routine authorized work, select reviewed ready unowned tasks, dispatch fresh executor/tester and reconcile closeout before continuing.

## Scope

_State what is in scope and what is out of scope._

Role source, generated Scion modes/prompts and command examples, explicit runtime context and durable atoms/docs. No replacement lifecycle engine, automatic policy decisions, pi-subagents or unrelated CC tasks.

## Implementation Path

_Outline the expected implementation route or affected surface._

Source contract: correct RoleDoc via SLDB, permitting modeled workflow CLI mutations but no implementation by supervisor. Ordinary implementation questions answered from task/source evidence; escalate only unresolved owner decisions, actual ownership conflicts or external credentials/permissions. Never rerun an accepted review with unchanged input; bound technical retries and report precise blockers instead of broad diagnostic loops. Add optional --context-file JSON to existing runtime template command (and matching generator context kwarg); context keys project, workspace_root, desk_root, source_root, sldb_root are absolute paths within workspace_root except project. Emit DESKOPS_DESK_ROOT, DESKOPS_SOURCE_ROOT, DESKOPS_SLDB_SOURCE_ROOT, DESKOPS_WORKSPACE_ROOT, DESKOPS_SCION_PROJECT and PYTHONPATH plus a supported volume source=workspace_root target=workspace_root. No secrets in context. Preserve no-context behavior. Include tester mode in existing --mode choices, auto-detect tester RoleDoc, and separate tester scope/completion instructions. Coordinator recovers this configured current desk/tools, checks canonical/dirty state, board DAG/review gates and existing ownership (labels/RunDoc/worktrees), skips blocked/owned tasks, selects one reviewed ready leaf. Deterministic task+contract-derived agent names and task/role labels: write run intent BEFORE start and reconcile existing matching Scion child before any new start; duplicate-name protection stays Scion native, not a new scheduler/registry. Explicit --project, --workspace, --type, --harness-auth api-key, --non-interactive and correct subcommand --root flags in examples. Executor -> independent tester -> coordinator validates evidence -> deskops closeout -> reconcile phase -> recover/select again. Failed tester cannot close; request bounded correction and fresh test. Waiting-for-child uses Scion blocked/completion notifications (already subscribed); only real human decisions ask_user. Capture source atom before operator docs, generate from source, test YAML/modes/context and actual command examples; runtime task supplies hooks/bootstrap and unattended integration. Concrete interface choices: project is a nonempty Scion slug or UUID (not a filesystem path); mode literal is tester. Context JSON requires all five named keys; reject missing/unknown/invalid/relative/out-of-workspace paths before generation, no partial defaults; omitted --context-file preserves existing behavior. sldb_root already names its src directory. PYTHONPATH is source_root + os.pathsep + sldb_root, without inherited stale paths. Existing role model preferences never override explicit configured harness/model alias. Bound technical retries to 2 per unchanged input and implementation correction/test cycles to 2 per task contract; if still failing persist exact blocker, do not ask owner for facts already in sources. Run intent is the existing RunDoc with in_progress outcome in the assigned run_dir, explicitly intent not proof of start. Deterministic child identity: role-specific prefix deskops-e or deskops-t plus first 12 hex of SHA256(task_id + NUL + contract_sha256 + NUL + role); labels deskops.task_id, deskops.contract_sha256, deskops.role. Reconcile exact project+name+labels and RunDoc before start; conflicting ownership blocks that task only. Matching running child is observed, stopped child resumed, completed child reviewed; never launch duplicate. Independent testers use role-deskops-tester/--mode tester and a distinct role identity. Scope also includes deskops/cli/commands/runtime.py to load/pass context-file; test helpers may be added in runtime/scion.py but no replacement scheduler or lifecycle engine. Final clarifications: source_root is the repository root containing the deskops/ package. contract_sha256 is the SLDB task __contract__ digest, obtained using existing sldb.store.hashing.hash_fields_with_map(TaskDoc, markdown) then sldb.store.graph.language.contract_hash.contract_hash(TaskDoc, field_hashes); no local reimplementation or raw-file hash. Add a runtime helper for command examples that derives child name/labels from the task path and role enum executor or tester. Status/history/references changes must not alter identity; goal/scope/contract changes must. Both retry bounds mean 2 total attempts, not 2 additional retries. Among eligible unowned ready leaves use existing Board order as deterministic tie-breaker; no invented priority. Mode autodetection applies only to the explicitly selected RoleDoc: explicit --mode wins; selected name/id ending in -tester chooses tester, supervisor/coordinator chooses coordinator, otherwise executor; never search other roles to choose one. Source task unit validation can complete independently, but final unattended acceptance/phase integration requires the declared setup runtime task; dependency output commit is recorded then, not requested as owner policy. Retry identity clarification: attempt is integer 1 or 2, first uses the base child name and second appends -a2; include deskops.attempt label. RunDoc attempts and evidence are immutable: never overwrite a previous attempt, never create attempt 3. Unknown, unavailable or active Scion state is observed or recorded as a blocker rather than duplicated. Match stopped children resume the same identity; prior completed attempts are reviewed before any correction attempt. desk_root means the task repository root containing desk/, and all task --root flags use it. Preserve omitted-context environment/path and CLI compatibility while correcting faulty instructions in all modes. Template-only generation is side-effect-free apart from its output files; supplied task/agent records intent before manual launch. Unit tests use temporary task Markdown and compare canonical SLDB digests, deterministic names/labels, bad attempts, context validation before output, tester scope and full generated command flags.

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


FILE:desk/rituals/phase.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:20Z'
  authority: generated
  via: update_document
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
- 1. Apply [ritual-context-review](context-review.md) cheaply and recursively to the
  root, packages and every leaf with their dependency interfaces. Compare reformulation,
  ambiguities and detailed non-executing dry-run with intent; correct briefs and split
  large nodes into children and edges before selecting ready leaves.
- 1. Identify the ready dependency layer of tasks whose prerequisites are satisfied
  and whose planned changes do not overlap operationally.
- '1. Confirm each task has a fresh execution context bundle: the task doc, board-routed
  instructions, bound pills, linked atoms, linked files, and validation targets.'
- 1. Run the execution ritual for each task in the phase before implementation begins.
- 1. Execute phase tasks in parallel when the environment supports it, or in isolated
  fresh contexts when parallelism is unavailable.
- 1. Require each task to close with its own targeted validation and atomic task commit
  before considering the phase complete.
- 1. When all phase tasks are closed, run shared integration or end-to-end validation
  for the combined layer.
- 1. Fix interaction regressions uncovered by the phase-level validation before phase
  closeout.
- '1. Reconcile the pill set touched by the phase: retire stale pills, merge or delete
  redundant pills, and promote durable residue into atoms and materializations.'
- 1. Capture newly discovered tasks, dependencies, or next-phase pills before advancing.
- 1. Create one descriptive phase-closing commit for the integration and reconciliation
  pass.
# e.g., layer:workflow, system:sldb
tags:
- system:sldb
- workspace:desk
- topic:rituals
- topic:phases
---

# Phase ritual for dependency-layer execution

## Purpose

_Explain why this ritual exists._

Run one horizontal dependency layer of tasks as the workflow unit above individual task execution, then close that layer with integration validation, pill reconciliation, and next-phase preparation. Review decomposition under [ritual-context-review](context-review.md) before selecting leaves; this adds no lifecycle state.

## Trigger

_State when this ritual should start._

Start during decomposition of the multilevel DAG, before promotion or selection of a ready non-overlapping layer; close the layer only after every task closes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The board's active tasks and dependencies are explicit.
- The ready phase has been identified as a non-overlapping layer.
- Each task has a named context bundle and validation target.
- Phase-level validation expectations are known.
- A pill reconciliation pass is planned for phase closeout.
- Ready leaves and their governing root/package contracts have current accepted cheap context reviews; expert council verdicts and topological order do not satisfy this gate.

## Validation

_List the checks that prove the ritual was performed correctly._

- Every task in the phase executed from fresh context.
- Every task closed with its own tests and its own commit.
- Shared phase validation passed after task integration.
- Regressions caused by task interaction were fixed before advancing.
- Pills touched by the phase were reconciled as stale, redundant, durable, or still active.
- Durable residue from pills was promoted into atoms and materializations when needed.
- Newly discovered work for later phases was captured explicitly.
- The phase closeout has its own descriptive commit.
- Cheap reviews are evidenced by node/input/attempt under ritual-context-review; changed inputs or dependency contracts invalidated affected reviews and retries used new processes.

## Failure Modes

_List common mistakes this ritual prevents._

- Starting a phase without identifying the actual dependency layer.
- Treating a semantic milestone as a phase even when tasks still depend on one another.
- Letting tasks share one long-lived execution context instead of fresh task-specific bundles.
- Advancing to the next phase after isolated task tests without integration validation.
- Carrying stale or overlapping pills forward because each task closed independently.
- Hiding phase-level regressions inside later task commits instead of closing the layer explicitly.
- Selecting leaves from a root-only or expert-reviewed plan without recursive cheap reviews; treating hierarchy or structural PASS as execution authorization.

## Completion

_Describe what completion looks like._

The current dependency layer is integrated, reconciled, and committed, and the board is ready to start the next phase.


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


FILE:desk/contexts/pill-001-task-closure-commit.md
---
# pill-xxx
id: pill-001
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:guardrail
- topic:git
- topic:task-closure
---

# Guardrail: close every task with its own commit

## What

_Define the context or guardrail this pill carries._

Task closure in this routine is defined by a completed change plus a dedicated closing commit in git.

## Why

_Explain why this context matters for safe execution._

If a task can be called done without a closing commit, the board and desk documents drift away from the durable execution record.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task is being finished, deleted from `desk/tasks/`, or removed from a board.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/closeout.md`, `desk/rituals/testing.md`, task closeout, and any future workspace that reuses this routine.

## How

_Describe the correct way to apply this guidance._

Keep task files active until tests, cleanup, board updates, and the closing change are ready, then create one atomic commit that closes the task.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not delete a finished task file and call it closed before the closing commit exists. Do not rely on memory or an uncommitted working tree as the record of closure.


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


FILE:desk/contexts/pill-007-phase-gated-task-flow.md
---
# pill-xxx
id: pill-007
# e.g., language:python, library:pydantic
tags:
- system:sldb
- workspace:desk
- pill-type:guardrail
- topic:workflow
- topic:phase-gates
---

# Guardrail: force every task through explicit phase gates

## What

_Define the context or guardrail this pill carries._

Every desk task must pass through explicit entry, handoff, testing, and closeout gates, and every board phase must open and close explicitly instead of flowing directly from implementation intent to completion.

## Why

_Explain why this context matters for safe execution._

Agents keep skipping atomization, task scoping, test review, integration validation, or the closing commits when those obligations live only as background expectations. Phase gates turn those obligations into mandatory stop points at both the task and dependency-layer levels.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a desk task is initialized, handed from execution to testing, handed from testing to closeout, or grouped into a ready phase for parallel execution.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/phase.md`, `desk/rituals/execution.md`, `desk/rituals/testing.md`, `desk/rituals/closeout.md`, and any task that changes code, docs, or workflow state.

## How

_Describe the correct way to apply this guidance._

Open each phase by identifying the ready dependency layer and each task by confirming clarity, file scope, validation targets, and atomization. Require an execution exit gate before testing, a testing exit gate before closeout, a final task closeout gate that ends in the dedicated task commit, and a phase closeout gate that runs integration validation plus pill reconciliation before the next phase begins.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat implementation as the default starting point. Do not jump from “code looks done” to task deletion or board cleanup without a testing handoff and a dedicated task closing commit. Do not treat a stack of closed tasks as permission to begin the next phase without a phase-level validation and reconciliation pass.


FILE:desk/contexts/pill-durable-pill-knowledge-graduates-to-atoms-at-closeout.md
---
# pill-xxx
id: pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:pills
- topic:atoms
- topic:closeout
---

# Guardrail: durable pill knowledge graduates to atoms at closeout

## What

_Define the context or guardrail this pill carries._

Treat task closeout as the final check that durable knowledge discovered or refined in pills has been distilled into atoms before the pill disappears.

## Why

_Explain why this context matters for safe execution._

Bugfix and feature work often starts with in-flight knowledge in pills. If closeout deletes or forgets that context without atomizing the durable residue, the project loses the ruling while keeping only code diffs or stale git history.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a task binds implementation-heavy pills, resolves a bug, introduces a feature rule, or closes out work that refined project knowledge.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to task closeout, pill audits, atom updates, and any future deskops closeout enforcement around knowledge graduation.

## How

_Describe the correct way to apply this guidance._

Review bound pills at closeout, identify which parts became durable project ruling, promote that residue into atoms, and only then delete or retire the pill if no active task still needs it.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not delete a pill just because the code landed. Do not leave durable bugfix or feature knowledge stranded only in task-local context.


FILE:desk/contexts/pill-phase-closeout-reconciles-pills-and-surfaces-next-work.md
---
# pill-xxx
id: pill-phase-closeout-reconciles-pills-and-surfaces-next-work
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:phases
- topic:pills
- topic:closeout
---

# Guardrail: phase closeout reconciles pills and surfaces next work

## What

_Define the context or guardrail this pill carries._

After all tasks in a dependency layer close, run one explicit phase closeout pass that checks integration behavior, reconciles the pill set, and captures newly discovered work before the next phase begins.

## Why

_Explain why this context matters for safe execution._

Task closeout proves each deliverable in isolation, but it does not by itself clean up overlapping pills, catch interaction regressions, or prepare the next execution layer. Without a phase pass, stale context and cross-task breakage accumulate between waves.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a board is executed through dependency layers and a full phase of non-overlapping tasks has finished task-level closeout.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/phase.md`, `desk/tasks/Board.md`, board-level execution planning, pill audits, and end-of-phase validation.

## How

_Describe the correct way to apply this guidance._

Treat phase closeout as mandatory: run integration or end-to-end validation, fix regressions, classify pills as stale, redundant, durable, or still needed, promote durable knowledge into atoms and materializations, and draft or bind the pills needed for the next ready phase.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not treat a stack of closed task commits as sufficient to start the next phase. Do not carry stale or overlapping pills forward just because each individual task passed its own tests.


FILE:desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
---
# pill-xxx
id: pill-ready-phases-prove-dependencies-and-non-overlap
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:phases
- topic:dependencies
---

# Guardrail: ready phases prove dependencies and non-overlap

## What

_Define the context or guardrail this pill carries._

Treat a board phase as ready only when its tasks form a real dependency layer: their prerequisites are satisfied and their planned operational changes do not overlap.

## Why

_Explain why this context matters for safe execution._

If a phase is only a semantic grouping or a wishful backlog slice, parallel execution becomes unsafe and phase closeout no longer proves integration at the right layer.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever a board chooses the next phase, groups tasks for parallel execution, or claims that multiple tasks are ready at once.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/rituals/phase.md`, `desk/tasks/Board.md`, dependency planning, and any future phase-aware execution tooling.

## How

_Describe the correct way to apply this guidance._

Name the dependency proof explicitly, check that no task in the candidate phase still depends on another task in the same layer, and check that the planned touched surfaces can be executed without operational overlap.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not call a backlog theme a phase. Do not group tasks into one phase just because they sound related if they still depend on one another or change the same operational surface unsafely.


FILE:desk/contexts/pill-board-routed-pills-stay-minimal-and-reusable.md
---
# pill-xxx
id: pill-board-routed-pills-stay-minimal-and-reusable
# e.g., language:python, library:pydantic
tags:
- system:deskops
- workspace:desk
- pill-type:guardrail
- topic:pills
- topic:boards
- topic:routing
---

# Guardrail: board-routed pills stay minimal and reusable

## What

_Define the context or guardrail this pill carries._

Treat the board-routed pill set as the smallest reusable baseline that most active tasks should see, not as a dumping ground for every historical or domain-specific pill in the workspace.

## Why

_Explain why this context matters for safe execution._

If the board routes too many pills, fresh subagents inherit stale or irrelevant context and start treating pills like task mirrors instead of reusable atomic truths.

## When

_Describe when an agent should apply this pill._

Apply this pill whenever the board pill list is updated, a new phase is prepared, or a pill audit asks whether a rule belongs in the board baseline or only on selected tasks.

## Where

_Name the files, surfaces, or scope this pill applies to._

Applies to `desk/tasks/Board.md`, `desk/contexts/pills.md`, pill conciliation passes, and future phase-preparation workflows.

## How

_Describe the correct way to apply this guidance._

Keep only cross-cutting reusable pills on the board. Bind domain-specific, risky, or file-specific pills directly on the tasks that need them. During phase closeout, remove board pills that no longer serve as reusable baseline guidance.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not route old tranche pills board-wide just because they still exist in `desk/contexts/`. Do not confuse "relevant to one active task" with "baseline context for most board work."


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


FILE:deskops/cli/commands/runtime.py
from __future__ import annotations

from pathlib import Path
from typing import Any

from deskops.cli.render import render
from deskops.cli.render import render_error
from deskops.config import DeskConfig
from deskops.runtime.grouping import group_agents_by_workspace
from deskops.runtime.herdr import HerdrClient, HerdrProvider
from deskops.runtime.initializer import ensure_herdr_server, initialize_desk
from deskops.runtime.supervise import SuperviseOutcome, run_supervise_loop


class RuntimeCLI:
    def run(self, args: Any) -> int:
        root = Path(args.root).resolve()
        executable = getattr(args, "herdr", "herdr")
        try:
            if args.runtime_command == "template":
                return self._template(args, root)
            if args.runtime_command == "supervise":
                return self._supervise(args, executable)
            if args.runtime_command == "workers":
                return self._workers(args, executable)
            if args.runtime_command == "init":
                ensure_herdr_server(executable)
                info, handle = initialize_desk(root, agents=args.agents, executable=executable)
                if handle is None:
                    print(f"Herdr Space already exists: {info.identity}")
                else:
                    print(f"DeskOps identity: {info.identity}; tasks discovered: {info.task_count}")
                    print(f"Created Herdr Space: {handle.workspace_id} ({info.identity})")
                    print(f"Panes: {handle.panes}")
                    if handle.agents:
                        print(f"Agents: {handle.agents}")
                return 0

            client = HerdrClient(executable)
            identity = DeskConfig.load(root / "desk").project_identity
            workspaces = client.call("workspace", "list").get("result", {}).get("workspaces", [])
            matches = [item for item in workspaces if isinstance(item, dict) and item.get("label") == identity]
            if args.runtime_command == "status":
                for workspace in matches:
                    print(f"{workspace.get('workspace_id')} | {workspace.get('label')} | panes={workspace.get('pane_count')}")
                if not matches:
                    print(f"No Herdr Space found for {identity}")
                return 0
            if not matches:
                print(f"No Herdr Space found for {identity}")
                return 1
            workspace_id = matches[0]["workspace_id"]
            if args.runtime_command == "attach":
                client.call("workspace", "focus", workspace_id)
                print(f"Focused Herdr Space: {workspace_id} ({identity})")
                return 0
            if args.runtime_command == "stop":
                client.call("workspace", "close", workspace_id)
                print(f"Closed Herdr Space: {workspace_id} ({identity})")
                return 0
        except (ValueError, RuntimeError) as exc:
            return render_error(
                str(exc),
                getattr(args, "format", "text"),
                type_name=type(exc).__name__,
                text=f"Error: {exc}",
            )
        return 1

    def _template(self, args: Any, root: Path) -> int:
        """Write a Scion template for one role; optionally record the dispatch as a RunDoc.

        Never calls ``scion``: launching (``scion start <agent> "<task>"
        --type <template>``) stays a deliberate gesture of the supervisor.
        """
        from deskops.runtime.scion import materialize_scion_template, record_scion_run

        out_dir = Path(args.out).expanduser().resolve() if getattr(args, "out", None) else None
        task_id = getattr(args, "task", None)
        agent = getattr(args, "agent", None)
        if bool(task_id) != bool(agent):
            raise ValueError("--task and --agent go together: the RunDoc needs both the task and the Scion agent slug")
        target = materialize_scion_template(
            root,
            args.role_id,
            harness=getattr(args, "harness", None),
            out_dir=out_dir,
            model_alias=getattr(args, "model_alias", "medium"),
            task_repo=getattr(args, "task_repo", None),
            mode=getattr(args, "mode", None),
        )
        print(f"Scion template: {target}")
        for name in ("scion-agent.yaml", "system-prompt.md", "agents.md"):
            print(f"  {name}")
        if task_id and agent:
            harness = getattr(args, "harness", None) or ""
            # Roles live in the deskops desk; the task may live in another repo's
            # desk. The RunDoc belongs next to the task.
            task_root = Path(args.task_root).expanduser().resolve() if getattr(args, "task_root", None) else root
            run_path = record_scion_run(
                task_root,
                task_id=task_id,
                role_id=args.role_id,
                kind=harness or "scion",
                agent_slug=agent,
                run_dir=getattr(args, "run_dir", None),
            )
            print(f"RunDoc: {run_path.relative_to(task_root)} (in {task_root})")
        print(f"Next: scion start {agent or '<agent>'} \"<task>\" --type {target.name}")
        return 0

    def _supervise(self, args: Any, executable: str) -> int:
        """Block on one agent, reporting blocked/done settles as they happen.

        Never answers a blocked agent's prompt (only notifies and reports —
        a human decides) and never advances desk state on done (only
        captures and reports). Both are the explicit anti-patterns this
        command exists to avoid; see
        desk/roles/deskops-supervisor.md and
        desk/drawer/features/feature-herdr-supervised-execution-runtime.md.
        """
        provider = HerdrProvider(HerdrClient(executable))
        agent_id = args.agent
        max_iterations = getattr(args, "max_iterations", None)
        read_lines = getattr(args, "read_lines", 200)

        def on_blocked(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[blocked] {outcome.agent_id} is waiting on input. Recent output:\n{excerpt_tail}")
            try:
                provider.notify(
                    f"{outcome.agent_id} blocked",
                    body="Waiting on input; not answering automatically.",
                )
            except Exception as exc:  # noqa: BLE001 - notification failure must not crash supervision
                print(f"(notification failed: {exc})")

        def on_done(outcome: SuperviseOutcome) -> None:
            excerpt_tail = "\n".join(outcome.excerpt.strip().splitlines()[-20:])
            print(f"[done] {outcome.agent_id} settled. Recent output:\n{excerpt_tail}")
            print(f"[done] {outcome.agent_id} did not advance any task; review and run `deskops advance` yourself.")

        outcomes = run_supervise_loop(
            provider,
            agent_id,
            max_iterations=max_iterations,
            read_lines=read_lines,
            timeout_ms=getattr(args, "timeout_ms", None),
            on_blocked=on_blocked,
            on_done=on_done,
        )
        if outcomes and outcomes[-1].status in {"timeout", "unknown"}:
            print(f"[{outcomes[-1].status}] stopped supervising {agent_id}.")
            return 1
        return 0

    def _workers(self, args: Any, executable: str) -> int:
        """List live Herdr agents machine-wide, grouped by workspace.

        Joins ``herdr agent list`` with ``herdr workspace list`` so each
        space shows its readable label and Herdr's own ordering by workspace
        number. Agents whose workspace is unknown to Herdr are kept in a
        trailing group rather than dropped.
        """
        provider = HerdrProvider(HerdrClient(executable))
        agents = provider.list_agents()
        spaces = group_agents_by_workspace(agents, provider.list_workspaces())
        payload = {
            "workers": [self._project_agent(agent) for agent in agents],
            "spaces": [
                {
                    "workspace": space["workspace"],
                    "label": space["label"],
                    "number": space["number"],
                    "status": space["status"],
                    "workers": [self._project_agent(agent) for agent in space["workers"]],
                }
                for space in spaces
            ],
        }
        return render(payload, getattr(args, "format", "text"), lambda _data: self._format_workers(agents, spaces))

    @staticmethod
    def _format_workers(agents: list[dict[str, Any]], spaces: list[dict[str, Any]]) -> str:
        if not agents:
            return "No live Herdr agents."
        lines: list[str] = []
        for space in spaces:
            lines.append(
                f"{space['workspace'] or '-'}  {space['label'] or '-'}  ({len(space['workers'])} workers)"
            )
            for agent in space["workers"]:
                lines.append(
                    f"  {agent.get('pane_id', '')} | {agent.get('agent', '')} | {agent.get('name') or '-'} | {agent.get('agent_status', '')} | {agent.get('cwd') or ''}"
                )
        return "\n".join(lines)

    @staticmethod
    def _project_agent(agent: dict[str, Any]) -> dict[str, Any]:
        """Project one raw Herdr agent onto the stable public worker shape."""
        return {
            "pane": agent.get("pane_id"),
            "kind": agent.get("agent"),
            "name": agent.get("name"),
            "status": agent.get("agent_status"),
            "cwd": agent.get("cwd"),
            "title": agent.get("terminal_title_stripped"),
            "workspace": agent.get("workspace_id"),
            "seq": agent.get("state_change_seq"),
            "focused": agent.get("focused"),
        }


FILE:deskops/cli/registry.py
"""Declarative registry of every deskops CLI command.

The parser in :mod:`deskops.cli.parser` only walks this data; it declares no
command itself. Each command appears exactly once, with its full path, help
text, arguments, handler, and whether it can mutate desk state.

``--help`` output must stay byte-identical to ``tests/fixtures/golden/help``:
argument order, help text, descriptions, epilogs, and formatter choice are all
part of the contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

from sldb.store.layout import project_root

from deskops.cli.model_introspection import DEFAULT_FACTORY
from deskops.cli.model_introspection import REQUIRED
from deskops.cli.model_introspection import artifact_model_fields
from deskops.cli.model_introspection import model_cli_fields
from deskops.errors import UsageError
from deskops.identity import find_context_root
from deskops.identity import find_local_store
from deskops.operations import ARTIFACT_SUBJECTS


ROOT_DESCRIPTION = "deskops: Workflow-domain layer for the hum-ecosystem."
ROOT_EPILOG = """
Typical flow:
  deskops bootstrap
  deskops init .
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest" --task-type task.code
  deskops list tasks --root .
  deskops show task task-fix-thing --root .
  deskops advance task task-fix-thing --root .

A task's type declares how it closes; without --task-type the type is task.code.
When the work is done and the task's references carry that evidence, close it with
`deskops closeout commit --root . --task task-fix-thing --no-run --reason "..."`
(or --run-dir for a subagent run); it verifies the declared evidence first and
makes the closing commit. `deskops doctor --root .` checks the desk afterwards.

Run `deskops faq` for first-use questions; the full walkthrough is docs/quickstart.md
in the deskops repository.
""".strip()

SELECTOR_HELP = "Selectors accept an exact id, filename, stem, or unique slug fragment where supported."


@dataclass(frozen=True, slots=True)
class Arg:
    """One parser argument. Args sharing ``group`` share an exclusive group."""

    flags: tuple[str, ...]
    kwargs: dict[str, Any] = field(default_factory=dict)
    group: str | None = None
    group_required: bool = False


@dataclass(frozen=True, slots=True)
class Command:
    """One command path. ``handler`` is a dotted ``module:attribute`` path."""

    path: tuple[str, ...]
    help: str
    args: tuple[Arg, ...]
    handler: str
    mutates: bool
    epilog: str | None = None
    description: str | None = None
    raw_text: bool = False
    subcommand_dest: str | None = None
    deprecated_for: tuple[str, ...] | None = None


def A(flags: str | tuple[str, ...], **kwargs: Any) -> Arg:
    """Shorthand for an argument declaration."""

    normalized = (flags,) if isinstance(flags, str) else tuple(flags)
    group = kwargs.pop("group", None)
    group_required = kwargs.pop("group_required", False)
    return Arg(
        flags=normalized,
        kwargs=dict(kwargs),
        group=group,
        group_required=group_required,
    )


ROOT_ARG = A("--root", default=".", help="Target repository root.")
ROOT_ARG_NO_PERIOD = A("--root", default=".", help="Target repository root")
ROOT_ARG_MESSAGE = A("--root", default=None, help="Repository root whose desk/ holds the inbox")
ROOT_ARG_INBOX = A(
    "--root",
    help="Repository root whose desk/ holds the inbox; the same --root every other subcommand takes",
)
ROOT_ARG_WHOAMI = A("--root", default=".", help="Repository root to identify")
DESK_ROOT_ARG = A("--desk-root", help="Desk root directory override; defaults to the active project desk")
STORE_ARG = A("--store", help="Store path used to resolve the target project root for the default desk")
REPO_ARG = A("--repo", help="Target a registered repository name in the ecosystem")
PYTHONPATH_ARG = A(
    "--pythonpath",
    help="Project path used when auto-tracking messages through the registered model",
)
PYTHONPATH_INBOX_ARG = A(
    "--pythonpath",
    help="Project path used when auto-tracking inbox notes through a registered InboxNoteDoc model",
)
OUTPUT_FORMAT_ARG = A("--format", choices=("text", "json"), default="text", help="Output format.")
OUTPUT_FORMAT_YAML_ARG = A("--format", choices=("text", "json", "yaml"), default="text", help="Output format.")
HERDR_ARG = A("--herdr", default="herdr", help="Herdr executable.")
RUNTIME_ROOT_ARG = A("--root", default=".", help="Target repository root.")


def _add_subject_commands() -> list[Command]:
    """``deskops add <artifact>`` generated from the Pydantic models."""

    commands: list[Command] = []
    models = artifact_model_fields()
    for artifact_id, meta in ARTIFACT_SUBJECTS.items():
        # Reviews are receipts written by `deskops review` (GC03), never created through
        # the generic add surface; `edit review`/`show review`/`list reviews` still exist.
        if meta.get("create") is False:
            continue
        subject = str(meta["subject"])
        article = "an" if subject[:1] in "aeiou" else "a"
        help_text = f"Create {article} {subject} artifact."
        if subject == "repository":
            help_text = (
                "Create a local repository artifact doc; use 'deskops repo register' "
                "for canonical ecosystem registration."
            )
        args = [
            ROOT_ARG,
            A("--from-yaml", help=f"Load the {subject} payload from a YAML file."),
        ]
        model = models.get(artifact_id)
        if model is not None:
            include_special = artifact_id in {"artifact.task"}
            for fmeta in model_cli_fields(model, include_special=include_special):
                # No model field is argparse-required: --from-yaml may supply it,
                # and the model validates what the payload still misses.
                kwargs: dict[str, object] = {"required": False, "help": fmeta.help}
                if fmeta.is_list:
                    kwargs["action"] = "extend"
                    kwargs["nargs"] = "+"
                    kwargs["default"] = []
                if fmeta.choices:
                    kwargs["choices"] = fmeta.choices
                # Carry the default if set (but not sentinel values)
                if fmeta.default is not None and fmeta.default not in (
                    DEFAULT_FACTORY,
                    REQUIRED,
                ):
                    kwargs["default"] = fmeta.default
                args.append(A(fmeta.cli_option, **kwargs))
        commands.append(
            Command(
                path=("add", subject),
                help=help_text,
                args=tuple(args),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=True,
                epilog=_add_subject_example(subject, model),
                description=help_text,
                raw_text=True,
            )
        )
    return commands


# Sample values for the generated ``deskops add <subject>`` example, by field
# name. Any other required field is shown as "..."; enum fields show their
# first choice. The example must run as printed.
_EXAMPLE_VALUES: dict[str, str] = {
    "title": "Example",
    "name": "example",
    "created_at": "2026-01-01T00:00:00",
}


def _add_subject_example(subject: str, model: type | None) -> str | None:
    """The ``Example:`` epilog, built from the model's required fields."""

    if model is None:
        return None
    parts = [f"deskops add {subject} --root ."]
    for fmeta in model_cli_fields(model):
        if not fmeta.is_required:
            continue
        if fmeta.choices:
            value = fmeta.choices[0]
        else:
            value = _EXAMPLE_VALUES.get(fmeta.name, "...")
        parts.append(f'{fmeta.cli_option} "{value}"')
    return "Example:\n  " + " ".join(parts)


def _list_subject_commands() -> list[Command]:
    commands: list[Command] = []
    for meta in ARTIFACT_SUBJECTS.values():
        kind = str(meta["list_subject"])
        args = [ROOT_ARG]
        if kind == "atoms":
            args.append(
                A(
                    "--axis-value",
                    help="Filter atoms by the configured atom_folder_axis namespace value (e.g. licitaciones).",
                )
            )
        args.append(OUTPUT_FORMAT_ARG)
        commands.append(
            Command(
                path=("list", kind),
                help=f"List {kind}.",
                args=tuple(args),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=False,
            )
        )
    return commands


def _edit_subject_commands() -> list[Command]:
    subjects = ["task", *[str(meta["subject"]) for meta in ARTIFACT_SUBJECTS.values()]]
    return [
        Command(
            path=("edit", subject),
            help=f"Edit one {subject} field.",
            args=(
                A("selector", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}"),
                A("field", help="Model field name to update; hyphens are accepted for underscores."),
                A("value", help="New field value, parsed like an SLDB field value."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
        )
        for subject in subjects
    ]


def _show_subject_commands() -> list[Command]:
    commands: list[Command] = [
        Command(
            path=("show", "task"),
            help="Show one actionable task by selector.",
            args=(
                A("task_id", help=f"Task selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog=f"Example:\n  deskops show task task-fix-thing --root .\n\n{SELECTOR_HELP}",
            raw_text=True,
        )
    ]
    for meta in ARTIFACT_SUBJECTS.values():
        subject = str(meta["subject"])
        commands.append(
            Command(
                path=("show", subject),
                help=f"Show one {subject} by selector.",
                args=(
                    A("doc_id", help=f"{subject.capitalize()} selector. {SELECTOR_HELP}"),
                    ROOT_ARG,
                    OUTPUT_FORMAT_ARG,
                ),
                handler="deskops.cli.commands.operations:OperationsCLI",
                mutates=False,
            )
        )
    return commands


def _operation_shared_commands() -> list[Command]:
    """The ``add/edit/bind/next/list/show/advance`` command group."""

    commands: list[Command] = [
        Command(
            path=("add",),
            help="Create desk workflow artifacts from modeled templates.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog="""
Examples:
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest" --task-type task.code
  deskops add task --root . --title "Document the API" --goal "..." --scope "..." --task-type task.docs
  deskops add pill --root . --title "Guardrail: Keep layers clean" --what "..." --why "..." --when "..." --where "..." --how "..." --how-not "..."

A task's closeout evidence is declared by its type; see `deskops add task --help`.
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("add", "task"),
            help="Create an actionable task bundle.",
            args=(
                A("payload", nargs="?", help="Inline JSON payload for the task."),
                A("--from-yaml", help="Load the task payload from a YAML file."),
                ROOT_ARG,
                A("--title", help="Task title"),
                A("--why", help="Rationale or business driver"),
                A("--goal", help="Task goal"),
                A("--scope", help="Task scope"),
                A("--implementation-path", help="Implementation path"),
                A("--done-when", help="Task completion rule"),
                A(
                    "--from-drawer",
                    help="Drawer file this task is authored from (path, stem, or slug fragment). "
                    "Recorded in the task's from_drawer field; the drawer file is kept for manual cleanup.",
                ),
                A(
                    "--validation",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Validation command or assertion; repeat or space-separate as needed.",
                ),
                A(
                    "--depends-on",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Task identifiers that must complete first; repeat or space-separate as needed.",
                ),
                A(
                    "--task-type",
                    help="Workflow task type; one of the registered types (task.code, task.docs, "
                    "task.debug, task.refactor, task.decision, task.aggregate, task.external, plus any "
                    "desk-local type registered from desk/models/*.py). Defaults to task.code.",
                ),
                A(
                    "--evidence",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Closeout evidence kinds: tests, commit, atom, materialization, document, external. "
                    "The task type declares its own evidence as a floor; --evidence may only add kinds, "
                    "never remove one the type requires.",
                ),
                A(
                    "--inherits-from",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Task identifiers that provide inherited workflow context; repeat or space-separate as needed.",
                ),
                A(
                    "--atom",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Workflow or knowledge atom refs bound to the task; repeat or space-separate as needed.",
                ),
                A(
                    "--inherit-acceptance-context",
                    action="store_true",
                    help="Inherit validation and done-when context from tasks listed in --inherits-from.",
                ),
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog="""
Examples:
  deskops add task --root . --title "Fix thing" --goal "..." --scope "..." --validation "pytest" --task-type task.code
  deskops add task --root . --title "Document the API" --goal "..." --scope "..." --task-type task.docs

The task type declares how the task closes; --evidence only adds kinds to the type's
floor. Without --task-type the type is task.code.
""".strip(),
            raw_text=True,
        ),
        *_add_subject_commands(),
        Command(
            path=("edit",),
            help="Update one field on a modeled desk artifact.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops edit task task-fix-thing goal "Updated goal" --root .
  deskops edit pill pill-keep-layers-clean how-not "Do not bypass the guardrail." --root .

Values are parsed with SLDB's field-value parser and the document is re-rendered through its model.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        *_edit_subject_commands(),
        Command(
            path=("bind",),
            help="Bind workflow context artifacts to tasks.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops bind pill task-fix-thing pill-phase-gate --root .

This updates the task's modeled `pills` list through the deskops artifact layer.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("bind", "pill"),
            help="Bind one pill to one task.",
            args=(
                A("task", help=f"Task selector. {SELECTOR_HELP}"),
                A("pill", help=f"Pill selector. {SELECTOR_HELP}"),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops bind pill task-fix-thing pill-phase-gate --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("next",),
            help="Show the next valid workflow action for a task without mutating it.",
            args=(
                A("task_id", nargs="?", help=f"Task selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                A(
                    "--diagram",
                    action="store_true",
                    help="Render the workflow state machine as Mermaid from its source spec.",
                ),
                A(
                    "--why",
                    action="store_true",
                    help="Explain why this task and these actions were selected.",
                ),
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog="""
Examples:
  deskops next task-fix-thing --root .
  deskops next --diagram
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("list",),
            help="List desk workflow artifacts.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog="""
Examples:
  deskops list tasks --root .
  deskops list pills --root .
  deskops list atoms --root .
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("list", "tasks"),
            help="List actionable tasks.",
            args=(
                ROOT_ARG,
                A(
                    "--include-repos",
                    action="store_true",
                    help="Also list tasks routed by registered sibling repositories' desk/tasks/Board.md files.",
                ),
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
        ),
        *_list_subject_commands(),
        Command(
            path=("show",),
            help="Show one desk workflow artifact by selector.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=False,
            epilog=f"""
Examples:
  deskops show task task-fix-thing --root .
  deskops show pill pill-keep-layers-clean --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        *_show_subject_commands(),
        Command(
            path=("advance",),
            help="Advance an operational artifact through the desk's lifecycle graph.",
            args=(),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement fires the first lifecycle transition (an sldb RelationDoc between rituals) whose condition holds for the task.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="subject",
        ),
        Command(
            path=("advance", "task"),
            help="Advance one actionable task through the desk's lifecycle graph.",
            args=(
                A("task_id", help=f"Task selector. {SELECTOR_HELP}"),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.operations:OperationsCLI",
            mutates=True,
            epilog=f"""
Example:
  deskops advance task task-fix-thing --root .

Advancement fires the first lifecycle transition (an sldb RelationDoc between rituals) whose condition holds for the task.
{SELECTOR_HELP}
""".strip(),
            raw_text=True,
        ),
    ]
    return commands


def _message_target_args(*, root_arg: Arg, repo: bool = True) -> list[Arg]:
    args = [
        root_arg,
        DESK_ROOT_ARG,
        STORE_ARG,
    ]
    if repo:
        args.append(REPO_ARG)
    args.extend([PYTHONPATH_ARG, OUTPUT_FORMAT_YAML_ARG])
    return args


def _commands() -> list[Command]:
    commands: list[Command] = [
        Command(
            path=("about",),
            help="Print a short overview of deskops and its first-use commands.",
            args=(),
            handler="deskops.cli.commands.core:AboutCLI",
            mutates=False,
        ),
        Command(
            path=("doctor",),
            help="Detect and repair common broken desk states safely.",
            description=(
                "Check the desk and report two kinds of findings: errors, which break the desk\n"
                "(exit 1), and alerts, which only mean the store moved under an expected change\n"
                "(always printed, exit 0). Alerts are registered with `deskops desk update --apply`."
            ),
            raw_text=True,
            args=(
                ROOT_ARG,
                A("--repair", action="store_true", help="Attempt non-destructive repairs of errors; alerts are left alone."),
            ),
            handler="deskops.cli.commands.doctor:DoctorCLI",
            mutates=True,
        ),
        Command(
            path=("status",),
            help="Deprecated alias for `deskops doctor`.",
            args=(ROOT_ARG,),
            handler="deskops.cli.commands.doctor:DoctorCLI",
            mutates=False,
            deprecated_for=("doctor",),
        ),
        Command(
            path=("faq",),
            help="Browse the first-use FAQ by question.",
            args=(
                A(
                    "question",
                    nargs="?",
                    help="Question index, slug, or text fragment. Omit to list available questions.",
                ),
                OUTPUT_FORMAT_YAML_ARG,
                A(
                    "--faq-path",
                    default="docs/faq.md",
                    help="FAQ markdown path (default: docs/faq.md; when it does not exist, "
                    "the FAQ packaged with deskops at data/faq.md is used)",
                ),
            ),
            handler="deskops.cli.commands.faq:FAQCLI",
            mutates=False,
        ),
        Command(
            path=("bootstrap",),
            help="Install or repair sldb and register deskops models in the global store.",
            args=(),
            handler="deskops.cli.commands.core:BootstrapCLI",
            mutates=True,
        ),
        Command(
            path=("init",),
            help="Initialize a local .sldb store and scaffold desk/ if needed.",
            args=(A("path", nargs="?", default=".", help="Target repository path"),),
            handler="deskops.cli.commands.core:InitCLI",
            mutates=True,
        ),
        Command(
            path=("inbox",),
            help="Deprecated alias for `deskops message`; use message send/list/read/ack.",
            args=(
                A("message", nargs="?", help="Inbox note body"),
                A(
                    "--kind",
                    choices=("unclear", "suggestion"),
                    default="unclear",
                    help="Type of inbox message to write",
                ),
                A("--title", help="Short title for the note"),
                ROOT_ARG_INBOX,
                DESK_ROOT_ARG,
                STORE_ARG,
                REPO_ARG,
                A("--sender", help="Override the resolved sender identity with a registered project id"),
                PYTHONPATH_INBOX_ARG,
                A("--list", action="store_true", help="List desk inbox notes"),
                A("--show", help="Show one inbox note by filename, stem, or slug fragment"),
                A("--ack", help="Acknowledge one inbox note by filename, stem, or slug fragment"),
                A("--limit", type=int, default=20, help="Limit listed notes"),
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
            deprecated_for=("message",),
            epilog="""
Deprecated: use `deskops message send|list|read|ack`. Each inbox form below
has a `deskops message` equivalent; prefer it.

Examples:
  deskops inbox "Need clearer CLI help" --kind unclear --title "CLI help"
    -> deskops message send "Need clearer CLI help" --kind unclear --title "CLI help"
  deskops inbox --repo sibling-repo --sender current-repo "Need follow-up"
    -> deskops message send "Need follow-up" --to sibling-repo --from current-repo
  deskops inbox --list --root .
    -> deskops message list --root .
  deskops inbox --show 20260614-cli-help --root .
    -> deskops message read 20260614-cli-help --root .
  deskops inbox --ack 20260614-cli-help --root .
    -> deskops message ack 20260614-cli-help --root .

--show/--ack selector: filename, stem, or slug fragment.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("message",),
            help="Send, list, read, or acknowledge cross-desk messages.",
            args=(),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
            epilog="""
Examples:
  deskops message send "Need follow-up" --to sibling-repo --title "Follow-up"
  deskops message list --root .
  deskops message read 20260614-cli-help --root .
  deskops message ack 20260614-cli-help --root .

read/ack selector: filename, stem, or unique slug fragment.
""".strip(),
            raw_text=True,
            subcommand_dest="message_command",
        ),
        Command(
            path=("message", "send"),
            help="Send a message to a project desk.",
            args=(
                A("body", help="Message body"),
                A("--title", help="Short title for the message"),
                A(
                    "--kind",
                    choices=("unclear", "suggestion"),
                    default="suggestion",
                    help="Type of message to send",
                ),
                A("--to", dest="repo", help="Target a registered repository name in the ecosystem"),
                A(
                    "--from",
                    dest="sender",
                    help="Override the resolved sender identity with a registered project id",
                ),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE, repo=False),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
        ),
        Command(
            path=("message", "list"),
            help="List received messages.",
            args=(
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
                A("--limit", type=int, default=20, help="Limit listed messages"),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=False,
        ),
        Command(
            path=("message", "read"),
            help="Read one received message.",
            args=(
                A("selector", help="Message filename, stem, or unique slug fragment"),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=False,
        ),
        Command(
            path=("message", "ack"),
            help="Acknowledge one received message.",
            args=(
                A("selector", help="Message filename, stem, or unique slug fragment"),
                *_message_target_args(root_arg=ROOT_ARG_MESSAGE),
            ),
            handler="deskops.cli.commands.message:MessageCLI",
            mutates=True,
        ),
        Command(
            path=("review",),
            help="Run and dispose cold context reviews (node, preflight, bundle, status, dispose).",
            args=(),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Examples:
  deskops review preflight task-fix-thing --root .
  deskops review bundle task-fix-thing --root .
  deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
  deskops review status task-fix-thing --root .
  deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
  deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .

Every run writes ritual evidence under runs/subagents/<run>/context-review/<key>/<sha>/attempt-N/
and a ReviewDoc receipt under desk/reviews/. `--engine` names a RuntimeProfileDoc under desk/runtimes/
(default runtime-pi-deepseek-flash). An unchanged input is not reviewed again; `--max-attempts` (default 2)
caps good attempts per key unless --force --reason. `record` writes a reproduction, goldens or owner
receipt from evidence the operator names, without calling the model; `dispose` gives it the verdict.
Where no model is available (CI scenarios, the quickstart), `record --kind preflight|bundle --operator`
writes a human receipt that says so.
""".strip(),
            raw_text=True,
            subcommand_dest="review_command",
        ),
        Command(
            path=("review", "node"),
            help="Review the nodes of a drawer dag.yaml (contract, neighbours, and gates).",
            args=(
                A("plan_dir", help="Plan directory that contains dag.yaml (relative to --root or absolute)."),
                A("ids", nargs="*", help="Node ids to review; defaults to every node in the dag."),
                ROOT_ARG,
                A("--engine", help="RuntimeProfileDoc id under desk/runtimes (default runtime-pi-deepseek-flash)."),
                A("--max-attempts", type=int, default=2, help="Maximum good attempts per key (default 2)."),
                A("--force", action="store_true", help="Re-review even when the cap is reached; requires --reason."),
                A("--reason", help="Why this forced re-review runs; recorded in manifest.json and the ReviewDoc."),
                A("--timeout", type=int, default=900, help="Model call timeout in seconds (default 900)."),
                A("--run", help="Run directory name under runs/subagents/ (default a timestamp)."),
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Example:
  deskops review node desk/drawer/plans/gates-por-tipo GC03 --root .
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("review", "preflight"),
            help="Review a task from its TaskDoc alone (before dispatch).",
            args=(
                A("task", help="Task selector."),
                ROOT_ARG,
                A("--engine", help="RuntimeProfileDoc id under desk/runtimes (default runtime-pi-deepseek-flash)."),
                A("--max-attempts", type=int, default=2, help="Maximum good attempts per key (default 2)."),
                A("--force", action="store_true", help="Re-review even when the cap is reached; requires --reason."),
                A("--reason", help="Why this forced re-review runs; recorded in manifest.json and the ReviewDoc."),
                A("--timeout", type=int, default=900, help="Model call timeout in seconds (default 900)."),
                A("--run", help="Run directory name under runs/subagents/ (default a timestamp)."),
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Example:
  deskops review preflight task-fix-thing --root .
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("review", "bundle"),
            help="Review a task with its full cold bundle (routed rituals, pills, atoms, files).",
            args=(
                A("task", help="Task selector."),
                ROOT_ARG,
                A("--engine", help="RuntimeProfileDoc id under desk/runtimes (default runtime-pi-deepseek-flash)."),
                A("--max-attempts", type=int, default=2, help="Maximum good attempts per key (default 2)."),
                A("--force", action="store_true", help="Re-review even when the cap is reached; requires --reason."),
                A("--reason", help="Why this forced re-review runs; recorded in manifest.json and the ReviewDoc."),
                A("--timeout", type=int, default=900, help="Model call timeout in seconds (default 900)."),
                A("--run", help="Run directory name under runs/subagents/ (default a timestamp)."),
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Example:
  deskops review bundle task-fix-thing --root .
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("review", "status"),
            help="Compare current inputs with recorded reviews without calling the model.",
            args=(
                A("target", nargs="?", help="Task selector or plan directory; omit to list every key that has a review."),
                ROOT_ARG,
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=False,
            epilog="""
Example:
  deskops review status task-fix-thing --root .
  deskops review status desk/drawer/plans/gates-por-tipo --root .
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("review", "dispose"),
            help="Write the verdict on one pending review receipt.",
            args=(
                A("review_id", help="Review id (e.g. review-task-fix-thing-preflight-1)."),
                A("--verdict", choices=("accepted", "rejected", "incomplete"), required=True, help="Disposition verdict."),
                A("--reason", required=True, help="Why the review is disposed with this verdict."),
                ROOT_ARG,
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Example:
  deskops review dispose review-task-fix-thing-preflight-1 --verdict accepted --reason "..." --root .
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("review", "record"),
            help="Record a reproduction, goldens, owner, preflight, or bundle receipt from operator evidence (no model call).",
            args=(
                A("task", help="Task selector."),
                A(
                    "--kind",
                    choices=("reproduction", "goldens", "owner", "preflight", "bundle"),
                    required=True,
                    help="Receipt kind; node comes from its own review command. A recorded preflight or bundle is a human receipt (engine human), not a model review.",
                ),
                A(
                    "--evidence",
                    action="append",
                    default=[],
                    help="Existing file inside the root (repeatable); required for every kind but owner.",
                ),
                A("--reason", required=True, help="What the operator checked; recorded in the ReviewDoc."),
                A(
                    "--operator",
                    help="Name of the human who reviewed; required for preflight and bundle, recorded as the receipt's actor.",
                ),
                ROOT_ARG,
                OUTPUT_FORMAT_YAML_ARG,
            ),
            handler="deskops.cli.commands.review:ReviewCLI",
            mutates=True,
            epilog="""
Example:
  deskops review record task-fix-thing --kind reproduction --evidence runs/repro.log --reason "..." --root .
  deskops review record task-fix-thing --kind owner --reason "approved by the owner" --root .
  deskops review record task-fix-thing --kind preflight --operator "Ana" --evidence desk/tasks/task-fix-thing.md --reason "read the contract; no ambiguity" --root .

The receipt is a ReviewDoc with verdict pending, engine human, and input_sha256 over the sorted
evidence files; `deskops review dispose <review-id>` writes its verdict. A preflight or bundle
recorded by hand requires --operator and says "no model available": it is for desks without a
model (CI scenarios, the quickstart), never a stand-in for `deskops review preflight|bundle`.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("promote",),
            help="Promote inbox notes into loose drawer candidates. Drawer items become tasks only by authoring them with `deskops add task`.",
            args=(),
            handler="deskops.cli.commands.promote:PromoteCLI",
            mutates=True,
            epilog=f"""
Examples:
  deskops promote inbox-to-drawer-task 20260614-unclear --root .

{SELECTOR_HELP}
""".strip(),
            raw_text=True,
            subcommand_dest="promote_command",
        ),
        Command(
            path=("promote", "inbox-to-drawer-task"),
            help="Promote one inbox note into a deferred drawer task candidate.",
            args=(
                A("selector", help="Inbox filename, stem, or unique slug fragment"),
                ROOT_ARG_NO_PERIOD,
                A("--title", help="Override the drawer task title"),
            ),
            handler="deskops.cli.commands.promote:PromoteCLI",
            mutates=True,
        ),
        Command(
            path=("drawer",),
            help="Manage deferred drawer entries.",
            args=(),
            handler="deskops.cli.commands.drawer:DrawerCLI",
            mutates=True,
            subcommand_dest="drawer_command",
        ),
        Command(
            path=("drawer", "remove"),
            help="Remove one drawer entry, its tracking, and its bullets on the drawer board.",
            args=(
                A("selector", help=f"Drawer file selector. {SELECTOR_HELP}"),
                ROOT_ARG_NO_PERIOD,
                A(
                    "--force",
                    action="store_true",
                    help="Remove even when a task in desk/tasks/ records the entry in from_drawer.",
                ),
            ),
            handler="deskops.cli.commands.drawer:DrawerCLI",
            mutates=True,
        ),
        Command(
            path=("retire",),
            help="Retire one obsolete desk document that has no dedicated verb, with its reason and refs.",
            args=(
                A("path", help="Path of the file under desk/ to retire (pills, inbox notes, steps, roles, runtimes, faq, logbook, materializations, leftovers)."),
                ROOT_ARG_NO_PERIOD,
                A("--reason", required=True, help="Why the document is obsolete."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Commit (HEAD or an ancestor) or existing path that replaces or resolves it. Repeatable.",
                ),
                A(
                    "--force",
                    action="store_true",
                    help="Retire even when other desk or docs files still reference it.",
                ),
            ),
            handler="deskops.cli.commands.retire:RetireCLI",
            mutates=True,
            raw_text=True,
            epilog=(
                "Example:\n"
                "  deskops retire desk/contexts/pill-old.md --root . \\\n"
                "    --reason \"Describes the retired routine primitives\" --ref a0e00e3\n\n"
                "Tasks, drawer entries, atoms and registry entries keep their own verbs:\n"
                "closeout, drawer remove, atoms delete, repo remove."
            ),
        ),
        Command(
            path=("issue",),
            help="Close and list desk issues.",
            args=(),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=True,
            subcommand_dest="issue_command",
            epilog="""
Examples:
  deskops issue close issue-empty-selector --root . --reason "Fixed by the CLI" --ref abc1234
  deskops issue list --root . --status open

Issues live under desk/issues/ or desk/drawer/issues/. Closing keeps the file and appends a ## Resolution section.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("issue", "close"),
            help="Close one issue with its reason, keeping the file as the trace.",
            args=(
                A("selector", help=f"Issue selector. {SELECTOR_HELP}"),
                A("--reason", required=True, help="Why the issue is closing."),
                A(
                    "--ref",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Commit or path supporting the close; repeat or space-separate as needed.",
                ),
                ROOT_ARG,
                A("--force", action="store_true", help="Close again even when already closed."),
            ),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=True,
            epilog="""
Example:
  deskops issue close issue-empty-selector --root . --reason "Fixed by the CLI" --ref abc1234 --ref deskops/cli

Selector: issue id, filename, stem, or unique slug fragment under desk/issues/ or desk/drawer/issues/.
The issue status is set to closed and a ## Resolution section records Closed, Reason and Refs.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("issue", "list"),
            help="List desk issues with id, status and title.",
            args=(
                ROOT_ARG,
                A(
                    "--status",
                    choices=("open", "closed", "all"),
                    default="all",
                    help="Filter issues by status group.",
                ),
            ),
            handler="deskops.cli.commands.issue:IssueCLI",
            mutates=False,
        ),
        *_operation_shared_commands(),
        Command(
            path=("repo",),
            help="Repository registration and discovery.",
            args=(),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            subcommand_dest="repo_command",
        ),
        Command(
            path=("repo", "register"),
            help="Canonically register a repository in the ecosystem registry and track it in SLDB.",
            args=(
                A("name", help="Human-readable name"),
                A("path", nargs="?", help="Repository root path (relative to ecosystem root or absolute)"),
                A(
                    "--path",
                    dest="path_option",
                    help="Repository root path (relative to ecosystem root or absolute)",
                ),
                A("--id", help="Stable unique ID, defaults to slugified name"),
                A("--description", help="Markdown description"),
                A("--tags", help="Comma-separated tags"),
                A("--store", help="Store path to anchor the registry"),
                A("--pythonpath", help="Python path for model resolution"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            description="Canonically register a repository in the ecosystem registry and track it in SLDB.",
        ),
        Command(
            path=("repo", "whoami"),
            help="Print the canonical project identity for the current repository.",
            args=(
                ROOT_ARG_WHOAMI,
                A("--store", help="Store path to anchor the registry lookup"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=False,
            description="Print the canonical project identity for the current repository.",
        ),
        Command(
            path=("repo", "remove"),
            help="Remove a repository from the ecosystem registry so it can be registered again.",
            args=(
                A("selector", help=f"Repository id, file stem, or repo-<id>. {SELECTOR_HELP}"),
                ROOT_ARG,
                A("--store", help="Store path to anchor the registry lookup"),
            ),
            handler="deskops.cli.commands.repo:RepoCLI",
            mutates=True,
            description="Remove a repository from the ecosystem registry so it can be registered again.",
        ),
        Command(
            path=("desk",),
            help="Desk workspace management.",
            args=(),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
            subcommand_dest="desk_command",
        ),
        Command(
            path=("desk", "install"),
            help="Scaffold a minimal local desk/ surface in a repo.",
            args=(A("path", help="Target repository path"),),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "migrate"),
            help="Adopt a legacy or partial desk into the current non-destructive workspace contract.",
            args=(ROOT_ARG,),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "replace"),
            help="Replace an exact substring in one desk file that has no modeled edit verb.",
            args=(
                A(
                    "path",
                    help="Path of the file under desk/ (desk/... or relative to the desk root).",
                ),
                ROOT_ARG,
                A("--old", required=True, help="Exact text to replace; must occur --count times."),
                A("--new", required=True, help="Replacement text."),
                A(
                    "--count",
                    type=int,
                    default=1,
                    help="Exact number of occurrences of --old to require (default: 1).",
                ),
            ),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("desk", "update"),
            help="Report and repair divergence between the current desk, its models, and its store.",
            args=(
                ROOT_ARG,
                A("--apply", action="store_true", help="Apply repairs (dry run by default)."),
            ),
            handler="deskops.cli.commands.desk:DeskCLI",
            mutates=True,
        ),
        Command(
            path=("atoms",),
            help="Atom model and namespace management.",
            args=(),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
            subcommand_dest="atoms_command",
        ),
        Command(
            path=("atoms", "add-namespace"),
            help="Add an extensible atom tag namespace to desk/atoms/tag-namespaces.yaml.",
            args=(
                A("namespace", help="Namespace name, such as pattern."),
                ROOT_ARG,
                A("--meaning", required=True, help="What this namespace means."),
                A("--use-when", required=True, help="When to use this namespace."),
                A(
                    "--do-not-use-when",
                    required=True,
                    help="When an existing namespace should be preferred instead.",
                ),
                A(
                    "--example",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Example tag using the namespace; repeat or space-separate as needed.",
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "list"),
            help="Deprecated alias for `deskops list atoms`; list all atoms.",
            args=(
                ROOT_ARG,
                A(
                    "--axis-value",
                    help="Filter atoms by the configured atom_folder_axis namespace value (e.g. licitaciones).",
                ),
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
            deprecated_for=("list", "atoms"),
        ),
        Command(
            path=("atoms", "reorganize"),
            help="Move atoms into folders derived from the configured atom_folder_axis tag namespace. Idempotent.",
            args=(
                ROOT_ARG,
                A("--dry-run", action="store_true", help="Report planned moves without changing files."),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "show"),
            help="Deprecated alias for `deskops show atom`; show an atom.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
            deprecated_for=("show", "atom"),
        ),
        Command(
            path=("atoms", "validate"),
            help="Validate one atom or all atoms for lifecycle safety checks.",
            args=(
                A(
                    "doc_id",
                    nargs="?",
                    help=f"Atom selector; required unless --all is given. {SELECTOR_HELP}",
                    group="target",
                    group_required=True,
                ),
                A(
                    "--all",
                    action="store_true",
                    help="Validate all atoms under desk/atoms/.",
                    group="target",
                    group_required=True,
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
        ),
        Command(
            path=("atoms", "create"),
            help="Create one atom from a pill, graph finding, or diagram source while preserving exact provenance.",
            args=(
                A("doc_id", help="New atom id to create, conventionally atom-<slug>."),
                A(
                    "--five-wh-one-plus",
                    required=True,
                    choices=("what", "why", "how", "how_not", "when", "where", "for_whom"),
                    help="The single 5WH1+ question this atom answers.",
                ),
                A("--title", help="Optional title override for the created atom."),
                A(
                    "--tag",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Atom tag to add; repeat or space-separate as needed.",
                ),
                A(
                    "--from-pill",
                    metavar="PILL_ID",
                    help="Create the atom from one pill field chosen by --five-wh-one-plus.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--from-graph",
                    metavar="SOURCE_ID->TARGET_ID",
                    help="Create the atom from one missing graph finding resolved by source and target ids.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--from-diagram",
                    metavar="SPEC_PATH",
                    help="Create the atom from one diagram source file such as docs/diagrams/example/source.mmd.",
                    group="source",
                    group_required=True,
                ),
                A(
                    "--graph",
                    help="Optional graph snapshot path consulted in addition to declared-edge findings when resolving --from-graph.",
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "delete"),
            help="Delete one atom after checking inbound references.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help="Delete even when inbound atom:<id> references are present.",
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "split"),
            help="Split one atom into new atoms while keeping the original as a redirect stub.",
            args=(
                A("doc_id", help=f"Atom selector. {SELECTOR_HELP}"),
                A(
                    "--into",
                    nargs="+",
                    required=True,
                    metavar="NEW_ATOM_ID",
                    help="New atom ids to create from the source atom. Provide at least two.",
                ),
                A(
                    "--section",
                    action="append",
                    default=[],
                    metavar="NEW_ATOM_ID:SECTION_HEADING",
                    help=(
                        "Assign a created atom id to a specific markdown heading inside the source atom answer. "
                        "Repeat once per target. When omitted, sections are assigned to --into ids in order."
                    ),
                ),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help=(
                        "Proceed even when inbound atom:<id> references exist. The original atom is kept as a redirect stub; "
                        "referrers are not rewritten automatically."
                    ),
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "merge"),
            help="Merge one source atom into an existing target atom while rewriting inbound references.",
            args=(
                A("doc_id", help=f"Source atom selector. {SELECTOR_HELP}"),
                A(
                    "--into",
                    required=True,
                    metavar="TARGET_ATOM_ID",
                    help="Existing target atom selector that absorbs the source atom.",
                ),
                ROOT_ARG,
                A(
                    "--force",
                    action="store_true",
                    help=(
                        "Proceed when merge semantics are ambiguous, such as conflicting five_wh_one_plus values. "
                        "Inbound atom:<source> references are rewritten to atom:<target>, and the source atom is kept as a redirect stub for traceability."
                    ),
                ),
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "crossroad"),
            help="Write the crossroad of a domain path: the mandatory parent that describes what hangs below it.",
            args=(
                A(
                    "path",
                    help="Domain path such as pizzeria.carta; its parent path needs a crossroad first.",
                ),
                A("--title", required=True, help="Short title of the domain area."),
                A("--content", required=True, help="Written description of what hangs below this path."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "proto"),
            help="Create a protoatom: a free atom with a title, content and tags.",
            args=(
                A("doc_id", help="New protoatom id, conventionally proto-<slug>."),
                A("--title", required=True, help="Short title of the free knowledge unit."),
                A("--content", default="", help="Free markdown content."),
                A(
                    "--tag",
                    action="extend",
                    nargs="+",
                    default=[],
                    help="Atom tag; a single domain:<path> tag places the protoatom in the domain tree.",
                ),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "type"),
            help="Type a protoatom into another sldb model, keeping the protoatom as a redirect stub.",
            args=(
                A("doc_id", help="Protoatom selector: id or filename."),
                A("--model", required=True, help="Target sldb model name, such as AtomDoc or TaskDoc."),
                A("--id", dest="new_id", help="Id of the typed document; defaults to <model>-<slug>."),
                A(
                    "--content-field",
                    help="Target field that receives the protoatom content; defaults to 'content' when the model has it.",
                ),
                A("--data", help="Inline JSON with the remaining fields the target model requires."),
                ROOT_ARG,
            ),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=True,
        ),
        Command(
            path=("atoms", "tree"),
            help="Show the domain tree: crossroads and the documents hanging from them.",
            args=(ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.atoms:AtomsCLI",
            mutates=False,
        ),
        Command(
            path=("graph",),
            help="Build and inspect deskops KGDB graph runtime outputs.",
            args=(),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
            subcommand_dest="graph_command",
        ),
        Command(
            path=("graph", "build"),
            help="Build the KGDB graph snapshot runtime artifact.",
            args=(
                ROOT_ARG,
                A(
                    "--output",
                    help="GraphSnapshot destination; relative paths are resolved from --root.",
                ),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
        ),
        Command(
            path=("graph", "neighbors"),
            help="Show incoming and outgoing neighbors for one graph node.",
            args=(
                A(
                    "id",
                    help="Graph node id to inspect, formatted as type:id (e.g. atom:atom-name, task:task-name, issue:issue-name).",
                ),
                ROOT_ARG,
                A("--graph", help="Graph snapshot path; defaults to the root runtime snapshot."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=False,
        ),
        Command(
            path=("graph", "missing"),
            help="Report missing graph targets and dangling declared references.",
            args=(
                ROOT_ARG,
                A("--graph", help="Optional graph snapshot path to check for missing edge targets."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=False,
        ),
        Command(
            path=("graph", "reflect"),
            help="Write review-only self-reflection findings for a graph snapshot.",
            args=(
                ROOT_ARG,
                A("--graph", help="Graph snapshot path; defaults to the root runtime snapshot."),
            ),
            handler="deskops.cli.commands.graph:GraphCLI",
            mutates=True,
        ),
        Command(
            path=("materialize",),
            help="Render tracked desk role prompts into installed pi-agent files.",
            args=(
                ROOT_ARG,
                A("--out", help="Output directory override; defaults to ~/.pi/agent/agents."),
            ),
            handler="deskops.cli.commands.materialize:MaterializeCLI",
            mutates=True,
        ),
        Command(
            path=("drift",),
            help="Check for role-agent drift between tracked role docs and installed agent files.",
            args=(),
            handler="deskops.cli.commands.drift:DriftCLI",
            mutates=False,
            subcommand_dest="drift_command",
        ),
        Command(
            path=("drift", "check"),
            help="Compare rendered role-agent output to installed files.",
            args=(
                ROOT_ARG,
                A("--out", help="Agent directory override; defaults to ~/.pi/agent/agents."),
            ),
            handler="deskops.cli.commands.drift:DriftCLI",
            mutates=False,
        ),
        Command(
            path=("closeout",),
            help="Workflow closeout operations.",
            args=(),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            subcommand_dest="closeout_command",
        ),
        Command(
            path=("closeout", "commit"),
            help="Verify the task's declared closeout evidence, then create the tool-made closing commit, "
            "linked to a run evidence directory or marked manual.",
            args=(
                ROOT_ARG,
                A("--run-dir", help="Run evidence dir under runs/subagents/.", group="closing_route"),
                A(
                    "--no-run",
                    action="store_true",
                    help="Close without a subagent run; requires --reason. Use instead of --run-dir.",
                    group="closing_route",
                ),
                A("--reason", help="Why the task closes without a run; required with --no-run."),
                A("--task", required=True, help="Task id being closed."),
                A(("-m", "--message"), help="Commit message subject."),
                A(
                    "--paths",
                    nargs="*",
                    default=None,
                    help="Paths to stage; defaults to run.yaml touched paths, else staged index.",
                ),
                A("--run-id", help="Subagent run id to record in run.yaml (--run-dir only)."),
                A("--session", help="Child session.jsonl path to hash into run.yaml (--run-dir only)."),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout commit --root . --task task-fix-thing \\
    --run-dir runs/subagents/20260729-120000-task-fix-thing \\
    --run-id 6046eaef --session ~/.pi/agent/sessions/<dir>/6046eaef/run-0/session.jsonl \\
    --paths deskops/foo.py tests/test_foo.py

Without a subagent run, close the task manually and say why:
  deskops closeout commit --root . --task task-fix-thing \\
    --no-run --reason "Fixed by the supervisor directly; no subagent was dispatched" \\
    --paths deskops/foo.py tests/test_foo.py

Gate: for a task routed on desk/tasks/Board.md (as `deskops add task` leaves
it) the command first runs the same check as `deskops closeout verify`. The
task's type declares which kinds the task must show (its own non-empty
closeout_evidence overrides it): tests, commit, atom|materialization, document,
external. Each kind is looked up in the task's references (and files, for
documents); the result is printed as one line,
"esta tarea declaró X; encontró Y" (declared X; found Y). If any declared kind
is missing the command stops and no commit is made. Alerts (ALERTA ...) are
printed but do not block.

With --run-dir the commit message carries Task-Id/Run-Dir/Run-Id/Session-Sha256
trailers; with --no-run it carries Task-Id/Closeout-Mode: manual/Closeout-Reason.
Either way an index entry is recorded back into runs/subagents/index.jsonl
and committed with the closing commit; it names the task and run, and the
commit hash is resolved from the commit's Task-Id trailer. The commit is made
by this command, not by agent discretion.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "supersede"),
            help="Close a task whose subject no longer exists, naming a reason and a resolvable ref.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being closed."),
                A("--reason", required=True, help="Why the task's subject no longer exists."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Ancestor commit id or existing path; repeat for more refs.",
                ),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout supersede --root . --task task-fix-thing \\
    --reason "The owner deleted the target feature in 9f64f0f; there is nothing left to do" \\
    --ref 9f64f0f

Supersede skips the evidence gates, because no run, test, or atom describes
work that was never done. It still makes exactly one closing commit: status and
history record `superseded`, the commit carries Closeout-Mode: superseded with
Closeout-Reason and one Closeout-Ref per ref, the task leaves the Board, and
the run index entry is marked superseded.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "retire"),
            help="Remove a task that was already resolved before the ritual lifecycle.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being retired."),
                A("--reason", required=True, help="Why the task is already resolved."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Ancestor commit id that resolved the task; repeat for more refs.",
                ),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout retire --root . --task task-fix-thing \\
    --reason "Resolved before the ritual lifecycle existed" \\
    --ref 3900ad4

Retire removes a task whose status is already resolved, closed, done or
complete, as pre-lifecycle tasks are. The ref must be a commit that is HEAD or
an ancestor. The status is not rewritten and the evidence gates do not run. It
makes exactly one closing commit: the task leaves the Board, the commit carries
Closeout-Mode: legacy-resolved with Closeout-Reason and one Closeout-Ref per
ref, and the run index entry is marked legacy-resolved.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "resolved-by"),
            help="Close a task whose work already entered the history, naming an ancestor commit and a test.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being closed."),
                A("--reason", required=True, help="Where the task's work entered the history."),
                A(
                    "--ref",
                    action="append",
                    required=True,
                    help="Ancestor commit id or http(s) URL (the PR); at least one commit; repeat for more refs.",
                ),
                A(
                    "--test",
                    action="append",
                    required=True,
                    help="Test file the tests gate accepts; repeat for more tests.",
                ),
                A(("-m", "--message"), help="Commit message subject."),
                A("--paths", nargs="*", default=None, help="Extra paths to stage into the closing commit."),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=True,
            epilog="""
Example:
  deskops closeout resolved-by --root . --task task-fix-thing \\
    --reason "The fix entered main through PR #42 before the closeout" \\
    --ref 9f64f0f --ref https://example.com/org/repo/pull/42 \\
    --test tests/test_fix_thing.py

Resolved-by closes a task whose work is already committed, so it does not ask
for an atom per changed file. At least one --ref must be a commit that is HEAD
or an ancestor; the others may be ancestor commits or http(s) URLs. At least
one --test is required, and every test must be an existing .py file the tests
gate accepts (under a tests/ directory or declared in the task's files). A
refusal writes nothing. It makes exactly one closing commit: status `resolved`
and history `resolved-by`, the commit carries Closeout-Mode: resolved-by with
Closeout-Reason, one Closeout-Ref per ref and one Closeout-Test per test, the
task leaves the Board, and the run index entry is marked resolved-by.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("closeout", "verify"),
            help="Check the closeout evidence the task declared, without committing; print a structured report.",
            args=(
                ROOT_ARG,
                A("--task", required=True, help="Task id being verified."),
            ),
            handler="deskops.cli.commands.closeout:CloseoutCLI",
            mutates=False,
            epilog="""
Example:
  deskops closeout verify --root . --task task-fix-thing

The gate checks exactly the kinds the task's type declares (its own non-empty
closeout_evidence overrides it): tests, commit, atom|materialization, document,
external. Each kind is looked up in the task's references (and files, for
documents). A task with no type and no field predates the types and is gated as
code, with an alert.

Output: stdout carries a JSON report (declared, found, per-gate findings,
alerts, ok, summary); stderr carries the one-line summary "esta tarea declaró
X; encontré Y" (declared X; found Y) and any ALERTA lines. Exit 0 when
everything declared was found, else 1.
`deskops closeout commit` runs this same gate before committing.
""".strip(),
            raw_text=True,
        ),
        Command(
            path=("view",),
            help="Read-only views of this desk for the deskops UI (contract: docs/deskops-ui.md).",
            args=(),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
            subcommand_dest="view_command",
        ),
        Command(
            path=("view", "board"),
            help="Board view: one column per lifecycle node with task cards, gates, closeout evidence, pills and atoms.",
            args=(ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
        ),
        Command(
            path=("view", "task"),
            help="Task view: the board card plus the TaskDoc sections, next actions and the advance revision.",
            args=(A("task_id", help=f"Task selector. {SELECTOR_HELP}"), ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
        ),
        Command(
            path=("view", "drawer"),
            help="Drawer view: deferred tasks in desk/drawer/tasks with excerpt and the add task --from-drawer command.",
            args=(ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
        ),
        Command(
            path=("view", "inbox"),
            help="Inbox view: notes in desk/inbox with sender, target, date, ack state and body.",
            args=(ROOT_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
        ),
        Command(
            path=("view", "agents"),
            help="Agents view: live Herdr workers and the latest runs of runs/subagents/index.jsonl.",
            args=(
                ROOT_ARG,
                HERDR_ARG,
                A("--runs", type=int, default=20, help="How many of the latest run index entries to include."),
                OUTPUT_FORMAT_ARG,
            ),
            handler="deskops.cli.commands.view:ViewCLI",
            mutates=False,
        ),
        Command(
            path=("runtime",),
            help="Manage the live Herdr runtime for this DeskOps desk.",
            args=(),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
            subcommand_dest="runtime_command",
        ),
        Command(
            path=("runtime", "init"),
            help="Initialize or reuse this desk's Herdr Space.",
            args=(
                RUNTIME_ROOT_ARG,
                A("--agents", action="store_true", help="Start executor and tester Pi agents."),
                HERDR_ARG,
            ),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
        ),
        Command(
            path=("runtime", "status"),
            help="Show this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "attach"),
            help="Focus this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "stop"),
            help="Close this desk's Herdr Space.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
        ),
        Command(
            path=("runtime", "workers"),
            help="List live Herdr agents across all workspaces on this machine.",
            args=(RUNTIME_ROOT_ARG, HERDR_ARG, OUTPUT_FORMAT_ARG),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "supervise"),
            help="Block on one agent's Herdr lifecycle and report blocked/done settles without advancing the desk.",
            args=(
                A("agent", help="Herdr agent name or pane id to supervise, e.g. deskops-executor."),
                RUNTIME_ROOT_ARG,
                HERDR_ARG,
                A(
                    "--max-iterations",
                    type=int,
                    default=None,
                    help="Stop after this many settle events instead of running forever (mainly for testing).",
                ),
                A(
                    "--read-lines",
                    type=int,
                    default=200,
                    help="Terminal lines to capture from the agent on a blocked or done settle.",
                ),
                A(
                    "--timeout-ms",
                    type=int,
                    default=None,
                    help="Give up waiting after this many milliseconds per settle attempt (default: wait indefinitely).",
                ),
            ),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=False,
        ),
        Command(
            path=("runtime", "template"),
            help="Materialize a RoleDoc + RuntimeProfileDoc as a Scion agent template (scion-agent.yaml, system-prompt.md, agents.md).",
            args=(
                A("role_id", help="RoleDoc id or name, e.g. role-deskops-executor or deskops-executor."),
                RUNTIME_ROOT_ARG,
                A(
                    "--harness",
                    default=None,
                    help="Scion harness-config / runtime kind to target (claude, codex, antigravity, pi); defaults to the role's kind.",
                ),
                A("--out", default=None, help="Template directory; defaults to <root>/.scion/templates/<role-name>/."),
                A(
                    "--model-alias",
                    choices=("small", "medium", "large", "extra-large"),
                    default="medium",
                    help="Portable Scion model size alias written to the template (the harness-config resolves it).",
                ),
                A("--task-repo", default=None, help="Repository under /workspace the agent may write to; named in agents.md."),
                A(
                    "--mode",
                    choices=("executor", "coordinator"),
                    default=None,
                    help="Which agents.md to write: executor (one bounded task) or coordinator (owns a desk). Default: by role name.",
                ),
                A("--task", default=None, help="Task id being dispatched; with --agent, also records a RunDoc under runs/subagents/."),
                A("--agent", default=None, help="Scion agent slug for the RunDoc (what you pass to `scion start`)."),
                A(
                    "--task-root",
                    default=None,
                    help="Repository root whose desk owns --task; the RunDoc is written there (defaults to --root).",
                ),
                A(
                    "--run-dir",
                    default=None,
                    help="Existing evidence directory (relative to the task root) the RunDoc points at; defaults to a new runs/subagents/<ts>-<task> path.",
                ),
            ),
            handler="deskops.cli.commands.runtime:RuntimeCLI",
            mutates=True,
        ),
    ]
    return commands


def command_registry() -> tuple[Command, ...]:
    """Return every command in declaration order (parents before children)."""

    return tuple(_commands())


def command_for_path(path: tuple[str, ...]) -> Command:
    """Look up one command by its full path."""

    for command in command_registry():
        if command.path == path:
            return command
    raise KeyError(path)


def resolve_context(args: Any) -> tuple[Path, Path | None]:
    """Resolve one ``(desk_root, store)`` pair for every command.

    ``--root`` sets the desk root and ``--store`` sets the store. When both are
    given they must agree (the store must be ``<root>/.sldb``). With neither,
    the upward walk stops at the nearest ancestor containing ``desk/`` or
    ``.git``; the store is that boundary's ``.sldb`` only, never an ancestor's.
    """
    root_arg = getattr(args, "root", None)
    store_arg = getattr(args, "store", None)
    root_given = bool(
        getattr(args, "_deskops_root_explicit", False)
        or getattr(args, "_deskops_root_override", False)
        or root_arg not in (None, "", ".")
    )
    store_path = Path(store_arg).expanduser().resolve() if store_arg else None

    if root_given:
        root = Path(root_arg).expanduser().resolve() if root_arg else Path.cwd().resolve()
        if store_path is not None:
            expected = (root / ".sldb").resolve()
            if store_path != expected:
                raise UsageError(
                    f"--root '{root}' and --store '{store_path}' disagree; "
                    f"when both are given the store must be '{expected}'."
                )
        else:
            store_path = find_local_store(root)
        return root, store_path

    if store_path is not None:
        return project_root(store_path), store_path

    root = find_context_root()
    return root, find_local_store(root)


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


FILE:desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:17Z'
  authority: generated
  via: create_document
id: atom-cheap-zero-context-reviews-test-the-brief-recursively
title: Cheap zero-context reviews test the brief recursively
five_wh_one_plus: how
tags:
- system:deskops
- topic:workflow
- topic:subagents
- topic:context-review
---

# Cheap zero-context reviews test the brief recursively

## Answer

Before promoting or executing work, test the quality of the question with a cheap, ephemeral, zero-context reviewer. Supply only the exact versioned brief and explicitly necessary references: no chat history, previous reviews, oral fixes, persistent memory, automatic skills or context files. The reviewer restates the objective, lists ambiguities, and describes a detailed dry-run of readings, proposed changes, dependencies and validation without executing commands or editing sources. The coordinator compares this with the owner's intent, corrects the written brief and recursively splits oversized nodes into children with explicit dependency edges. Review the root, packages and every leaf, including their interfaces and edges; a root review never covers all descendants. Retry each changed input in a fresh process. Unresolved ambiguity blocks execution; an APTO label is insufficient.

TaskDoc-only preflight and cold-bundle coverage review remain distinct cheap comprehension gates before Executor dispatch. Expert council review, execution and independent implementation testing are separate roles and evidence; expert capability cannot rescue or approve a failed cheap brief review. A transport/quota failure is technical evidence, not proof of ambiguity. Record per-node/input/attempt evidence under runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/: exact input bytes and SHA-256, chosen cheap provider/model/profile and selection reason, command/isolation flags, reformulation/ambiguities/dry-run, coordinator comparison and required edits. Keep TaskDoc-only reformulation in preflight.md. New input or a changed dependency contract invalidates affected reviews; unrelated typos do not invalidate every review. This is a documented gate, not runtime enforcement or human product approval. See [context-review ritual](../../rituals/context-review.md).
