# Executor comparison — WS22, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION

**Propósito:** que el lector del workspace muestre el Board real como trabajo navegable, sin sustituir el workflow.

**Resultado:** tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc y sus pills/átomos referenciados, con selección y links comunes con el lector. Estados y condiciones de lifecycle se leen de deskops (Board, lifecycle), no de `dag.yaml`.

**Repo dueño:** `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/board/` y `tests/`.

**Límites:** no reemplazar workflow con drag-and-drop de status; no duplicar tareas; no presentar un predicado satisfecho como test aprobado. Depende de WS13 (agregado lector) y WS09 (catálogo de renderizaciones); requiere G_UI_READ por delta.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
