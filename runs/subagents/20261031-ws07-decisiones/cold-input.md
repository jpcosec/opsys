FILE:desk/tasks/task-ws07-mantener-registro-trazado-de-decisiones-acordadas.md
---
id: task-ws07-mantener-registro-trazado-de-decisiones-acordadas
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/workspace-documental/decisiones.md
- runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json
- desk/drawer/plans/workspace-documental/dag.yaml
- runs/subagents/20261031-cierre-revision9/phase-closeout.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- runs/subagents/20261031-ws07-decisiones/coverage-report.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws07.md
closeout_evidence:
- commit
- document
---

# WS07: Mantener registro trazado de decisiones acordadas

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión root aprobó el cierre de la revisión 9 y autorizó solo WS07, verificando primero si ya está cubierto. Autorización acotada: runs/subagents/20261031-cierre-revision9/phase-closeout.md; execution_authorized global sigue false.

## Goal

_Describe the concrete result this task must produce._

Determinar con evidencia si el registro P01-P09 de desk/drawer/plans/workspace-documental/decisiones.md cumple la aceptación de WS07, y dejar el resultado en runs/subagents/20261031-ws07-decisiones/coverage-report.md. Si está cubierto, no se reescribe nada.

## Scope

_State what is in scope and what is out of scope._

Reutilizar decisiones.md y owner-decisions.json: respuestas humanas literales 0–2, mapeo P01–P09, actor/fecha/fuente. P07/P09 son defaults técnicos delegados, no firmas humanas. source_mode=editable condicionado a G_SOURCE. Responsabilidad producto/recepción graph_ui/sldb/spec2viz es del solicitante; operador y permisos Scion se designan al abordar E sin bloquear L/M. baseline_proposal es el string raíz de dag.yaml suministrado: conservar base acordada y actualizar solo ante nueva decisión explícita con fuente verificable. Cobertura documental se refiere a decisiones.md + owner-decisions.json y covered_work de este nodo, no sustituye cobertura de UFs ni auditorías WS06.

Primero verificar. Comprobar en runs/subagents/20261031-ws07-decisiones/coverage-report.md, por cada Pxx: resultado concreto, tipo humano o técnico, actor, fuente, nodos y gates. Citar para cada fila humana el ítem y texto literal de runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json, y comprobar que decisiones.md reproduce las respuestas 0 a 2 exactas. P07 y P09 se verifican como defaults técnicos delegados, sin atribuirles firma humana. Comprobar que cada nodo y gate citado existe en dag.yaml. Comprobar que baseline_proposal y parameters.source_mode coinciden con las respuestas. Comprobar el estado de G_PRODUCT y G_WRITE_POLICY sin inferir aceptación de API o UI ni permiso Scion.

Regla de edición. decisiones.md es input de revisión de todos los nodos; editarlo invalida esos bundles. Se edita solo si hay un defecto real frente a la aceptación: dato falso, fila sin actor o fuente, cita inexistente, o cambio real de decisión. Un nodo o gate derivado después, como WS45 y G_PAYLOAD_PRECONDITION, que no cambia decisión ninguna, se registra como observación en el informe y no motiva edición, salvo que la evidencia muestre que el registro queda falso. Si aparece un defecto real, no se corrige aquí: se describe con evidencia en el informe y el Supervisor decide.

Roles: el Executor solo lee y escribe runs/subagents/20261031-ws07-decisiones/coverage-report.md y runs/subagents/20261031-ws07-decisiones/result-summary.md. El Supervisor corre validaciones, commits y closeout. Tester independiente de solo lectura. Sin preguntar nada al solicitante. Fuera de alcance: WS08-12, código, Scion, UI, push, dag.yaml, y la suite general, que no es requisito de esta tarea.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer decisiones.md, runs/subagents/20261031-finalizar-plan-workspace/owner-decisions.json, dag.yaml. 2. Escribir tabla P01-P09 en runs/subagents/20261031-ws07-decisiones/coverage-report.md. 3. Comprobaciones de baseline, source_mode y gates. 4. Dictamen: cubierto, o defecto real con evidencia. 5. runs/subagents/20261031-ws07-decisiones/result-summary.md.

## Validation

_List the checks required before this task can close._

- test -s runs/subagents/20261031-ws07-decisiones/coverage-report.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- Tester independiente de solo lectura deja runs/subagents/20261031-ws07-decisiones/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Registro concreto de cada Pxx con tipo humano/técnico, actor, fuente y nodos/gates. No repetir preguntas ya resueltas ni inferir aceptación de API/UI o permiso Scion. Verificar y reutilizar cobertura documental ya producida; actualizar solo por cambio real de decisión. El informe dictamina cubierto o describe el defecto real, build --check, validate --check y status siguen en verde, y un Tester independiente da PASS.

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

FILE:runs/subagents/20261031-cierre-revision9/phase-closeout.md
# Cierre de fase correctiva de la revisión 9 — 2026-10-31

Fase: correcciones posteriores a WS06, en serie por tocar el mismo plan. Tareas cerradas: consolidación canónica `17847bd7`, corrección de la revisión 9 `70984a8a`, helper `5e1ac87d` y cierre `336e77b6`. Sin tareas activas al cerrar.

**Aprobación.** Revisión root de `9b438e08`, recibida en `w3Y:p1` el 2026-10-31: «APROBADO el cierre correctivo de revisión 9». Verificó de forma independiente build, validate, status, 13 pruebas del helper, los 73 bundles, ledger, recibos y DAG completo contra d9877e86 salvo evidence. Acepta WS13, WS15 y WS33, WS35 como decisión pendiente, WS12 leído completo y la vigencia 37/31/5, no universal v2. Recibos históricos incompletos siguen sin crédito.

**Validación compartida.** Plan: build --check 0, validate --check 0, status all current. Foco: 13 pruebas del helper en verde. **Suite general: no completa.** Root la inició como comprobación adicional y la detuvo a los 82 s: 2 passed y KeyboardInterrupt, exit 2. No está verde ni se afirma. Mi última corrida completa, anterior a esta fase, dio 635 passed, 3 failed, 3 skipped; uno se corrigió después sin repetir la suite. No se encargó reparar fallos ajenos.

**Pills.** Sin nuevas ni retiradas. Las ligadas se sostuvieron.

**Residuo durable.** Átomo `review-attestations-state-only-what-was-actually-read`, con procedencia en el ledger.

**Trabajo capturado.** Hueco de `closeout verify` en `desk/inbox/20261031-195117-unclear-closeout-verify-no-anticipa-la-evidencia-que-exige-closeout-commit.md`. `promotion-notes.md` para las TaskDoc futuras.

**Siguiente.** Solo WS07. `execution_authorized` global sigue false.

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

