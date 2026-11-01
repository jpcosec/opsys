REFORMULACION
Propósito: agrupar, sin ejecución propia, navegación y representaciones del desk sobre identidad común. Resultado: paquete integrado donde Board (WS22), procedimiento (WS23) y conocimiento/grafo (WS24) abren los mismos documentos/soportes; WS17 aporta índices authored que resuelven contra fuentes; WS18 añade proyecciones ViewDoc/NotationDoc solo tras G_SPEC_VIEW, sin bloquear. Repo dueño: deskops para la agrupación; salidas en deskops (WS17), spec2viz (WS18) y graph_ui (WS22–24). Límites: no autoriza tareas ni añade aristas; los renderers no escriben estado ni marcan pasos por lectura; los índices no duplican inventarios.

AMBIGUEDADES
Ninguna.

DRY-RUN
Hipotético, sin ejecutar. Precondiciones externas: WS09, WS11, WS13, WS40; G_UI_READ; para WS18, G_SPEC_VIEW.
1. WS17 lee WS11 y el manifiesto/corpus WS40; escribe plantillas `ejemplo/nav/` en deskops; se regenera el corpus WS40 con ellas y se comprueban links. Salida: plantillas; corpus regenerado para integración.
2. WS22, WS23 y WS24 pueden ir en paralelo tras WS13/WS09: WS22 produce lista/tablero/dependencias sobre TaskDoc; WS23 produce procedimiento read-only sobre RitualDoc/StepDoc/lifecycle; WS24 produce vista genérica, backlinks, clasificación y vecindad ≤2 hops. Salidas: código y pruebas en graph_ui, sin escrituras.
3. WS18, con gate, declara ViewDoc/NotationDoc en spec2viz y los prueba con el evaluador de graph_ui sobre store real; salida opcional hacia WS24.
Integración: sobre el corpus WS40 regenerado, abrir los mismos TaskDoc/soportes desde Board, procedimiento y conocimiento; verificar identidad, links/índices, cero peticiones de escritura, status intacto y pasos no auto-marcados. Sin WS18 el resto sigue válido.

FUTURO
P01/receptor emite recibos G_UI_READ/G_SPEC_VIEW por delta; supervisores de graph_ui/spec2viz promueven TaskDoc; WS16/WS30 validan lectura/edición y WS40 regenera el corpus.
