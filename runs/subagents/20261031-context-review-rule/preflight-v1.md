1. **Qué entendí**  
TaskDoc en `draft` para oficializar un **context review barato, aislado, no ejecutor y recursivo** del DAG. Superficies explícitas: átomo, `desk/rituals/context-review.md`, `execution.md`, `phase.md`, `docs/workflow-policy-reference.md`, skill Pi lifecycle y anotaciones/generación de `workspace-documental`. El revisor sería un proceso efímero Pi `deepseek-flash` con `no-session/no-context-files/no-skills/no-extensions/no-tools`, paquete explícito sin historial, salida = reformulación + ambigüedades + dry-run detallado **sin ejecutar**. No crear estado lifecycle nuevo; no tocar dirty closeout, código de producto, skill global ni `.opencode`; no correr/aprobar 44 nodos; cerrar solo esta entrega documental con commit propio.

2. **Ambigüedades / datos faltantes**  
- `status: draft`, `summary` vacío, `history` vacío; no sé el estado real ni autorización.  
- No sé qué son `pills` ni su efecto.  
- “Capturar átomo por CLI”: no está el comando exacto.  
- No está el formato/ubicación de “evidencias por nodo/revisión”.  
- No están definidos los nombres de roles baratos ni los gates “experto/ejecución/tester”.  
- No se especifica qué cambios exactos van en cada ritual/documento/skill.  
- No se especifica cómo marcar el concilio del plan como experto ni dónde anotar los “cold baratos pendientes”.  
- No se identifica la “otra tarea” que mantiene abierta la fase.  
- No se indica mensaje/rama del commit oficial.  
- No puedo verificar existencia ni contenido de los archivos listados.

3. **Cómo lo ejecutaría, según el documento y sin inventar**  
Orden propuesto, no confirmado por el documento:  
1. Capturar el átomo por CLI — comando exacto no determinado.  
2. Actualizar `desk/rituals/context-review.md`, `execution.md` y `phase.md` para el review previo a planificación/promoción/ejecución, sin nuevo estado lifecycle.  
3. Actualizar `docs/workflow-policy-reference.md` y la skill Pi lifecycle mediante `skill-creator`.  
4. Añadir anotaciones/generación en `desk/drawer/plans/workspace-documental` y `desk/drawer/tasks/workspace-documental`, marcando concilio experto y cold baratos pendientes, sin correr/aprobar 44 nodos.  
5. Validar lectura/model roundtrip de rituales/átomo, links y consistencia documentación/skill — método exacto no indicado.  
6. Ejecutar como validación declarada: `python desk/drawer/plans/workspace-documental/build_plan.py --check` y `python desk/drawer/plans/workspace-documental/validate_plan.py --check`.  
7. Commit oficial propio — mensaje/rama no especificados.

4. **Qué no podría determinar**  
No puedo determinar el comando CLI del átomo, el contenido exacto de cada edición, el esquema de evidencias, la ubicación de anotaciones del plan, cómo actualizar la skill con `skill-creator`, los criterios completos del “gate docs”, ni si los scripts de validación existen o pasan. Tampoco puedo declarar la tarea completada ni autorizarla. No ejecuté nada.
