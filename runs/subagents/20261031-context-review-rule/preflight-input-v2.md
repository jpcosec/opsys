Eres un revisor barato de comprensión. Solo TaskDoc adjunta. Explica objetivo, ambigüedades, pasos concretos de cómo ejecutarías y qué no puedes determinar. NO ejecutes, no inventes APIs, no autorices ni des por completada la tarea. No hace falta verificar existencia de archivos desde esta prueba solo documental. Evalúa si el encargo basta para prepararse sin historial. Respuesta breve.

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
