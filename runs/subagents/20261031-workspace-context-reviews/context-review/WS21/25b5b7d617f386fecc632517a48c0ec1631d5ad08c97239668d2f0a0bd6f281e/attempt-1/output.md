REFORMULACION
Propósito: integrar en graph_ui la alternancia fuente/render según la variante P04 de `source_mode`. Resultado: en `editable`, fuente/render editables con guardado autorizado, revisión, conflicto y roundtrip; en `read_only`, fuente legible no editable y edición por campos; buffer sucio conservado y composición limitada al documento dueño. Repo: graph_ui (`frontends/mindmap/views/workspace/`; `tests/`). Límites: ejecutar solo la variante elegida; con `pending` no se prepara ni promueve; sin G_SOURCE no hay guardado fuente; campos workflow protegidos fuera; composición sin soporte queda solo lectura; WS30/manual no declaran edición fuente en `read_only`.

AMBIGUEDADES
1. «Al alternar con cambios sin guardar se conserva el buffer; nunca se descarta sin confirmación explícita de la persona usuaria» no aparece en la aceptación, que solo exige «Cumplir la aceptación específica de la variante P04» y, en editable, «edición/conflicto/roundtrip». Obliga a inventar si conservar/confirmar el buffer es criterio aceptable y cómo comprobarlo.
2. «En editable ... se prueba edición/conflicto/roundtrip» no precisa si «edición» incluye campos; en `read_only` sí exige «edición por campos probada». Obliga a decidir si el modo editable debe probar también edición por campos, no solo fuente.

DRY-RUN
Un ejecutor futuro comprobaría que `source_mode` no es `pending` y leería TaskDoc WS21, contrato WS12 (composición y precondición), salidas WS19/WS48 y, si editable, WS20/G_SOURCE; exigiría G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT por delta. Cambiaría solo `frontends/mindmap/views/workspace/` y `tests/`: alternancia, buffer sucio, guardado fuente autorizado, edición por campos con documento dueño y degradación readonly. Validaría en store temporal: roundtrip, conflicto, campos protegidos, buffer conservado y composición. Si falta contrato, gate o API: detenerse, registrar hueco con repo dueño y no sustituirlo.

FUTURO
WS07/P04 confirma la variante; WS12 fija contrato y precondición; WS45 produce G_PAYLOAD_PRECONDITION; P01 emite el acta G_UI_WRITE; WS30 valida manualmente; WS20/G_SOURCE en editable.
