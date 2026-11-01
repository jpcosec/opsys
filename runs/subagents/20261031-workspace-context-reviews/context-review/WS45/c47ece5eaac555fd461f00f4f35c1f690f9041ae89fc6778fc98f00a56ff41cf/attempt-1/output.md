REFORMULACION
Propósito: verificar o completar en sldb la precondición de escritura de payload que fije WS12. Resultado: inventario con path/símbolo/commit y pruebas focalizadas por operación y escritor; código solo si falta capacidad, en tarea propia de sldb. Repo: sldb (`src/sldb/api/documents/`, `src/sldb/cli/serve/`, `tests/`). Límites: independiente de `source_mode` y de raw-source; no UI, no CAS global ni algoritmo de hash por inercia; P03 intacto; `promotion: not_authorized`. Depende de WS12 y de `G_SLDB_WRITE`/`G_WRITE_CONTRACT` por delta.

AMBIGUEDADES
1. «código solo si al ejecutar falta capacidad, con tarea propia en sldb» frente a «si es parcial, se completa solo lo faltante y se vuelve a probar todo el contrato». No queda claro si el ejecutor de WS45 puede modificar `src/` o solo abrir/entregar una tarea separada en sldb. Obliga a inventar la autorización y el actor de esa tarea; además, alcance.md prohíbe crear una segunda ejecución concurrente.
2. «No mezcla UI ni productor condicional alguno». «Productor condicional» no está definido en las fuentes; obliga a inventar si excluye la completitud de capacidad permitida, WS20/raw-source u otro productor.

DRY-RUN
Nodo ejecutable, no agregado. Lecturas: contrato WS12 en deskops (representación de precondición, operaciones, escritores), repo sldb y su historial para localizar capacidad existente. Cambios previstos: inventario en la ubicación que fije el TaskDoc y pruebas en `tests/`; `src/` solo si falta capacidad y existe tarea propia autorizada. Consumo: `G_WRITE_CONTRACT` aceptado para WS45 y recibo `G_SLDB_WRITE`; si faltan, detener y registrar hueco con repo dueño. Validación futura: ejecutar pruebas focalizadas con store temporal real; precondición obsoleta rechazada sin cambios, vigente aplicada y rechazo observable por el llamante; si se completa capacidad, repetir todo el contrato. Errores: contrato sin representación o capacidad ausente sin tarea -> operación no disponible, sin sustituto. Cierre: commit/blob en sldb como evidencia de `G_PAYLOAD_PRECONDITION`.

FUTURO
WS12 produce el contrato y la representación; el receptor P01 emite `G_SLDB_WRITE` por delta; el TaskDoc de promoción fija archivos y casos; WS21 consume `G_PAYLOAD_PRECONDITION`; WS20 conserva raw-source. La aceptación final del gate corresponde a su verificador, no a este nodo.
