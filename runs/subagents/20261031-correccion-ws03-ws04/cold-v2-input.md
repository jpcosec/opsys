FILE:desk/tasks/task-corregir-auditorías-ws03-y-ws04-tras-revisión-independiente.md
---
id: task-corregir-auditorías-ws03-y-ws04-tras-revisión-independiente
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-correccion-ws03-ws04/review-source.md
- runs/subagents/20261031-ws02-04-checkpoint/handoff.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/rituals/context-review.md
depends_on: []
pills: []
files:
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- runs/subagents/20261031-ws02-04-checkpoint/handoff.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-corregir-auditorias-ws03-y-ws04-tras-revision.md
closeout_evidence:
- commit
- document
---

# Corregir auditorías WS03 y WS04 tras revisión independiente

## Rationale

_Explain why this task exists or the business driver behind it._

La revisión independiente del checkpoint WS02-WS04 halló cuatro afirmaciones documentales inexactas. Las tareas WS03 y WS04 ya cerraron, y sus cierres y evidencia se conservan: esta tarea corrige con commit propio. Fuente: runs/subagents/20261031-correccion-ws03-ws04/review-source.md.

## Goal

_Describe the concrete result this task must produce._

Dejar desk/drawer/plans/workspace-documental/auditoria/infraestructura.md y desk/drawer/plans/workspace-documental/auditoria/ui.md coherentes con las fuentes en los cuatro puntos revisados, sin ampliar alcance.

## Scope

_State what is in scope and what is out of scope._

Corrige exactamente estos cuatro puntos, descritos en runs/subagents/20261031-correccion-ws03-ws04/review-source.md. Las rutas ../ son relativas a la raíz de deskops.

Punto 1, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, §2.1 fila Verificación optimista en HTTP, filas de cache y resumen: hoy dice que el payload actual se extrae del archivo. Debe decir payload obtenido por carga runtime sujeta a cache, con el límite de frescura: una edición externa que no altere índices puede preceder a /save y no observarse en expected. Abrir http_server.py, save_routes.py, store/runtime_cache.py y store/runtime_cache_signature.py en ../sldb/src/sldb y citar las líneas reales, incluido dónde se llama o no new_operation. Decir que es deducción estática, no reproducida en runtime. No afirmar cache fresca por defecto. Mantener a la vez dos hechos: no hay CAS por hash, y expected sí es una comparación optimista pública por valor.

Punto 2, desk/drawer/plans/workspace-documental/auditoria/ui.md, fila de SPEC sobre + Add relation: SPEC.md:79-82 habla de aristas semánticas sin archivo físico directo; connect-dialog.js:9-17 modifica campos de referencia. No equivalen. La comparación debe decir capacidad no cubierta o no comprobada como arista autónoma, sin refutar al SPEC con WS19.2 sin un puente demostrado.

Punto 3, desk/drawer/plans/workspace-documental/auditoria/ui.md, línea de task.txt de ../UIs/graph_ui/runs/subagents/20261031-workspace-ui: es snapshot histórico. Comprobar con git que f16fcd1 elimina o cierra la TaskDoc y que 134a665 actualiza Board, y dejar registrado que no hay contradicción actual.

Punto 4, desk/drawer/plans/workspace-documental/auditoria/infraestructura.md, fila Consultas guardadas: delimitar con la capacidad vecina ProjectionDoc de pron, persistida y evaluada: pron/models/projection.py:14, world/projection_reader.py:22, world/lexicon.py:137 bajo ../pron/src. Precisar qué selecciona, cómo se evalúa y por qué no equivale a un where guardado ni a ViewDoc. El grep de saved_query no alcanza para negar toda selección persistida; la fila distingue lo verificado.

Roles: el Executor edita solo esos dos archivos y escribe evidencia en runs/subagents/20261031-correccion-ws03-ws04/ (result-summary.md). El Supervisor agrega en runs/subagents/20261031-ws02-04-checkpoint/handoff.md una nota de supersesión fechada, sin borrar el texto original, y escribe el handoff nuevo. El Supervisor corre validaciones, commits y closeout. Un Tester independiente de solo lectura verifica.

Fuera de alcance: código de sldb, pron, spec2viz o graph_ui, dag.yaml, reconciliacion.md, brief.md, WS02, WS06, las demás filas, y reabrir cierres previos. Si algo no se puede comprobar leyendo, queda «no ejecutado» o «fuera de alcance», nombrando el test aislado futuro que lo probaría, sin diseñarlo. Si la fuente contradice un punto de la revisión, no lo corrijas a ciegas: repórtalo con cita en result-summary.md.

Punto 5, ViewDoc, en desk/drawer/plans/workspace-documental/auditoria/infraestructura.md §5.2 y §6 y en desk/drawer/plans/workspace-documental/auditoria/ui.md: el dictamen «solo modelo, sin evaluador» es válido únicamente dentro del universo sldb, pron y spec2viz de WS03, y eso debe decirse así. §6 no concluye que WS18 deba construir un evaluador: remite a que graph_ui ya tiene un consumidor. En ui.md, agregar como base reutilizable lo que exista en ../UIs/graph_ui: frontends/mindmap/projection_views.py (evaluate_view, selección, relation_edges, list_views, find_view), views_routes.py (GET /api/views, GET y POST /api/views/evaluate, POST /api/views/save), su conexión en serve.py incluido el límite local-only (remote 501), tests/test_projection_views.py y tests/e2e_review_workbench_views.py como pruebas existentes no ejecutadas, y los commits 0eb7dd7, b9ab83c y 2a15356. Abrir cada archivo y citar las líneas reales. Enlazar WS18 y WS24 donde corresponda; WS18 no está en la lista de 35 nodos graph_ui de ui.md, así que se agrega como nota o fila solo referencia indicando que su dueño es otro repo. Mantener separados modelo, evaluador, renderer y notación. No anunciar aceptación del producto ampliado.

Precisiones. Los repos de los commits f16fcd1, 134a665, 0eb7dd7, b9ab83c y 2a15356 son ../UIs/graph_ui. Las auditorías son fuentes authored, no generadas: build_plan.py no las reescribe. «Resumen» = secciones de la propia auditoría que repitan la afirmación corregida, incluida §6 de infraestructura.md. «Filas de cache» = filas de §1 y §2.1 que mencionen runtime_cache, cache o frescura. Línea de encabezado: una línea de texto bajo el título, con «Corrección 2026-10-31» y motivo. Nota de supersesión: párrafo fechado 2026-10-31 al inicio de handoff.md. Este PASS del Tester es requisito de closeout.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer review-source.md y las fuentes citadas. 2. Editar solo las filas de los cuatro puntos y el resumen afectado, conservando el formato de tabla. 3. Agregar a cada archivo una línea en su encabezado con fecha y motivo de la corrección. 4. Escribir result-summary.md con antes y después de cada fila.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- test -s desk/drawer/plans/workspace-documental/auditoria/ui.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status
- git diff --stat 2286b976..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/dag.yaml desk/drawer/plans/workspace-documental/reconciliacion.md queda vacío (deskops/ es el paquete de código, no el repo)
- Tester independiente de solo lectura deja runs/subagents/20261031-correccion-ws03-ws04/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Los cuatro puntos están corregidos con citas abiertas en la fuente, sin afirmar nada ejecutado, sin tocar otras filas, y un Tester independiente da PASS.

FILE:runs/subagents/20261031-correccion-ws03-ws04/review-source.md
# Hallazgos de la revisión independiente, texto recibido

Fuente: mensaje de Codex `w3Y:p2` en el pane Claude `w3Y:p1`, 2026-10-31, durante la revisión del checkpoint WS02–WS04.

1. WS03 infraestructura.md §2.1 fila expected/409 (~línea49) promete 'payload actual extraído del archivo'. Puede ser runtime cache vieja: ../sldb/src/sldb/cli/serve/http_server.py:22–26 abre store una vez; save_routes.py:38–40 llama load_runtime_documents sin new_operation; runtime_cache.py:37–42 reusa hits; runtime_cache_signature.py:39–43,56–66,79–86 reutiliza stats/leaves hasta new_operation. Una edición externa que no altere índices puede preceder /save y no observarse en expected; no es solo carrera después del precheck. Deducción estática, no runtime reproducido. Corregir a payload obtenido por carga runtime sujeto a cache; extender límite de frescura en filas cache/expected y resumen. No anunciar cache fresca por defecto. Hay ausencia de CAS por hash, pero expected es comparación optimista por valor, no negar esa capability pública.

2. WS04 ui.md:165 atribuye al SPEC que +Add relation está fuera del plan. SPEC.md:79–82 se refiere a aristas semánticas sin archivo físico directo; editor connect-dialog modifica campos de referencia (connect-dialog.js:9–17). No equivalen. Corregir comparación: esa capability no cubierta/no comprobada como arista autónoma; no refutar SPEC por WS19.2 sin puente demostrado.

3. WS04 ui.md:42 trata task.txt active de runs/subagents/20261031-workspace-ui como incertidumbre de estado vigente. Es snapshot histórico; f16fcd1 elimina/cierra TaskDoc y HEAD134a665 actualiza Board. No hay contradicción actual. Corregir auditoría y handoff (preservando original ronda con nota de supersesión claramente fechada si es evidencia histórica).

4. WS03 ausencia de consultas guardadas: delimitar con capacidad vecina pron.ProjectionDoc persistida/evaluada: ../pron/src/pron/models/projection.py:14, world/projection_reader.py:22, world/lexicon.py:137. No equivale where guardado ni ViewDoc, pero grep saved_query no basta para negar toda selección persistida. Añadir distinción fuente verificada, sin inventar soporte.

Regla adicional: lo no probado queda como fuera de alcance/no ejecutado, con futuro test aislado explícito, sin ampliar la tarea a arreglar producto. No cambiar código SLDB/UI ni DAG. Testers de solo lectura son válidos para inventario estático si distinguen leído de no ejecutado.

## Hallazgo adicional, mensaje posterior de Codex `w3Y:p2`, 2026-10-31

Hallazgo ADICIONAL SUSTANTIVO de revisión propia root: el resumen global «ViewDoc solo modelo/sin evaluador» NO se sostiene en el ecosistema. En graph_ui TRACKED hay:
- frontends/mindmap/projection_views.py:107 evaluate_view: runtime_documents→selección _selected model/where(:52)→relation_edges relaciones/direction(:113), layout y notación resolve_documents. list_views/find_view :127+.
- frontends/mindmap/views_routes.py:1–7 y dispatch: GET /api/views, GET/POST /api/views/evaluate (ref guardada o payload), POST /api/views/save (guarda ViewDoc por sldb), save_view:58+.
- frontends/mindmap/serve.py:147–155 _api_views y dispatchGET:332/POST:382: conecta rutas, local mode; remote devuelve501.
- tests/test_projection_views.py sobre stores temporales reales; tests/e2e_review_workbench_views.py integra rutas. NO afirmo ejecutados.
- git ls-files confirma fuentes trackeadas; commits 0eb7dd7→b9ab83c→2a15356 (último 'Vistas (ViewDoc): ...resolve_documents...review-workbench la dibuja').

WS03 puede decir con precisión que no hay evaluador dentro de su universo sldb/pron/spec2viz, pero §6 no debe concluir que WS18 necesitará construirlo sin consultar consumidor. WS04 omitió por completo proyección/evaluación/guardado ViewDoc en su base reutilizable (rg ViewDoc/projection_views/views_routes en ui.md no da nada). Añadir esa base y enlazar WS18/WS24 donde corresponda; corregir handoff global y dictamen de ausencia: ya existe consumidor en graph_ui con límites local-only y pruebas existentes no ejecutadas. Mantener distinción modelo vs evaluador vs renderer y notación, sin anunciar aceptación del producto ampliado. No tocar código/repos hermanos. Incorporar a misma tarea de corrección del checkpoint antes WS06.

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

