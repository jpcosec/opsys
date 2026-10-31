REFORMULACION
PK03 no es una tarea ejecutable: agrupa la revisión y el resultado sustantivo de la Entrega L. Propósito: un lector temprano útil, con descubrimiento y navegación, validado por humano. Resultado del paquete: lector integrado que abre soporte modelado/no modelado, foco/historia, Code/grafo, búsqueda navegable y errores/degradación; Taller reproducible con dos desks y un repo sin desk; acta humana WS16 con mediciones P08 de apertura/búsqueda/arranque. Repo dueño de la agrupación: deskops; implementación en graph_ui; contrato y flujos en deskops. Límites: no ejecutar, no añadir aristas, no autorizar tareas, no editar/guardar, no Changes/Scion, no sustituir aprobación humana; guardado y WS30 quedan fuera. Completitud sustantiva = hijos cumplen + integración WS16, no solo gate de comprensión.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotético, sin ejecutar:
1. Entradas externas: contrato WS11 y user-flows WS08; G_UI_READ.
2. WS40 tras WS11/WS08: genera dos repos con desk y uno sin desk, stores/documentos, commits y manifiesto JSON. Entrega corpus/manifiesto a WS41 y WS16.
3. WS13 tras WS11: integra lector en graph_ui; WS13.1 aporta grafo/Code e integración documental; agrega explorador, dos documentos, tabs/historia y foco. Entrega UI/tests a WS14, WS15 y WS41.
4. WS14 y WS15 tras completar WS13, en paralelo: WS14 entrega búsqueda con estados vacío/error/degradado; WS15 entrega errores de lectura y orientación sin desk. Ambos alimentan WS16.
5. WS41 tras WS13, WS11 y WS40: lee dos stores del manifiesto, enlaces entre desks y errores de alias/path/store; entrega lectura multidesk a WS16.
6. WS16 al final, con WS14/15/08/40/41: humano recorre el Taller y mide apertura/búsqueda/arranque; registra acta y fallos. Integración probada por WS16; no implementa correcciones.

FUTURO
WS11 produce contrato; WS08, flujos; WS40, corpus/manifiesto; WS13/14/15/41, UI y pruebas; WS16, acta humana y mediciones. G_UI_READ debe satisfacerse; P08 y recepción de deltas los confirma el humano. WS30 medirá guardado. Fallos de WS16 se atribuyen por evidencia en repo receptor.
