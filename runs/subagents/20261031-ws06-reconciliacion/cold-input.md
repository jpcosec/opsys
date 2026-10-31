FILE:desk/tasks/task-ws06-proponer-correspondencia-de-alcance-con-repos-dueños.md
---
id: task-ws06-proponer-correspondencia-de-alcance-con-repos-dueños
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- runs/subagents/20261031-ws02-04-checkpoint/approval.md
- desk/drawer/plans/workspace-documental/auditoria/deskops.md
- desk/drawer/plans/workspace-documental/auditoria/infraestructura.md
- desk/drawer/plans/workspace-documental/auditoria/ui.md
- desk/drawer/plans/workspace-documental/dag.yaml
- desk/drawer/plans/workspace-documental/decisiones.md
- desk/drawer/plans/workspace-documental/alcance.md
- desk/rituals/context-review.md
depends_on: []
pills:
- desk/contexts/pill-001-task-closure-commit.md
- desk/contexts/pill-005-subagent-execution.md
- desk/contexts/pill-007-phase-gated-task-flow.md
- desk/contexts/pill-ready-phases-prove-dependencies-and-non-overlap.md
files:
- desk/drawer/plans/workspace-documental/reconciliacion.md
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/workspace-documental/task-ws06.md
closeout_evidence:
- commit
- document
---

# WS06: Proponer correspondencia de alcance con repos dueños

## Rationale

_Explain why this task exists or the business driver behind it._

Las auditorías WS02-WS04 fueron aprobadas como inventario documental y levantan la pausa de WS06 (runs/subagents/20261031-ws02-04-checkpoint/approval.md). La matriz traduce sus datos a capacidades y deltas por repo dueño antes de definir contratos.

## Goal

_Describe the concrete result this task must produce._

Agregar a desk/drawer/plans/workspace-documental/reconciliacion.md una matriz de correspondencia por capacidad o delta único, agrupada por repo dueño, con evidencia citada y sin aceptar nada.

## Scope

_State what is in scope and what is out of scope._

Una matriz con una fila por delta o capacidad única (varios nodos pueden remitir a la misma fila), agrupada por repo dueño: ya cubierto (capacidad observable en código implementado, citando path/símbolo y commit observado), extender ticket existente (incluido un draft del Board) o nuevo delta. La fila Scion RunDoc/cierre de reconciliacion.md conserva el tratamiento ya registrado (descomposición en WS32/33) sin requerir WS05. Registrar en reconciliacion.md la atomización propuesta, sin notificar, despachar ni modificar el Board de graph_ui; el responsable receptor ya designado en P01 acepta por delta en WS11/12.

Salida: agregar a desk/drawer/plans/workspace-documental/reconciliacion.md una sección «Matriz de correspondencia WS06» y conservar sin cambios el texto existente. Las rutas ../ son relativas a la raíz del repo deskops. Insumos autoritativos: desk/drawer/plans/workspace-documental/auditoria/deskops.md, infraestructura.md y ui.md, aprobados en runs/subagents/20261031-ws02-04-checkpoint/approval.md; desk/drawer/plans/workspace-documental/dag.yaml, decisiones.md, alcance.md y el texto actual de reconciliacion.md. Se puede abrir el código citado para confirmar una fila; no reauditar.

Formato: un subtítulo por repo dueño (graph_ui, sldb, spec2viz, deskops y otros si aparecen) y una tabla con columnas: ID estable C-nn; capacidad o delta; nodos DAG que remiten a ella; clasificación (ya cubierto, extender ticket, nuevo delta); path o símbolo y commit observado; ticket o delta destino; responsable; límites de evidencia. Una fila por capacidad: varios nodos pueden remitir a la misma fila, y no se agrupa por nodo. Clasificación: ya cubierto = capacidad observable en código, con path o símbolo y commit, sin afirmar aceptación ampliada; extender ticket = cabe en un ticket existente, incluido un draft del Board; nuevo delta = no cabe, se propone atomizado. El dueño de la fila es el repo donde vive el código a cambiar, no el owner_repo del nodo si difieren; la diferencia se dice en límites.

Cobertura: al final, una tabla con los 63 nodos de dag.yaml y su fila C-nn, o el motivo por el que no generan delta (planificación, validación humana, agregado). Ningún nodo queda sin fila.

Reglas de contenido:
- Responsable: P01 designa al solicitante para graph_ui, sldb y spec2viz. Si un repo dueño no está en P01, se escribe «no designado en P01», sin inventar. El operador Scion se designa después y solo aparece en el ramal E.
- Tickets de edición y Changes: comparten serve.py, views/workspace/ y docs/workspace-ui.md. Se extienden en serie; no se propone ejecución paralela a ellos.
- frontends/workspace de graph_ui no se adopta como base aprobada: fila con ese estado, sin reclamo en Board o TaskDoc, sin commit.
- ViewDoc: reutilización primero. El modelo vive en spec2viz; el evaluador y las rutas en graph_ui, solo en modo local. No proponer evaluador de cero.
- expected: existe como comparación pública por valor en HTTP, pero no acredita CAS compartido ni frescura para API o CLI. Fila de capacidad, limitación y tarea dueña, sin inventar garantía. No proponer API que no exista como si existiera: un faltante es delta con productor.
- Scion RunDoc/cierre conserva la descomposición en WS32/33, sin requerir WS05.
- WS06 no produce aceptación ni permiso interrepo. El texto «acepta por delta en WS11/12» se lee así: el receptor P01 produce recibos externos en su repo al preparar cada delta; WS11 y WS12 son fuente de contrato y solo enlazan recibos. Ninguna fila dice aceptado.
- Sin notificar, despachar, ni tocar el Board de graph_ui. No reabrir decisiones P01-P09.

Cambios fuera de scope: si la matriz revela algo imprescindible en brief.md, dag.yaml, candidatas u otro documento, no se aplica. Se lista en runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md con archivo, cambio propuesto, evidencia y nodos afectados.

Efecto esperado y declarado: reconciliacion.md es input de revisión barata de 25 nodos (PK01, WS04, WS06, WS13, WS13.1, WS13.2, WS13.3, WS14, WS15, WS15.1, WS15.2, WS19, WS19.1, WS19.2, WS21, WS22, WS23, WS24, WS29, WS32, WS32.1, WS32.2, WS33, WS33.1, WS33.2). Tras editarla, context_review.py status debe listar exactamente esos nodos como «input changed» y validate_plan.py --check falla por eso. No se corrige en WS06, porque exige escribir en dag.yaml: el Supervisor lo captura como tarea de ajuste canónico.

Roles: el Executor edita solo reconciliacion.md y escribe runs/subagents/20261031-ws06-reconciliacion/canonical-adjustments.md y runs/subagents/20261031-ws06-reconciliacion/result-summary.md; sin commits ni closeout. El Supervisor corre validaciones, commits y closeout. Un Tester independiente de solo lectura verifica. Fuera de alcance: WS05, WS07, WS08-12, código, dag.yaml, brief.md, auditorías.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Leer insumos. 2. Extraer capacidades únicas de las tablas de ui.md, infraestructura.md y deskops.md y de reconciliacion.md. 3. Escribir la matriz por repo dueño. 4. Escribir la tabla de cobertura de nodos. 5. Escribir canonical-adjustments.md. 6. result-summary.md con conteos, decisiones de clasificación dudosas y lo no comprobado.

## Validation

_List the checks required before this task can close._

- test -s desk/drawer/plans/workspace-documental/reconciliacion.md
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/context_review.py status lista exactamente los 25 nodos declarados y ninguno más
- git diff --stat 3e1c24f0..HEAD -- deskops/ tests/ docs/ desk/drawer/plans/workspace-documental/dag.yaml desk/drawer/plans/workspace-documental/brief.md desk/drawer/plans/workspace-documental/auditoria/ vacío (deskops/ es el paquete de código)
- Tester independiente de solo lectura deja runs/subagents/20261031-ws06-reconciliacion/tester-result-summary.md

## Done When

_Name the observable condition that makes the task complete._

Acceptance: Matriz con una fila por delta o capacidad propuesta, agrupada por repo dueño, no por nodo del DAG; correspondencia ticket/delta y responsable ya designado P01; operador Scion posterior solo para ramal E; no produce gates de aceptación ni aprueba deltas que aún no están definidos. WS11/12 obtienen aceptación específica por repo receptor. Aclaración vigente: la aceptación específica la producen recibos externos del receptor P01; WS11 y WS12 son fuente de contrato. Además: cada nodo de dag.yaml aparece en la cobertura, y un Tester independiente da PASS.

FILE:runs/subagents/20261031-ws02-04-checkpoint/approval.md
# Aprobación del checkpoint WS02–WS04

Fuente: dictamen final root de Codex `w3Y:p2`, recibido en el pane Claude `w3Y:p1` el 2026-10-31. Revisión root de seis correcciones, hashes y lectura independientes, scope documental.

Resultado: corrección WS03/WS04 aprobada documentalmente; checkpoint WS02–WS04 aprobado como inventario documental; se levanta la pausa de WS06. Entregables revisados: `infraestructura.md` sha256 1e1fda815bf56e91f7e47aa13d11d90fc84f7b1f2d44458597add63e44e0d662, `ui.md` sha256 b3272dc9586d88975bae7f92f4ed392411b83c0ca7b2932b382a287ce3c477a6; commits 32ef48d1, 3e1c24f0, 542bf364.

No es validación de runtime, UI ni suite global. Los residuales de citas y la clave de cache incompleta no bloquean la matriz; si se usa su forma exacta en un contrato, se contrasta con el código. `handoff.md` y `handoff-correccion.md` quedan como evidencia histórica.

## Condiciones recibidas para WS06

- Matriz en reconciliacion.md: una fila por capacidad o delta único, agrupada por dueño; reusable, extender ticket o nuevo delta; path, símbolo y commit; responsable P01; límites de evidencia.
- No crear ejecución paralela a los tickets de edición y Changes compartidos, ni adoptar frontend/workspace como base aprobada.
- ViewDoc ya evaluado por graph_ui: reutilización primero, sin evaluador de cero.
- `expected` público por valor existe, pero no acredita CAS compartido ni frescura para API/CLI: mapear capacidad, limitación y tarea dueña sin inventar garantía.
- WS06 no produce aceptación de deltas ni permiso interrepo. Receptor P01 produce recibos externos; WS11/12 son fuente de contrato. Si el texto de WS06 sugiere que WS11/12 escriben actas, aclararlo en la TaskDoc.
- Cambios imprescindibles fuera del scope de WS06 se capturan como tarea de ajuste canónico acotada, no dentro de WS06, y se traen al checkpoint.
- Sin WS05, sin Scion, sin push, sin WS07/WS08–12 ni código UI antes de la revisión root.

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

FILE:desk/drawer/plans/workspace-documental/reconciliacion.md
# Reconciliación verificada — 2026-10-31

Auditoría acotada de Board, commits y código actual; no aceptación de producto ampliado. graph_ui HEAD 134a665: Board enruta solo edición contextual y Changes, ambos draft. Workspace integrado a1b2b22, cierre f16fcd1 y actualización Board 134a665. No recrear su TaskDoc eliminado: recibo `git -C ../UIs/graph_ui show f16fcd1^:desk/tasks/task-workspace-multiproyeccion-documento-grafo-local-codigo-y-contexto.md`. Las referencias externas de dag.yaml apuntan a fuente durable actual con SHA-256; editing/Changes conservan hash actual del draft.

Fuentes inspeccionadas: `frontends/mindmap/workspace_routes.py`, `views/workspace/node/workspace-view.js`, `workspace.mjs`, `workspace.css`, `deskops_routes.py`. Base real: GET /api/workspace/nodes y /node, identidad Model:name, IR/payload, vecindad 1–2 hops, Code referenciado con límites de repo/gitignore/binario/tamaño, contexto relaciones/hash, errores por proyección. UI tiene catálogo modelado con filtro local, alternancia Document/Graph/Code, historia URL/popstate, relaciones navegables y diagnóstico. No equivale a lectura raw-source genérica o búsqueda backend.

| Nodo/delta | Reutilización comprobada | Aceptación ampliada todavía pendiente |
|---|---|---|
| WS13 / WS13.1 | Workspace integrado, IR/payload, contexto/origen, grafo/Code y selección nodo | Markdown sin modelo, fuente íntegra legible, enlaces/foco cruzado con todos los soportes y contrato WS11 |
| WS13.2 | Catálogo de documentos del store | Explorar Markdown no modelado del desk y altas dinámicas sin conocer ID |
| WS13.3 | Historia browser y tab de representación | Pestañas de documentos, divisiones simultáneas, foco por documento; no confundir TABS Document/Graph/Code con pestañas documentales |
| WS14 | filterCatalog sobre id/título/modelo ya cargado | Búsqueda texto/campos/semántica por API pública real; teclado, consulta/foco, vacío/error/degradación distintos |
| WS15 / WS15.1 | Errores catálogo/nodo/proyección y problems_report reales | Link roto, backend ausente, fallos CDN y degradación bajo guion Taller; no afirmar offline |
| WS15.2 | Errores store inexistente | Orientación proyecto sin desk y handoff init probado |
| WS19 e hijos / WS21 | IR/payload y hash/contexto reutilizables; ticket edición sigue draft | Guardado por campos/relaciones, CAS/409/conflicto y guardas; raw-source depende WS20/G_SOURCE |
| WS22 | deskops_routes.py lee Board/tarea/gates/next con rutas validadas | Lista/tablero/dependencias integrados al lector, mismas identidades y soporte; status no es test aprobado |
| WS23 | Lifecycle/payload navegables como documentos | Procedimiento/StepDoc/ritual con pasos/fuentes; no marcar realizado por leer |
| WS24 | Grafo entrante/saliente y hasta 2 hops; lector genérico IR/payload | Markdown no modelado, clasificación, backlinks y navegación completa; no esperar ViewDoc WS18 opcional |
| WS27 / WS27.1 | Code puede inspeccionar referencias seguras | Diff e historial Git reales acotados a tarea/repos; no son Code preview |
| WS27.2 | Task payload/gates de lifecycle | Mostrar evidencia declarada/encontrada/verificada y soporte diferenciado mediante contrato closeout público |
| WS28 | POST /api/desk/advance con revisión Board+task y lock de proceso; solo avanza lifecycle | Verify/handoff cierre externo y refresco verificable. advance no cierra; lock UI no coordina escritores CLI/agentes |
| WS29 | Problems del índice de aristas y hashes contexto | Changes sigue draft: check/doctor/drift e impacto real; no CST/Merkle Kimun |
| WS32 e hijos | Infraestructura closeout existente, candidato Scion ya capturado | Correlación intento/manifiesto/RunDoc e idempotencia con Scion real; no autorizados ni duplicados por este plan |

WS06 mantiene esta matriz al promover: integrar delta en ticket receptor vigente, vincular evidencia ya existente, o tarea atómica propia sin solapamiento. Nunca volver a implementar base porque el TaskDoc histórico ya no existe. Ningún nodo completo solo por commit: cada aceptación ampliada debe probarse. WS01/WS07 ya tienen contenido documental cubierto en brief/decisiones; verificar ese recibo al promover, no reescribirlo como nuevo trabajo.

Recepción: solicitante fue designado producto/aceptación graph_ui/sldb/spec2viz en ítem 2. Eso no es acta técnica. Receptor solicitante P01 registra acta por delta concreto con actor, alcance/IDs, fecha, efecto y commit/blob en su repo al preparar/promover ese delta. WS11/12 mapean esos requisitos en contratos y solo enlazan actas existentes; Executor deskops no escribe actas interrepo. G_UI_READ/G_UI_WRITE/G_SLDB_WRITE/G_SPEC_VIEW/G_WRITE_CONTRACT no exigen aceptar otros deltas. Lector/manual no esperan Changes, modelos, Scion ni spec2viz opcional.

Closeout: implementación 59244c9 y cierre 1fefa97 verificables, con Task-Id histórico; fuentes durables `deskops/services/closeout_gates.py`, `services/closure.py`, tests de evidencia declarada y lifecycle. Recibo `git show 1fefa97^:desk/tasks/task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo.md`. G_CLOSEOUT se decide con prueba focalizada actual y asociación task→commit exacta, nunca por desaparición. Autoría se refiere al registro de cierre según contrato existente, sin añadir una nueva capa de permisos. Baseline histórico reporta fallos ajenos de suite; esta tarea no arregla producto ni afirma suite global verde.

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

