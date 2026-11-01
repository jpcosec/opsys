REFORMULACION
Propósito: revisar WS19.2 como encargo de planificación, no como producto ni ejecución. Resultado: dictamen sobre si permite implementar alta/baja de relaciones sin inventar alcance. Repo dueño: `graph_ui`. Límites: solo input explícito; no reviso contratos vecinos, no ejecuto pruebas, no autorizo promoción ni mutaciones UI.

AMBIGUEDADES
Ninguna.

WS19.2 delega las relaciones permitidas y los endpoints en WS12; `alcance.md` fija qué hacer si falta contrato: detenerse y registrar el hueco. La precondición de escritura queda cubierta por `G_PAYLOAD_PRECONDITION`, cuyo productor es WS45, y la aceptación es comprobable: persistencia tras recarga y rechazo visible de relación no permitida o revisión obsoleta.

DRY-RUN
Lecturas: guía de revisión, brief, alcance, decisiones, cobertura, reconciliación, nodo WS19.2, aristas WS12/WS19, gates y referencia externa `editing`. Cambios previstos: ninguno; solo dictamen. Dependencias declaradas: WS12; gates `G_HUMAN_READ`, `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT`; solapamiento con `editing` mediante `delta_or_existing_ticket`, sin duplicación paralela. Validaciones futuras: contrato WS12 con whitelist y endpoints; evidencia de WS45 para la precondición; prueba de alta/baja persistente tras recarga; rechazo visible de relación no permitida y revisión obsoleta; recepción P01 por delta; preflight y TaskDoc de promoción.

FUTURO
WS12 publicará la operación, campos, canal, revisión esperada, efectos y endpoints autorizados. WS45 verificará la precondición de escritura de payload. El receptor P01 emitirá el acta del delta concreto en `graph_ui`. El TaskDoc de promoción fijará archivos, pruebas, textos y evidencia; WS16 aportará el acta humana de lectura. Nada de esto se ejecuta aquí.
