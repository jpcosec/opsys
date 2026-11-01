REFORMULACION
Propósito: nodo agregado que integra edición de campos con conflicto visible y alta/baja de relaciones permitidas, sobre el workspace graph_ui a1b2b22, reutilizando editores/API y la precondición de escritura que fija WS12 y verifica WS45. Resultado: salidas de WS19.1 y WS19.2; el agregado no se ejecuta por sí mismo. Repo dueño: graph_ui. Límites: campos workflow-protected no editables por este canal; no crear semántica de relaciones en componente; usar API real y before-image; G_HUMAN_READ solo habilita uso de mutaciones en UI, sin bloquear desarrollo/pruebas aisladas de API. Dependencias: WS12, WS19.1 y WS19.2. Aceptación: agregada, cuando ambos hijos cumplen la suya.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas previstas: contrato WS12 (whitelist, precondición de escritura, canal y efectos), aceptación de WS19.1 y WS19.2, estado de G_HUMAN_READ/G_PAYLOAD_PRECONDITION/G_UI_WRITE/G_WRITE_CONTRACT, base a1b2b22 y referencia editing para evitar duplicación. Cambios previstos: ninguno propio; un aggregate no modifica archivos ni se ejecuta. Dependencias: WS12 como fuente de contrato; WS19.1/WS19.2 como hijos; WS45 vía G_PAYLOAD_PRECONDITION; WS16 vía G_HUMAN_READ; receptor P01 vía G_UI_WRITE. Validaciones futuras: aceptación de cada hijo, recibos per_delta y pruebas de guardado/conflicto y de relaciones; no ejecutadas.

FUTURO
WS12 publica la whitelist y la representación de la precondición; WS45 produce G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 emite actas G_UI_WRITE por delta. WS19.1 y WS19.2 implementan y prueban. Un humano decide la promoción —no autorizada— y la aceptación; el TaskDoc fijará archivos y textos.
