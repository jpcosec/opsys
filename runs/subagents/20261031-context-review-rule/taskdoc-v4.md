---
sldb:
  by: agent
  at: '2026-10-31T04:02:14Z'
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
- '3554396'
- docs/workflow-policy-reference.md
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

ORDEN OBLIGATORIO: primero el COORDINADOR obtiene review TaskDoc-only y bundle frío baratos, corrige la descripción y acepta la reformulación/dry-run; SOLO DESPUÉS despacha al EXECUTOR. El executor no implementa antes de esos gates. Al terminar, un TESTER independiente (otro agente/proceso sin historial de implementación) verifica documentos/comandos y emite evidencia; no es el revisor de comprensión ni el mismo executor.
Capturar átomo por CLI y actualizar documentos modelados por SLDB. Añadir ritual de context review antes de planificación/promoción/ejecución sin crear nuevo estado lifecycle. Revisor barato desde proceso efímero Pi deepseek-flash con no-session/no-context-files/no-skills/no-extensions/no-tools; paquete explícito sin historial. Salida: reformulación, ambigüedades y dry-run detallado SIN ejecutar. Usar fallos para corregir encargo/descomponer jerarquía; revisar raíz/paquetes/hojas y aristas; evidencias por nodo/revisión y fresh retry. Conservar preflight TaskDoc-only y cobertura de bundle con roles distintos y baratos. Revisión experta, ejecución y tester son gates diferentes. Actualizar skill Pi mediante skill-creator; opencode no tiene copia lifecycle aplicable. Marcar concilio del plan como experto y cold baratos pendientes, no correr ni aprobar 44 nodos en esta tarea. La fase sigue abierta por otra tarea; cerrar solo esta entrega documental. Detalle de ejecución: trabajar en checkout actual main, sin crear ramas. Pill significa documento reusable de guardarraíl, enlazado por id; leer rutas oficiales AGENTS.md, README y .pi/skills/use-deskops antes de actuar. La otra tarea activa es task-closeout-la-evidencia-exigida-depende-de-lo-que-la-tarea-toca-no-es-la-misma-para-todo: no tocar sus archivos dirty ni cerrar fase.
1. Crear AtomDoc en desk/atoms/workflow-model/atom-cheap-zero-context-reviews-test-the-brief-recursively.md con sldb docs create --model AtomDoc -o <ruta-absoluta> <payload.yaml> --store .sldb --pythonpath .; required fields id,title,five_wh_one_plus=how,answer,tags. El answer captura la regla del Goal y la distinción experto/context-review.
2. Crear RitualDoc id ritual-context-review en desk/rituals/context-review.md por la misma operación sldb; fields title,id,purpose,trigger,preconditions,steps,validation,failure_modes,completion,tags. Debe regir borradores/planes/paquetes/hojas antes de promover o ejecutar: el revisor barato explica objetivo, enumera ambigüedades y produce dry-run detallado (lecturas/cambios/validación/dependencias propuestas), sin ejecutar comandos ni editar fuentes. El coordinador compara con intención, corrige texto y divide nodos grandes en hijos con edges. Cada nodo/hoja se revisa, no solo raíz; fresh process en cada intento. Fallos son señales para mejorar encargo; no reemplazarlo por experto ni aprobar por palabra APTO. Si ambigüedad persiste no ejecutar. No convertir el ritual en nuevo estado de lifecycle.
3. Integrar ritual-context-review en execution.md (preflight TaskDoc-only barato y bundle frío barato siguen separados), phase.md (DAG multinivel + revisiones por nodo antes de seleccionar hojas listas), docs/workflow-policy-reference.md y skill .pi/skills/deskops-task-lifecycle/SKILL.md. Actualizar documentos modelados con sldb docs update <ref> <full-payload-file> --store .sldb --pythonpath . (el payload es completo). Atoms de docs frontmatter y enlaces al ritual deben reflejar la regla durable. Skill-creator está en /home/jp/.codex/skills/.system/skill-creator/SKILL.md, para instrucciones de skill; editar solo skill local Pi, no global ni opencode. Validar skill con /home/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py.
4. Evidencia por nodo/revisión: runs/subagents/<run-dir>/context-review/<node-id>/<bundle-sha256>/attempt-<n>/. Guardar input explícito/hash, modelo/proveedor/perfil barato elegido, aislamiento comprobado (sin historial/memoria/skills/contexto automático, no-tools para reviewer), salida con reformulación+ambigüedades+dry-run, comparación del coordinador y cambios requeridos. Preflight-only en preflight.md. Un nuevo input/contrato invalida reviews afectados; iteración usa sesión nueva sin correcciones orales/historia. Esto es un test del encargo, no una prueba de implementación ni aprobación humana. Un fallo de transporte/quota no es ambigüedad del plan y se registra aparte.
5. Paquete workspace: en dag.yaml, council_review.scope distingue experto de review barato. Añadir por task context_review.status=pending y evidence=[], required_protocol=ritual-context-review; el root/hierarquía también quedan pendientes. No cambiar aristas/decisiones del producto ni simular reviews de los 44 nodos. build_plan.py debe materializar esa advertencia en README y fichas; validate_plan.py reporta la falta de reviews baratos sin convertir estructura PASS en execution-ready. Ejecutar generadores existentes y verificar sus --check sin editar proyecciones a mano.
6. Validación de modelos con sldb validate deskops.models:AtomDoc --input <atom-path> --pythonpath . y equivalente RitualDoc para los tres rituales. Chequear links y comparar regla en doc/skill/rituales. No pytest completo por cambio documental; no prometer enforcement runtime. Tester independiente confirma evidencias. Executor escribe stdout.log/stderr.log/validation.log/result-summary.md en runs/subagents/20261031-context-review-rule y no cambia Board/tarea ni commitea. Coordinador hace cierre con deskops closeout commit --task task-oficializar-context-review-barato-recursivo --run-dir runs/subagents/20261031-context-review-rule --paths <solo-paths-del-alcance>; subject elegido por coordinador, no ambigüedad del executor. No terminar fase mientras quede la otra tarea. Precisión de comprensión v3: el executor sí puede inspeccionar los archivos listados y referencias explícitas al ejecutar; no conocer su contenido desde la TaskDoc no es por sí mismo ambigüedad. Este gate solo prueba reformulación/dry-run del encargo.
Esquema del plan para esta tarea: cada tasks[i].context_review = {status: pending, required_protocol: ritual-context-review, evidence: []}; root hierarchy_context_review tiene mismo objeto. council_review.scope conserva APTO experto pero aclara que no acredita reviews baratos; status del plan = expert_reviewed_pending_cheap_context_reviews_and_decisions. No se agregan otros campos ni se crean aprobaciones. build_plan.py debe mostrar status/protocolo en README y fichas; validate_plan.py debe comprobar ese esquema pendiente y reportar 0/44 reviews baratos, con execution_authorized=false. Artefactos generados incluidos en el alcance declarado se regeneran, no se editan a mano.
Esta tarea solo ejecuta reviews baratos de su PROPIO encargo/bundle para validar comprensión; no ejecuta reviews de los 44 nodos ni crea ejemplos ficticios como evidencia. Los outputs reales de esta tarea están en runs/subagents/20261031-context-review-rule. Contexto mínimo = encargo exacto/versionado + solo referencias expresamente necesarias y suministradas; sin historial, revisiones anteriores, soluciones orales, memoria persistente o instrucciones automáticas no incluidas. Primer preflight solo TaskDoc; segundo bundle usa TaskDoc+pills+átomos+rituales concretos. El reviewer puede nombrar qué leería, comandos y resultados esperados como dry-run, pero no ejecutar.
Perfil comprobado en esta máquina para prueba: pi --provider deepseek --model deepseek-flash --thinking low --offline --no-session --no-context-files --no-skills --no-extensions --no-prompt-templates --no-tools --system-prompt <rol-revisor> --print @<input.md>. Registrar comando y sha256 de bytes UTF-8 exactos de input.md; sin canonicalización adicional. El artefacto input.md es la concatenación explícita documentada por el coordinador (orden/rutas+texto); mismos bytes = misma revisión. Nueva versión o contrato/campo de dependencia que cambie el input invalida el review afectado, no todos por un typo irrelevante. Registro de selección explica proveedor/modelo barato disponible elegido; no se declara mínimo precio global sin medirlo. No usar modelo experto para rescatar/aprobar por capacidad un encargo fallido.
Bootstrap de evidencia: las reformulaciones reales preflight-v1/v2/v3 y cold-review quedan en el run de esta tarea; el coordinador guarda receipt.json con inputs/hashes, CLI/aislamiento, outputs y disposición de fallos. El nuevo ritual define para futuras revisiones la ruta por nodo/revisión/attempt-n. No inventar evidence para nodos pendientes.
Tres rituales a validar: context-review.md, execution.md y phase.md. Validación objetiva = sldb validate de AtomDoc y esos RitualDoc pasan, links resuelven, skill quick_validate pasa, plan generación y checks pasan, tester independiente deja validation.log/result-summary. Gate docs es deskops closeout verify --task task-oficializar-context-review-barato-recursivo; commit/document declarados, referencias incluyen átomo/doc y 3554396 (ancestro). Cierre del coordinador solo --paths con fuentes del scope+proyecciones del plan y evidencia del run; la herramienta gestiona Board/task/index automáticamente, no se stagean cambios dirty previos de .sldb/store.yaml/closeout/código. El executor no elige commit ni stagea; esa elección no bloquea su comprensión. Aclaraciones de libertad acotada: redactar la prosa de átomo/ritual siguiendo la regla íntegra del Goal no es inventar una decisión del dueño; el executor tiene libertad editorial. El receipt.json no requiere esquema de modelo nuevo: objeto JSON libre con inputs[{path,sha256}], model, provider, command, isolation_flags, output_paths y disposition; guardar bytes exactos del input y hashes. Esto es evidencia de proceso, no enforcement runtime.
Lista congelada para este bundle frío, en orden: TaskDoc de esta tarea; pill-001-task-closure-commit.md, pill-005-subagent-execution.md, pill-007-phase-gated-task-flow.md (bajo desk/contexts); atom-clean-subagent-ambiguity-review.md y atom-tasks-enable-zero-context-subagents.md (bajo desk/atoms/workflow-model); execution.md y phase.md (bajo desk/rituals). Concatenar encabezado FILE:<path> y texto UTF-8; hash del resultado, sin normalización. Solo este bundle explícito, sin resultados de reviews ni estas aclaraciones verbales fuera del TaskDoc.
Si modelo/proveedor barato no está disponible, registrar fallo técnico y parar/reintentar modelo barato disponible con perfil/razón explícitos; no usar experto para obtener un aprobado. Los flags CLI + input guardado + proceso nuevo sin --continue/--resume constituyen la evidencia operativa de aislamiento en esta máquina, no una promesa sobre memoria interna del proveedor.
Skill .pi y docs humanos no modelados se editan como texto cuando no estén trackeados; NO usar sldb docs update para una skill no modelada. Consultar tracking antes; rituales/átomo son StructuredNLDoc y se escriben por SLDB. quick_validate.py espera exit0 sin errores de frontmatter; no prueba calidad de la skill. Cierre/staging son del coordinador y contienen solo las rutas declaradas más artefactos generados dentro de los dos directorios del plan y evidencia del run; los cambios ajenos siguen unstaged.

## Validation

_List the checks required before this task can close._

- Validar lectura/model roundtrip de rituales/átomo modificados
- Comprobar links y consistencia documentación/skill
- python desk/drawer/plans/workspace-documental/build_plan.py --check
- python desk/drawer/plans/workspace-documental/validate_plan.py --check

## Done When

_Name the observable condition that makes the task complete._

Regla durable y superficies oficiales coherentes; comprensión barata guarda evidencia no ejecutora; plan no atribuye contexto cero al concilio experto; gate docs pasa y commit oficial propio.
