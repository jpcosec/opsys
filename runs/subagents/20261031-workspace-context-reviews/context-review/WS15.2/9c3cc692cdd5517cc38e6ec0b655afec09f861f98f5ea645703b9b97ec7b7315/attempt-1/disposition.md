# Executor comparison — WS15.2

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION

- **Propósito**: entregar, en `graph_ui`, la orientación para un proyecto sin desk dentro del lector del workspace.
- **Resultado**: al abrir un proyecto sin desk se muestra orientación, la ruta absoluta del proyecto como destino y el comando `deskops init <ruta>`; nunca se inicializa por GET; tras un `init` externo real, refrescar lectura muestra el desk real.
- **Repo dueño**: `graph_ui` (`frontends/mindmap/views/workspace/orientation/`; rutas de lectura según contrato WS11; `tests/`).
- **Límites**: no crear desks desde UI; solo orientación y handoff al CLI; sin mutaciones; aceptación pendiente de recibo G_UI_READ por delta; implementación no autorizada aún.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
