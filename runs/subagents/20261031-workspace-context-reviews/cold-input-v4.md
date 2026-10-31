FILE:desk/drawer/tasks/task-revisar-dag-workspace-con-agentes-baratos.md
# Revisar recursivamente DAG workspace con agentes baratos

id: task-revisar-dag-workspace-con-agentes-baratos
title: Revisar recursivamente DAG workspace con agentes baratos
why: El dueño pide revisar los 44 nodos y raíz del plan con agentes baratos nuevos
  que prueben la calidad del encargo, sin ejecutar producto.
goal: Revisar realmente raíz, paquetes explícitos y cada candidata WS01–WS44; corregir
  los encargos y descomponer cuando haga falta, conservando evidencia y bloqueos honestos.
scope: Solo desk/drawer/plans/workspace-documental/ y desk/drawer/tasks/workspace-documental/,
  y evidencia de esta tarea en runs/subagents/20261031-workspace-context-reviews/.
  No implementar UI, auditar ahora todos los repos, tocar cambios ajenos ni resolver
  decisiones humanas Pxx. Se permite modificar helpers/generadores del plan para materializar
  correctamente nuevos contratos/jerarquía/reviews y sus validaciones. No cambiar
  workflow oficial en esta tarea.
implementation_path: 'Executor independiente orquesta revisores baratos deepseek/deepseek-flash
  thinking low mediante un proceso Pi nuevo por nodo y por intento, --offline --no-session
  --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools
  --system-prompt explícito --print @input.md. No resume, historia, reviews anteriores
  ni instrucciones orales. Registrar proceso/argv, versión, SHA256 de bytes exactos,
  manifest de fuentes y salida/stderr/exit. Cada reviewer reformula, busca ambigüedades
  y produce dry-run detallado de lecturas/cambios/dependencias/validaciones SIN ejecutar.
  Rol explícito: evaluar claridad como plan, distinguiendo contratos que una dependencia
  futura debe producir de lagunas del propio encargo; no inventar API/decisiones.

  Primero mapear raíz y paquetes de tareas grandes en dag.yaml sin confundir jerarquía
  con aristas de ejecución ni fases. Usar agrupación por entregable/intención y pertenencia
  única de candidatas; contratos de interfaz explícitos. Revisar raíz, cada paquete
  y cada candidata/hijo añadido, incluyendo aristas entrantes/salientes y gates. Si
  un nodo grande tiene varias entregas separables, dividir en hijos con salida/dependencia/aceptación
  propia, no solo lista de pasos. Producir brief autosuficiente de planificación por
  nodo, sin ejecutar, derivado del plan/fuentes ya existentes; rutas no comprobadas
  siguen como hipótesis a auditar, nunca APIs inventadas.

  Input por nodo contiene definición actual, glosario y límites mínimos, contratos
  relevantes de dependencias/sucesores/gates y fuentes pertinentes explícitas. No
  inyectar review previo. Primer intento prueba el texto actual (con contexto pertinente);
  luego coordinador compara con intención y corrige fuente escrita, reintenta fresh.
  Disposición por hallazgo: corregido con referencia al cambio, error del reviewer
  con justificación, o bloqueo real. No aprobar solo por APTO ni callar ambigüedades.
  Registrar por separado comprensión de planificación y preparación para ejecución:
  las candidatas siguen sin autorizar ejecución, pendientes TaskDoc real y preflight
  TaskDoc-only/cold bundle futuro. Dependencias aún no ejecutadas no son contratos
  completados. Revisión sin ambigüedad no satisface gates humanos ni externos.

  Evidencia ritual-context-review en runs/subagents/20261031-workspace-context-reviews/context-review/<node-id>/<bundle-sha256>/attempt-<n>/:
  input.md, manifest.json con fuentes/orden/hashes y argv/aislamiento/modelo/razón
  perfil flash barato, output.md, stderr.log, receipt.json, disposition.md. No afirmar
  precio mínimo global. Fallos de transporte separados; reintentar barato sin crédito
  ficticio. Guardar comparación objetiva con reformulación/dry-run antes de aceptar.
  Cambiar input/contrato invalida reviews afectados; al final verificar vigencia por
  hashes semánticos/inputs y volver a correr afectados. Evitar ciclos de vigencia
  por metadatos: excluir estados/evidencia de review del contrato semántico; documentar
  selección.

  Dag.yaml sigue fuente única de IDs/aristas/gates/jerarquía/estado. Añadir metadatos
  revisados con referencias verificables y resumen legible, regenerar fichas/README/diagrama
  mediante helpers y spec2viz si cambia DAG. Mantener expert council separado. No
  marcar revisado si quedan ambigüedades de encargo; blocked/deferred deben quedar
  visibles, con responsable/dependencia. No crear reviews falsos de nodos añadidos.
  No completar ni promover nodos de producto. execution_authorized=false, estados
  candidatos y gates pendientes conservados. Tester independiente comprueba integridad/cobertura/vigencia/coherencia/aislamiento
  y toma muestras de interpretación. Supervisor hace cierre oficial. Otra tarea Board
  sigue activa; no cerrar fase.

  Precisiones operativas v2: supervisor/coordinador acepta solo si la reformulación
  identifica propósito/resultado/repo/límites, el dry-run respeta autoridad y secuencia
  de dependencias, la aceptación es comprobable y no queda decisión de encargo sin
  dueño. Tester verifica esta rúbrica en raíz, TODOS los paquetes e hijos nuevos,
  y WS01/07/11/12/16/20/21/28/30/32/40/41/43/44. Fallar una muestra exige corregir
  y re-review barato de afectados. Discrepar con reviewer solo con cita de texto explícito
  del input que resuelva su duda, o argumento verificable de que pide ejecutar el
  trabajo futuro; sin cita/razón se corrige o queda bloqueado.

  Conservar WS01–WS44 siempre; al dividir, original pasa a paquete no ejecutable cuyos
  hijos se nombran WSxx.1, WSxx.2...; la terminación del paquete exige hijos, y aristas
  externas siguen apuntando al paquete como agregador. Paquetes superiores usan PK01...,
  raíz ROOT. Toda candidata pertenece una vez a paquete superior; paquetes no sustituyen
  dependencias de ejecución ni crean tarea activa. El esquema exacto de jerarquía
  se escribe en dag.yaml antes de revisión.

  Hash input es SHA256 de bytes exactos de input.md. Hash contrato de nodo es JSON
  UTF8 sort_keys=True,separators=('','','':''),ensure_ascii=False sobre definición
  de ese nodo excluyendo SOLO context_review; la proyección exacta se guarda en contract.json
  para poder reproducirlo. Bundle contiene snapshot del nodo, contratos de aristas
  relevantes y fuentes explícitas, ninguno con estado/evidencia de review; no se manda
  dag.yaml completo con metadatos recursivos. Contratos revisados/corregidos son fuente
  vigente y SÍ se suministran; lo excluido es output/disposición de reviewers anteriores.
  Manifest registra cada fragmento/proyección y hash, y vigencia compara fuentes/proyecciones
  actuales. Si cambia contrato de vecino suministrado, repetir review afectado. Metadatos
  de revisión nunca deben inyectarse como contrato de entrada. Referencias archivo
  completo sin modificación pueden congelarse con ruta/hash.

  Los briefs por nodo sirven para evaluar planificación, no se preparan fingiendo
  TaskDoc ejecutable ni pruebas de API que aún debe producir auditoría. Preflight
  TaskDoc-only y cold-bundle de implementación siguen pendientes de promoción, con
  paths/contratos reales resultantes. Bloqueos de dependencias futuras se nombran
  con productor/artefacto/condición de aceptación; no son ambigüedad si el encargo
  define cómo obtenerlos y cómo detenerse cuando falten. Alcance helpers significa
  solo .py bajo desk/drawer/plans/workspace-documental/; workflow oficial bajo desk/rituals/,
  docs/ y skills no se modifica. execution_authorized es campo de dag.yaml y permanece
  false.

  Fallo transporte es exit no cero, timeout o salida vacía; guardar stderr/receipt
  sin contarlo como review. Hasta 3 intentos técnicos baratos por input, luego bloqueo
  técnico explícito; correcciones semánticas no limitadas a 3. Si respuesta no contiene
  reformulación y dry-run, registrar fallo de comprensión y reescribir input o repetir
  modelo barato con motivo, no darle crédito. Distinguir HTTP/quota y bloqueo del
  contrato. Run-dir fijo identifica esta tarea aunque siga otro día; no sobrescribir
  intentos. d7933e2 es baseline documental precedente. La otra tarea activa a preservar
  es task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo.
  Integración/cierre los hace supervisor tras tester; no cerrar fase.


  Fuentes y términos explícitos v3: cwd /home/jp/proyectos/SLDB_1/deskops, repo coordinador;
  owner_repo de cada nodo define repo de eventual producto según repo_roots de desk/drawer/plans/workspace-documental/dag.yaml.
  Este YAML existe: nivel superior tasks (44 candidatas), gates (15), repo_roots,
  parameters.source_mode, hierarchy_context_review pending; hoy NO tiene paquetes
  ni jerarquía explícita, la tarea debe authorarlos. Fuentes a leer: desk/drawer/plans/workspace-documental/{dag.yaml,brief.md,alcance.md,decisiones.md,cobertura.md,reconciliacion.md,validacion-humana.md,borradores/*.md}.
  Glosario viene de brief.md y límites de alcance.md; incluir fragmentos con encabezados/rutas/hash
  según pertinencia al nodo. Decisiones P01–P09 y resolución humana están en decisiones.md;
  gates humanos/externos y sus productores/contratos están en dag.yaml. El review
  de la tarea no audita ahora esos contenidos; son lecturas explícitas del trabajo
  del Executor.

  TaskDoc = tarea activa modelada, autorizada/ruteada en Board; candidatas drawer
  no lo son. Preflight TaskDoc-only = review barato de TaskDoc sola; cold-bundle =
  otro review barato de TaskDoc más fuentes/guardarraíles explícitos. Concilio experto
  = reviews de alta capacidad previos, evidencia distinta. spec2viz = dueño de generación
  desde spec: ejecutar helper existente python desk/drawer/plans/workspace-documental/render_diagram.py
  tras build_plan.py si diagrama cambia; leer helper antes de invocar. Los dos comandos
  build_plan.py --check y validate_plan.py --check comprueban proyecciones sin escribir.

  manifest.json mínimo: node_id, role, attempt, input_sha256, ordered_sources [{path,sha256,projection}],
  node_contract_sha256, edge_contracts [{id,sha256}], provider, model, thinking, selection_reason,
  isolation_flags, argv. receipt.json mínimo: argv, cwd, pi_version, start/end UTC,
  PID, returncode, input_sha256, output_sha256, technical_failure; sin secretos. contract.json
  guarda JSON canónico exacto como definido. No agregar a contrato campos de review
  salvo context_review; otros datos de review viven dentro de ese único campo o fuera
  del contrato, nunca en campos semánticos. Toda variación de bytes de fuente suministrada
  o contrato vecino invalida su review (regla conservadora, incluso typo en ese fragmento);
  typo en fuente NO suministrada no invalida ese nodo. Guía breve de planificación
  es fuente escrita, sin memoria previa.

  Tester es nuevo subagente independiente del Executor y coordinador, sin fork de
  historial, recibe solo task + handoff/fuentes/rutas explícitas, no edita producto
  ni plan. Registra muestras/resultados/limitaciones en validation.log y result-summary.md.
  Puede usar modelo por defecto; NO cuenta como review barato ni experto sustituto.
  Las firmas/models se verifican en sus tareas futuras. Se acepta que reviewer diga
  que no ha visto fuentes a leer, pero debe poder describir orden/roles/límites; pedir
  auditoría de contenidos futuros no bloquea comprensión del encargo de esta tarea.


  Precisiones v4: bundle-sha256 en ruta ES input_sha256. Executor autora ROOT y paquetes
  antes de review; esquema hierarchy: {root: {id: ROOT, title, scope, acceptance,
  children: [PK...]}, packages: [{id: PK01, title, scope, acceptance, children: [WS...]}]};
  cada objeto contiene context_review (único campo excluido de contrato). Raíz/PK
  son agrupaciones de revisión, no nuevas dependencias operativas. Las tareas partidas
  siguen en tasks: padre original node_role=aggregate con children=[WSxx.1,...], hijos
  node_role=delivery,parent_id=WSxx. Original WSxx conserva ID y aristas externas:
  sus dependientes siguen dependiendo WSxx, y WSxx ahora depende de todos sus hijos
  para declarar entrega completa. Cada hijo depende de prerrequisitos originales pertinentes,
  nunca del padre; esto impide ciclo padre-hijo. Contratos de vecinos incluyen condición
  de terminación agregada. Si no se divide, node_role=delivery sin children.

  Criterio de corte: dividir cuando hay dos o más resultados que pueden verificarse/aceptarse
  independientemente, con operaciones o contratos distintos (p.ej. campos y relaciones);
  no dividir lecturas/pruebas de una misma entrega como trabajo separado ni por tamaño
  estimado. Executor propone esquema/contenido jerárquico y splits dentro del encargo
  explícito; supervisor acepta integración tras pruebas. Coordinador/Executor de ESTA
  tarea puede redactar y comparar propuestas contra intención escrita; solo reviewer
  barato carece de herramientas y no interpreta resultados de otros intentos. Supervisor
  revisa disposiciones y tester las contrasta. Formato validation.log libre legible
  con comandos/exit/resultados; identidad/versiones/hashes en manifests/receipts descritos.

  Guía breve de planificación = documento nuevo bajo desk/drawer/plans/workspace-documental/context-review-guide.md
  que el Executor redacta desde brief.md/alcance.md con reglas de lectura y criterios
  anteriores; su ruta/hash se suministra si forma parte del input. El esquema y guía
  se congelan antes de lote final; cambios invalidan solo nodos que los recibieron.
  TaskDoc de esta tarea contiene todo el encargo; se pueden leer fuentes de producto
  en el paso de planificación sin pedir al reviewer que las haya auditado ahora.

  '
validation:
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check
- 'Comprobar raíz + paquetes + 44 nodos originales + hijos nuevos: evidencia real,
  hashes, argv aislado, disposiciones, contrato vigente y cero autorización de producto'
- Tester independiente valida muestras de reformulación/dry-run contra encargos; reporta
  límites y fallos sin fingir gates humanos
- 'Para cambios helpers .py: pytest; registrar fallo baseline CLI ya conocido sin
  modificar código ajeno; no repetir suite si nueva evidencia no lo justifica'
done_when: Cada nodo tiene intento barato real y comparación; ambigüedades corregidas
  y re-revisadas hasta comprensión o bloqueo externo explícito; plan/generados/evidencia
  coherentes; tester independiente y cierre oficial. Ningún producto implementado
  ni decisión humana inventada.
pills:
- pill-001
- pill-005
- pill-007
references:
- desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md
- desk/rituals/context-review.md
- desk/drawer/plans/workspace-documental/brief.md
- d7933e2
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


FILE:.agents/skills/subagent-execution/SKILL.md
---
name: subagent-execution
description: Use when launching a bounded execution subagent for a deskops task in this repository. Recover desk state first, create run evidence, launch one task-scoped execution lane, and keep execution separate from closeout.
---

# Subagent Execution

Use this skill when launching an execution subagent for one bounded task.

## Non-negotiables

- Launch only one bounded task.
- Recover desk state first.
- Snapshot evidence directly from deskops and git.
- Keep execution separate from retirement.
- Treat terminal orchestration tools as optional outer layers, not workflow logic.

## Preconditions

```bash
deskops show board Board --root .
deskops list tasks --root .
deskops show task <task-id> --root .
deskops next <task-id> --root .
deskops graph missing --root .
git status --short --branch
```

Do not launch if:

- the task is not active
- scope is unclear
- allowed files are unclear
- the worktree is contaminated with unrelated generated junk

## Create run evidence

```bash
TS="$(date +%Y%m%d-%H%M%S)"
RUN_DIR="runs/subagents/$TS-<task-id>"
mkdir -p "$RUN_DIR"

deskops show board Board --root . > "$RUN_DIR/board.txt"
deskops show task <task-id> --root . > "$RUN_DIR/task.txt"
deskops next <task-id> --root . > "$RUN_DIR/next.txt"
deskops graph missing --root . > "$RUN_DIR/graph.txt"
git status --short --branch > "$RUN_DIR/git-status.txt"
```

Also write a short brief:

```bash
cat > "$RUN_DIR/brief.md" <<'EOF'
Role: executor
Task: <task-id>
Rules:
- stay within task scope
- do not expand into other tasks
- persist evidence
- run focused validation first
- hand off instead of self-retiring
EOF
```

## Launch contract

The launched lane should be told to:

- read the task and bound references
- recover desk state before edits
- implement only task scope
- save `stdout.log` and `stderr.log`
- write `result-summary.md`
- save `validation.log` when tests are run

## Required outputs

- `board.txt`
- `task.txt`
- `next.txt`
- `graph.txt`
- `git-status.txt`
- `brief.md`
- `stdout.log`
- `stderr.log`
- `result-summary.md`
- `validation.log` when applicable

## Anti-patterns

Do not:

- launch from hidden chat context alone
- run multiple tasks in one execution burst
- mutate board state from the execution lane
- close or delete the task from the execution lane
