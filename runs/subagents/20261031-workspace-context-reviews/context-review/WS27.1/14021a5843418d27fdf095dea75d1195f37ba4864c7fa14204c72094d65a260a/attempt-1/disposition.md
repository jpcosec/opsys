# Executor comparison — WS27.1, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
- **Propósito:** añadir al workspace una vista read-only de diff e historial Git junto a la TaskDoc, usando `TaskDoc.references` y `TaskDoc.files`.
- **Resultado:** diff real e historial acotados a repo/tarea; una sección por repo alcanzado, con root declarado; sin commits, diff working tree→HEAD; ruta sin repo resoluble queda no disponible.
- **Repo:** `graph_ui`; salida en `frontends/mindmap/views/workspace/diff/` y `tests/`.
- **Límites:** no escribir ni revertir; no mostrar integridad del store (WS29); la asociación a intento llega en WS35; `G_UI_READ` es por delta y sigue pendiente; no se ejecuta nada.

##

## Hallazgos/disposición contra intención

Descartado como estados de error/ausencia ya asignados a contratos WS11/12 y TaskDoc: scope limita historial a commits resolubles y files, declara ausencia de historial cuando no hay commits y ruta sin repo no disponible. No permite convertir ref inválida en éxito. UI del motivo/filtro vacío son detalle de esos escenarios futuros, no cambio de resultado/dueño/autoridad. Dry-run identifica casos con/sin commits y varios repos, sin escrituras.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
