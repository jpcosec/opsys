REFORMULACION
Propósito: revisar WS34.2 como encargo de planificación de un adaptador público restringido para reply de Scion, vinculado al intento, con timeout/errores y autoridad del coordinador. Resultado: adaptador en deskops (`runtime/`; `cli/commands/runtime.py` o API que fije WS12; `tests/`), sin enviar mensajes durante planificación. Repo dueño: deskops. Límites: depende de WS33, WS12 y WS34.1; requiere G_EXEC, G_SCION y G_WRITE_CONTRACT; aceptación mediante agente real y timeout según umbral del contrato WS12; no duplica transporte ni shell.

AMBIGUEDADES
Ninguna. El vínculo con el intento se apoya en WS33/WS34.1; canal, actor, efectos, errores y umbral se delegan a WS12; los gates pendientes son intencionales y el alcance excluye mensajes en planificación.

DRY-RUN
Lecturas: input completo —guía, brief, alcance, decisiones, cobertura, nodo WS34.2 y contratos vecinos—, sin herramientas ni ejecución. Cambios previstos: ninguno; solo revisión. Dependencias: WS33 aporta referencias mensaje/intento, dedup y procedencia; WS12, contrato de operación, autoridad, errores/umbral; WS34.1, identidad de intento en dispatch. Gates: G_EXEC, G_SCION y G_WRITE_CONTRACT. Validaciones futuras: agente real demuestra respuesta al intento correcto; timeout se reporta como fallo sin confirmación; G_SCION se comprueba vía WS44; G_WRITE_CONTRACT se recibe por delta; la promoción fijará archivos y pruebas.

FUTURO
WS12 produce contrato y recibo por delta; WS44/operador designado produce el probe de G_SCION; un humano/external resuelve G_EXEC; WS33 y WS34.1 entregan referencias e identidad de intento; el TaskDoc de promoción fija archivos, escenarios y textos; el repo receptor emite acta de recepción. Nada de ello es ambigüedad ni autoriza ejecución.
