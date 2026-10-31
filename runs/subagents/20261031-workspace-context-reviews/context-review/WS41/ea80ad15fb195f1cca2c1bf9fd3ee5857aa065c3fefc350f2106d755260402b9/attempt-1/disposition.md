# Executor comparison — WS41, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION

**Propósito:** implementar lectura segura entre desks en `graph_ui`, resolviendo aliases/roots autorizados por el contrato WS11 mediante APIs públicas de store.

**Resultado:** UF08 sobre dos stores del corpus WS40: identidad/origen visibles, seguimiento de enlaces authored entre desks, retorno por historia y errores visibles ante alias no autorizado, path escapado o store ausente. Sin federación ni copia de contenido.

**Repo dueño:** `graph_ui`, en `frontends/mindmap/source/`, `views/workspace/` y `tests/`.

**Límites:** solo lectura; cada request conserva proyecto/store sin alterar `SLDB_STORE` global; sin mutaciones cruzadas; requiere recibo `G_UI_READ` por delta. Promoción no autorizada.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
