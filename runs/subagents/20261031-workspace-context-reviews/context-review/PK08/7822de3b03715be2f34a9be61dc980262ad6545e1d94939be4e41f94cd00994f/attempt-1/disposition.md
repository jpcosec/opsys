# Executor comparison — PK08, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

- **Propósito:** revisar PK08 como encargo de planificación del ramal Scion opcional, sin ejecutarlo.
- **Resultado sustantivo:** paquete integrado de delegación Scion posterior con intento/manifiesto/RunDoc/cierre idempotentes, mensajes/resultados/decisiones con procedencia y dedup, dispatch/reply autorizados, trazabilidad e intervención humanas, aceptación con agente real y capítulo de manual verificado.
- **Repo dueño:** `deskops`; hijos en `deskops` y `graph_ui`.
- **Límites:** agrupación sin ejecución propia; no autoriza tareas ni añade aristas; no duplica el pipeline Scion; ningún permiso de núcleo se convierte en dispatch; sin acceso real el ramal queda bloqueado; no se inventan permisos, actas ni estados.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
