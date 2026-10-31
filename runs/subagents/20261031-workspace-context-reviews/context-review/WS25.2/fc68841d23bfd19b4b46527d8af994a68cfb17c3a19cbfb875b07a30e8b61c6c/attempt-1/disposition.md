# Executor comparison — WS25.2, final per-effect contract input

State: accepted_current

## Reformulación examinada

REFORMULACION  
Propósito: encargo de implementación para captura interna en UI, con destino elegido explícitamente por la persona usuaria: candidato de drawer o protoátomo, usando operaciones permitidas por WS12 y sin exigir tarea. Resultado: una captura persiste tras recargar en el destino elegido, con origen tipado —ruta o mensaje— registrado y mostrado, sin tarea implícita y con permisos del contrato aplicados; cada destino se prueba por separado. Repo: `graph_ui`, alcance `frontends/mindmap/views/workspace/capture/`, endpoints autorizados por WS12 y `tests/`. Límites: no ejecutar; depende de WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; no inventar endpoints ni tareas; promoción aún no autorizada.

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
