## REFORMULACION
**Propósito:** integrar en graph_ui la navegación entre conocimiento y grafo local reutilizando el grafo y el documento genérico existentes. **Resultado:** vista de grafo/contexto que muestra átomos, protoátomos, crossroads, materializaciones, pills, clasificación y vecindad, con ida/vuelta por fuentes y backlinks derivados, y soporte no modelado visible. **Repo:** graph_ui (`output_base: graph_ui:repository_root/`), alcance en `frontends/mindmap/views/workspace/graph/; Context; tests/`. **Límites:** depende de WS13 y WS18; exige G_UI_READ; no promueve ni duplica tarea existente; no crea un renderer obligatorio por clase.

## AMBIGUEDADES
1. **«backlinks derivados»** — no se indica qué contrato, store o consulta los deriva ni quién los produce. Obliga a inventar la fuente y el criterio de derivación, y la aceptación deja de ser comprobable.
2. **«clasificación y vecindad»** — no se define qué clasificación (¿átomos/protoátomos/crossroads?) ni qué relaciones o profundidad constituyen vecindad. Obliga a inventar semántica funcional.
3. **«soporte no modelado visible»** — no se especifica qué cuenta como no modelado ni qué visibilidad mínima se exige. Obliga a inventar el criterio de aceptación.
4. **«preservar Code local de tarea actual»** — no se identifica la tarea ni qué parte de Code debe preservarse. Obliga a inventar el límite de no regresión.

## DRY-RUN
**Lecturas previstas:** nodo WS24 en `dag.yaml`, guía de revisión, brief, alcance, decisiones, cobertura y reconciliación. **Cambios previstos:** ninguno en esta revisión; una ejecución futura tocaría vistas de grafo, Context y tests en graph_ui. **Dependencias:** WS13 (lector agregado), WS18 (proyecciones ViewDoc/NotationDoc) y G_UI_READ pendiente. **Validaciones futuras:** aceptación de G_UI_READ por WS11; prueba de ida/vuelta y backlinks; validación manual WS30; consumo posterior por WS29 y WS42.

## FUTURO
WS11 obtiene G_UI_READ y designa al responsable receptor; WS18 entrega las proyecciones; WS13 entrega el lector; WS06/WS12 confirman integración sin duplicar tarea; WS30 ejecuta la validación humana; WS29 y WS42 consumen este nodo.
