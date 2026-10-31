## Objetivo entendido

Dejar documentada y oficializada una práctica de **context review barato**: una revisión aislada, sin historial, no ejecutora y recursiva del DAG/encargo, que sirve para probar si el brief se entiende y para detectar ambigüedades. Debe quedar reflejada en átomo, ritual, ejecución, fase, política y skill local Pi, y el plan `workspace-documental` debe marcar revisiones baratas pendientes sin ejecutarlas ni aprobar los 44 nodos. No se debe cerrar la fase ni tocar la otra tarea dirty.

## Ambigüedades relevantes

- No está definido el **esquema exacto** de `context_review` en `dag.yaml`: campos, ubicación por nodo/raíz, valores permitidos y cómo lo materializan `build_plan.py`/`validate_plan.py`.
- “Reconocer revisiones pendientes” no aclara si esta tarea debe **crear evidencia de ejemplo**, solo anotar `pending`, o ejecutar alguna revisión mínima. El texto dice no correr los 44 nodos, pero no si hay que ejecutar alguna revisión propia.
- El **paquete explícito sin historial** no tiene formato, contenido mínimo ni criterio de inclusión/exclusión.
- El **revisor barato** se describe por modelo/proceso, pero no hay comando, perfil, flags exactos ni método de verificación de aislamiento.
- La ruta de evidencia usa `<bundle-sha256>` y `attempt-<n>`, pero no se especifica canonicalización del bundle, hash, ni qué invalida exactamente una revisión.
- “Tres rituales” en validación es inferible pero no explícito.
- “Gate docs pasa” no está definido como comando o criterio objetivo.
- No queda claro el límite exacto de `--paths` para closeout: ¿incluye proyecciones generadas del plan?, ¿solo fuentes?, ¿excluye Board?
- `pills` se define conceptualmente, pero no se conoce su contenido ni si condiciona el encargo.

## Cómo lo ejecutaría, a alto nivel

1. Leer `AGENTS.md`, `README`, `.pi/skills/use-deskops` y los documentos referenciados.
2. Inspeccionar modelos `AtomDoc`/`RitualDoc`, rituales existentes, `dag.yaml`, `build_plan.py`, `validate_plan.py` y la skill local Pi.
3. Crear el `AtomDoc` con la regla durable y la distinción experto/context-review.
4. Crear `ritual-context-review` con propósito, disparadores, pasos, validación, fallos y criterio de completitud.
5. Integrar referencias en `execution.md`, `phase.md`, política y skill local, sin crear estado nuevo de lifecycle.
6. Añadir anotaciones `context_review.status=pending`, `evidence=[]` y `required_protocol` al plan, sin cambiar aristas ni decisiones de producto.
7. Ejecutar generadores y sus `--check`, validar modelos y enlaces.
8. Preparar evidencia no ejecutora según el protocolo, si el alcance finalmente lo exige.
9. Dejar el cierre al coordinador con `deskops closeout commit`.

## Lo que no puedo determinar solo con este TaskDoc

- Contenido actual y forma exacta de los documentos/modelos a modificar.
- Comandos y APIs reales disponibles; no asumo su existencia ni comportamiento.
- Esquema real de `dag.yaml`, `build_plan.py` y `validate_plan.py`.
- Si hay que ejecutar revisiones baratas ahora o solo documentar el protocolo y marcar `pending`.
- Criterio objetivo de “oficial”, “coherente” y “gate docs pasa”.
- Alcance exacto del commit y de los paths permitidos.
- Si la ruta de `skill-creator` y `quick_validate.py` es aplicable sin más contexto.

## Veredicto

El encargo **basta para prepararse a alto nivel**, pero no para ejecutar sin inspeccionar el repositorio y resolver ambigüedades de esquema, evidencia y alcance. Es útil como brief de comprensión barata; no autoriza ejecución, no valida APIs y no permite dar la tarea por completada.
