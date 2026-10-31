# Executor comparison — WS21, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

REFORMULACION
Propósito: integrar en el workspace de graph_ui la alternancia fuente/renderizado del mismo origen documental, conservando foco y buffer sucio, usando solo guardado fuente autorizado. Resultado: delta en `frontends/mindmap/views/workspace/` y `tests/`; con P04 `editable`, fuente/render editables con API reversible, conflicto y roundtrip; con `read_only`, fuente no editable y campos editables por API. Repo dueño: graph_ui. Límites: no crear semántica de composición fuera de WS12; sin soporte, composición read-only declarada; no descartar buffer sin confirmación; no preparar/promover con `pending`; no prometer edición fuente en read_only. Depende de WS19 y, en editable, de WS20/G_SOURCE; gates G_UI_WRITE y G_WRITE_CONTRACT. Aceptación comprobable por variante y contratos.

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
