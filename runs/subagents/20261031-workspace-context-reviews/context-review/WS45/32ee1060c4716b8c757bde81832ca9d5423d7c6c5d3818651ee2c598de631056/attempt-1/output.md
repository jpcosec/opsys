## REFORMULACION
Propósito: verificar o completar en sldb la precondición de escritura de payload que fije WS12. Resultado: inventario con path/símbolo/commit de la capacidad existente y pruebas reales focalizadas por operación/escritor; código solo si falta capacidad. Repo: sldb. Límites: no fuerza CAS ni algoritmo de hash, no toca UI ni raw-source (WS20), es independiente de `source_mode`; no crea productor condicional; P03 intacto.

## AMBIGUEDADES
1. «código solo si al ejecutar falta capacidad, con tarea propia en sldb». No nombra actor ni autorización para crear/promover esa tarea en sldb; obligaría a inventar si el ejecutor de WS45 la crea, la registra como hueco/handoff, o quién la autoriza, dado `promotion: not_authorized`.

## DRY-RUN
Un ejecutor futuro leería el contrato WS12 y comprobaría `G_WRITE_CONTRACT` y el recibo `G_SLDB_WRITE` de este delta; si faltan, se detiene y registra el hueco con repo dueño. Leería `src/sldb/api/documents/`, `src/sldb/cli/serve/` y `tests/` para inventariar la capacidad existente (path, símbolo, commit). Escribiría el inventario en sldb y añadiría pruebas focalizadas en `tests/` con store temporal real: precondición obsoleta rechazada sin cambios, vigente aplicada y rechazo observable por el llamante. Si la capacidad es parcial, modificaría solo lo faltante en `src/` y repetiría todo el contrato; si es completa, no duplicaría código. Errores: contrato ausente, recibo ausente, capacidad ausente sin tarea autorizada o prueba que no observe rechazo: no se satisface `G_PAYLOAD_PRECONDITION`. Validación esperada: inventario y pruebas verdes citando commit/blob en sldb.

## FUTURO
WS12 produce la representación, operaciones y escritores alcanzados. El receptor humano P01 emite el acta `G_SLDB_WRITE` por delta. WS20 conserva raw-source y WS21 queda bloqueado por `G_PAYLOAD_PRECONDITION`. La creación de tarea en sldb y la aceptación del recibo son decisiones humanas, no de este nodo.
