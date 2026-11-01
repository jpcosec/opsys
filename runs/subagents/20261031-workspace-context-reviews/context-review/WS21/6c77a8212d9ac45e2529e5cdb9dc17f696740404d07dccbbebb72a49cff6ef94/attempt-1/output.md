## REFORMULACION
WS21 es un encargo de implementación en `graph_ui`: integrar en `frontends/mindmap/views/workspace/` la alternancia fuente/render sobre el mismo origen, con revisión, buffer sucio y guardado autorizado; la composición solo escribe en el documento dueño y, sin soporte, queda en lectura declarada. Resultado: la variante P04; con `source_mode=editable` exige WS20/G_SOURCE y prueba edición, conflicto y roundtrip; `read_only` deja fuente no editable y campos por API. Límites: no crear semántica de relaciones, no escribir Markdown directo desde browser, no descartar buffer sin confirmación, no ejecutar con `pending` ni duplicar WS19. Repo `graph_ui`; alcance `views/workspace/` y `tests/`; depende de WS19 y de G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «El guardado por campos exige G_PAYLOAD_PRECONDITION en ambas variantes» frente a «Alternar fuente/render... usar guardado fuente autorizado». Obliga a inventar si WS21 implementa/ajusta el guardado por campos o solo integra y prueba el de WS19; el límite y el riesgo de duplicación no están fijados.
2. «Al alternar con cambios sin guardar se conserva el buffer...» no se recoge en «se prueba edición/conflicto/roundtrip». Obliga a inventar si conservar buffer/foco es criterio de aceptación verificable o comportamiento auxiliar.

## DRY-RUN
Lecturas: contrato WS12, recibos G_SOURCE/G_PAYLOAD_PRECONDITION/G_WRITE_CONTRACT/G_UI_WRITE, API de WS20, WS19 integrado, rutas y tests actuales. Cambios previstos: conectar el toggle fuente/render al mismo payload; cargar/guardar fuente por API autorizada con revisión; preservar buffer/foco y confirmar descarte; tratar 409 y campos protegidos; composición solo en documento dueño; sin escritura directa de Markdown. Dependencias: WS19 y WS20/G_SOURCE; gates. Si falta contrato/API/gate, detener y registrar hueco sin sustituto. Validación esperada: tests de roundtrip, conflicto, buffer, protegidos y composición; recibo G_UI_WRITE; después WS30. Errores: 409, fuente no disponible, backend ausente y composición sin soporte (solo lectura declarada).

## FUTURO
WS20 produce la API/G_SOURCE; WS45, G_PAYLOAD_PRECONDITION; WS12, G_WRITE_CONTRACT; el receptor P01 emite G_UI_WRITE; WS30 valida manualmente; WS19 entrega la edición de campos. Nada autoriza aún promoción ni implementación.
