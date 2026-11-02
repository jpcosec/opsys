## REFORMULACION
WS26 es un agregado de planificación no ejecutable: integra en `graph_ui` la autoría explícita desde candidato —evidencia, dependencias y pills— y el enrutamiento en Board con capa lista, sin confundir ruta con ejecución. Su resultado es la suma verificada de WS26.1 y WS26.2. Límites: no crea tarea activa ni promoción por sí mismo; promoción solo por canal autorizado que respete commits previos, o handoff declarado; mutaciones UI sujetas a G_HUMAN_READ. Repo dueño: `graph_ui`.

## AMBIGUEDADES
Ninguna. Los detalles de autoría, handoff, promoción, capa lista y errores quedan definidos por los hijos, el contrato WS12 o el TaskDoc de promoción; el input no obliga a inventar resultado, repo, dependencia ni aceptación.

## DRY-RUN
Agregado no ejecutable: un ejecutor futuro no modifica archivos ni produce cambios propios. Consumiría el contrato WS12, la representación Board de WS22 y las salidas de WS47/WS48. Verificaría, en orden lógico de integración —no de arista entre hermanos—, que WS26.1 entrega el candidato preparado: campos autorables persistidos con `expected`, rechazo 409 sin pérdida local, pills conservadas y handoff explícito cuando no hay canal; y que WS26.2 recibe ese candidato y solo entonces ejecuta la operación conjunta autorizar/crear/enrutar, mostrando la tarea separada de ejecución y la capa lista con solapamientos comprobados o pendientes.

Transferencia: WS26.1 no crea tarea ni Board; WS26.2 no repite la preparación ni implementa promoción nueva. Ambos comparten la selección y enlaces del lector/Board de WS22. Gates: G_CLOSEOUT ya satisfecho; G_WRITE_CONTRACT y G_UI_WRITE se comprueban por delta; G_PAYLOAD_PRECONDITION para escritura de payload; G_HUMAN_READ antes de habilitar mutaciones UI. Si falta contrato, API o permiso, se registra el hueco y la operación queda no disponible; no se sustituye. Validación conjunta: aceptación de ambos hijos y, después, WS30 sobre UF02/03/04/05; el agregado no se declara ejecutado por sí solo.

## FUTURO
WS30 validará el recorrido humano conjunto. WS12 publicará el contrato por delta; WS45 verificará G_PAYLOAD_PRECONDITION; WS47/WS48 aportarán guardado y admisión. El receptor P01 emitirá recibos G_UI_WRITE por delta y el TaskDoc de promoción fijará archivos, escenarios y textos.
