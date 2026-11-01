## REFORMULACION
WS34 es un **agregado no ejecutable** de implementación en `deskops`: agrupa la exposición de un adaptador público restringido para despacho y respuesta Scion autorizados, con confirmación, identidad de intento, timeout/errores y autoridad del coordinador. Su resultado es el agregado de las salidas de WS34.1 y WS34.2; no produce por sí mismo código ni pruebas. Límites: no habilita ejecución real, comunicaciones ni shell arbitrario; depende de WS33, WS12 y sus hijos, y requiere G_EXEC, G_SCION y G_WRITE_CONTRACT, todos pendientes/intencionales. La promoción está `not_authorized`.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro no implementa WS34: comprueba el cierre del agregado. Lecturas: `task-ws34.md`, aceptaciones/evidencias de WS34.1 y WS34.2, contrato WS12 por delta y estado de gates. Cambios previstos: ninguno propio; `output_scope` remite a las salidas de los hijos.

Recorrido de hijos:
- **WS34.1** entrega el adaptador de dispatch y evidencia de un dispatch aceptado y otro rechazado o vencido, correlacionado con el intento local previo de WS32.1/WS32.2. Transfiere a WS34.2 el dispatch autorizado y la política de timeout aplicable.
- **WS34.2** entrega el adaptador de reply vinculado al intento correcto y reporta timeout como fallo sin confirmación. Transfiere a WS34 ambas salidas implementadas y probadas.

Dependencias consumidas: política y umbral de timeout producidos por WS12 para cada delta; referencias de WS33; verificaciones G_EXEC/G_SCION/G_WRITE_CONTRACT por delta. Errores: si falta un hijo, su aceptación o la sección de WS12, el agregado queda incompleto y se registra el hueco; no se elige umbral ni se simula confirmación.

Validación conjunta: ambas aceptaciones hijas cumplidas, agentes reales usados, dispatch aceptado y rechazado/timeout observados, reply vinculado al intento y timeout reportado como fallo, gates verificados por delta; entonces WS34 puede declararse cumplido y WS36 sigue dependiendo de este ID.

## FUTURO
WS12 produce la política de timeout por delta; WS34.1 y WS34.2 implementan y aportan evidencia; WS44/G_SCION aporta el probe; un humano resuelve G_EXEC; la recepción verifica gates por delta; WS36 consume el adaptador agregado.
