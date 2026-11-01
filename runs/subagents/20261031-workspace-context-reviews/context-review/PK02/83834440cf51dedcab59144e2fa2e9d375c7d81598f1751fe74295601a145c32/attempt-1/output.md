## REFORMULACION
PK02 es un paquete de planificación, sin ejecución propia, con repo dueño `deskops`. Su propósito es consolidar los contratos que permiten preparar cada delta: decisiones trazadas, user-flows observables, catálogo de vistas, convención del manual, navegación/identidad y operaciones/escritura. El resultado esperado son los artefactos de sus hijos —`decisiones.md` y `baseline_proposal`, `borradores/user-flows.md`, `borradores/vistas.md`, `borradores/manual.md`, `contratos/navegacion.md`, `contratos/operaciones.md`— con Pxx trazadas, UFs con operaciones/errores/IDs/gates, vistas con soporte/origen, APIs y huecos con productor. Límites: no ejecuta tareas, no crea aristas, no implementa UI/API, no supone editable sin `G_SOURCE`, no convierte recepciones por delta en aceptación conjunta y no habilita Scion.

## AMBIGUEDADES
ninguna

## DRY-RUN
Hipotéticamente, un ejecutor recorrería las aristas reales: primero WS07 consume WS06 y reutiliza las decisiones humanas, produciendo el registro P01–P09; WS08 consume ese registro y genera UFs con operaciones, errores, nodos y gates; WS10 consume WS07 —y WS02 externo— y fija índice/convención del manual; WS09 consume WS07, WS08 y WS10 y cataloga vistas con origen, contrato, renderer, acción, error y estado; WS11 consume WS08 y WS09 y cierra identidad/navegación y lectura multidesk; WS12 consume WS08 y WS11 y publica whitelist, precondición, efectos, huecos y recepción por delta. La integración contrastaría que cada UF remite a operaciones y nodos existentes, cada vista tiene soporte o hueco asignado, cada hueco tiene productor y cada operación respeta `G_SOURCE`/`G_WRITE_POLICY`. Si falta un contrato o API de una dependencia, se detendría y registraría el hueco, sin sustituto. La validación conjunta sería revisión trazable de artefactos y consistencia cruzada, no ejecución de producto.

## FUTURO
WS06 aporta la matriz de reconciliación; WS02, el inventario Deskops; WS20 y WS45 producen `G_SOURCE` y la precondición de payload; el receptor P01 registra actas por delta. `G_PRODUCT` y `G_WRITE_POLICY` siguen pendientes y corresponden a decisión/verificación humana o técnica, no a este paquete.
