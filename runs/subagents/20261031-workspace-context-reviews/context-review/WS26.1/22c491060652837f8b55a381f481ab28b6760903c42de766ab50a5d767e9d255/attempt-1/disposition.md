# Executor comparison — WS26.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** encargo de implementación en `graph_ui` para autoría explícita de una tarea desde un candidato del drawer, con evidencia declarada, dependencias y binding de contexto/pills.

**Resultado:** UF04 sobre TaskDoc real: candidato autorado, evidencia/dependencias/pills vinculadas y visibles tras recargar; nunca editar `status` para avanzar; si una operación Git carece de contrato o dueño, queda handoff explícito y no disponible.

**Repo dueño:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** depende de WS12 y WS22; requiere G_CLOSEOUT (satisfecho), G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; no ejecuta promoción, commits ni closeout por sí mismo.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
