# Executor comparison — WS27.2, round2

State: superseded_input_changed_requires_fresh_review

## Reformulación examinada

## REFORMULACION
Propósito: definir la vista de evidencia junto a la TaskDoc, mostrando estados declarada, encontrada y verificada sin crear un modelo de comentarios. Resultado esperado: UI en `graph_ui`, bajo `frontends/mindmap/views/workspace/evidence/`, con pruebas, capaz de abrir soportes Markdown del workspace y señalar rutas no soportadas. Repo dueño: `graph_ui`. Límites: depende de WS13 (lector) y WS12 (contrato de operaciones); requiere `G_UI_READ` por delta; no infiere evidencia por extensión; “verificada” es el resultado del gate vía `deskops closeout verify`, no prueba independiente; reporte ausente o fallo es no verificable con error; no hay mutaciones ni cierre nuevo; promoción no autorizada.

##

## Hallazgos/disposición contra intención

Comparación aceptada: propósito/resultado/repo/límites coinciden con contrato; dry-run enumera fuentes, cambio futuro/hijos, dependencias y aceptación comprobable sin ejecutar. Futuro asigna APIs/actas/permisos a productores reales; no convierte decisiones base ni commit existente en aprobación de delta. Ninguna ambigüedad no resuelta. La aceptación procede del contenido completo, no APTO.

Se leyó output completo (reformulación, ambigüedades, dry-run y futuro); comparación evalúa resultado/repo/límites, secuencia/autoridad, aceptación y ausencia de decisiones inventadas. No se suministra output/disposición en siguientes intentos.
