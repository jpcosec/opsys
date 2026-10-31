FILE:desk/tasks/task-consolidar-ajuste-canónico-del-plan-workspace-tras-ws06.md
---
id: task-consolidar-ajuste-canónico-del-plan-workspace-tras-ws06
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-ajuste-canonico-ws06/review-source.md
- runs/subagents/20261031-ws06-reconciliacion/handoff.md
- runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/brief.md
- desk/drawer/plans/workspace-documental/reconciliacion.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/brief.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/reconciliacion.md
- runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-ajuste-canonico-tras-ws06.md
closeout_evidence:
- commit
- document
---

# Consolidar ajuste canónico del plan workspace tras WS06

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root de WS06 rechazó dejar validate_plan en FAIL y corrigió extrapolaciones de la matriz. Autorización y seis cambios obligatorios en runs/subagents/20261031-ajuste-canonico-ws06/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar brief.md, dag.yaml, reconciliacion.md y canonical-adjustments.md coherentes con la evidencia, con los nodos afectados re-revisados y build --check, validate --check y context_review status en verde, sin implementar nada.

## Scope

_State what is in scope and what is out of scope._

Solo planificación en deskops. Archivos permitidos: desk/drawer/plans/workspace-documental/brief.md, desk/drawer/plans/workspace-documental/dag.yaml, desk/drawer/plans/workspace-documental/reconciliacion.md, runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md y las proyecciones que build_plan.py y render_diagram.py generan, incluidas fichas en desk/drawer/tasks/workspace-documental/. Helpers locales del plan solo si son imprescindibles, nunca debilitando un validador. runs/subagents/20261031-ajuste-canonico-ws06/review-source.md es parte obligatoria del contrato: los puntos A a F rigen sobre este resumen.

A, ViewDoc: C-50 y ajuste 3. No falta portabilidad genérica: ViewDoc es datos sin ruta de store, y evaluate_view(store, view) evalúa con store por petición. C-50 pasa a nuevo delta de autoría de ViewDoc y NotationDoc concretos definidos por WS09/WS11 y su comprobación sobre stores reales reutilizando C-37 y C-49. Se retira «falta portabilidad o independencia del host» y toda extracción o compartición implícita del evaluador. WS18 no pide servicio, CLI ni runtime fuera de graph_ui. output_scope sldb/views/ con output_base spec2viz puede ser legítimo: se confirma ruta y registro según contrato, sin cambiar dueño por el prefijo.

B, revisión: C-41 y ajuste 1. Glosario de brief.md distingue tres cosas: before-image por valor existente (expected, HTTP 409); token publicado (version/content_hash); y comparación o escritura pública con precondición compartida, aún no probada. No se niega la capacidad optimista real, no se infiere frescura por cada CLI, no se fuerza CAS en toda CLI ni un algoritmo: WS12 define representación, precondición, operaciones y escritores alcanzados. P03 no cambia. Se crea un nodo productor nuevo, WS45, en sldb, para verificar o completar la precondición de escritura de payload, independiente de source_mode: primero reutilizar, pruebas reales focalizadas, código solo si falta al ejecutarlo. WS20 conserva raw-source; C-41 deja de decir que WS20 solo nombra raw-source. Consumidores conectados por efecto real o gate técnico explícito, sin bloquear al lector.

C, captura: C-55 y ajuste 2. Pasa a canal permitido de captura a drawer con origen preservado, sin tarea activa y colisiones controladas, pendiente del contrato WS12, que compara API SLDB existente, composición y eventual wrapper Deskops. Primitivas a citar: sldb.api create_document y DrawerService. No se crea API ni modelo por reflejo; message send más promote no queda aprobado, por borrar la nota y dejar why apuntando a una ruta borrada, y por meter trabajo local en inbox. Productor Deskops explícito solo si falta conducta de workflow, antes de WS25.2.

D, Scion y recibos: C-64 y ajuste 4. Precisar que WS06 puede clasificar y conservar la descomposición sin ejecutar WS05, y que WS32/33 conservan dependencias y gates canónicos. Textos ambiguos de WS06 pasan a acta del receptor P01 y WS11/12 como fuente de contrato, sin firmas, gates ni recepción ficticia. «No designado en P01» de deskops es dato de esa tabla, no un permiso que frene trabajo local.

E, coherencia: en esta consolidación no se preservan como prefijo intacto cláusulas viejas contradictorias de reconciliacion.md; la historia está en Git. No cambian P01-P09, código de producto, repos hermanos, Scion, ni frontends/workspace. WS45 lleva owner, prerrequisitos, entregable, aceptación y revisión real, sin mezclarse con UI ni con un productor condicional. El plan no afirma implementación ni aceptación de deltas.

F, orden y validación: primero los cambios A-D y correcciones de la matriz; luego fuentes congeladas; luego re-review barato de todos los inputs y contratos afectados y de todos los nodos nuevos y agrupadores. Los 25 son el estado actual, no el límite: un cambio en brief.md puede invalidar todos. Procesos frescos sin contexto ni herramientas, stdin DEVNULL, disposiciones sinceras por nodo. Regenerar proyecciones. Tester independiente. No debilitar validadores ni dar covered_work como cierre de TaskDoc. execution_authorized sigue false y status final_plan_reviewed.

Roles: el Executor edita los archivos permitidos y puede correr build_plan.py para regenerar, sin commits. No corre context_review.py run. El Supervisor congela, corre revisiones, escribe disposiciones, registra context_review en dag.yaml, hace commits y closeout. Si aparece una decisión de producto no cubierta, se registra en runs/subagents/20261031-ajuste-canonico-ws06/open-decisions.md antes de improvisar.

Fuera de alcance: WS07, WS08-12, WS05, código, tocar auditorías, reabrir cierres, push.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y las fuentes. 2. Executor aplica A-E y escribe runs/subagents/20261031-ajuste-canonico-ws06/result-summary.md con antes y después. 3. Supervisor revisa, regenera y congela. 4. context_review.py run --stale y disposiciones. 5. Si una revisión revela defecto, corregir y repetir solo lo afectado. 6. Tester. 7. Closeout y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- git diff --name-only 6d41f301..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/decisiones.md desk/drawer/plans/workspace-documental/auditoria/ queda vacío (deskops/ es el paquete de código)
- Tester independiente de solo lectura deja runs/subagents/20261031-ajuste-canonico-ws06/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

build_plan.py --check y validate_plan.py --check salen 0, context_review.py status dice all reviews current, WS45 existe con contrato completo, C-41, C-50, C-55 y C-64 cumplen A-D, sin código ni P01-P09 cambiados, y un Tester independiente da PASS.

FILE:runs/subagents/20261031-ajuste-canonico-ws06/review-source.md
# Decisión de revisión root WS06, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31. Autoriza la consolidación canónica acotada `task-ajuste-canonico-tras-ws06`.

Verificado por root: 68 filas únicas (33/32/2/1), 63/63, hash 7a85a581…6bce, prefijo 3e1c24f0 intacto, build --check PASS, validate --check FAIL por exactamente 25 inputs declarados. Ese FAIL no se acepta como estado final: se restaura antes de WS07 o código.

A) C50/ajuste 3: NO falta una capability genérica de portabilidad. ViewDoc es datos sin store path; projection_views.py:107 evaluate_view(store,view) y views_routes.py:9-10,69+ evalúan con store por petición. test_projection_views.py:151-156 usa dos stores (no ejecutado; cambia filtros, no alegar que prueba idéntico payload completo). WS18 «mismo ViewDoc sin código específico del host» NO pide crear servicio/CLI/runtime fuera de graph_ui. C50 puede ser NUEVO DELTA de AUTORÍA de ViewDoc/NotationDoc concretos que WS09/WS11 definan y su comprobación sobre stores reales REUTILIZANDO C37/C49. Retirar «falta portabilidad/independencia host» y extracción/compartición del evaluador como requisito implícito. `store.parent / sldb/views/` (views_routes.save_view) es carpeta en proyecto dueño del store, NO prueba que output_scope sldb/views/ pertenezca al repo hermano sldb. Con output_base spec2viz:repository_root puede ser spec2viz/sldb/views/ legítimo: confirmar ruta/registro según contrato, no cambiar dueño por prefijo textual.

B) C41/ajuste 1: fijar glosario distinguiendo before-image por VALOR existente (expected HTTP 409), token publicado (version/content_hash), y comparación/escritura pública con precondición compartida aún no probada. No negar capacidad optimista real, no inferir frescura por cada CLI. No forzar CAS en toda CLI ni algoritmo hash por inercia: contrato WS12 define representación/precondición/operaciones/escritores alcanzados; P03 sigue UI read-only/handoff si otro coordinador hasta canal seguro real. Como el guardado de CAMPOS no puede depender del modo raw-source, crear productor de verificación/compleción de la precondición de escritura payload INDEPENDIENTE de source_mode cuando no hay capacidad que satisfaga contrato (sldb; reuse first, test reales focalizados, código solo si falta al ejecutarlo). No meterlo silenciosamente en WS20 condicionado editable; WS20 conserva raw-source. Conectar consumidores por efecto real/gate técnico explícito sin bloquear lector. Corregir también C41 frase «WS20 solo nombra raw-source»: WS20 ya exige revisión/conflicto para raw-source; hueco de campos separado.

C) C55/ajuste 2: ausencia de comando DESKOPS especializado no equivale ausencia de primitiva pública. sldb.api.create_document(model,payload,path) existe (create_document.py:22); DrawerService define candidato TaskDoc drawer.py:255. No afirmo canal UI completo: hay colisiones/sobrescritura/origen/whitelist que verificar. Reformular C55 a CANAL PERMITIDO de captura drawer con origen preservado, sin tarea activa y colisiones controladas, pendiente contrato WS12. WS12 compara API SLDB existente, composición y eventual wrapper Deskops. No crear API/modelo nuevo por reflejo. message send + promote NO se aprueba automáticamente: promoción borra nota y why apunta a ruta borrada (drawer.py:261), hay que probar tipos de origen/fallo parcial y no meter trabajo local innecesariamente en inbox (AGENTS). Solo si falta conducta WORKFLOW, productor Deskops explícito ANTES de WS25.2; si API compuesta cumple, se documenta prueba/contrato y no se inventa otro productor. Dependencia futura WS12 está asignada, no es permiso para implementar fake.

D) C64/ajuste 4: precisar literal «WS06 puede clasificar y conservar descomposición sin EJECUTAR WS05; WS32/33 conservan dependencias/gates canónicos». Hoy «no se requiere WS05» puede leerse eliminar WS32→WS05; no hacerlo. Recibos externos: reemplazar textos ambiguos WS06 por receptor P01 acta / WS11/12 contract source, no agregar firmas, gates ni recepción ficticia. «No designado en P01» deskops es dato limitado de esa tabla, NO crear nuevo permiso que frene trabajo local autorizado por usuario.

E) AJUSTE COHERENTE: TaskDoc puede incluir reconciliacion.md (C41/C50/C55/C64 y referencias relacionadas), canonical-adjustments.md, brief.md, dag.yaml, candidatas/proyecciones/helpers locales imprescindibles. No preservar cláusulas viejas contradictorias como prefijo «intacto» en esta consolidación; historia ya en Git. No cambiar decisiones humanas P01-P09 ni código de producto/repos hermanos. No Scion ni adoptar frontends/workspace. Nuevo nodo productor debe tener owner/prerrequisitos/entregable/aceptación y review real; no mezclarlo con UI/producer condicional incompatible. Plan no afirma implementación ni aceptación del delta.

F) Validación: cambios 1-4 y correcciones matriz PRIMERO, congelar fuentes; re-review todos los inputs/contratos realmente afectados y TODOS los nodos nuevos/agrupadores. Los 25 son estado ACTUAL, NO límite: brief común puede invalidar todos. Procesos baratos fresh sin contexto/tools, stdin DEVNULL, evidencia/disposiciones sinceras; no green por APTO. Regenerar y Tester independiente; terminar build --check/validate --check PASS y status all current 0 stale. No debilitar validador ni dar covered_work como cierre TaskDoc. Capturar fuente nueva de autorización/revisión en run, commits drawer/promoción previos como agente proyecto establece; la captura de esta tarea era trabajo local y debió ir directo a drawer, no inbox: conservar historia, corregir ruta en futuras, no reset.

Siguiente checkpoint: ajuste canónico terminado con evidencia, primitivas nuevas SOLO planificadas, no código implementado, todos los reviews actuales. No activar WS07/WS08-12 ni UI antes de revisión root de ese checkpoint. Es autorización concreta de consolidación, no pedir otra aprobación para los mismos 6 puntos. Si aparece decisión de producto nueva no cubierta, registrar antes de improvisar.

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

FILE:runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md
# Ajustes canónicos requeridos por la matriz WS06

Estado: propuesta para el Supervisor. Ninguno está aplicado. Cada uno nace de una fila de la sección «Matriz de correspondencia WS06» de `desk/drawer/plans/workspace-documental/reconciliacion.md`. Se listan solo cambios que la matriz vuelve imprescindibles; las ediciones de abajo no las hace WS06.

## 1. Revisión esperada: el CAS por hash no existe y WS19.1 lo da por hecho

- Archivos: `desk/drawer/plans/workspace-documental/dag.yaml` (WS19.1, scope, línea ≈1252-1253 «revisión esperada (hash CAS del documento)»; WS20, scope y acceptance) y `desk/drawer/plans/workspace-documental/brief.md` (línea 40, «Revisión / before-image: hash con que una escritura prueba que partió del estado actual»).
- Cambio propuesto: en brief.md, distinguir lo que existe (comparación pública por valor `expected` en `POST /save` de sldb, que da 409) de lo que se busca (revisión por `version`/`content_hash` en la API pública de escritura). En dag.yaml, o bien ampliar WS20 (sldb) para producir también la revisión esperada de la escritura de payload, o bien cambiar WS19.1 para decir «`expected` por valor (comparación de payload)» hasta que ese productor exista. Hoy WS12 solo admite un requisito de API faltante en el nodo productor WS20, y WS20 ya exige «revisión» y pruebas de conflicto, pero para raw-source (dag.yaml:1331-1339); el vacío es el CAS de guardado de payload por campos, no raw-source.
- Evidencia: matriz C-40 (`expected`, ya cubierto con límites) y C-41 (CAS, nuevo delta sin nodo productor); `auditoria/infraestructura.md` sección 2.1 (`save_plan.py:50,58`; `grep` de `expected_hash`, `If-Match`, `etag` sin resultados) y sección 6, puntos 2 y 3.
- Nodos afectados: WS19, WS19.1, WS19.2, WS20, WS21, WS12 (y WS42, que depende de un canal con autoridad compartida).

## 2. Productor faltante de captura directa a drawer

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (WS25.2, y un nodo productor en deskops).
- Cambio propuesto: WS25.2 (owner graph_ui) exige «candidato de drawer … mediante operaciones permitidas por el contrato WS12», pero deskops solo crea candidatos desde una nota de inbox (`promote inbox-to-drawer-task`, que además borra la nota). Registrar un productor deskops (nodo nuevo o ampliación de uno existente) para la captura directa, o fijar en WS12/WS25.2 que la captura es la composición `message send` al mismo desk más `promote inbox-to-drawer-task`. Es condicional: no hace falta si WS12 elige la composición.
- Evidencia: matriz C-55 (nuevo delta, productor deskops) y C-21; `auditoria/deskops.md`, fila A1 `deskops promote inbox-to-drawer-task`.
- Nodos afectados: WS25.2, WS25, WS12.

## 3. ViewDoc como «contrato existente de spec2viz» y alcance de WS18

- Archivos: `desk/drawer/plans/workspace-documental/brief.md` (línea 24, glosario «Proyección de grafo ViewDoc») y `desk/drawer/plans/workspace-documental/dag.yaml` (WS18, scope y acceptance, líneas ≈1158-1180; también `output_scope: sldb/views/`, ruta de sldb para un nodo con `owner_repo: spec2viz`).
- Cambio propuesto: en brief.md, escribir que el modelo `ViewDoc` existe en spec2viz y que el evaluador, las rutas de evaluación y guardado y el render existen en graph_ui, solo en modo local (501 en remote); ningún código de sldb, pron ni spec2viz evalúa un ViewDoc. En WS18, decir que se reutiliza el evaluador de graph_ui y la notación de spec2viz (`resolve_documents`), que «renderiza sobre un store real» se prueba con ese camino, y corregir o confirmar `output_scope` con el dueño de spec2viz. No se propone evaluador de cero.
- Evidencia: matriz C-37 (evaluador y rutas en graph_ui), C-48 (modelo) y C-50 (ViewDoc portables, nuevo delta); `auditoria/infraestructura.md` sección 5.2 y sección 6, punto 1; `auditoria/ui.md` sección 3.1.
- Nodos afectados: WS18, WS24 (extensión opcional), WS09, WS11.

## 4. Texto «acepta por delta en WS11/12» (WS06) y «aceptación específica» en acceptance de WS06

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (WS06, scope línea ≈485 «el responsable receptor ya designado en P01 acepta por delta en WS11/12»; acceptance «WS11/12 obtienen aceptación específica por repo receptor»). WS18 ya dice «recepción G_SPEC_VIEW para ese delta» y no usa «acepta»; no necesita cambio por esta razón.
- Cambio propuesto: reemplazar por «el receptor P01 produce recibos externos en su repo al preparar cada delta; WS11 y WS12 son fuente de contrato y solo enlazan esos recibos». WS06 no produce aceptación ni permiso interrepo. La TaskDoc de WS06 ya tiene esta lectura; el dag.yaml conserva la anterior, que una lectura literal entiende como que WS11/12 escriben actas.
- Evidencia: aprobación del checkpoint (`runs/subagents/20261031-ws02-04-checkpoint/approval.md`, condición sobre recibos); `decisiones.md` («recepción técnica pendiente por delta»); `alcance.md` («Las actas se guardan y commitean en repo receptor»).
- Nodos afectados: WS06, WS11, WS12.

## 5. Revisiones baratas de 25 nodos invalidadas por editar reconciliacion.md

- Archivo: `desk/drawer/plans/workspace-documental/dag.yaml` (`context_review.input_sha256` y `status` de los nodos que leen reconciliacion.md).
- Cambio propuesto: tras integrar la matriz, correr la revisión de contexto de esos nodos y actualizar `input_sha256` y `evidence`; `validate_plan.py --check` falla hasta entonces. Es el efecto declarado en la TaskDoc de WS06, listado aquí para que el Supervisor lo capture como tarea de ajuste canónico y no dentro de WS06.
- Evidencia: sección «Efecto esperado y declarado» de la TaskDoc de WS06.
- Nodos afectados: PK01, WS04, WS06, WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS19, WS19.1, WS19.2, WS21, WS22, WS23, WS24, WS29, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2.

## Considerados y descartados

- Sin cambio en `decisiones.md` ni `alcance.md`: la matriz no reabre P01-P09.
- Sin cambio en las auditorías: sus residuales de citas no bloquean (approval.md).
- La falta de un canal de escritura con autoridad compartida (P03) ya la registra WS12 como hueco y dueño; no se propone nodo aquí.

FILE:desk/drawer/plans/workspace-documental/decisiones.md
# Decisiones finales de núcleo — 2026-10-31

Responsable de producto y recepción de deltas graph_ui/SLDB/spec2viz: solicitante humano de esta sesión. Fuente verificable: `runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json`, tool call `call_387acc8d34de4f35bc4bafab9263bd58`, ítems 0–2. Acepta decisiones de producto y participa en Taller; no ha aceptado implementación, contratos API ni actas de uso.

## Respuestas humanas literales

Ítem 0. Para la primera entrega, ¿confirmamos extender el Mindmap existente usando SLDB/pron y Deskops, sin migrar a Kimun, con lectura y operación manual primero y Scion como ramal posterior?

> Sí, mantener esa base y Scion después

Ítem 1. ¿Qué alcance de edición dejamos en el plan? En ambos casos: guardar no hace commit; cierre y promoción respetan el workflow Deskops; con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado.

> Markdown editable tras probar API reversible, conflictos y campos protegidos

Ítem 2. ¿Quedas tú como responsable de producto y aceptación de deltas en graph_ui, SLDB y spec2viz, y como participante de las pruebas de uso sobre el proyecto temporal Taller? Los objetivos iniciales serían abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s; Scion se designa cuando abordemos ese ramal.

> Sí, yo; acepto Taller y esos objetivos iniciales

## Registro por decisión

Todas las filas están resueltas como base de planificación; las técnicas son revisables por cambio real, sin nueva firma artificial. Fecha común 2026-10-31.

| ID | Resultado concreto | Tipo/actor/fuente | Nodos y gates |
|---|---|---|---|
| P01 | Extender Mindmap; solicitante responsable producto/aceptación de deltas graph_ui/sldb/spec2viz. Operador Scion se designa después. | Humana; solicitante; ítems 0 y 2 | WS04/06/07/11/12/13; G_PRODUCT; recepción técnica pendiente por delta |
| P02 | SLDB/pron + Deskops; Kimun fuera de esta línea base | Humana; solicitante; ítem 0 | WS03/06/07; G_PRODUCT |
| P03 | Con otro coordinador escritor, UI read-only/handoff hasta canal público con autoridad compartida CLI/agentes/UI probado; lock solo UI no basta | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/19/25/26/28/34/36/42; G_WRITE_POLICY/G_WRITE_CONTRACT |
| P04 | source_mode=editable; guardar Markdown solo tras API reversible con revisión, conflictos, recuperación y campos protegidos probados | Humana; solicitante; ítem 1 | WS20/21/30/31; G_PRODUCT/G_SOURCE/G_SLDB_WRITE |
| P05 | Guardar no hace commit; cierre mediante workflow CLI/coordinador y refresco verificable | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/27/28; G_WRITE_POLICY/G_CLOSEOUT |
| P06 | Promoción y cierre respetan workflow Deskops; preparar/handoff hasta canal completo comprobado | Humana; solicitante; pregunta y respuesta ítem 1 | WS12/26/28; G_WRITE_POLICY |
| P07 | Foco/historia/disposición locales; multidesk inicialmente read-only con rutas/aliases explícitos | Técnica conservadora; Executor por encargo TaskDoc v2 | WS11/13.3/41; G_PRODUCT |
| P08 | Taller temporal; solicitante participa. Objetivos abrir/buscar ≤2 s, guardar ≤3 s, arranque ≤10 s | Humana; solicitante; ítem 2 | WS08/16/30/40; G_PRODUCT; actas humanas aún pendientes |
| P09 | Entradas reales desk/README.md + mapa authored en deskops reutilizando registry; publicar WS43 tras validación | Técnica conservadora; Executor por encargo TaskDoc v2 | WS11/17/43; G_PRODUCT |

G_PRODUCT y G_WRITE_POLICY registran esta base, no funciones disponibles. G_SOURCE es producido por WS20 en sldb: contrato público de guardado raw-source con revisión esperada, extracción/validación/roundtrip, protección de campos y buffer recuperable ante conflicto/fallo. G_WRITE_CONTRACT/recepción se verifican por delta y efecto, sin aceptar modelos, Changes o Scion para habilitar campos/intake. Un recibo técnico nombra actor, IDs/alcance, fecha y commit/blob en repo dueño. Ninguna decisión autoriza dispatch, mensajes o acceso Scion; G_EXEC/G_SCION siguen pendientes. No repetir decisiones ya respondidas al promover WS07: verificar y reutilizar este registro.

