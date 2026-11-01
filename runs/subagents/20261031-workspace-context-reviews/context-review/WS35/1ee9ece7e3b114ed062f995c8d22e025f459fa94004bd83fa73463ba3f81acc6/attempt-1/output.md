## REFORMULACION

Propósito: planificar una vista de solo lectura en `graph_ui` que muestre la cadena tarea→intento→mensajes/resultados→decisión con trazabilidad a la fuente. Resultado: un nodo de implementación `WS35` (kind implementation, delivery) en `frontends/mindmap/views/workspace/execution/` y `tests/`, con aceptación comprobable por test. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: no edita ni aprueba; `completed` no equivale a aprobado/cerrado; solo lectura de datos producidos por otros nodos; promoción `not_authorized`. Depende de WS33 (vínculos mensaje/resultado/decisión) y WS27 (diff/evidencia); requiere G_SCION (aún `unverified`) y G_UI_READ (per_delta, sin recibos).

## AMBIGUEDADES

1. “Cada mensaje, resultado y decisión se muestra bajo su intento y tarea” frente a “los mensajes no vinculados quedan como hueco de procedencia” (WS33.1). El input no dice qué hace la vista con mensajes/resultados sin intento resoluble: ¿se ocultan, se agrupan en una sección de huecos de procedencia, o se muestran sin agrupación? Obligaría a inventar el criterio de presentación y su aceptación para ese caso, que WS33.1 declara existente.

## DRY-RUN

Lecturas previstas: `dag.yaml` (nodo, aristas WS33/WS27/WS33.1, gates), guía, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md` y `desk/drawer/tasks/workspace-documental/task-ws35.md` al promover. Cambios previstos: vista de ejecución/trazabilidad y pruebas en `graph_ui`; sin tocar tablas Scion ni backend. Dependencias: WS33 (agregado, incluye WS33.1), WS27 (agregado), lector WS13 para abrir evidencia. Validaciones futuras: acta de recepción G_UI_READ específica de este delta, G_SCION resuelto por WS44, pruebas de enlace a fuente y de que `completed` no se rotula como aprobado/cerrado. Sin ejecución.

## FUTURO

La promoción (TaskDoc, archivos exactos, pills, preflight) la produce el nodo de promoción; la autorización de implementación no existe aún. WS36 consume esta vista para delegación/intervención. El acta per_delta la emite el receptor humano de `graph_ui` (P01). WS44 resuelve G_SCION.
