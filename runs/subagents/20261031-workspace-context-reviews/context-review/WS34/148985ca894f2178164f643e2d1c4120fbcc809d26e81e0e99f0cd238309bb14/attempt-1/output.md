## REFORMULACION
WS34 es un nodo agregado de planificación (no ejecutable) del plan workspace-documental. Propósito: encargar la exposición de un adaptador público restringido para dispatch/reply de Scion, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Resultado: agregado de las salidas de WS34.1 (dispatch) y WS34.2 (reply). Repo dueño: deskops. Límites: nada de shell arbitrario ni duplicar transporte; no enviar mensajes en planificación; cada hijo solo avanza con la política de timeout que WS12 produzca para su delta, deteniéndose y registrando el hueco si falta; gates G_EXEC, G_SCION y G_WRITE_CONTRACT pendientes; promoción no autorizada.

## AMBIGUEDADES
Ninguna. Las referencias a «autoridad del coordinador» y a la política de timeout remiten a WS12, productor nombrado; «identidad de intento» se concreta en WS32.1/WS32.2; la ubicación exacta de archivos la fija el contrato/TaskDoc, no el nodo.

## DRY-RUN
Al ser agregado, WS34 no se ejecuta: termina cuando ambos hijos aceptan.

WS34.1: lee el contrato WS12 (sección de política y umbral de timeout para dispatch), esquemas WS33 y registros WS32.1/WS32.2; modifica `runtime/`, `cli/commands/runtime.py` o la API fijada por WS12, y `tests/`; consume G_EXEC/G_SCION/G_WRITE_CONTRACT (per_delta). Valida con agente real un dispatch aceptado y uno rechazado/vencido, correlacionados al id de intento local; sin confirmación observada no declara éxito ni fallo remoto. Si falta la política de timeout, se detiene.

WS34.2: depende de WS34.1; lee el mismo contrato para reply; modifica runtime/API y tests; valida respuesta vinculada al intento correcto y timeout como fallo sin confirmación. Transfiere a WS34 su adaptador de reply.

Validación conjunta: ambos hijos cumplen aceptación; el agregado produce el adaptador que WS36 consume como única vía de dispatch/reply. Errores esperados: timeout ausente en WS12, gate no satisfecho, transporte duplicado.

## FUTURO
WS12 fija política/umbral por delta; WS44 produce el probe de G_SCION; el solicitante/designee autoriza G_EXEC; WS36 integra el adaptador; la promoción requiere preflight y autorización humana.
