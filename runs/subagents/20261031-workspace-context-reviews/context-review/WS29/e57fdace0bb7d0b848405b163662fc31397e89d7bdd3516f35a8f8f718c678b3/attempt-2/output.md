## REFORMULACION

Propósito: que graph_ui integre una vista Changes que haga comprobable el impacto de una mutación real y agrupe hallazgos de integridad. Resultado: delta sobre el ticket Changes existente, con salida en `frontends/mindmap/views/workspace/changes/`, rutas de integridad fijadas por contrato WS11 y tests. Repo dueño: graph_ui. Límites: no supone CST ni árbol Kimun; no repara automáticamente, solo enlaza al comando documentado; no bloquea lector/manual básico. Depende de WS15 (errores/modo degradado) y WS24 (conocimiento/grafo local); G_UI_READ se recibe por delta.

## AMBIGUEDADES

ninguna

## DRY-RUN

Leería el contrato WS11 para rutas de integridad, el ticket Changes y su draft, las salidas de WS15/WS24, la documentación de `sldb stores check`, `deskops doctor` y `deskops drift check`, y el corpus o store temporal. Cambios previstos: nueva vista bajo `changes/`, enlace desde el workspace y tests; sin reparación automática. Consumiría G_UI_READ de WS29 —acta del receptor P01—, no de otros deltas. Validaría creando un store temporal real, introduciendo una mutación y comprobando documento afectado, relaciones entrantes/salientes a 1 hop vía API de grafo de sldb y errores agrupados por comando, con enlaces a la documentación del repo dueño. Si falta WS11, la API de grafo o un comando, se detiene y registra el hueco con repo dueño, sin sustituto. La promoción fijará archivos exactos y escenarios de prueba.

## FUTURO

WS11 produce el contrato de rutas; WS15 y WS24 sus implementaciones; WS40 el corpus; el receptor P01 emite el acta G_UI_READ de WS29. La promoción autoriza y concreta archivos, pills, evidencia y pruebas; el dueño del ticket Changes decide extensión o delta. La documentación de los tres comandos la producen deskops y sldb en sus repos.
