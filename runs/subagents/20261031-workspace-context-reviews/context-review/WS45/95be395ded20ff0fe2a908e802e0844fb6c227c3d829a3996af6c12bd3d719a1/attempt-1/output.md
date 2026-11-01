## REFORMULACION

- **Propósito**: verificar en sldb la precondición de escritura de payload que fije el contrato WS12, o completar solo la capacidad faltante.
- **Resultado**: inventario con path/símbolo/commit y pruebas focalizadas por operación y escritor alcanzado; evidencia para G_PAYLOAD_PRECONDITION.
- **Repo dueño**: sldb.
- **Límites**: independiente de `source_mode` y de raw-source (WS20); no mezcla UI; no fuerza CAS en toda CLI ni elige algoritmo de hash; reutiliza primero; código solo si falta capacidad y con tarea propia en sldb; no declara implementación ni aceptación.

## AMBIGUEDADES

ninguna.

## DRY-RUN

- **Lecturas previstas**: contrato WS12; código e inventarios existentes en `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/`; evidencia de `expected`/HTTP 409 y `version`/`content_hash`.
- **Cambios previstos**: ninguno por defecto. Si al ejecutar falta capacidad, cambios acotados en sldb con tarea propia; pruebas focalizadas en `tests/`.
- **Dependencias**: WS12 produce representación, operaciones y escritores alcanzados. Gates requeridos: G_SLDB_WRITE y G_WRITE_CONTRACT.
- **Validaciones futuras**: prueba real por operación/escritor de rechazo de precondición obsoleta sin cambios, aplicación de precondición vigente y rechazo observable; recibo G_SLDB_WRITE para este delta; evidencia para G_PAYLOAD_PRECONDITION. Sin ejecución en esta revisión.

## FUTURO

WS12 debe publicar el contrato de precondición y sus pruebas/API existentes o productor si falta. El solicitante P01 emite el acta de recepción G_SLDB_WRITE por delta en el repo sldb. La promoción y cualquier tarea de código en sldb requieren autorización humana; este nodo no la concede. WS45, al ejecutarse, produce el inventario, las pruebas y la evidencia de G_PAYLOAD_PRECONDITION.
