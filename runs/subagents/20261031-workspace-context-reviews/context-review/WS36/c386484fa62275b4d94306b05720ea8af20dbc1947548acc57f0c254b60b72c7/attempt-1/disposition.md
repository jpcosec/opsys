# Executor comparison — WS36, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** integrar en `graph_ui` la delegación e intervención humanas sobre ejecución Scion. **Resultado:** dispatch/reply mediante el adaptador WS34 y registro de decisión con WS33.2, con revisión de actor humano y evidencia enlazada; errores por ausencia de API/permisos visibles y probados. **Repo dueño:** `graph_ui`; salida en `frontends/mindmap/views/workspace/execution/`, ruta fina al adaptador WS34 autorizada por WS12, y `tests/`. **Límites:** invocar solo el adaptador WS34 para dispatch/reply; no autoaprobación ni simulación; requires y gates pendientes; promoción no autorizada. No se ejecuta nada.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
