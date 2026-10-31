# Executor comparison — WS34, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

Propósito: dejar escrito un encargo de planificación para un adaptador público restringido de dispatch/reply Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: WS34 es un agregado no ejecutable; su cumplimiento es la suma de WS34.1 (dispatch) y WS34.2 (reply), con salidas en `runtime/`, CLI/API y tests. Repo dueño: `deskops`. Límites: no habilita ejecución ni mensajes reales; exige G_EXEC, G_SCION y G_WRITE_CONTRACT; no duplica transporte ni admite shell arbitrario; `promotion: not_authorized`.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
