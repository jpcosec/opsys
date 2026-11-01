REFORMULACION
WS21 es un encargo de implementación de graph_ui: integrar en el workspace la alternancia fuente/renderizado de un documento según `source_mode`, con un único origen, revisión y buffer sucio. Resultado: vista que conserva buffer/foco, no descarta cambios sin confirmación y, en la variante editable, permite guardar fuente por API autorizada con conflicto/roundtrip; si WS12 no define soporte de composición, esta queda read-only y declarada. Repo dueño: graph_ui. Alcance: `frontends/mindmap/views/workspace/` y `tests/`. Límites: no implementa WS20/WS45, no edita campos protegidos, no promueve ni ejecuta variantes `pending`; archivos, textos y pruebas exactas son del TaskDoc de promoción.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería el nodo y su variante, `source_mode`, WS12/G_WRITE_CONTRACT, G_PAYLOAD_PRECONDITION, G_UI_WRITE, WS19 y, en editable, WS20/G_SOURCE; revisaría la implementación existente del workspace y sus tests. Cambios previstos: alternancia fuente/render y estado de buffer en `views/workspace/`; guardado de fuente solo por API autorizada; guardado por campos con precondición y conflicto visible; composición limitada al documento dueño; pruebas en `tests/`. Dependencias: WS19 terminado y gates por delta satisfechos; en editable, WS20 y G_SOURCE. Errores: gate/contrato ausente ⇒ detener y registrar hueco, operación no disponible; conflicto ⇒ no sobrescribir y conservar buffer; falta de confirmación ⇒ conservar buffer. Validación esperada: tests de alternancia, buffer, conflicto/roundtrip, campos protegidos y composición read-only si no hay soporte, con store temporal/WS40; después WS30/manual. No se ejecuta aquí.

FUTURO
Otros nodos/humanos producen: WS20/G_SOURCE; WS45/G_PAYLOAD_PRECONDITION; WS12/G_WRITE_CONTRACT; WS19 y sus hijos; el receptor P01 emite G_UI_WRITE por delta; WS30/WS31 y el manual validan el uso. La promoción fija archivos, TaskDoc, pills y textos. Un humano decide cualquier cambio de `source_mode` o alcance; no se inventa.
