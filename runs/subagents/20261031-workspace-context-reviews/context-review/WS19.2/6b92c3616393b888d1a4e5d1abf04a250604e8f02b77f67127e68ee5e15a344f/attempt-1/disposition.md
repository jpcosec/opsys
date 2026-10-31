# Executor comparison — WS19.2, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
**Propósito:** implementar en `graph_ui` el alta y baja de relaciones permitidas por el contrato de WS12, usando API real y before-image, sin definir semántica de relaciones en el componente.

**Resultado:** mutaciones de relaciones que persisten y se confirman tras recargar; una relación no permitida o una revisión obsoleta se rechaza con error visible.

**Repo:** `graph_ui`.

**Límites:** alcance en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`; no crear semántica de relaciones; no editar campos workflow-protected; G_HUMAN_READ solo habilita uso de mutaciones en UI, no bloquea desarrollo/pruebas aisladas de API; no duplicar la base ya integrada; promoción no autorizada.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
