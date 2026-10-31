# Executor comparison — WS25, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION

Propósito: WS25 es un agregado de revisión, no una tarea ejecutable, para integrar en la UI de `graph_ui` la lectura/ack de inbox y la captura interna en drawer/protoátomo mediante operaciones autorizadas por WS12; «triage» no se define como capacidad separada. Resultado: agregado de salidas de WS25.1 y WS25.2; se cumple cuando ambos hijos cumplen su aceptación. Repo dueño: `graph_ui`; `output_base: graph_ui:repository_root/`; `output_scope` agregado. Límites: ack no es aprobación; sin envío interdesk; sin tarea implícita ni cron de triage; G_HUMAN_READ se exige antes de habilitar mutaciones en UI, no para desarrollo/pruebas aisladas de API. Depende de WS12 y sus hijos; gates por delta. Promoción no autorizada.

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
