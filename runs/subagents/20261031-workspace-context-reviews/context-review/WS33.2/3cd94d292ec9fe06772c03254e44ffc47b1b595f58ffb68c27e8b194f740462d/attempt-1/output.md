## REFORMULACION
WS33.2 es un nodo de implementación en `deskops` cuyo propósito es registrar una decisión humana explícita —aprobar o pedir corrección— asociada a un intento y, por él, a su tarea. El resultado esperado es un registro con actor humano, referencia al intento y a la tarea, y resultado explícito; si es corrección, con su texto. Límites: no escribe los estados `validated`/`closed` de deskops, no registra `completed` del agente como aprobación, no despacha ni responde a Scion, y solo usa la operación que fije WS12; si falta, debe detenerse y registrar el hueco con repo dueño.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Lecturas hipotéticas: nodo y aristas en `dag.yaml`; contrato WS12 para actor, operación, campos, revisión y efectos; salidas de WS32 sobre identidad de intento y vínculo con tarea; artefactos de WS33.1; evidencia de G_SCION producida por WS44. Cambios previstos: adaptador en `runtime/` según contrato, modelos/reportes y tests. Dependencias y gates: consumiría WS32 y WS33.1; comprobaría G_SCION resuelto y G_WRITE_CONTRACT con recibo per-delta para WS33.2. Si falta contrato, API, dato o permiso, se detendría sin crear sustituto. Validación esperada: prueba con store temporal real de que una aprobación exige actor humano, intento y tarea; una corrección sin texto se rechaza; `completed` del agente no queda como aprobado; la decisión no altera estados de cierre. Errores esperados: contrato ausente, intento no resoluble o tarea no asociada se registran como hueco, no se inventan.

## FUTURO
WS12 debe fijar la operación y la identidad del actor; WS32 debe aportar la identidad de intento y su vínculo con la tarea; WS44 debe producir la evidencia de G_SCION; una persona emitirá la decisión real durante la validación. La promoción fijará archivos, pruebas y textos dentro de esta aceptación. WS33 cerrará como agregado cuando sus hijos cumplan.
