## Comprensión

Entiendo que la tarea es **documental y de oficialización de una regla**, no de implementación de producto:

1. Crear un `AtomDoc` durable que fije la regla: los *context reviews* baratos, aislados, sin herramientas y recursivos prueban la calidad del encargo; no son ejecución, no son revisión experta y no son aprobación humana.
2. Crear un `RitualDoc` nuevo, `ritual-context-review`, aplicable antes de planificar, promover o ejecutar borradores/planes/paquetes/hojas.
3. Integrar ese ritual en `execution.md`, `phase.md`, `docs/workflow-policy-reference.md` y la skill local `.pi/skills/deskops-task-lifecycle/SKILL.md`, sin crear un estado nuevo de lifecycle y conservando separados:
   - preflight barato solo-TaskDoc,
   - cold review barato con bundle explícito,
   - revisión experta,
   - ejecución,
   - tester independiente.
4. Actualizar el plan `workspace-documental` para que:
   - cada tarea tenga `context_review = {status: pending, required_protocol: ritual-context-review, evidence: []}`,
   - la raíz tenga el mismo objeto,
   - `council_review.scope` aclare que el APTO experto no acredita reviews baratos,
   - el estado del plan sea `expert_reviewed_pending_cheap_context_reviews_and_decisions`,
   - `build_plan.py` materialice la advertencia,
   - `validate_plan.py` reporte `0/44` reviews baratos y `execution_authorized=false`,
   - no se simulen reviews de los 44 nodos ni se cambien aristas/decisiones del producto.
5. Guardar evidencia real del proceso en `runs/subagents/20261031-context-review-rule`: inputs explícitos, hashes, modelo/proveedor/perfil barato, flags de aislamiento, outputs, comparación del coordinador, disposición de fallos y `receipt.json`.
6. Cerrar solo esta entrega documental con commit propio del coordinador. La fase sigue abierta por la otra tarea activa; no se tocan sus archivos dirty ni se cierra fase.

La regla central es: **si el revisor barato no puede reformular el encargo y hacer un dry-run sin ambigüedades, el encargo se corrige o se divide; no se ejecuta y no se “aprueba” por capacidad de un modelo experto**.

## Ambigüedades relevantes

No detecto una ambigüedad que obligue a inventar una decisión del dueño sobre la regla. La prosa exacta del átomo, ritual, política y skill es **libertad editorial** mientras respete la regla completa.

Sí veo puntos de coordinación/forma que conviene fijar sin cambiar la regla:

- **Propiedad de `validation.log` / `result-summary.md`**: la TaskDoc dice que el executor escribe `validation.log/result-summary.md` y también que el tester independiente deja `validation.log/result-summary`. No queda claro si el tester sobrescribe, añade o usa otro directorio. No bloquea la comprensión, pero el coordinador debería fijar una convención de rutas para evitar colisiones.
- **Nombres exactos de los artefactos bootstrap**: se dice que `preflight-v1/v2/v3` y `cold-review` quedan en el run, pero no se fijan nombres exactos ni subdirectorio. La ruta futura por nodo/revisión/attempt está definida; para esta tarea solo falta una convención de nombres.
- **Contrato textual exacto de `build_plan.py` / `validate_plan.py`**: el contenido está fijado, pero no el formato literal de salida. Si existen goldens o tests de strings, el executor debe inspeccionarlos. No es una decisión del dueño.
- **Forma exacta de `council_review.scope`**: se exige conservar el APTO experto y aclarar que no acredita reviews baratos, pero el esquema concreto debe mirarse en `dag.yaml`. Es inspección, no invención.

## Dry-run de actuación

### Coordinador

1. Leer rutas oficiales: `AGENTS.md`, `README`, `.pi/skills/use-deskops`, TaskDoc, pills, átomos y rituales del bundle.
2. Confirmar que la fase sigue abierta y que no se tocará la otra tarea activa ni sus cambios dirty.
3. Ejecutar el preflight barato solo-TaskDoc con un proceso nuevo:
   ```bash
   pi --provider deepseek --model deepseek-flash --thinking low --offline \
     --no-session --no-context-files --no-skills --no-extensions \
     --no-prompt-templates --no-tools \
     --system-prompt <rol-revisor> --print @<input.md>
   ```
   Guardar input exacto, hash SHA-256 de bytes UTF-8, comando, flags, output y disposición. Si hay ambigüedad, corregir la TaskDoc y repetir con proceso nuevo; un input nuevo invalida la revisión anterior.
4. Ejecutar el cold review barato con el bundle explícito y congelado: TaskDoc + pills 001/005/007 + átomos + `execution.md` + `phase.md`. Concatenar `FILE:<path>` y texto UTF-8, sin normalización. Guardar input, hash, output y `receipt.json`.
5. Comparar la reformulación y el dry-run con la intención. Aceptar solo si reproduce el encargo sin ambigüedad bloqueante. No usar la salida como “APTO”.
6. Solo después despachar al executor con bundle limpio y rol claro.
7. Tras el tester, ejecutar el gate documental y el cierre:
   ```bash
   deskops closeout verify --task task-oficializar-context-review-barato-recursivo
   deskops closeout commit --task task-oficializar-context-review-barato-recursivo \
     --run-dir runs/subagents/20261031-context-review-rule \
     --paths <solo-paths-del-alcance>
   ```
   El subject lo elige el coordinador. No se stagean cambios dirty ajenos, `.sldb/store.yaml`, closeout o código.

### Executor

1. Inspeccionar los archivos listados y referencias explícitas. No hace falta que la TaskDoc contenga su contenido.
2. Crear el átomo:
   ```bash
   sldb docs create --model AtomDoc -o <ruta-absoluta> <payload.yaml> \
     --store .sldb --pythonpath .
   ```
   Campos requeridos: `id`, `title`, `five_wh_one_plus=how`, `answer`, `tags`.
3. Crear `RitualDoc` `ritual-context-review` en `desk/rituals/context-review.md` con `title`, `id`, `purpose`, `trigger`, `preconditions`, `steps`, `validation`, `failure_modes`, `completion`, `tags`.
4. Actualizar `execution.md`, `phase.md`, política y skill:
   - rituales/átomo modelados por SLDB con `sldb docs update <ref> <full-payload-file> --store .sldb --pythonpath .`;
   - skill/textos no modelados como texto, consultando tracking antes;
   - skill local Pi únicamente, no global ni `.opencode`.
5. Validar la skill:
   ```bash
   /home/jp/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill>
   ```
6. Editar `dag.yaml` con el esquema indicado, sin cambiar aristas/decisiones. Actualizar `build_plan.py` y `validate_plan.py`; regenerar proyecciones y comprobar `--check`.
7. Validar modelos:
   ```bash
   sldb validate deskops.models:AtomDoc --input <atom-path> --pythonpath .
   sldb validate deskops.models:RitualDoc --input desk/rituals/context-review.md --pythonpath .
   sldb validate deskops.models:RitualDoc --input desk/rituals/execution.md --pythonpath .
   sldb validate deskops.models:RitualDoc --input desk/rituals/phase.md --pythonpath .
   ```
8. Escribir logs y resumen en el run. No cambiar Board/tarea ni commitear.

### Tester independiente

1. Proceso nuevo, sin historial de implementación, distinto del revisor y del executor.
2. Verificar:
   - modelos y links,
   - `quick_validate.py`,
   - `build_plan.py --check`,
   - `validate_plan.py --check`,
   - `0/44` reviews baratos,
   - `execution_authorized=false`,
   - estado pendiente en cada tarea y raíz,
   - que no se simularon reviews de los 44 nodos,
   - que no se tocaron closeout dirty, producto, `.opencode` ni skill global.
3. Dejar `validation.log` y `result-summary` en la ruta que fije el coordinador. No commitear.

## Guardarraíles y pills

- **pill-001, cierre con commit propio**: se respeta. El executor no commitea; el coordinador cierra con commit atómico tras tester y gate docs. La tarea no debe darse por cerrada antes del commit.
- **pill-005, subagentes frescos**: se respeta. Revisor, executor y tester son contextos distintos y reciben bundle explícito. No debe haber `--continue`/`--resume` ni correcciones orales que sustituyan inputs versionados.
- **pill-007, gates de fase**: se respeta. Hay gate de ejecución, handoff a testing, tester independiente y closeout. La fase no se cierra porque queda otra tarea activa; no se ejecuta reconciliación de fase completa.
- **Átomos**: `atom-clean-subagent-ambiguity-review` exige que un subagente limpio devuelva ambigüedad en vez de improvisar; encaja con el preflight/cold review. `atom-tasks-enable-zero-context-subagents` exige bundle explícito; la lista congelada y el `receipt.json` lo cubren.
- **Rituales actuales**: `execution.md` ya tiene preflight TaskDoc-only y cold review; la tarea añade `ritual-context-review` sin eliminar esos gates. `phase.md` debe incorporar revisiones por nodo antes de seleccionar hojas listas, sin convertir el ritual en estado lifecycle.

## Conclusión

Mi reformulación reproduce el encargo y el dry-run es ejecutable sin decisiones del dueño. Las lagunas detectadas son de coordinación/evidencia y pueden resolverse por inspección o convención, no inventando regla. No he ejecutado nada ni emito autorización de ejecución.
