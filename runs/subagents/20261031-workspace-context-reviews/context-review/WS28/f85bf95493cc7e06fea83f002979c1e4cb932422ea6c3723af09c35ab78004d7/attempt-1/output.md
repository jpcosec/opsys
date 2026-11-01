REFORMULACION  
WS28 encarga integrar en graph_ui la verificación de cierre y el handoff: consultar/ejecutar `deskops closeout verify` por el canal que fije el contrato WS12, diagnosticar faltantes y ofrecer handoff con evidencia a `deskops closeout commit` por CLI en modo manual o al coordinador activo (P03). Resultado: UF05 puede terminar con cierre externo confirmado por `deskops show task` y commit, refrescando estado desde deskops; comando o solicitud no equivalen a cierre. Repo dueño: graph_ui; salidas: frontends/mindmap/views/workspace/review/, endpoints, tests/. Límites: no commit/close por HTTP en baseline ni terminal embebido genérico; depende de WS27/WS12 y requiere G_CLOSEOUT, G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT.

AMBIGUEDADES  
ninguna.

DRY-RUN  
Un ejecutor futuro, solo tras promoción y TaskDoc, leería task-ws28.md, contrato WS12, salidas de WS27, evidencia G_CLOSEOUT y recibos G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT para WS28. Cambiaría archivos de review y pruebas bajo graph_ui, integrando el adapter WS12 para verify, vista de faltantes, generación de handoff y refresco de estado; no añadiría commit/close HTTP ni terminal. Si falta canal/contrato WS12 o recibo de gate, se detendría, registraría hueco y no habilitaría uso UI; podría probar aislado. Errores: verify no disponible, faltantes, conflicto de estado, handoff no ejecutado o refresco fallido → diagnóstico/degradado, nunca cierre inferido. Validación esperada: tests con store temporal/corpus WS40 y comprobación de que `deskops show task` y commit externo confirman cierre; WS30 hará validación humana.

FUTURO  
WS12 publica contrato/canal y whitelist; WS27 entrega revisión/evidencia; WS16 produce acta G_HUMAN_READ; P01 receptor emite G_UI_WRITE por delta; CLI/coordinador ejecuta el commit de closeout; WS30 valida UF05 y WS43 publica entradas reales.
