# Executor comparison — WS19.2

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

**Propósito:** planificar la edición de relaciones —alta y baja— solo para las permitidas por el contrato de operaciones de WS12, sin definir semántica de relaciones dentro del componente.

**Resultado esperado:** en `graph_ui`, una vista/componente de relaciones que persiste altas y bajas mediante API real y before-image, confirma el cambio tras recargar y rechaza con error visible una relación no permitida o una revisión obsoleta.

**Repo dueño:** `graph_ui`, con salida en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por el contrato WS12 y `tests/`. Modo de integración: delta sobre ticket existente o ticket atómico, nunca duplicado paralelo.

**Límites:** depende de WS12; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT. G_HUMAN_READ bloquea el uso de mutaciones en UI, no el desarrollo ni pruebas aisladas de API. No se autoriza promoción.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
