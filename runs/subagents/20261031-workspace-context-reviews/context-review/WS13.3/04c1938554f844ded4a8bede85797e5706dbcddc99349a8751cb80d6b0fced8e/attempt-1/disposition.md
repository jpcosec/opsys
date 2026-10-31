# Executor comparison — WS13.3, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
- **Propósito:** encargar en `graph_ui` la apertura de documentos en pestañas y en dos divisiones, con foco e historia de navegación.
- **Resultado:** pestañas que se abren, cambian y cierran; dos documentos lado a lado; alternancia de documento activo; “volver” que conserva documento, foco, origen e historia; disposición local de sesión, sin persistencia tras recargar.
- **Repo:** `graph_ui`, en `frontends/mindmap/views/workspace/layout/`, rutas de lectura del contrato WS11 y `tests/`.
- **Límites:** depende de WS11 y WS13.1; gate `G_UI_READ` pendiente por delta; no duplica el workspace ni exige persistencia; no se ejecuta nada.

##

## Hallazgos/disposición contra intención

Descartados 1–3: nodo depende WS11, cuyo contrato explícito fija foco/enlaces/historia. Combinación de pestañas/divisiones y qué cambios originan historia se concreta allí/TaskDoc antes implementar, sin reducir apertura/cambio/cierre/volver con foco/origen. Guía delega escenarios exactos/pantallas a promoción. No se pretende probar aceptación sin ese contrato; regla común detiene si falta. Reformulación/dry-run sí recuperan función completa y gate por delta.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
