FILE:desk/tasks/task-cerrar-corrección-de-la-revisión-9-del-plan-workspace.md
---
id: task-cerrar-corrección-de-la-revisión-9-del-plan-workspace
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-cierre-revision9/review-source.md
- runs/subagents/20261031-correccion-revision9/comparison-ledger.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
files:
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-correccion-revision9/comparison-ledger.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-cerrar-correccion-revision-9.md
closeout_evidence:
- commit
- document
---

# Cerrar corrección de la revisión 9 del plan workspace

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aceptó lo sustantivo y dejó tres cierres: dry-run de agregados, disposición de WS35 y recibos manuales. El helper ya está reparado. Fuente: runs/subagents/20261031-cierre-revision9/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dar crédito operativo completo a los cinco nodos pendientes, corregir por supersesión WS35 y el conteo de instrucciones, y dejar build --check, validate --check y status en verde.

## Scope

_State what is in scope and what is out of scope._

Planificación en deskops. Archivos: runs/subagents/20261031-cierre-revision9/ como evidencia, desk/drawer/plans/workspace-documental/dag.yaml solo en context_review de los nodos que se repiten y proyecciones generadas, runs/subagents/20261031-correccion-revision9/comparison-ledger.md con adenda fechada, runs/subagents/20261031-ajuste-canonico-ws06/promotion-notes.md, disposiciones nuevas e intentos bajo runs/subagents/20261031-workspace-context-reviews/context-review/.

Punto 1. WS13, WS15 y WS33 se repiten con `context_review.py run WS13 WS15 WS33 WS12 WS37 --new-attempt --reason <razón>`, ya con instrucción durable. Se conservan los intentos previos. El dry-run de un agregado debe recorrer por sus hijos el trabajo, las transferencias y la validación; una reformulación detallada no sustituye al dry-run. Si aparece ambigüedad real se resuelve por escrito y solo se invalidan los inputs afectados. Mismo contrato si sigue claro.

Punto 2. WS35: por supersesión fechada, la clasificación pasa a decisión de presentación pendiente al promover: mostrar o excluir mensajes sin intento. Productor: TaskDoc de WS35, con aceptación de ese caso antes de ejecutar. Sin decidir la UX de Scion, sin consultar producto y sin cambiar contrato. Deja de estar vigente «no es ambigüedad». La disposición original se conserva.

Punto 3. WS12 y WS37 reciben intentos frescos por el canal reparado, sin cambiar sus briefs. Sus intentos manuales quedan como evidencia histórica declarada, con recibo incompleto; no se rellenan.

Conteo: el ledger afirmó 39 y 34; lo real es 40 con SYSTEM original y 33 con ampliado, según root. Se corrige la afirmación del resumen por adenda, sin reescribir evidencia. Los otros 68 outputs no se repiten; el ledger declara qué versión de instrucción tiene cada intento vigente.

Comparación: el coordinador lee contrato completo, incluidos depends_on, requires y output_scope, output y disposición de los cinco nodos, y firma lo que leyó. Una disposición nueva no prueba que la anterior se haya leído.

Integridad: comprobar los 73 con excepciones históricas explícitas y ninguna vigente oculta, y que ningún intento registrado tenga recibo incompleto.

Roles: el Supervisor ejecuta todo lo anterior. Tester independiente de solo lectura. Fuera de alcance: WS07, WS08-12, código de producto, Scion, push, decisiones de producto, reabrir correcciones aceptadas, y revisar los otros 68. Se preservan cuatro rutas sucias ajenas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Adenda documental y WS35, commit. 2. Revisiones de los cinco. 3. Comparar, disposiciones, registrar. 4. Integridad y checks. 5. Tester. 6. Closeout, cierre de fase y handoff.

## Validation

_List the checks required before this task can close._

- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- python -m pytest -q tests/test_context_review_helper.py
- Tester independiente de solo lectura deja runs/subagents/20261031-cierre-revision9/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los cinco nodos tienen intento fresco con recibo completo y dry-run sustantivo; WS35 reclasificado; conteo corregido; build --check, validate --check y status en verde; Tester independiente da PASS.

FILE:runs/subagents/20261031-cierre-revision9/review-source.md
# Revisión root del checkpoint d9877e86, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31.

Aceptadas las correcciones sustantivas previas. No se libera la siguiente capa. Tres correcciones acotadas, con autorización para resolverlas con el workflow habitual y enviar checkpoint final.

Verificación root: build --check 0; validate --check 0; status all current; reconstrucción byte a byte de los 73 inputs contra bundle actual y contratos, hashes input/output/disposition contra las 73 filas del ledger: todos coinciden. Código de producto, decisiones, auditorías y validadores sin cambios desde 5f05281c. Hay 71 receipts con PID (71 distintos); WS12/WS37 no tienen ese dato. El conteo real de SYSTEM en argv es 40 original / 33 ampliado, no 39 / 34 o 35: corregir únicamente la afirmación del resumen, sin reescribir evidencia histórica.

1) Calidad del dry-run en agregados: WS33 final 1b03f9.../attempt-1 describe revisar nodo/status/aceptaciones, no cómo se produce la vinculación, dedup/procedencia y decisión por sus hijos. Con el mismo criterio, WS13 (3d32236.../attempt-1) y WS15 (add171.../attempt-1) tampoco describen ejecución hipotética sustantiva por hijos. No es incorrecto que no ejecuten ni tengan salida propia; lo insuficiente es usar eso para omitir el recorrido de trabajo/transferencias/validación. Repetir SOLO esas tres revisiones baratas en procesos frescos con instrucción explícita de agregado. Mismo contrato si sigue claro, sin pedir implementación propia ni convertir vecinos en nodos a revisar. No aceptar solo una reformulación detallada como sustituto del dry-run. Conservar intentos previos; comparación nueva y ledger actualizado. Si el nuevo revisor encuentra ambigüedad real, resolver/decomponer por escrito e invalidar solo inputs afectados.

2) WS35: el output final plantea una duda válida; la disposición la descarta extrapolando «resultados vinculados por WS33.1» a los mensajes recibidos por API. Scope WS35 distingue esas dos fuentes; no prueba que los mensajes no vinculados estén excluidos. promotion-notes ya reconoce la elección mostrar huecos/excluir. Corregir por supersesión fechada la clasificación a decisión de presentación pendiente al promover, con productor TaskDoc de WS35 y aceptación de ese caso ANTES de ejecutar. No hace falta decidir hoy la UX de Scion ni pedir producto otra vez; no mantener simultáneamente «no es ambigüedad» como aceptación vigente y una elección pendiente. Si se cambia contrato canónico, renovar solamente inputs afectados. No rescatar la evidencia barata con interpretación experta.

3) Runner/recibos: reproducido attempts('WS12', hash) y attempts('WS37', hash): KeyError 'technical_failure'. Los receipts manuales omiten technical_failure/output_sha256/pid/otros campos; manifest fue copiado del intento 1. Rompe reanudación con helper y no justifica afirmar recibo completo. Autoriza una tarea ESPECÍFICA y acotada de mantenimiento del helper (drawer commit, promoción commit, contexto fresco/executor/tester/cierre), sin tocar validadores ni UI: hacer durable la instrucción de ejecución hipotética; poder solicitar un intento nuevo tras rechazo semántico sin reutilizar answered por mismo input; producir recibo/manifest propios coherentes con argv y prompt efectivo; reconocer recibos históricos incompletos sin crash ni tratarlos silenciosamente como completos. No rellenar retrospectivamente PIDs/fechas que no fueron capturados. Verificar con pruebas pequeñas significativas de receipts incompletos y rechazo semántico/cache, sin invocar proveedor en pruebas. Antes de usar el helper reparado, respetar el preflight correspondiente. Los dos intentos manuales se conservan como evidencia histórica declarada; para crédito operativo completo a WS12/WS37 generar intentos frescos por el canal reparado, sin cambiar sus briefs por mero metadato. Conjunto a revisar de nuevo: WS13, WS15, WS33, WS12 y WS37, más solo los inputs que realmente cambien.

Orden sugerido: congelar corrección documental necesaria; reparar/verificar helper; lanzar las cinco revisiones correctamente registradas, comparar y actualizar ledger/meta final. Un cambio del helper no obliga a repetir los otros 68: declarar versiones de instrucción y recibos, sin inventar nueva vigencia universal. Leer reformulación/dry-run completo y contrato completo, no solo lista de ambigüedades. Una nueva disposición del coordinador no demuestra retroactivamente que la anterior se leyó; mantener supersesión honesta.

Cierre: build/validate/status, integridad 73 con excepciones históricas explícitas y ninguna vigente oculta, tester independiente, tarea/phase según corresponda; handoff a root con paths/commits y límites. Preservar cuatro dirty ajenos. NO WS07, WS08-12, código UI, Scion ejecución, push ni nuevas decisiones de producto. No reabre correcciones sustantivas aceptadas.

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

