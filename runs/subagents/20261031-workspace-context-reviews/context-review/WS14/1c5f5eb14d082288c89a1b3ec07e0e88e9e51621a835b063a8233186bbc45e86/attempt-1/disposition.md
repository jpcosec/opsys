# Executor comparison — WS14

State: requires_contract_correction_rereview

## Reformulación examinada

## REFORMULACION

**Propósito**: integrar en el workspace de `graph_ui` una búsqueda navegable que use la API real de búsqueda (`sldb find` o su ruta en `sldb serve`), sin parser propio, abriendo resultados con su identidad y ruta de origen.

**Resultado**: búsqueda con teclado que conserva consulta y foco al abrir y volver; tres estados diferenciados (sin resultados, error de backend declarado, búsqueda degradada con límite declarado); sin recargar el grafo completo por tecla.

**Repo dueño**: `graph_ui`; salidas en `frontends/mindmap/source/`, `views/workspace/`, `tests/`.

**Límites**: candidato `status: candidate`, `promotion: not_authorized`; depende de WS13 (agregado) y, de forma transitiva, del contrato WS11 (produce `G_UI_READ`, pendiente) y de `auditoria/infraestructura.md` de WS03. Sin ejecución en esta revisión.

##

## Comparación con intención / hallazgos

1 ambigüedad léxica corregida (Sin resultados = búsqueda vacía, no prohibición). 2 prueba observable añadida: tecleo no dispara petición de carga completa de grafo; no requiere inventar umbral/debounce.

Se leyó reformulación, ambigüedades, dry-run y futuro del output completo. Se compara propósito/resultado/repo/límites, secuencia/autoridad, aceptación y decisiones con contrato suministrado. No se inyecta este output o disposición al siguiente modelo.
