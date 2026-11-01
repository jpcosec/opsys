REFORMULACION
Propósito: que el lector workspace de graph_ui muestre errores de lectura y modo degradado sin crear otro lector ni guardado. Resultado: el panel afectado muestra referencia rota, documento ausente, modelo no importable y backend caído; no borra historial ni finge vacío; declara la fuente sin permiso como límite read-only, no como fallo; diagnostica el fallo CDN sin prometer offline. Repo dueño: graph_ui. Límites: salidas en frontends/mindmap/views/workspace/errors/, rutas de lectura del contrato WS11 y tests/; reutiliza la lectura Markdown de WS13.1; empaquetado offline queda fuera.

AMBIGUEDADES
1. «Fuente sin permiso/capacidad de edición es límite read-only visible, no fallo de lectura». La aceptación no indica cómo comprobar que es un límite y no un error. Obliga a inventar la evidencia y el criterio de aceptación de ese estado.
2. «pruebas distinguen ambos sin inventar respuesta del backend ausente». «Ambos» puede referirse a errores de API frente a estados de red sin respuesta, o a backend caído frente a fallo CDN. Obliga a inventar qué dos clases se contrastan y qué evidencia las separa.

DRY-RUN
Un ejecutor leería el contrato WS11 (transitivo por WS13), la lectura de WS13.1, el foco/historia de WS13.3, el panel actual y los tests. Comprobaría G_UI_READ como recibo per_delta de WS15.1, sin convertirlo en aceptación global. Crearía en errors/ los estados de error y su integración, sin lector ni guardado nuevos; mapearía errores de API y red sin respuesta al panel afectado, conservando historial; añadiría reintento que recupera lectura con pestañas/foco/historia y diagnóstico CDN con prueba de no carga. Validaría con store temporal real los casos de referencia rota, documento ausente, modelo no importable, backend caído, reintento y CDN. Si faltan WS11, la lectura de WS13.1 o el contrato de rutas, se detendría y registraría el hueco; no inventaría respuesta del backend ni recuperación offline.

FUTURO
WS11 produce el contrato de errores y rutas; WS13.1 la lectura; WS13.3 foco/historia; P01 emite el acta G_UI_READ por delta; el TaskDoc de promoción fija archivos, pruebas y textos; WS16 valida con el corpus WS40 cuando exista.
