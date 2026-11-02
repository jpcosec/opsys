## REFORMULACION
WS45 es un nodo de implementación en `sldb` que debe verificar o completar la precondición de escritura de payload: inventariar la capacidad existente (before-image `expected`/409, token `version`/`content_hash`, comparación compartida) y probarla contra la representación, operaciones y escritores que fije el contrato WS12. El resultado es un inventario con path, símbolo y commit, más pruebas focalizadas por operación/escritor; solo si falta capacidad se añade código mínimo en `src/sldb/api/documents/` o `src/sldb/cli/serve/`, con tarea propia en sldb. Límites: no UI, no raw-source (WS20), independiente de `source_mode`, sin imponer CAS global ni algoritmo de hash; P03 no cambia. El gate `G_PAYLOAD_PRECONDITION` solo se satisface con evidencia verificable.

## AMBIGUEDADES
Ninguna.

## DRY-RUN
Un ejecutor futuro leería el contrato producido por WS12, el recibo `G_SLDB_WRITE` de este delta, `G_WRITE_CONTRACT` para WS45, el TaskDoc promovido y el código/pruebas reales de sldb. Si falta el contrato o el recibo, se detendría y registraría el hueco con repo dueño, sin sustituirlo.

Después levantaría un inventario que enfrente cada operación y escritor alcanzados con path, símbolo, commit y estado (existente, parcial o ausente). Escribiría pruebas reales focalizadas: precondición obsoleta rechazada sin cambios, vigente aplicada y rechazo observable por el llamante. Ejecutaría las pruebas y, si la capacidad es parcial o ausente, crearía la tarea propia en sldb, implementaría solo lo faltante dentro del `output_scope` y repetiría todas las pruebas del contrato. Errores esperados: contrato ausente, rechazo no observable, escritor fuera de alcance o recibo no aplicable; todos obligan a detenerse o registrar hueco. Validación esperada: cobertura completa de operaciones/escritores, resultados de pruebas y commit/blob verificable en sldb.

## FUTURO
WS12 decide la representación de la precondición, operaciones y escritores. El receptor P01 emite el acta `G_SLDB_WRITE` por delta. La promoción fija archivos, pruebas y evidencias; si se requiere código, una tarea en sldb lo autoriza. La evidencia producida alimenta `G_PAYLOAD_PRECONDITION` y habilita al consumidor WS21.
