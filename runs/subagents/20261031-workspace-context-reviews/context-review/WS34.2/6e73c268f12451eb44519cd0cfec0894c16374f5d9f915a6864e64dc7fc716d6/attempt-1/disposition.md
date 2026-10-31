# Executor comparison — WS34.2, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION
**Propósito:** revisar WS34.2 como encargo de planificación, no como producto ni ejecución.
**Resultado:** adaptador público restringido para reply vinculado al intento, con timeout/errores y autoridad del coordinador; aceptación mediante agente real y timeout reportado como fallo sin confirmación.
**Repo:** `deskops`; salidas en `runtime/`, `cli/commands/runtime.py` o API definida, y `tests/`.
**Límites:** no enviar mensajes en planificación; no implementar aquí; `promotion: not_authorized`; dependencias y gates son prerrequisitos, no permisos concedidos.

##

## Hallazgos/disposición contra intención

Comparación aceptada por contenido completo: propósito/resultado/repo/límites coinciden con contrato; dry-run identifica fuentes, cambios futuros, dependencias/transferencias y pruebas específicas, sin ejecutar. Gates técnicos se verifican por efecto propio, sin sustituirlos por permiso/UI o receipt vecino. Respeta estados reales/no disponibles, decisiones registradas y autorización futura separada. Ninguna ambigüedad real pendiente; no se acepta por token APTO. Timeout es fallo local de operación sin confirmación; jamás afirma resultado remoto del Hub no observado (límite de WS34.1/identidad WS32 y contrato WS12), observación no bloqueante del concilio separada.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
