REFORMULACION
Propósito: integrar autoría explícita desde candidato, evidencia declarada, dependencias, contexto/pills y enrutamiento Board/capa lista como agregado no ejecutable. Resultado: agregado de WS26.1 y WS26.2; se cumple cuando ambos cumplen su aceptación. Repo dueño: graph_ui. Límites: no ejecuta; no confunde Board route con ejecución; mutaciones UI solo con G_HUMAN_READ y contratos/gates; promoción no autorizada y sujeta a preflight/canal autorizado; no commits automáticos.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: nodo WS26, hijos WS26.1/WS26.2, contratos WS12/WS22 y gates G_CLOSEOUT/G_HUMAN_READ/G_UI_WRITE/G_WRITE_CONTRACT. Cambios previstos: ninguno propio del agregado; solo consolidar salidas de hijos. Dependencias: WS12, WS22 y ambos hijos; G_CLOSEOUT satisfecho, G_HUMAN_READ pendiente y los gates de escritura se evalúan por delta. Validaciones futuras: aceptación de cada hijo, recibos por delta y WS30 aguas abajo; sin ejecutar.

FUTURO
WS12 produce whitelist/contrato de operaciones y recibos por delta; WS22 entrega la representación Board; WS26.1/WS26.2 producen autoría/enrutamiento y capa lista. Humano/WS16 aporta acta G_HUMAN_READ; WS12 y el aceptador registran G_UI_WRITE/G_WRITE_CONTRACT; la promoción requiere autorización y preflight TaskDoc. Nada de esto es ambigüedad.
