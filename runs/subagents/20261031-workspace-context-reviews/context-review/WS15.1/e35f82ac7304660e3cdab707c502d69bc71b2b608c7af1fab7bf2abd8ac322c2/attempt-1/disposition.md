# Executor comparison — WS15.1

State: accepted_old_input_superseded

## Reformulación examinada

## REFORMULACION
Propósito: que el lector del workspace muestre errores de lectura y degradación sin fingir vacío ni perder estado. Resultado: error en el panel afectado, distinguido por la respuesta de la API según WS11; fallo CDN visible; reintento manual que conserva pestañas, foco e historia; tests. Repo: `graph_ui`. Límites: solo `frontends/mindmap/views/workspace/errors/`, rutas definidas por WS11 y `tests/`; sin empaquetado offline ni mutaciones; `G_UI_READ` se recibe por delta.

##

## Comparación con intención / hallazgos

Aceptado por comparación: reformula propósito/resultado y repo del contrato suministrado; dry-run identifica lecturas, cambios futuros (o agregación hijos), prerrequisitos y validación real. Respeta límites/no ejecución y asigna contratos/actas/permisos futuros a productores sin inventar aprobación. Ambigüedades: ninguna. Coincide con alcance y aceptación del nodo; no se usa un veredicto APTO como evidencia.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
