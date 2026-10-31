FILE:desk/drawer/tasks/task-finalizar-plan-workspace-documental.md
# Finalizar plan workspace reconciliado y revisado

id: task-finalizar-plan-workspace-documental
title: Finalizar plan workspace reconciliado y revisado
why: El solicitante pide terminar el plan y confirmó las decisiones de núcleo en owner-decisions.json,
  después del cierre de revisión barata a8601fe.
goal: Entregar un plan final coherente con decisiones humanas registradas, referencias
  externas actuales, deltas reales, ramales opcionales desacoplados y reviews baratos
  vigentes. No implementar producto.
scope: Solo desk/drawer/plans/workspace-documental/, desk/drawer/tasks/workspace-documental/
  y evidencia runs/subagents/20261031-finalizar-plan-workspace/. Se permite usar runner
  existente context_review.py que escribe evidencia nueva en runs/subagents/20261031-workspace-context-reviews/context-review/;
  no sobrescribir intentos existentes. No modificar código de producto, rituales/skills/Board
  de repos hermanos ni cambios dirty ajenos. Supervisor administra TaskDoc/Board/cierre.
implementation_path: 'Executor independiente lee TaskDoc, pills 001/005/007 y ritual-context-review;
  fuentes explícitas: desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,alcance.md,decisiones.md,reconciliacion.md,cobertura.md,validacion-humana.md,context-review-guide.md,borradores/*.md,build_plan.py,validate_plan.py,context_review.py,render_diagram.py};
  evidencia de decisiones en runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json;
  revisión previa a8601fe y runs/subagents/20261031-workspace-context-reviews/result-summary.md.
  Leer estado actual de git y Board de ../UIs/graph_ui, commits a1b2b22/f16fcd1/134a665
  y código workspace_routes.py, views/workspace/node/, deskops_routes.py; deskops
  commits 59244c9/1fefa97 y tests/test_closeout_declared_evidence.py/evidencia de
  cierre. Refs borradas por closeout se reemplazan por código/documento durable actual
  y recibos git show verificables de tarea histórica, nunca recrear task activa desaparecida.

  Registrar tres respuestas humanas exactas con actor/fecha/origen: host Mindmap+SLDB/pron+Deskops,
  Kimun fuera y Scion posterior; source_mode=editable solo tras guardas reales, guardar
  sin commit y cierre/promoción por workflow, UI read-only/handoff con coordinador
  escritor hasta canal seguro; humano solicitante acepta deltas graph_ui/sldb/spec2viz
  y participa en Taller, objetivos 2s lectura/búsqueda, 3s guardado, 10s arranque.
  P01/P02/P03/P04/P05/P06/P08 se actualizan de acuerdo al alcance literal confirmado,
  sin extenderlo a aceptación de implementación ni permisos Scion. P07 local/read-only
  multidesk y P09 rutas authored son decisiones técnicas conservadoras de este plan
  delegadas por el encargo, no atribuir firma humana no dada; sacar requisitos de
  firma artificiales. Modelo de producto aprobado no equivale a contrato técnico o
  API comprobada. Operador/permisos Scion se designan al abordar ramal y no bloquean
  L/M.

  Reconciliar workspace base real con deltas WS13 y sus hijos, WS14/15/19/22–24/27–29/32;
  no dar nodos completos porque hay commit: distinguir reutilización comprobada de
  aceptación expandida pendiente. Workspace cerrado con código real no draft; editing
  y Changes siguen drafts con hashes actuales. G_CLOSEOUT: verificar evidencia focalizada
  de contrato y recibos; si todavía falta prueba de autoridad/identidad requerida,
  dejar condición concreta pendiente con productor/artefacto verificable y tarea documental
  de revalidación explícita si no hay productor, no referencia a task borrada. No
  exigir suite global verde para llamar claro a un plan; registrar riesgos reales
  de validación existente, sin arreglar producto ni fingir éxito.

  Corregir contradicciones: Scion posterior no bloquea producto núcleo; navegación
  base no espera aceptación spec2viz opcional; aceptación receptora y whitelist se
  registran por delta concreto y efecto, sin obligar reader/manual a esperar Changes/modelos/Scion.
  Cada gate conserva productor, condición, evidencia y scope; si hay split añadir
  IDs acotados y revisar todos nuevos, actualizar cobertura/aristas. Fuente editable
  espera G_SOURCE real; no concederlo por decisión. Mutaciones requieren G_HUMAN_READ
  para habilitar uso en UI, no prohibir desarrollo/pruebas aisladas de API. Toda capacidad
  desconocida queda clasificada y con tarea/productor, no workaround. Conservar root/PK/WS01–44/19
  hijos ya trazados; añadir nodos solo si falta entregable real, nunca para pulido
  editorial.

  Preparar cierre.md dentro paquete con base acordada, qué existe/qué resta, secuencia
  por entregas y primera capa preparable, quién decide/ejecuta/acepta, manual/vistas/user-flows
  y evidencia, condiciones reales de inicio. Identificar paquete final terminado como
  planificación, execution_authorized=false y candidatas aún no TaskDoc. Decisiones
  humanas no sustituyen actas de uso/capability/recepción técnica. No afirmar que
  producto está disponible. Plan final debe poder leerse sin chat.

  Regenerar desde dag.yaml. Modificar helpers .py locales solo si hace falta soportar
  estados finales/recibos/ramal y comprobarlos con semántica real; no debilitar validación
  para ocultar pendiente. context_review.py status detecta inputs afectados: corregir
  fuentes primero y congelar, luego lanzar solo afectados con Pi deepseek-flash low
  NUEVO proceso por nodo/intento, no-session/no-context-files/no-skills/no-extensions/no-prompt-templates/no-tools,
  stdin=DEVNULL; recibos exactos, no reviews anteriores en input, guardar reformulación/ambigüedades/dry-run
  sin ejecutar. Supervisor/Executor compara cada output contra intención, dispone
  hallazgos con cita real/razón, corrige y re-revisa. APTO no basta. Gates/decisiones
  suministrados cambiados invalidan afectados; no marcar vigente sin input actual.
  Evidencia extra append-only en run previo permitida, resumen/receipts nuevos en
  run de esta tarea. No pedir concilio experto para salvar comprensión; supervisor
  consulta concilio final separado y Tester independiente al acabar. Executor NO commitea,
  NO cierra ni cambia Board. Handoff incluye findings/disposiciones y limitaciones.'
validation:
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- 'python desk/drawer/plans/workspace-documental/context_review.py status: all reviews
  current'
- 'Independiente: integridad/hashes/aislamiento/cobertura/dry-runs de todos los reviews
  nuevos; refs actualizadas y decisiones trazadas; ninguna autorización producto ni
  gate humano falso'
- Validación focalizada de G_CLOSEOUT por tester si se propone satisfecho; no ejecutar
  suite global larga ya fallida salvo cambio o hallazgo que lo justifique. Para helpers
  .py usar checks semánticos y pytest focalizado apropiado; registrar baseline externo.
done_when: Plan final consistente, sin referencias obsoletas conocidas ni decisiones
  de núcleo sin dueño, ramales opcionales independientes, pendientes técnicos explícitos
  con productor/evidencia, reviews baratos vigentes y tester independiente; cierre
  oficial propio y fase documental. No producto ejecutado.
pills:
- pill-001
- pill-005
- pill-007
references:
- a8601fe
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/drawer/plans/workspace-documental/README.md
files:
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
closeout_evidence:
- commit
- document


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


FILE:runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
{
  "date": "2026-10-31",
  "actor": "solicitante humano de esta sesión, identificado por respuestas vinculadas",
  "source_tool_call": "call_387acc8d34de4f35bc4bafab9263bd58",
  "answers": [
    {
      "question": "Para la primera entrega, ¿confirmamos extender el Mindmap existente usando SLDB/pron y Deskops, sin migrar a Kimun, con lectura y operación manual primero y Scion como ramal posterior?",
      "answer": "Sí, mantener esa base y Scion después",
      "item": 0
    },
    {
      "question": "¿Qué alcance de edición dejamos en el plan? En ambos casos: guardar no hace commit; cierre y promoción respetan el workflow Deskops; con otro coordinador escribiendo, la UI queda en lectura/handoff hasta contar con un canal de escritura coordinado.",
      "answer": "Markdown editable tras probar API reversible, conflictos y campos protegidos",
      "item": 1
    },
    {
      "question": "¿Quedas tú como responsable de producto y aceptación de deltas en graph_ui, SLDB y spec2viz, y como participante de las pruebas de uso sobre el proyecto temporal Taller? Los objetivos iniciales serían abrir/buscar ≤2 s, guardar ≤3 s y arrancar ≤10 s; Scion se designa cuando abordemos ese ramal.",
      "answer": "Sí, yo; acepto Taller y esos objetivos iniciales",
      "item": 2
    }
  ]
}
