REFORMULACION
WS34.2 encarga en deskops un adaptador público restringido para responder (reply) vinculado a un intento, con timeout/errores y autoridad del coordinador. El resultado es runtime/, CLI/API fijada y tests que demuestren, con agente real, respuesta al intento correcto y timeout reportado como fallo sin confirmación, usando el umbral que WS12 produzca para este delta. Límites: no enviar mensajes durante planificación; sin esa política en WS12/G_WRITE_CONTRACT, detenerse y registrar el hueco, sin elegir umbral propio.

AMBIGUEDADES
1. «un timeout se reporta como fallo sin confirmación» frente a WS34.1: «sin convertir ausencia de confirmación en éxito/fallo remoto no observado». El ejecutor debe inventar si el timeout es un fallo local comprobable o un fallo remoto declarado sin observación, y cómo etiquetarlo. Aunque WS12 prevé la clasificación «vencido sin confirmación», no aclara si «fallo» es local o remoto.
2. «con timeout/errores y autoridad del coordinador» no aparece en la aceptación, que solo exige respuesta al intento correcto y timeout como fallo. El ejecutor debe inventar si implementa y prueba la autorización del coordinador o solo la documenta; WS12 define la policy, pero no la prueba de este nodo.

DRY-RUN
Leería WS12 (sección de timeout/reply y autoridad del coordinador), salidas de WS33 (referencias mensaje/intento, dedup), WS34.1 (dispatch y correlación al intento) y los gates. Cambiaría runtime/, cli/commands/runtime.py o la API que fije WS12, y añadiría tests/. Consumiría G_EXEC (autorización en scion.md), G_SCION (probe WS44) y G_WRITE_CONTRACT del delta. Si falta la política de timeout, se detiene y registra el hueco. Validaría con agente real: reply vinculado al intento correcto; timeout reportado como fallo sin confirmación; ningún mensaje en planificación. Errores esperados: timeout, rechazo y contrato/gate ausente.

FUTURO
WS12 fija el umbral y la autoridad; WS44 produce G_SCION; el solicitante/designee resuelve G_EXEC; el receptor registra el acta por delta. La promoción exige TaskDoc, archivos/pills y preflight, y no está autorizada.
