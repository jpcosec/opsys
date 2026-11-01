REFORMULACION
Propósito: verificar o completar en sldb la precondición de escritura de payload que fije WS12, distinguiendo before-image `expected`/HTTP 409, token `version`/`content_hash` y precondición pública compartida. Resultado: inventario con path, símbolo y commit, más pruebas focalizadas por operación y escritor; código mínimo solo si falta capacidad, con tarea propia en sldb. Repo dueño: sldb (`output_base: sldb:repository_root/`). Límites: no UI, no CAS forzado en toda CLI, no algoritmo de hash por inercia, no raw-source, sin mezclar otro productor; P03 intacto; es plan y su promoción no está autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
- Lecturas: nodo WS45, dependencia WS12, gates `G_SLDB_WRITE`, `G_WRITE_CONTRACT` y `G_PAYLOAD_PRECONDITION`, brief, alcance y decisiones.
- Cambios previstos: inventario en sldb; pruebas en `tests/`; solo si falta capacidad, cambios acotados en `src/sldb/api/documents/` y `src/sldb/cli/serve/`, con tarea propia en sldb.
- Dependencias: contrato WS12 —representación de la precondición, operaciones y escritores alcanzados— y recibos por delta de `G_WRITE_CONTRACT` y `G_SLDB_WRITE`.
- Validaciones futuras: precondición obsoleta rechazada sin cambios; vigente aplicada; rechazo observable por el llamante; si se completa capacidad parcial, volver a probar todo el contrato; evidencia para `G_PAYLOAD_PRECONDITION`. Sin ejecutar nada.

FUTURO
WS12 produce el contrato que fija representación, operaciones y escritores. El receptor P01 emite el acta/recibo `G_SLDB_WRITE` del delta concreto. Si falta capacidad, se abre y ejecuta la tarea propia en sldb. La promoción del nodo y la satisfacción de `G_PAYLOAD_PRECONDITION` con evidencia verificable quedan fuera de esta revisión; un humano decide autorizar la promoción.
