## REFORMULACION
WS28 es un nodo `implementation` de graph_ui que integra en la vista de revisión la verificación de closeout mediante `deskops closeout verify` por el canal del contrato WS12: diagnostica faltantes y ofrece handoff explícito con evidencia a `deskops closeout commit` por CLI en modo manual, o al coordinador activo (P03). Prohíbe commit/cierre por HTTP y terminal embebido genérico. Resultado: UF05 verificable y handoff, sin ejecutar el cierre. Límites: salidas en `review/`, `endpoints` y `tests/`; dependencias WS27/WS12/WS48; gates G_CLOSEOUT/G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT.

## AMBIGUEDADES
1. «frontends/mindmap/views/workspace/review/; endpoints; tests/» (output_scope). Obliga a inventar qué endpoints, si son HTTP de solo lectura para verify o parte del adapter, y su contrato, cuando solo se prohíbe commit/close por HTTP.
2. «y se refresca el estado desde deskops» (acceptance). Obliga a inventar quién ejecuta el refresco, con qué comando/canal y cómo se comprueba; el nodo solo prepara handoff y el cierre lo ejecuta un actor externo.

## DRY-RUN
Un ejecutor leería el nodo, el contrato WS12 (operaciones verify/commit, adapter, efectos por delta), el punto de admisión WS48, la integración de revisión WS27 y la aceptación. Cambios previstos: añadir en `review/` el bloque de verificación que invoca verify por el adapter, lista faltantes y ofrece handoff copiable/solicitud con evidencia; sin ruta HTTP de commit; pruebas con store temporal. Consumo: WS12 debe entregar la operación y su recibo por delta; si falta, detenerse y registrar hueco en deskops; WS48 se consulta antes de toda escritura UI y puede devolver lectura/handoff con causa; G_CLOSEOUT ya satisfecho. Gates: G_WRITE_CONTRACT/WS28 y G_UI_WRITE/WS28 por delta; G_HUMAN_READ habilita uso, no desarrollo/pruebas aisladas. Errores: verify falla → mostrar faltantes; admisión denegada → lectura/handoff; cierre externo no ejecutado → comando o solicitud no equivalen a cierre. Validación: tests con store temporal y comprobación de `deskops show task` más commit de closeout y refresco.

## FUTURO
WS12 publica el contrato por delta; WS48 publica la admisión; WS16 produce el acta G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; CLI/coordinador ejecuta el commit externo; WS30 valida UF05.
