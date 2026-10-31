REFORMULACION
Propósito: integrar en el workspace de graph_ui la alternancia fuente/renderizado del mismo origen documental, conservando foco y buffer sucio, usando solo guardado fuente autorizado. Resultado: delta en `frontends/mindmap/views/workspace/` y `tests/`; con P04 `editable`, fuente/render editables con API reversible, conflicto y roundtrip; con `read_only`, fuente no editable y campos editables por API. Repo dueño: graph_ui. Límites: no crear semántica de composición fuera de WS12; sin soporte, composición read-only declarada; no descartar buffer sin confirmación; no preparar/promover con `pending`; no prometer edición fuente en read_only. Depende de WS19 y, en editable, de WS20/G_SOURCE; gates G_UI_WRITE y G_WRITE_CONTRACT. Aceptación comprobable por variante y contratos.

AMBIGUEDADES
Ninguna. La composición, el guardado autorizado y la revisión remiten a contratos con productor identificado (WS12, WS20); las reglas comunes cubren su ausencia y el TaskDoc de promoción fijará archivos, textos y pruebas.

DRY-RUN
- Lecturas previstas: nodo WS21, `source_mode`/P04, contratos WS12 y WS20/G_SOURCE, WS19, guía; sin ejecutar.
- Cambios previstos: solo workspace de graph_ui y tests; alternancia fuente/render, conservación de buffer/foco, guardado fuente autorizado en editable, escritura de composición solo al documento dueño si WS12 lo soporta, fallback read-only declarado.
- Dependencias: WS19; WS20 y G_SOURCE solo en editable; G_UI_WRITE/G_WRITE_CONTRACT por delta.
- Validaciones futuras: G_SOURCE/G_WRITE_CONTRACT, edición/conflicto/roundtrip, no descarte sin confirmación, composición dueña o read-only, edición por campos en read_only, etiquetado manual/WS30.

FUTURO
WS20 produce API/G_SOURCE; WS12 define el contrato de composición; el receptor humano emite G_UI_WRITE por delta; WS19.1/19.2 habilitan edición por campos; WS30 y el manual validan y etiquetan alcance; WS06/promoción fija TaskDoc, archivos y pruebas; la persona usuaria decide en uso si confirma el descarte del buffer.
