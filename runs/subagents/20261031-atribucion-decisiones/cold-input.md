FILE:desk/tasks/task-separar-procedencia-humana-y-técnica-en-el-registro-de-decisiones.md
---
id: task-separar-procedencia-humana-y-técnica-en-el-registro-de-decisiones
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-atribucion-decisiones/review-source.md
- runs/subagents/20261031-ws07-decisiones/coverage-report.md
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-atribucion-decisiones/attribution-map.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-separar-atribucion-en-decisiones-p01-p06.md
closeout_evidence:
- commit
- document
---

# Separar procedencia humana y técnica en el registro de decisiones

## Rationale

_Explain why this task exists or the business driver behind it._

La auditoría WS07 halló filas Humana con precisiones técnicas que el solicitante no dijo, y fuentes incompletas en P07 y P09. Root eligió corregir en fuente canónica. Autorización: runs/subagents/20261031-atribucion-decisiones/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/decisiones.md con procedencia humana y técnica explícita y fuentes reales en P01, P03 a P07 y P09, sin cambiar ninguna decisión, y las 73 revisiones renovadas.

## Scope

_State what is in scope and what is out of scope._

Parche único en desk/drawer/plans/workspace-documental/decisiones.md. Hallazgos de partida: runs/subagents/20261031-ws07-decisiones/coverage-report.md. runs/subagents/20261031-atribucion-decisiones/review-source.md es contrato obligatorio.

Se mantienen sin cambio: IDs P01-P09, las preguntas y respuestas literales, source_tool_call, decisiones sustantivas, restricciones, actores, y la columna de nodos y gates. P02 y P08 no se reescriben por vocabulario. WS45 no se agrega. O1 a O5 no se tocan. dag.yaml solo cambia en context_review, no en contratos ni gates.

Parche: en P01, P03, P04, P05 y P06, la afirmación humana conserva solo lo aceptado en pregunta y respuesta, citando ítem. Las precisiones técnicas no se borran: pasan a una derivación técnica de planificación rotulada como tal, con fuente exacta existente: path, sección o líneas, y commit si aplica. preflight-input-v2.md 108-113 y 127-128 de runs/subagents/20261031-finalizar-plan-workspace son encargo técnico, no aprobación humana.

P07 y P09: siguen técnicas, sin firma humana y sin rediseño. Se sustituye la fuente sin ruta por la real. Buscar el registro técnico histórico de rutas/aliases, registry y WS43 tras validación en git log de decisiones.md y en los runs previos del plan. Distinguir registro histórico de regla técnica vigente: una cita al DAG sirve para la regla vigente, no prueba quién la decidió. Si un detalle solo tiene respaldo derivado, se etiqueta así y se declara el límite, sin inventar autor, fecha ni fuente.

Forma: el Executor elige la mínima que mantenga legible el registro; puede ser separar en la celda o agregar una sección de procedencia, sin mover IDs. El mapa de atribución queda en runs/subagents/20261031-atribucion-decisiones/attribution-map.md: por cada fragmento de P01 a P09, tipo, fuente exacta y límite.

No cambiar bundle ni fuentes para evitar invalidar revisiones. decisiones.md entra completo en todos los bundles, así que las 73 entradas se renuevan.

Roles. Executor: edita solo desk/drawer/plans/workspace-documental/decisiones.md, escribe attribution-map.md y result-summary.md en runs/subagents/20261031-atribucion-decisiones; sin commits. Supervisor: revisa y congela el parche, corre `context_review.py run --stale` con el helper sin cambios, compara contrato completo, reformulación y dry-run de cada nodo, registra context_review, valida y cierra. Agente preparatorio: puede redactar borradores de disposición, y debe declararse así. Tester independiente de solo lectura, que distingue lo que verificó de los datos del Supervisor.

Fuera de alcance: helper, validadores, código, UI, Scion, WS08-12, push, preguntar al solicitante, y la suite general.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Executor: fuentes históricas, parche, mapa. 2. Supervisor revisa y congela. 3. Tanda de 73 con v2. 4. Comparación y disposiciones. 5. Registro, chequeos, Tester. 6. Cobertura efectiva WS07, closeout y fase.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- test -s runs/subagents/20261031-atribucion-decisiones/attribution-map.md
- git diff --name-only 7b045a6f..HEAD -- deskops/ tests/ desk/drawer/plans/workspace-documental/context_review.py desk/drawer/plans/workspace-documental/validate_plan.py desk/drawer/plans/workspace-documental/build_plan.py queda vacío
- Tester independiente de solo lectura deja runs/subagents/20261031-atribucion-decisiones/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Respuestas 0-2 intactas, mapa con fuentes reales, diff que prueba que no cambiaron decisiones, contratos ni gates; 73 bundles, recibos completos y disposiciones actuales con v2; build --check, validate --check y status en verde; Tester independiente PASS.

FILE:runs/subagents/20261031-atribucion-decisiones/review-source.md
# Decisión root sobre WS07, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31, revisión de HEAD 7b045a6f. Autorización de trabajo documental local; no es aprobación humana nueva ni ejecución global.

D1 sí es defecto real acotado de procedencia: una fila Humana atribuye a ítem 1 precisiones que proceden del encargo técnico. El criterio «dato falso» incluye esa atribución aunque el contenido y las decisiones de fondo sean correctos. No hay cambio de producto que requiera volver a preguntar al humano.

DECISIÓN ROOT: A, corrección en fuente canónica. Autoriza promover/ejecutar desk/drawer/tasks/task-separar-atribucion-en-decisiones-p01-p06.md. No escoger B ni dejar el texto canónico rotulado falsamente Humana con solo una nota externa.

Un solo entregable coherente: registro de decisiones con procedencia humana/técnica explícita y revisiones actualizadas. Mantener IDs P01-P09, literal de preguntas/respuestas y source_tool_call, decisiones sustantivas, baseline/source_mode, restricciones, actores/gates y contratos de tareas sin cambios. No borrar precisiones técnicas útiles para que la frase quepa bajo Humana. Separarlas como derivación técnica de planificación y citar fuente exacta ya existente (path/sección/commit pertinente); la afirmación humana conserva solo lo aceptado en pregunta+respuesta. P03 es el caso principal; revisar misma atribución mixta en P01/P04/P05/P06. P02/P08 no necesitan reescritura por simple cambio de vocabulario o estado técnico en columna de gates: no toda referencia a un gate representa una declaración humana.

Completar en esta MISMA pasada las fuentes de P07/P09, actualmente «Executor por encargo TaskDoc v2» sin ruta y cobertura incompleta. No rediseñarlas ni atribuirles firma humana. Buscar el registro técnico histórico y fuente de los añadidos (rutas/aliases, registry, WS43 tras validación); distinguir registro histórico y regla técnica vigente. Una cita al propio DAG sirve para regla vigente pero no prueba quién la decidió históricamente. Si un detalle solo tiene respaldo técnico derivado, etiquetarlo como tal y declarar límite de procedencia, sin inventar autor/fecha/fuente. preflight-input-v2.md 108-113 y 127-128 son fuentes de encargo técnico, no aprobación humana. No abrir O1-O5 como tareas de limpieza ni cambiar gates por esta autorización. No sumar WS45 al registro como si fuese nueva decisión humana.

Secuencia: ajustar candidato/TaskDoc y commits drawer/promoción; preflight TaskDoc-only y cold-bundle baratos, executor/tester independientes. Revisar primero TODO el parche documental de atribución y congelarlo antes de lanzar la tanda. decisiones.md es whole_file en todos los bundles: renovarán realmente las 73 entradas con v2 durable y procesos baratos frescos sin historial, herramientas, salidas previas ni correcciones orales. No cambiar bundle/normalizar/recortar fuentes para eludir esta invalidación. No reutilizar viejo answered; el input nuevo debe tener hash nuevo. Preservar evidencia anterior como histórica. Comparar contrato completo + reformulación + dry-run de cada nodo; no aceptar solo «ninguna». Si la tanda detecta ambigüedad real, aplicar protocolo y renovar solo entradas afectadas; no resolver con rescate experto ni perseguir reformulaciones textuales equivalentes como defectos. Declarar solo lo ejecutado y comprobado.

Validación de cierre: respuestas 0-2 intactas; mapa de atribución con fuentes reales; diff antes/después prueba que no se cambiaron decisiones ni contratos/gates; 73 bundles/evidencias/recibos completos/hash/argv/versiones/disposiciones actuales; build/validate/status y pruebas focales del helper si se requiere comprobar su uso, sin repetir ni reparar suite general. No tocar helper/validadores ni código UI. Tester independiente de solo lectura debe saber qué verificó por sí mismo y qué recibe como datos del Supervisor.

WS07 aún NO queda «cubierta sin observaciones»: auditoría cerrada, corrección de procedencia pendiente de este entregable. Después de corregir, documentar la cobertura efectiva y closeout/phase aplicable. Checkpoint con dictamen/evidencias/commits/límites. NO activar WS08-12, UI, Scion, push ni alterar cuatro dirty ajenos. No pedir al solicitante confirmar de nuevo.

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

