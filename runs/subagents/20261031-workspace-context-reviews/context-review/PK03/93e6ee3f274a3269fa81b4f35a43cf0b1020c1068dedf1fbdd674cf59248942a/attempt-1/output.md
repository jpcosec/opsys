REFORMULACION
Propósito: agrupar la entrega de un lector útil con descubrimiento sin ID y aceptación humana temprana. Resultado: paquete integrado donde una persona abre soporte modelado y no modelado, usa foco/historia/tabs, Code/grafo, busca y ve errores/degradación; existe Taller con dos desks y un repo sin desk; y acta WS16 con mediciones P08 de apertura/búsqueda/arranque. Repo dueño: deskops (agrupación); hijos ejecutables en graph_ui. Límites: no edición, Changes ni Scion; guardado solo WS30; la agrupación no autoriza tareas ni añade aristas; revisión de comprensión no equivale a producto.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético, sin ejecutar. Prerrequisitos externos: WS11 (contrato de navegación/identidad) y WS08 (user-flows, transitivo vía WS11). WS40 usa WS11/WS08 y CLIs reales para generar dos repos con desk, un tercer repo sin desk, stores, documentos, enlaces y manifiesto JSON. En paralelo, WS13 ejecuta WS13.1–13.3 sobre graph_ui con el registro existente: lector fuente/render, explorador modelado/no modelado, dos documentos lado a lado, tabs/historia/foco y Code/grafo; entrega lector integrado. WS14 consume ese lector y `sldb find`/`serve` según WS03/WS11: buscar, abrir, volver conservando consulta/foco; estados sin resultados/error/degradado. WS15 ejecuta WS15.1 (errores de lectura) y WS15.2 (orientación sin desk) sobre WS13. WS41 usa WS13, WS11 y manifiesto WS40: aliases/roots autorizados, segundo desk, volver por historia y errores por alias no autorizado/path escapado/store ausente. WS16 consume manifiesto WS40, WS14, WS15, WS41 y WS08; humano real recorre UF01/03/07/08/10, registra tiempos P08 de apertura/búsqueda/arranque y pruebas técnicas separadas, atribuye fallos y mantiene gate pendiente si se excede. Validación conjunta: aceptaciones de hijos más acta WS16; no se mide guardado. Gates: G_UI_READ en WS13/14/15/40/41; G_HUMAN_READ no bloquea desarrollo aislado.

FUTURO
WS11 produce el contrato; WS08 los user-flows; WS40 corpus/manifiesto; WS16 y el humano P01/P08 deciden aceptación y revisión de umbrales.
