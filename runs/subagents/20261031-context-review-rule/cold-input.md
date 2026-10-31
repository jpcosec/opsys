Revisor barato sin historial: examina solo bundle explícito. Reformula encargo, identifica ambigüedades/guardarraíles omitidos y describe dry-run de ejecución por pasos, sin ejecutar ni usar memoria. Distingue reglas actuales que esta tarea cambia de requisitos faltantes. No resuelvas por suposición. No leas artefactos fuera de este texto. No declares tarea implementada.


FILE: desk/tasks/task-oficializar-context-review-barato-recursivo.md
---
sldb:
  by: agent
  at: '2026-10-31T03:59:35Z'
  authority: generated
  via: update_document
id: task-oficializar-context-review-barato-recursivo
status: active
summary: 'Documentar política explícita del dueño: prueba barata de calidad del encargo,
  no ejecución ni revisión experta.'
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md
- desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md
depends_on: []
pills:
- pill-001
- pill-005
- pill-007
files:
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- desk/rituals/execution.md
- desk/rituals/phase.md
- docs/workflow-policy-reference.md
- .pi/skills/deskops-task-lifecycle/SKILL.md
- desk/drawer/plans/workspace-documental
- desk/drawer/tasks/workspace-documental
task_type: docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-oficializar-context-review-barato-recursivo.md
closeout_evidence:
- commit
- document
---

# Oficializar context review barato recursivo

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión explícita del dueño: zero-context review prueba calidad del encargo; no es un concilio experto.

## Goal

_Describe the concrete result this task must produce._

Hacer oficial el review barato, aislado, no ejecutor y recursivo del DAG; reconocer revisiones pendientes del plan workspace.

## Scope

_State what is in scope and what is out of scope._

Solo átomo, ritual nuevo/context-review, ejecución y fase, docs/workflow-policy-reference.md, skill Pi lifecycle y anotaciones/generación del paquete workspace-documental. No tocar dirty closeout, código de producto, skill global ni .opencode.

## Implementation Path

_Outline the expected implementation route or affected surface._

Capturar átomo por CLI y actualizar documentos modelados por SLDB. Añadir ritual de context review antes de planificación/promoción/ejecución sin crear nuevo estado lifecycle. Revisor barato desde proceso efímero Pi deepseek-flash con no-session/no-context-files/no-skills/no-extensions/no-tools; paquete explícito sin historial. Salida: reformulación, ambigüedades y dry-run detallado SIN ejecutar. Usar fallos para corregir encargo/descomponer jerarquía; revisar raíz/paquetes/hojas y aristas; evidencias por nodo/revisión y fresh retry. Conservar preflight TaskDoc-only y cobertura de bundle con roles distintos y baratos. Revisión experta, ejecución y tester son gates diferentes. Actualizar skill Pi mediante skill-creator; opencode no tiene copia lifecycle aplicable. Marcar concilio del plan como experto y cold baratos pendientes, no correr ni aprobar 44 nodos en esta tarea. La fase sigue abierta por otra tarea; cerrar solo esta entrega documental. Detalle de ejecución: trabajar en checkout actual main, sin crear ramas. Pill significa documento reusable de guardarraíl, enlazado por id; leer rutas oficiales AGENTS.md, README y .pi/skills/use-deskops antes de actuar. La otra tarea activa es task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo: no tocar sus archivos dirty ni cerrar fase.
1. Crear AtomDoc en desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md con sldb docs create --model AtomDoc -o <ruta-absoluta> <payload.yaml> --store .sldb --pythonpath .; required fields id,title,five_wh_one_plus=how,answer,tags. El answer captura la regla del Goal y la distinción experto/context-review.
2. Crear RitualDoc id ritual-context-review en desk/rituals/context-review.md por la misma operación sldb; fields title,id,purpose,trigger,preconditions,steps,validation,failure_modes,completion,tags. Debe regir borradores/planes/paquetes/hojas antes de promover o ejecutar: el revisor barato explica objetivo, enumera ambigüedades y produce dry-run detallado (lecturas/cambios/validación/dependencias propuestas), sin ejecutar comandos ni editar fuentes. El coordinador compara con intención, corrige texto y divide nodos grandes en hijos con edges. Cada nodo/hoja se revisa, no solo raíz; fresh process en cada intento. Fallos son señales para mejorar encargo; no reemplazarlo por experto ni aprobar por palabra APTO. Si ambigüedad persiste no ejecutar. No convertir el ritual en nuevo estado de lifecycle.
3. Integrar ritual-context-review en execution.md (preflight TaskDoc-only barato y bundle frío barato siguen separados), phase.md (DAG multinivel + revisiones por nodo antes de seleccionar hojas listas), docs/workflow-policy-reference.md y skill .pi/skills/deskops-task-lifecycle/SKILL.md. Actualizar documentos modelados con sldb docs update <ref> <full-payload-file> --store .sldb --pythonpath . (el payload es completo). Atoms de docs frontmatter y enlaces al ritual deben reflejar la regla durable. Skill-creator está en /home/jp/.codex/skills/.system/skill-creator/SKILL.md, para instrucciones de skill; editar solo skill local Pi, no global ni opencode. Validar skill con /home/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py.
4. Evidencia por nodo/revisión: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/. Guardar input explícito/hash, modelo/proveedor/perfil barato elegido, aislamiento comprobado (sin historial/memoria/skills/contexto automático, no-tools para reviewer), salida con reformulación+ambigüedades+dry-run, comparación del coordinador y cambios requeridos. Preflight-only en preflight.md. Un nuevo input/contrato invalida reviews afectados; iteración usa sesión nueva sin correcciones orales/historia. Esto es un test del encargo, no una prueba de implementación ni aprobación humana. Un fallo de transporte/quota no es ambigüedad del plan y se registra aparte.
5. Paquete workspace: en dag.yaml, council_review.scope distingue experto de review barato. Añadir por task context_review.status=pending y evidence=[], required_protocol=ritual-context-review; el root/hierarquía también quedan pendientes. No cambiar aristas/decisiones del producto ni simular reviews de los 44 nodos. build_plan.py debe materializar esa advertencia en README y fichas; validate_plan.py reporta la falta de reviews baratos sin convertir estructura PASS en execution-ready. Ejecutar generadores existentes y verificar sus --check sin editar proyecciones a mano.
6. Validación de modelos con sldb validate deskops.models:AtomDoc --input <atom-path> --pythonpath . y equivalente RitualDoc para los tres rituales. Chequear links y comparar regla en doc/skill/rituales. No pytest completo por cambio documental; no prometer enforcement runtime. Tester independiente confirma evidencias. Executor escribe stdout.log/stderr.log/validation.log/result-summary.md en runs/subagents/20261031-context-review-rule y no cambia Board/tarea ni commitea. Coordinador hace cierre con deskops closeout commit --task task-oficializar-context-review-barato-recursivo --run-dir runs/subagents/20261031-context-review-rule --paths <solo-paths-del-alcance>; subject elegido por coordinador, no ambigüedad del executor. No terminar fase mientras quede la otra tarea.

## Validation

_List the checks required before this task can close._

- Validar lectura/model roundtrip de rituales/átomo modificados
- Comprobar links y consistencia documentación/skill
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check

## Done When

_Name the observable condition that makes the task complete._

Regla durable y superficies oficiales coherentes; comprensión barata guarda evidencia no ejecutora; plan no atribuye contexto cero al concilio experto; gate docs pasa y commit oficial propio.


FILE: desk/contexts/pill-001-task-closure-commit.md
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


FILE: desk/contexts/pill-005-subagent-execution.md
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


FILE: desk/contexts/pill-007-phase-gated-task-flow.md
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


FILE: desk/atoms/workflow-model/atom-clean-subagent-ambiguity-review.md
---
id: atom-clean-subagent-ambiguity-review
title: Clean subagents return ambiguous tasks
five_wh_one_plus: when
tags:
- system:deskops
- topic:subagents
- topic:tasks
---

# Clean subagents return ambiguous tasks

## Answer

The first action of a clean subagent is ambiguity review. If the task is unclear enough that implementation would require improvisation, the subagent returns the task instead of executing it.


FILE: desk/atoms/workflow-model/atom-tasks-enable-zero-context-subagents.md
---
id: atom-tasks-enable-zero-context-subagents
title: Tasks enable zero-context subagents
five_wh_one_plus: why
tags:
- system:deskops
- topic:tasks
- topic:pills
- topic:subagents
---

# Tasks enable zero-context subagents

## Answer

Tasks should be modular, testable, and accompanied by sufficient pills so a clean subagent with no prior context can execute without improvisation, ambiguity, or context overload. The expected task bundle is explicit: task doc, routed instructions, bound pills, linked atoms, linked files, and validation targets.


FILE: desk/rituals/execution.md
---
# ritual-xxx
id: ritual-execution
# List of step-xxx paths
steps:
- 1. Confirm the current phase is explicit and that this task belongs to the ready
  dependency layer being executed.
- 1. Open the initialization gate by making the active task, task scope, touched files,
  and validation targets explicit.
- 1. Atomize the work into one coherent deliverable.
- 1. Audit code, docs, tests, and git state before changing anything.
- '1. Run a zero-context preflight comprehension gate: give one fresh subagent only
  the TaskDoc and require it to restate the intended work step by step plus every
  ambiguity it sees.'
- 1. Store that TaskDoc-only reformulation at `runs/subagents/<run-dir>/preflight.md`.
- 1. Pass the preflight only when the reformulation reproduces the task intent closely
  enough to execute without guesswork; if the subagent reports any ambiguity or misses
  the intended work, fix the TaskDoc before dispatching any Executor.
- 1. Send one fresh subagent with no prior task context to review the task, board-routed
  instructions, bound pills, linked atoms, linked files, and planned validation only
  for ambiguity, missing guardrails, and likely missed pills.
- 1. Resolve or record the cold-review findings before implementation starts.
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

Carry one active desk task through scoped implementation inside an explicit phase with task and pill binding, including a zero-context TaskDoc comprehension gate and a fresh-context coverage check strong enough to catch missing guardrails before implementation starts.

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

## Validation

_List the checks that prove the ritual was performed correctly._

- The active task is explicit.
- A fresh-context subagent ran the TaskDoc-only preflight comprehension gate before any Executor was dispatched.
- The preflight reformulation was stored at `runs/subagents/<run-dir>/preflight.md`.
- The preflight passed only because the subagent's reformulation reproduced the intended work and surfaced no unresolved ambiguity.
- A fresh-context subagent reviewed the task bundle before implementation.
- Required pills are named in the task.
- Cold-review ambiguities were resolved, tracked, or converted into pill updates before code changes.
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

## Completion

_Describe what completion looks like._

The implementation is complete enough to enter the testing ritual through an explicit handoff gate.


FILE: desk/rituals/phase.md
---
# ritual-xxx
id: ritual-phase
# Ordered prose steps; not document references
steps:
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

Run one horizontal dependency layer of tasks as the workflow unit above individual task execution, then close that layer with integration validation, pill reconciliation, and next-phase preparation.

## Trigger

_State when this ritual should start._

Start when the board has one ready set of tasks whose dependencies are satisfied and whose execution can proceed without overlapping operational changes.

## Preconditions

_List the conditions that must hold before running the ritual._

- The board's active tasks and dependencies are explicit.
- The ready phase has been identified as a non-overlapping layer.
- Each task has a named context bundle and validation target.
- Phase-level validation expectations are known.
- A pill reconciliation pass is planned for phase closeout.

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

## Failure Modes

_List common mistakes this ritual prevents._

- Starting a phase without identifying the actual dependency layer.
- Treating a semantic milestone as a phase even when tasks still depend on one another.
- Letting tasks share one long-lived execution context instead of fresh task-specific bundles.
- Advancing to the next phase after isolated task tests without integration validation.
- Carrying stale or overlapping pills forward because each task closed independently.
- Hiding phase-level regressions inside later task commits instead of closing the layer explicitly.

## Completion

_Describe what completion looks like._

The current dependency layer is integrated, reconciled, and committed, and the board is ready to start the next phase.
