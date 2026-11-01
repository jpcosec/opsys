## REFORMULACION
WS22 encarga en `graph_ui` representar el Board real como trabajo navegable: lista, tablero agrupado por estado y representación de dependencias, abriendo el mismo TaskDoc y sus pills/átomos en el lector, con selección y links comunes, estados/lifecycle leídos de deskops, sin drag-and-drop de status, sin duplicar tareas y sin presentar un predicado satisfecho como test aprobado. Salida prevista en `frontends/mindmap/views/workspace/board/` y `tests/`; depende de WS13 y WS09 y requiere `G_UI_READ`.

## AMBIGUEDADES
1. «tablero agrupado por estado» / «estados y condiciones de lifecycle leídos de deskops (Board, lifecycle), no de dag.yaml». No se fija qué campo es «estado» —status del TaskDoc, `current_node`/estado de lifecycle o agrupación propia del Board— ni qué «condiciones de lifecycle» deben mostrarse. Obliga a inventar la clave de agrupación y el conjunto de condiciones; sin ello no es comprobable que se lean de deskops.
2. «con las dependencias declaradas en el TaskDoc» / «Las tres representaciones (lista, tablero y dependencias) abren el mismo TaskDoc». No se nombra el campo que contiene esas dependencias ni se exige comprobar que la representación las refleje: la aceptación solo prueba la apertura del TaskDoc. Obliga a inventar la fuente y el criterio de aceptación de la vista de dependencias.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml`, la salida de WS09 (`vistas.md`) y la de WS13 (lector, selección y links), las rutas/datos de deskops para Board, TaskDoc y lifecycle, y la vista Deskops existente; verificaría el acta `G_UI_READ` de WS22. Sin ejecutar: añadiría componentes y pruebas bajo `views/workspace/board/` y `tests/`, consumiría datos de deskops sin escribirlos, mantendría los links/foco del lector y probaría apertura del mismo TaskDoc desde las tres representaciones, ausencia de duplicados y separación predicado/test. Si faltara WS09, WS13, el acta o un dato de lifecycle, se detendría y registraría el hueco con repo dueño, sin crear sustituto. Validación esperada: pruebas de graph_ui y, posteriormente, recorrido humano de WS30.

## FUTURO
WS13 produce el lector y su selección/links; WS09 el catálogo de renderizaciones; el receptor P01 emite el acta por delta de `G_UI_READ`; WS30 valida el recorrido humano. WS22 no autoriza promoción ni implementación.
