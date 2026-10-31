# Executor comparison — WS25.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

**Propósito:** implementar en `graph_ui` la vista de inbox para leer mensajes, registrar ack y, solo si el contrato WS12 define la operación, respuesta local dentro del mismo desk. **Resultado:** UI en `frontends/mindmap/views/workspace/inbox/` con tests, consumiendo endpoints autorizados por WS12. **Repo:** `graph_ui`. **Límites:** sin envío interdesk; ack no equivale a aprobación; sin tarea implícita ni cron de triage; mutaciones en UI sujetas a gates.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
