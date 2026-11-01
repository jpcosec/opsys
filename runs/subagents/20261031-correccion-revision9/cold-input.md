FILE:desk/tasks/task-corregir-revisión-9-del-plan-workspace-tras-revisión-root.md
---
id: task-corregir-revisión-9-del-plan-workspace-tras-revisión-root
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-correccion-revision9/review-source.md
- runs/subagents/20261031-ajuste-canonico-ws06/handoff.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-correccion-revision9/comparison-ledger.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-revision-9-del-plan-tras-revision-root.md
closeout_evidence:
- commit
- document
---

# Corregir revisión 9 del plan workspace tras revisión root

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aceptó cuatro decisiones pero no aprobó la revisión 9: un contrato incondicional, una interfaz sin productor, un dry-run faltante y una atribución de revisión que no ocurrió. Fuente: runs/subagents/20261031-correccion-revision9/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Corregir esos cuatro puntos con evidencia sincera y dejar el plan con build --check, validate --check y status en verde, sin implementar nada.

## Scope

_State what is in scope and what is out of scope._

Planificación en deskops. Archivos: desk/drawer/plans/workspace-documental/dag.yaml y sus proyecciones generadas, evidencia en runs/subagents/20261031-correccion-revision9/ y disposiciones nuevas o atestaciones en runs/subagents/20261031-workspace-context-reviews/context-review/. runs/subagents/20261031-correccion-revision9/review-source.md es contrato obligatorio.

Punto 1. En la aceptación de WS12, la cláusula que mantiene a WS21 bloqueado pasa a decir G_PAYLOAD_PRECONDITION y, solo en variante editable, G_SOURCE. No cambia P04, ni añade gate ni actor.

Punto 2. WS12 asume en su aceptación producir, para el ramal E, la política y el umbral de timeout de dispatch y reply y su clasificación observable, como sección de contrato por delta. Sin elegir duración ahora, sin bloquear el cierre del contrato núcleo y sin permisos ni red nuevos. WS34.1 y WS34.2 declaran que solo avanzan con esa política aplicable y probada en el contrato de su delta. No se modifican los gates.

Punto 3. WS19.1 recibe un proceso barato nuevo que reformule y describa cambios futuros concretos de campos, consumo de precondición, bloqueo de campos protegidos, buffer y conflicto, y validación, sin ejecutar. El intento anterior se conserva sin crédito. No se inyecta su salida ni se rescata con experto. Si solo cambia la instrucción, se registran bytes y argv y no se usa el runner cuando devolvería answered.

Punto 4. Las disposiciones existentes se conservan: dicen revisado por el coordinador sin que esa revisión ocurriera nodo por nodo. Se escribe runs/subagents/20261031-correccion-revision9/comparison-ledger.md con supersesión fechada y, por cada nodo final: rol y actor real, sha de input, output y disposición, alcance de la comparación, resultado y fecha. El coordinador compara de verdad output y disposición finales de todos los nodos y asume la aceptación; el ledger dice exactamente qué leyó. Los defectos hallados se corrigen, no se waivan.

Además: result-summary.md de la consolidación afirma que WS42 no guarda payload por campos, y eso es falso; se corrige con nota fechada. WS42 sale de la justificación por tener guardas y contrato propios y WS19 transitivo, sin forzar un gate universal. promotion-notes.md se actualiza: no da por futuro lo que no tiene productor.

Roles: el Supervisor edita contratos, que la revisión root aceptó; corre revisiones, compara, firma el ledger, valida y cierra. Un agente puede preparar borradores, y el ledger lo dice. Un Tester independiente de solo lectura verifica los cuatro puntos y el cambio protector de G_SOURCE.

Fuera de alcance: código, validadores salvo fallo real con tarea específica, decisiones P01-P09, auditorías, reconciliacion.md salvo que un punto lo exija, WS07, WS08-12, UI, Scion, push.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Editar WS12, WS34.1 y WS34.2. 2. Regenerar y congelar. 3. Correr revisiones de los afectados según hashes. 4. Revisión nueva de WS19.1. 5. Comparar todos los nodos finales y corregir lo que aparezca. 6. Registrar context_review y ledger. 7. Tester. 8. Closeout y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- test -s runs/subagents/20261031-correccion-revision9/comparison-ledger.md
- git diff --name-only 5f05281c..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/decisiones.md desk/drawer/plans/workspace-documental/auditoria/ desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py desk/drawer/plans/workspace-documental/context_review.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-revision9/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

WS12 condiciona G_SOURCE a la variante editable; WS12 produce la política de timeout y WS34.1 y WS34.2 dependen de ella sin bloquear el núcleo; WS19.1 tiene dry-run real; cada nodo final tiene comparación verdadera en el ledger; build --check, validate --check y status en verde; y un Tester independiente da PASS.

FILE:runs/subagents/20261031-correccion-revision9/review-source.md
# Revisión root de la revisión 9, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31.

Verificado por root: build/validate/status PASS; 73 inputs reconstruidos byte a byte, contratos/hashes/ordered_sources/outputs/recibos/DEVNULL/flags, 73 PID únicos y versión 0.67.3. Ningún cambio en los tres validadores, código, auditorías ni decisiones. Esto NO basta para aceptar comprensión si una disposición waivera un dry-run faltante.

Cuatro decisiones del handoff ACEPTADAS: (1) WS21 consume precondición payload porque ambas variantes editan campos; (2) la autorización local Deskops no inventa receptor ni firma nueva; (3) criterios origen/sin tarea activa/colisiones para falta de conducta workflow son adecuados; (4) correcciones de brief/contrato por Supervisor están autorizadas por TaskDoc punto 5. No hace falta otro Executor para repetir esa redacción solo por rol. WS42 sí modifica payload, pero tiene guardas/contrato específico y WS19 transitivo: no justificar exclusión diciendo que no escribe payload, ni forzar gate universal por reflejo. WS45 tarea propia y WS39 enganche son detalles válidos para promoción, no bloqueantes actuales.

NO APROBADO todavía:

1) WS12 acceptance (dag≈768-771) conserva 'manteniendo consumidor WS21 bloqueado por G_SOURCE y G_PAYLOAD_PRECONDITION' sin condicionar. WS21/variante read_only excluyen G_SOURCE. Sustituir cláusula por 'G_PAYLOAD_PRECONDITION y, SOLO en variante editable, G_SOURCE'. No cambia P04 actual editable ni añade gate/actor.

2) Interfaz de timeout faltante. WS34.1 output identifica falta de umbral; disposition reconoce que WS12 no lo lista pero lo descarta como futuro. WS34.2 output/disposition afirma que WS12 produce umbral sin que exista ese compromiso. Un consumidor no crea la obligación de su productor. Comprometer explícitamente política/umbral dispatch/reply y clasificación observable en contrato producido por WS12 para ramal E (o reasignar productor de forma explícita y coherente). NO elegir duración ahora, NO bloquear contrato núcleo por Scion posterior, NO introducir permisos/red nuevos. Asegurar que consumidor solo puede avanzar con contrato aplicable probado; no declarar 'futuro asignado' si productor no lo asume. promotion-notes por sí solo no cierra interfaz.

3) WS19.1 review final NO cumple dry-run. output en c342b4d…/attempt-1 dice 'Cambios previstos: ninguno; solo revisión'; disposition: 'no describe el delta (observación menor)'. Es requisito central de ritual-context-review. Mantener intento histórico sin crédito actual y lanzar nuevo proceso barato fresco que reformule y DESCRIBA cambios futuros concretos de campos, consumo precondición, bloqueo de campos protegidos, buffer/conflicto y validación, SIN ejecutar. No rescatar con experto ni inyectar output previo. La pregunta/brief debe dejar claro que se pide ejecución hipotética del nodo y no acciones del reviewer. Si solo cambia instrucción por intento, registrar bytes/argv exactos y no usar el runner si devuelve automáticamente answered del mismo input como si fuera nueva revisión. Vecinos solo se invalidan si cambia contrato suministrado.

4) Provenancia de comparación: los disposition.md inspeccionados dicen 'Borrador ... y revisado por el coordinador', mientras handoff reconoce 'no cada disposición'. No atribuir revisión individual que no ocurrió. Completar comparación real de TODOS los outputs+disposiciones finales por nodo y dejar ledger firmado por rol/actor real/input/output/disposition/alcance/fecha, o corregir honestamente la atribución y quién hizo cada comparación. Para cerrar el checkpoint se solicita comparación final efectiva de todos los nodos, con coordinador asumiendo aceptación; no basta leer lista de ambigüedades. Delegar redacción/comparación preparatoria está permitido; cada afirmación de revisión debe ser verdadera. Preservar original y dejar supersesión/atestación posterior con fecha; no retrofechar ni borrar fallo anterior.

Root escaneó WS01/03/15/25.1/26/34 por 'cambios ninguno': no son el mismo defecto (WS01 verifica cobertura existente, WS03 produce auditoría, WS25.1 describe futuro, los otros son agregados). No repetirlos por esa palabra automáticamente; comparar resultado de verdad.

Antes del último lote, congelar TODAS las correcciones fuente, ejecutar revisiones baratas de todos afectados/nuevos según hashes, comparar y registrar evidencia final sincera. No limitar a 73 ni reenviar todos por defecto: afectados reales, y todos finales sí deben tener comparación. Regenerar y mantener validadores intactos salvo fallo real con tarea específica, status 0 stale, tester independiente sobre estos 4 puntos y cambio protector de G_SOURCE. Tester puede ser read-only. No código producto, no WS07/08-12 activos ni UI. Traer checkpoint correctivo y riesgos residuales. Registrar esta revisión como fuente y proceder dentro de este alcance.

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

