REFORMULACION

WS19 es un agregado de implementación en graph_ui: integrar edición contextual de campos y relaciones permitidas sobre el workspace integrado a1b2b22, reutilizando editores/API y la precondición de escritura que fije WS12 y verifique WS45, con conflicto visible que conserve el texto local y sin editar campos protegidos ni crear semántica de relaciones en el componente. El resultado son las salidas de WS19.1 (campos) y WS19.2 (relaciones), con pruebas; se acepta cuando ambos hijos cumplen sus aceptaciones y gates por delta. Límites: solo esos deltas; sin commits ni closeout.

AMBIGUEDADES

ninguna.

DRY-RUN

No ejecutable: es agregado; un ejecutor futuro no produce código propio, prepara y verifica sus hijos. Leería el contrato WS12 (whitelist, canal, representación de precondición, campos protegidos), la evidencia de G_PAYLOAD_PRECONDITION de WS45, la matriz WS06/editing y la base graph_ui a1b2b22. WS19.1 cambiaría `views/workspace/fields/` y tests: guardado/recarga, rechazo obsoleto conservando texto local y conflicto visible. WS19.2 cambiaría `views/workspace/relations/` y tests: alta/baja persistentes y rechazo visible de relación no permitida o revisión obsoleta. Ambos consumen WS12; no hay arista entre hermanos, así que no se transfieren nada. La integración conjunta exige que ambas mutaciones convivan en el mismo workspace sin semántica propia de relaciones ni edición de campos protegidos. Validación: aceptaciones de ambos hijos; G_HUMAN_READ antes de usar mutaciones en UI; G_PAYLOAD_PRECONDITION, G_WRITE_CONTRACT y G_UI_WRITE por delta. Si falta contrato/API, se detiene y registra el hueco, sin sustituto.

FUTURO

WS12 publica contrato y whitelist; WS45 produce la evidencia de G_PAYLOAD_PRECONDITION; WS16/humano emite el acta de G_HUMAN_READ; el receptor P01 emite G_UI_WRITE por delta; la promoción fija TaskDoc, archivos y pruebas. WS21 y WS42 consumen después; WS30 valida uso.
