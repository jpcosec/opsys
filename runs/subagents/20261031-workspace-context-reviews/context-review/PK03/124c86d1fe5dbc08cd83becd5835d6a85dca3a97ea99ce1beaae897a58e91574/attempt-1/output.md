REFORMULACION
PK03 es un paquete de revisión, no una tarea ejecutable. Su propósito es agrupar el lector útil temprano y el descubrimiento sin ID, con validación humana temprana. El resultado es un paquete integrado por lector, búsqueda, errores/orientación, corpus Taller y lectura entre desks, más acta humana de WS16. Repo dueño: `deskops`. Límites: no autoriza tareas ni añade aristas; no depende de edición, Changes ni Scion; las revisiones de comprensión no equivalen a producto entregado.

AMBIGUEDADES
Ninguna.

DRY-RUN
Hipotéticamente, tras los prerrequisitos externos WS11 y WS08, se ejecutaría WS13 y sus hijos WS13.1–13.3; WS13.1 aportaría grafo/Code y el agregado integraría documento/fuente, explorador modelado/no modelado, dos documentos lado a lado, tabs/historia y foco. En paralelo, cuando WS11/WS08 estén disponibles, WS40 generaría el corpus: dos desks y un repo sin desk, con commits reales y manifiesto JSON de roots, stores, commits y documentos clave. WS14 consumiría WS13 y el contrato WS11 para añadir búsqueda navegable, resultados con identidad/ruta y estados sin resultados/error/degradación. WS15 consumiría WS13 para errores de lectura y orientación sin desk. WS41 consumiría WS13, WS11 y WS40 para lectura segura del segundo desk, aliases autorizados y errores visibles. Finalmente WS16 consumiría WS14, WS15, WS08, WS40 y WS41: un humano recorrería el Taller, comprobaría lectura, búsqueda, errores, orientación y lectura entre desks, mediría aperturas/búsquedas/arranque P08 y registraría el acta; guardado no se mediría aquí. La validación conjunta usaría el manifiesto de WS40, abriría el repo sin desk y los dos desks, y verificaría que las salidas de los hijos están integradas sin exigir edición ni Scion.

FUTURO
WS11 y WS08 deben producir contrato de navegación y user-flows; WS40, el manifiesto del corpus; WS16, el acta humana con mediciones; los receptores/P01, los recibos G_UI_READ por delta. La aceptación humana y la eventual corrección tras fallos corresponden a WS16 y al supervisor del repo receptor.
