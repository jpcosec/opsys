REFORMULACION
Propósito: WS34 es un agregado no ejecutable que agrupa la exposición de un adaptador público restringido para despacho y respuesta Scion autorizados. Resultado: se cumple solo cuando WS34.1 y WS34.2 cumplen su aceptación; sus dependientes siguen dependiendo de WS34. Repo dueño: deskops. Límites: no ejecuta por sí mismo, no admite shell arbitrario ni duplicación de transporte, no envía mensajes en planificación y la confirmación/autoridad dependen de la API Scion y del contrato WS12; promotion not_authorized.

AMBIGUEDADES
Ninguna. Las referencias a contrato WS12, identidad de intento vía WS33, permiso G_EXEC, contrato público G_SCION producido por WS44 y timeout/errores tienen productor nombrado o se delegan al contrato/TaskDoc; los gates pendientes son intencionales.

DRY-RUN
Lecturas: dag.yaml (nodo, hijos, gates), task-ws34.md, contrato WS12, salidas WS33, evidencia G_EXEC/G_SCION y aceptaciones WS34.1/WS34.2. Cambios previstos: ninguno propio del agregado; solo verificar cierre de hijos si se promoviera. Dependencias: WS33, WS12, WS34.1, WS34.2; gates G_EXEC, G_SCION (WS44) y G_WRITE_CONTRACT (WS12, per_delta). Validaciones futuras: dispatch aceptado y rechazado o vencido por timeout con agente real, reply vinculado al intento correcto, timeout reportado como fallo sin confirmación, autoridad del coordinador y ausencia de transporte duplicado.

FUTURO
WS34.1 y WS34.2 implementan y aportan evidencia; WS12 fija el contrato de operaciones; WS44 produce G_SCION; un humano resuelve G_EXEC y autoriza la promoción; WS36 consume el adaptador. Nada de esto se ejecuta aquí.
