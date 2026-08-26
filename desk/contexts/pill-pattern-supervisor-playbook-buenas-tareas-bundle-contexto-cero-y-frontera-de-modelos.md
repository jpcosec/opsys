---
# pill-xxx
id: pill-pattern-supervisor-playbook-buenas-tareas-bundle-contexto-cero-y-frontera-de-modelos
# e.g., language:python, library:pydantic
tags:
- workspace:desk
- pill-type:pattern
- topic:supervision
- topic:task-authoring
- topic:subagents
---

# Pattern: supervisor playbook — buenas tareas, bundle contexto-cero y frontera de modelos

## What

_Define the context or guardrail this pill carries._

Playbook de supervisión en tres partes. PARTE 1 — Principio rector: una tarea está bien hecha cuando un agente nuevo, sin memoria del chat, puede ejecutarla sin adivinar ni preguntar; si el ejecutor tendría que adivinar una ruta, comando, convención o decisión de diseño, la tarea está incompleta. El bundle tiene tres artefactos con roles distintos — Task (el QUÉ y el cuándo-está-listo), Pills (guardarraíles del CÓMO, doctrina y prohibiciones), Atoms (conocimiento y PORQUÉS de las decisiones, con alternativas descartadas para que el ejecutor no re-litigue). PARTE 2 — Anatomía de una buena task: Rationale con driver de negocio y fuentes con ruta completa; Goal como resultado observable, no actividad; Scope IN numerado con nombres exactos de archivo; Scope OUT explícito archivo por archivo (tan importante como el IN); Implementation Path con comandos LITERALES, no descripciones; Validation con checks ejecutables tal cual y baseline verificado HOY (una suite skippeada da verde trivial); Done When contable; files con la lista exacta (blast radius). PARTE 3 — Frontera de modelos: los modelos de DESK (TaskDoc, PillDoc, AtomDoc, RitualDoc, StepDoc, BoardDoc...) gobiernan el TRABAJO sobre el repo y hablan al agente que ejecuta; los modelos del PRODUCTO (p. ej. los knowledge models de un runtime conversacional) gobiernan el COMPORTAMIENTO del sistema final y hablan a su runtime. Las reglas de desk aplican para desk; las reglas del producto viven en el producto. Una pill nunca reemplaza conocimiento que el sistema final necesita en su propio store; un AtomDoc de desk nunca sustituye a un modelo de dominio del producto, y viceversa.

## Why

_Explain why this context matters for safe execution._

El costo de preparar el bundle se paga una vez; el costo de un bundle ambiguo se paga en cada subagente que adivina distinto. Los checkpoints por fase detectan errores cuando son baratos. Y la confusión de planos normativos (desk vs producto) produce dos fallas simétricas y silenciosas — doctrina de compliance que solo existe en una pill y el runtime del producto jamás ve, o conocimiento de dominio metido en artefactos de desk donde ningún compilador del producto lo consume. Ambas se ven bien en el repo y fallan en producción.

## When

_Describe when an agent should apply this pill._

Siempre que una sesión actúe como supervisor: al redactar o revisar una tarea, al preparar un bundle para subagentes, al decidir dónde vive una regla nueva (¿desk o producto?), y antes de despachar cualquier executor.

## Where

_Name the files, surfaces, or scope this pill applies to._

Aplica a cualquier repo gobernado por deskops. Artefactos de desk en desk/ (tasks, contexts, atoms, rituals, primitives); modelos del producto en el store del producto (p. ej. knowledge/ en un runtime conversacional, con sus propios modelos SLDB y su propio ciclo de indexado). Referencias operativas: skill deskops-task-lifecycle, pill-005 (subagent execution), pill-001 (closeout commit), pill-007 (phase-gated flow).

## How

_Describe the correct way to apply this guidance._

Flujo operacional del supervisor. 1) Escribir el bundle completo (task + pills + atoms + files). 2) Commit de preparación — el worktree nace de estado limpio. 3) git worktree add con rama task/*, nunca trabajar sobre la rama principal. 4) Ambiguity review — un subagente contexto-cero SOLO LECTURA recibe el bundle y responde si puede ejecutar sin adivinar; corregir el bundle con sus hallazgos y commitear. Hallazgos típicos que el supervisor debe anticipar — fuentes que no existen en ningún repo (definir fallback explícito en la pill: qué marcar pendiente y qué está prohibido inventar), credenciales o servicios ausentes (criterio de degradación: qué checks se difieren y si bloquean el closeout), estado sucio del entorno (avisar y dar la remediación). 5) Ejecutar por FASES con subagentes executor: cada prompt de fase lleva contexto obligatorio con rutas exactas, alcance acotado con "y nada más", verificaciones locales, prohibiciones explícitas (incluido NO commitear) y formato del reporte; el supervisor revisa el DIFF REAL (no solo el reporte) y commitea él, un commit por fase con mensaje que cuenta qué se verificó. 6) Tester independiente — nunca el mismo agente que ejecutó — con evidencias en runs/subagents/. 7) Cierre con deskops closeout commit, nunca git commit manual. Para cada decisión de diseño no obvia, registrar un atom con el porqué y las alternativas descartadas. Para cada regla nueva preguntarse — ¿a quién le habla? Al ejecutor de la tarea: pill de desk. Al runtime del producto: modelo/átomo del store del producto. A ambos: las dos cosas, cada una en su plano, y mantenerlas consistentes.

## How Not

_Describe the shortcut or failure mode to avoid._

No implementar inline desde la sesión supervisora. No lanzar executors sin ambiguity review previo. No escribir "registrar el modelo" sin el comando literal. No aceptar checks de validación que pasan trivialmente (suite skippeada = verde falso). No dejar pills contradiciendo decisiones posteriores sin actualizarlas. No poner conocimiento del producto solo en pills o atoms de desk esperando que el runtime lo vea. No usar artefactos de desk como sustituto de modelos de dominio del producto ni viceversa. No ejecutar y testear con el mismo subagente. No dejar que el subagente commitee. No trabajar sobre la rama principal ni commitear con working tree mixto. No cerrar con git commit manual en lugar del closeout oficial.
