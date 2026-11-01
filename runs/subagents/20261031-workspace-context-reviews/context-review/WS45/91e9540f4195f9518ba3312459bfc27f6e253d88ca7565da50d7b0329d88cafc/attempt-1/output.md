REFORMULACION
Propósito: verificar o completar en sldb la precondición de escritura de payload que fije WS12, sin confundirla con `source_mode` ni con raw-source. Resultado: inventario con path, símbolo y commit, más pruebas focalizadas por operación/escritor; código solo si falta capacidad, con tarea propia en sldb. Repo dueño: sldb. Límites: no UI, no CAS forzado en toda CLI, no elegir algoritmo de hash por inercia, no productor condicional; P03 no cambia. Aceptación: precondición obsoleta rechazada sin cambios, vigente aplicada y rechazo observable; recibo G_SLDB_WRITE para este delta y evidencia para G_PAYLOAD_PRECONDITION.

AMBIGUEDADES
Ninguna. La representación de la precondición, las operaciones y los escritores alcanzados los fija WS12; si falta, alcance.md ordena detenerse y registrar el hueco. Los archivos exactos, TaskDoc y pruebas detalladas quedan para la promoción.

DRY-RUN
Lecturas previstas: contrato WS12, inventarios citados, código y pruebas de `src/sldb/api/documents/` y `src/sldb/cli/serve/`, estado de gates y `task_file`. Cambios previstos: inventario y pruebas; solo si el contraste revela hueco, código faltante bajo tarea propia en sldb, sin UI. Dependencias: WS12, G_WRITE_CONTRACT y G_SLDB_WRITE; salida G_PAYLOAD_PRECONDITION. Validaciones futuras: ejecutar la matriz con precondición obsoleta y vigente, comprobar ausencia de cambios en el rechazo, aplicación en el caso vigente y error observable por el llamante; repetir todo el contrato si hubo completado parcial; recibo humano por delta. Sin ejecutar.

FUTURO
WS12 decide representación, operaciones y escritores alcanzados. P01 emite el acta G_SLDB_WRITE por delta. La promoción, el TaskDoc y cualquier autorización de código corresponden a otro nodo o a un humano. WS20 conserva raw-source. G_PAYLOAD_PRECONDITION se resolverá con la evidencia producida por WS45.
