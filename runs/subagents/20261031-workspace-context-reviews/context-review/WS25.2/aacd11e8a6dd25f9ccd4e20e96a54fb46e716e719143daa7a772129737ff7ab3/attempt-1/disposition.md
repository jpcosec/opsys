# Executor comparison — WS25.2

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

**Propósito:** implementar en `graph_ui` la captura interna con destino elegido explícitamente por la persona usuaria —candidato de drawer o protoátomo— usando únicamente operaciones permitidas por el contrato WS12, sin exigir ni crear tarea.

**Resultado:** UI y endpoints en `frontends/mindmap/views/workspace/capture/` y `tests/`, con cada destino probado por separado. Una captura debe persistir tras recargar, conservar un origen tipado —ruta o mensaje— y mostrarlo, sin tarea implícita. Permisos del contrato aplicados.

**Repo dueño:** `graph_ui`.

**Límites:** no se autoriza promoción; no hay commits ni closeout; no se diseñan canales ausentes; no se exceden las operaciones del contrato WS12. Desarrollo y pruebas aisladas de API pueden avanzar sin acta humana, pero las mutaciones en UI requieren `G_HUMAN_READ`.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
