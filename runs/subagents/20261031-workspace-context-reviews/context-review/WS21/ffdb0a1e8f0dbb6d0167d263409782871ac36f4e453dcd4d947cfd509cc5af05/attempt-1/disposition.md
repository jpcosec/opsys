# Executor comparison — WS21

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

**Propósito:** entregar en `graph_ui` la alternancia fuente/renderizado de un documento bajo `source_mode`, conservando el mismo origen, revisión y buffer sucio.
**Resultado:** vista con fuente y render editables en la variante P04 vigente (`editable`), composición escribiendo solo en el documento dueño cuando WS12 lo soporte, y pruebas en `tests/`.
**Repo/límites:** propietario `graph_ui`, alcance `frontends/mindmap/views/workspace/; tests/`. Solo la variante elegida por P04; con `pending` no se prepara ni promueve; no implementa WS20, no hace commits, no modifica otros repos ni autoriza Scion. Si falta soporte de composición, queda solo lectura y se declara.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
