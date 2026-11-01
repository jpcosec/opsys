## REFORMULACION
**Propósito:** añadir a graph_ui un explorador que permita descubrir y abrir documentos modelados del store y Markdown no modelado del desk sin conocer su ID.
**Resultado:** delta en `frontends/mindmap/views/workspace/explorer/`, rutas de lectura según WS11 y tests; altas visibles tras refresco explícito del catálogo, sin reiniciar ni cambiar código.
**Repo dueño:** graph_ui. **Límites:** reutilizar catálogo/filtro existente para modelados; no crear índices nuevos ni otro workspace; no inventar API de sldb; WS11 fija API/seguridad para no modelados; gate G_UI_READ por delta.

## AMBIGUEDADES
Ninguna. El nodo nombra repo, resultado, aceptación comprobable y dependencias; las reglas para contratos ausentes están en alcance.md y WS11 es productor explícito.

## DRY-RUN
Un ejecutor futuro leería WS11 (`contratos/navegacion.md`), la salida de WS13.1, `workspace_routes.py`, `workspace-view.js`, `reconciliacion.md` (C-08) y el corpus/tests existentes. Cambiaría: componente explorador; listado del catálogo del store; listado seguro del árbol del desk según rutas/seguridad WS11; refresco explícito del catálogo; tests con store temporal real y archivos del desk. Consumiría el contrato WS11 y el lector de WS13.1; si falta el contrato, API, dato o permiso, se detendría y registraría el hueco con repo dueño, sin sustituto. G_UI_READ requiere acta de recepción del delta concreto; sin ella no se promueve. Validaría: abrir un modelado y un no modelado sin ID; añadir ambos y verlos tras refresco sin reiniciar ni cambiar código; no usar índices nuevos; ejecutar tests. El padre WS13 es agregado no ejecutable: se cumple cuando WS13.1–WS13.3 aceptan; WS13.2 transfiere el explorador al resultado conjunto del workspace, compartiendo archivos con sus hermanos sin crear secuencia entre ellos.

## FUTURO
WS11 produce el contrato de navegación; el solicitante P01/receptor produce el acta G_UI_READ por delta; la promoción fija TaskDoc, archivos, pills y evidencia; WS16 valida uso humano posterior.
