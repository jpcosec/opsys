## REFORMULACION
Propósito: verificar o completar en sldb la precondición de escritura de payload definida por WS12, independiente de `source_mode` y de raw-source. Resultado: inventario con path/símbolo/commit y pruebas focalizadas por operación/escritor; código solo si falta capacidad, en las rutas declaradas y con tarea propia en sldb. Repo dueño: sldb. Límites: no UI, no productor condicional, no forzar CAS ni elegir hash, no duplicar capacidad existente; WS45 no es aggregate. Alimenta `G_PAYLOAD_PRECONDITION` y requiere recibo `G_SLDB_WRITE` por delta.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería WS45, el contrato WS12, decisiones/alcance y el estado real de sldb; comprobaría `G_WRITE_CONTRACT` para este delta y el acta `G_SLDB_WRITE`. Si faltan, se detiene y registra el hueco. Inventariaría las tres capacidades (`expected`/409, `version`/`content_hash`, precondición compartida) con path, símbolo y commit, y las contrastaría con operaciones/escritores de WS12. Añadiría pruebas en `tests/` con store temporal real: precondición obsoleta rechazada sin cambios, vigente aplicada y rechazo observable. Si la capacidad es completa, no tocaría código; si es parcial, completaría solo lo faltante en `src/sldb/api/documents/` o `src/sldb/cli/serve/` con tarea propia en sldb y repetiría las pruebas del contrato. Validaría con la suite focalizada y commit verificable; falta de contrato/recibo o capacidad fuera de alcance se registra como hueco, sin sustituto. No ejecutaría UI ni raw-source.

## FUTURO
WS12 fija representación, operaciones y escritores; P01 emite el acta `G_SLDB_WRITE`; la promoción autoriza tarea/preflight y archivos exactos; WS21 queda bloqueado hasta `G_PAYLOAD_PRECONDITION`. La aceptación del gate y cualquier cambio de alcance corresponden a otro nodo/humano.
