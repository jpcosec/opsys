# Executor comparison — WS26.2, final per-effect contract input

State: accepted_current

## Reformulación examinada

## REFORMULACION

**Propósito:** definir el encargo de enrutar una tarea en el Board y mostrar la capa lista. **Resultado:** tarea añadida a `tasks` del BoardDoc por operación pública y visible en `deskops show board`/UI; capa lista separada de tareas en ejecución, con dependencias pendientes o archivos solapados. **Repo dueño:** `graph_ui`, en `frontends/mindmap/views/workspace/routing/`, endpoints autorizados por WS12 y `tests/`. **Límites:** no implementar promoción nueva; usar solo operación completa admitida por WS12 o dejar handoff/pendiente; no confundir enrutar con ejecutar; ante glob o resolución dudosa, no marcar lista con heurística optimista.

##

## Hallazgos/disposición contra intención

No hay gate humano nuevo: resultado requerido ante resolución dudosa es «no comprobado», nunca ready por heurística. Supervisor es rol del workflow del repo identificado en promoción; evidencia de no solapamiento/normalización sale contrato WS12 y ritual de fase, no override UI. TaskDoc/run fija responsable/canal antes ejecutar. Dry-run conserva caso negativo obligatorio; no inventa aprobación para escribir. Campo files ausente no prueba no-solapamiento: regla de «no comprobado» ante resolución dudosa y no heurística optimista lo cubre; TaskDoc/contrato WS12 deben completar archivos antes marcar capa lista. No se interpreta ausencia como autorización ready.

Se leyó y contrastó output completo (reformulación, ambigüedades, dry-run y futuro). Rúbrica: resultado/repo/límites, orden/autoridad, aceptación verificable, decisiones y efectos con dueño. Detalles asignados a contrato/TaskDoc no autorizan improvisación: si falta el contrato/capability, detener y registrar hueco. No se ejecuta producto ni se declara recepción. Ningún output/disposición anterior fue input del modelo.
