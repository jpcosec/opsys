# Executor comparison — WS32.1, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** separar identidad de intento y dispatch en el ramal Scion, sin segundo pipeline. **Resultado:** un registro local por intento con IDs distintos antes de dispatch y estado intent/no confirmado, sin red ni Hub simulado; código de modelo y RunDoc tratados por SLDB/API-CLI. **Repo:** `deskops`. **Límites:** no dispatch/reply, no evento Hub fingido, no afirmar fallo/éxito de Hub, no Markdown ad hoc; `promotion: not_authorized`. Depende del inventario WS05 y del contrato/ubicación WS12.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
