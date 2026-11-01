## REFORMULACION
**Propósito:** agrupar la revisión de navegación y representaciones authored del desk sobre identidad común, sin ejecución propia ni aristas nuevas.
**Resultado:** paquete navegable con índices/plantillas WS17, Board WS22, procedimiento WS23 y conocimiento/grafo WS24; WS18 ViewDoc queda opcional tras G_SPEC_VIEW. Integrado, debe abrir los mismos documentos/soportes desde lista, tablero, dependencias, procedimiento y conocimiento, sin escribir status desde renderers y con índices que siguen sus fuentes.
**Repo dueño:** deskops; hijos en graph_ui y spec2viz.
**Límites:** no ejecuta tareas, no autoriza promoción, no añade aristas; G_SPEC_VIEW está pendiente; WS18 no bloquea WS24.

## AMBIGUEDADES
1. «Completitud sustantiva del paquete requiere salidas de sus hijos e integración indicada»: no se define qué es la «integración indicada», ni su artefacto, responsable o criterio de aceptación conjunta. Obliga a inventar quién integra y cómo se declara completo el paquete.
2. «WS18 ViewDoc es extensión opcional tras G_SPEC_VIEW y no bloquea WS24» frente a «requiere salidas de sus hijos»: contradicción sobre si la salida de WS18 cuenta para la completitud. Obliga a decidir si el paquete puede cerrar sin WS18.
3. «ViewDoc concreto prueba su selección solo cuando se integra»: no nombra el destino de esa integración ni la condición de prueba. Obliga a inventar si «se integra» significa WS24, el paquete o un receptor externo.

## DRY-RUN
**Lecturas hipotéticas:** dag.yaml para IDs/aristas/gates; contratos WS11 y WS09; salidas de WS40 y WS13; estado de G_SPEC_VIEW.
**Orden y transferencias:** WS17, tras WS11 y WS40, produce `ejemplo/nav/`; WS40 regenera el corpus desde esas plantillas. WS18, tras WS09, WS11 y G_SPEC_VIEW, produce ViewDoc/NotationDoc y pruebas; no alimenta WS24 hasta su recibo. WS22, WS23 y WS24 pueden avanzar en paralelo tras WS13 y WS09: Board, procedimiento y conocimiento/grafo respectivamente.
**Integración prevista:** regenerar el corpus WS40 con las plantillas WS17; abrir los mismos TaskDoc/documentos desde cada representación; verificar resolución de roots/aliases, ausencia de peticiones de escritura y correspondencia de ViewDoc con su selección declarada.
**Dependencias:** WS11, WS09, WS13 y WS40; G_UI_READ por hijo; G_SPEC_VIEW solo para WS18.
**Validaciones futuras:** navegación cruzada, no escritura de status, índices derivados de fuente y prueba de ViewDoc. No se ejecuta nada.

## FUTURO
Producen otros nodos: WS11/WS09 sus contratos, WS40 el corpus, WS13 el lector, y los dueños de graph_ui/spec2viz ejecutan y promueven sus hijos. P01 o el receptor emiten G_UI_READ/G_SPEC_VIEW por delta. Un humano decide la aceptación integrada del paquete y el tratamiento de WS18 si se mantiene opcional.
