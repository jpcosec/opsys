# Executor comparison — WS14, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION

**Propósito:** integrar en el lector del workspace una búsqueda navegable sobre la API real de SLDB, sin parser propio ni duplicar el grafo.

**Resultado:** búsqueda por texto/campos/semántica según capacidad real; resultados que abren el documento con identidad y ruta de origen; estados distintos de sin resultados, error y degradación; consulta y foco conservados al volver; sin carga completa del grafo por tecla.

**Repo:** `graph_ui`, con salidas en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** no implementar búsqueda semántica inexistente, no crear parser alternativo, no prometer cobertura total si la API es parcial. Promoción aún no autorizada; gate `G_UI_READ` es por delta.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
