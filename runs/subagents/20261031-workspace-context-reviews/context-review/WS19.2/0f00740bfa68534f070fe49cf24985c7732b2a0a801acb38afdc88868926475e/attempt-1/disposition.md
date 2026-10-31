# Executor comparison — WS19.2, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

**Propósito:** implementar en `graph_ui` el alta y baja de relaciones que autorice el contrato WS12, usando API real y before-image, sin definir semántica de relaciones dentro del componente.

**Resultado:** las relaciones persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo:** `graph_ui`. Salidas en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`.

**Límites:** no crear semántica de relaciones; el uso de mutaciones en UI queda sujeto a G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT; si falta API/contrato, detenerse y registrar el hueco con repo dueño conforme a las reglas comunes; promoción no autorizada. No commit automático ni cierre desde UI.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
