FILE:desk/tasks/task-ws03-inventariar-persistencia-consultas-y-notaciones.md
---
id: task-ws03-inventariar-persistencia-consultas-y-notaciones
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/cierre.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- runs/subagents/20261031-ws02-04-checkpoint/activation.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws03.md
closeout_evidence:
- commit
- document
---

# WS03: Inventariar persistencia, consultas y notaciones

## Rationale

_Explain why this task exists or the business driver behind it._

Primera capa real del núcleo del plan workspace (cierre.md). Activada por runs/subagents/20261031-ws02-04-checkpoint/activation.md; las auditorías alimentan WS06 y WS08-12 con datos comprobados.

## Goal

_Describe the concrete result this task must produce._

Producir desk/drawer/plans/workspace-documental/auditoria/infraestructura.md como auditoría de solo lectura del estado actual, verificable fila por fila.

## Scope

_State what is in scope and what is out of scope._

Auditoría de solo lectura de sldb/pron/spec2viz: fuente/payload, conflictos y límites de locks (control de concurrencia real de sldb/pron: CAS por revisión/hash, locks de archivo o DB; a auditar), referencias documentales, búsquedas (índices o consultas expuestas) y alcance real ViewDoc. Kimun solo referencia. Solo lectura fuera del entregable. Rutas de lectura: ../sldb, ../pron, ../spec2viz. Kimun no se usa como fuente de decisión. Se escribe únicamente desk/drawer/plans/workspace-documental/auditoria/infraestructura.md y evidencia en runs/subagents/20261031-ws03-auditoria-infraestructura/. No se modifica código, otro repo, dag.yaml, reconciliacion.md, Board ajeno ni tareas de otros. Fuera de alcance: WS05 Scion, contratos nuevos, implementación.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer fuentes actuales. 2. Escribir desk/drawer/plans/workspace-documental/auditoria/infraestructura.md: encabezado con fecha, commit HEAD de cada repo leído y universo auditado; luego las filas. 3. Registrar comandos usados en runs/subagents/20261031-ws03-auditoria-infraestructura/commands.log. 4. Dejar runs/subagents/20261031-ws03-auditoria-infraestructura/result-summary.md (qué se hizo, huecos, qué revisar). Lo no comprobado se marca «no comprobado» con causa: no se infiere. El Executor no hace commits, no escribe en desk/ salvo desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, y no corre closeout.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente muestrea filas contra la fuente citada y deja runs/subagents/20261031-ws03-auditoria-infraestructura/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Una salida documental, sin cambios interrepo; distinguir API comprobada (lectura citada del estado actual), ausencia y hueco.

FILE:desk/rituals/execution.md
---
sldb:
  by: agent
  at: '2026-10-31T04:05:19Z'
  authority: generated
  via: update_document
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

FILE:desk/drawer/plans/workspace-documental/cierre.md
# Plan final del workspace documental

Este paquete termina la planificación; no entrega producto ni activa ejecución. `dag.yaml` mantiene `execution_authorized=false`; las fichas generadas siguen `candidate`, no son TaskDoc. Reviews baratos prueban comprensión de cada encargo, y el concilio y Tester emiten dictámenes separados. Ningún resultado sustituye promoción, pruebas reales ni aceptación humana del producto.

La base acordada es extender Mindmap con SLDB/pron y Deskops, lectura y operación manual primero, sin migración Kimun. Markdown será editable después de probar API reversible, conflictos, recuperación y campos protegidos; guardar no hace commit. Con otro coordinador escritor, la UI permanece en lectura/handoff hasta canal público coordinado real. El solicitante es responsable de producto/recepción de deltas en graph_ui, SLDB y spec2viz, y participante de Taller con objetivos abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s. Las tres respuestas exactas, fecha, actor y origen están en decisiones.md y owner-decisions.json del run. P07/P09 son defaults técnicos delegados documentados, sin firma humana inventada.

## Qué existe y qué queda

Workspace no es draft: a1b2b22 implementa lector IR/payload, catálogo modelado, contexto, grafo 1–2 hops, Code seguro e historia URL; f16fcd1 registra cierre y 134a665 reconcilia Board. `reconciliacion.md` delimita cada delta WS13/hijos, WS14/15/19/22–24/27–29/32. Faltan comprobaciones ampliadas como Markdown no modelado/fuente, explorador, pestañas documentales/splits, búsqueda backend, editores con conflicto, diff/evidencia y recorridos completos. Editing y Changes siguen drafts con hashes actuales. No volver a implementar base ni asumir que todos esos deltas estén aceptados por existir un commit.

Brief/glosario WS01 ya están documentados en esta tarea y tienen recibo de cobertura en DAG. La parte de decisión de WS07 también está cubierta por respuestas humanas y mapeo Pxx; resta verificar su aplicación contra auditorías/matriz WS06, sin volver a preguntar lo decidido. Cobertura documental no afirma lifecycle de candidatas cerrado. Inventarios amplios WS02–04 y matriz/contratos WS06/08–12 aún deben ejecutarse como tareas propias; esta auditoría acotada no los sustituye.

G_CLOSEOUT depende de evidencia focalizada actual del contrato de evidencia declarada y vínculo exacto task→commit, con recibos históricos verificables; no exige un nuevo sistema de autenticación. Su estado/recibo exacto en DAG es autoridad. Gate satisfecho no convierte verify en ejecutor de tests ni demuestra funcionalidad del workspace. Riesgos de suite histórica se registran sin afirmar suite global verde ni arreglar producto.

## Secuencia por entregas

1. Verificar cobertura documental WS01 al preparar el trabajo; promover auditorías pendientes WS02–04 con archivos, pills/átomos y validación. WS05 inventario Scion es ramal posterior y no bloquea núcleo. Consolidar WS06 y comprobar registro WS07 reutilizando las decisiones dadas; WS08–12 concretan flows/vistas/manual/identidad/operaciones sobre APIs reales.
2. Entrega L: recepción de cada delta lector, base reutilizada y deltas WS13–15, corpus Taller WS40, multidesk read-only WS41 y recorrido humano WS16. Ninguna dependencia de edición, Changes, modelos, Scion o ViewDoc opcional.
3. Entrega M: whitelist y recepción por delta/efecto, campos/conflictos WS19, raw-source WS20/G_SOURCE y WS21, representaciones WS22–24, captura WS25, autoría WS26, diff/evidencia WS27, cierre por handoff WS28, conocimiento WS42. Desarrollo/pruebas aisladas de API pueden avanzar con sus contratos; habilitar mutaciones en UI requiere G_HUMAN_READ. WS17 aporta entradas authored; WS30 acepta el recorrido, WS43 publica entradas reales y WS31 el manual con evidencia.
4. Extensiones independientes: WS18 ViewDoc/spec2viz se recibe por su propio delta y se añade sin bloquear navegación base WS24. WS29 Changes y WS39 modelos tienen pruebas/etiquetas propias. Sus capítulos permanecen propuestos hasta evidencia, sin frenar manual básico.
5. Ramal E posterior: WS05/44 inventario y probe real, operador/acceso designados al abordarlo, G_SCION; WS32–38 intento/trazabilidad/acciones/UI y aceptación con permisos explícitos G_EXEC. Ninguna respuesta de núcleo concede esos permisos ni autoriza mensajes.

## Primera capa preparable y responsables

La verificación semántica distingue dependencias documentadas de tareas cerradas: WS01 está cubierto por el brief actual (hash/recibo), no se reescribe. La primera capa real preparable del núcleo es WS02, WS03 y WS04; WS05 puede prepararse separadamente como inventario posterior sin acceso obligatorio. Revisar no solapamiento, fuentes actuales, recepción y gates antes de authorar TaskDoc en repo dueño; ninguna ficha por sí sola permite ejecutar. La salida de validate_plan.py informa esta preparación, nunca autorización de producto.

El solicitante decide producto y acepta alcance por delta. Supervisor del repo dueño promueve la TaskDoc completa; Executor produce pruebas/código/contratos; el receptor registra acta técnica por IDs/efecto/fecha/commit en su repo. Humano participante acepta recorridos Taller: agentes preparan y miden, no firman como usuario. Supervisor integra/cierra tareas/fases y conserva Tester independiente; Scion requiere operador y permisos futuros expresos.

## Manual, vistas, recorridos y evidencia

`borradores/vision.md`, `user-flows.md`, `vistas.md` y `manual.md` son contratos por contrastar, no manual de un producto disponible. `cobertura.md` traza UF01–10; `validacion-humana.md` fija Taller, dos desks y repo sin desk, mediciones y actas por rebanada. WS09 cataloga vistas, WS11/12 contratos, WS31 publica solo pasos comprobados y WS38 añade delegación demostrada. Actas humanas y recepción viven en repo dueño con commit/blob; este paquete guarda planificación y enlaces. Cualquier capacidad desconocida se clasifica y asigna a productor/repositorio antes de implementar, sin workaround.

Para empezar producto faltan tareas activas completas, auditorías/contratos actuales, recepción y pruebas del delta concreto, gates aplicables, capa sin solapamiento y ejecución/testing/cierre explícitos. `G_PRODUCT` y `G_WRITE_POLICY` solo registran acuerdos. `G_SOURCE`, actas de lectura/manual/modelos/delegación, contratos técnicos y permisos siguen exactamente el estado del DAG. No se anuncia producto disponible por terminar este plan.

FILE:desk/drawer/plans/workspace-documental/brief.md
# Brief autosuficiente y glosario — base final de planificación

## Encargo y acuerdos explícitos del solicitante

La persona solicita un DAG que cubra el workspace documental, sus vistas/renderizaciones, manual y user-flows; el encargo actual finaliza planificación con decisiones humanas registradas. Esto autoriza corregir el plan, no implementar la UI ni modificar tareas de otras sesiones.

Extractos textuales que delimitan intención, conservados aquí para no depender del historial:

> «cada documento es simplemente un markdown ... cada vista es basicamente una renderizacion»

> «nos faltan documentos para hacer el ecosistema realmente navegable o no?»

> «ahora si estamos en la misma pagina ... como te imaginas que un humano usaria esto?»

La última respuesta siguió al paralelo con Org-mode/Obsidian/IDE: exploración, lectura y edición sobre un proyecto. No se aprobó por ello una lista específica de pantallas, permisos, backend nuevo o cierre por HTTP. La crítica a la primera pestaña Deskops invalida usar esa pestaña como especificación suficiente del producto; no borra las capacidades reutilizables de Mindmap.

## Vocabulario

- **Documento**: archivo Markdown authored, con identidad de resolución; puede tener contrato estructurado o no. Renderizado/fuente no son dos copias.
- **Nodo**: elemento del grafo; puede corresponder a documento, modelo, sección, símbolo u otro soporte. No toda entidad runtime es Markdown.
- **Vista de trabajo**: selección de contenido más forma de presentarlo en el workspace. No implica página ni archivo nuevo.
- **Renderización/representación**: transformación visible del soporte; la edición se dirige a su origen y autoridad.
- **Renderer**: pieza de la UI que materializa una representación.
- **Proyección de grafo ViewDoc**: contrato existente de spec2viz para nodos por modelo/predicado, relaciones, dirección y notación/layout. No define por sí mismo formularios, tabs o tableros.
- **Composición**: representación que reúne contenido de varios documentos; cada edición va al documento dueño de ese contenido.
- **Consulta**: selección derivada evaluada por infraestructura; no un inventario authored duplicado. No se promete modelo de consulta guardada sin prueba de WS03.
- **Foco**: elemento seleccionado por una persona, compartido entre representaciones del mismo documento; no selección compartida entre usuarios.
- **Historia de navegación**: abrir/volver y documentos abiertos. Distinta de historial Git o decisiones de workflow.
- **Disposición**: pestañas, divisiones y preferencias locales. No datos de dominio ni registro compartido por defecto.

## Términos del desk y de operación

- **Drawer / candidato**: trabajo capturado en desk/drawer/; un candidato no es tarea hasta autorarlo con `deskops add task`.
- **Inbox**: mensajes entrantes en desk/inbox/; ack registra recepción, no aceptación del trabajo.
- **Protoátomo**: átomo libre con título y contenido, aún sin clasificar (`deskops atoms proto`).
- **TaskDoc / Board**: tarea modelada y su lista de enrutamiento; enrutar es añadirla al Board.
- **RitualDoc, StepDoc, lifecycle**: procedimiento, pasos y grafo de transiciones del desk.
- **Fase y capa lista**: tareas sin dependencias pendientes ni archivos solapados, según el ritual de fase.
- **Soporte / origen**: archivo o dato real que respalda una representación, y su ruta o referencia.
- **Revisión / before-image**: hash con que una escritura prueba que partió del estado actual; si no coincide, se rechaza.
- **Modo degradado**: el backend o una dependencia falla y la UI sigue mostrando lo que puede, declarando el límite.
- **Capability**: operación concreta con su canal y efectos.
- **Handoff**: la UI prepara una acción y la deja a otro canal o actor; no equivale a hecha.
- **Intento / RunDoc / manifiesto**: una ejecución de un agente sobre una tarea, su documento y su registro canónico.

## Criterio de éxito

Una persona puede entrar, comprender un desk, navegar conocimiento/trabajo/procedimientos, editar por canales autorizados y revisar evidencia sin reconstruir rutas o relaciones de memoria. Una sesión sin agentes es válida. Agentes y trazabilidad son otro ramal, no el centro obligatorio de la UI.

## Estado de las decisiones

Ver decisiones.md. El núcleo ya está registrado en decisiones.md y owner-decisions.json. WS07 verifica/reutiliza ese registro, no vuelve a pedir firmas. La decisión de producto no acredita APIs, recepción técnica, actas de uso ni permisos Scion.

