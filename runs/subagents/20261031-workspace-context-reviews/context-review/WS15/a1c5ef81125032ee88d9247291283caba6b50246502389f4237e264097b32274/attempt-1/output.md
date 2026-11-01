REFORMULACION
Propósito: agrupar en graph_ui la entrega de errores de lectura y modo degradado (WS15.1) y la orientación de proyecto sin desk (WS15.2). Resultado: WS15 es agregado no ejecutable; se cumple cuando ambos hijos cumplen su aceptación, y sus dependientes (WS16, WS29) siguen dependiendo de este ID. Repo dueño: graph_ui (`output_base: graph_ui:repository_root/`). Límites: reutiliza la base a1b2b22/f16fcd1/134a665 sin duplicar implementación ni inferir cierre por commit; no implementa otro lector ni guardado; G_UI_READ es por delta; empaquetado offline queda fuera.

AMBIGUEDADES
Ninguna.

DRY-RUN
WS15 no se ejecuta. WS15.1 escribiría en `frontends/mindmap/views/workspace/errors/` y tests; consumiría la lectura Markdown de WS13.1, las rutas de error del contrato WS11 y su recibo G_UI_READ. Cambios: panel de errores por proyección; validaría enlace roto, documento ausente, modelo no importable y backend caído sin borrar historial ni fingir vacío, límite read-only visible, fallo CDN declarado sin prometer offline, y reintento tras restaurar backend conservando pestañas/foco/historia. WS15.2 escribiría en `frontends/mindmap/views/workspace/orientation/` y tests; consumiría WS11 y su recibo; validaría orientación, ruta absoluta y comando `deskops init <ruta>` sin mutar por GET, y refresco tras init externo real. Sin arista entre hermanos: no se transfieren nada entre sí; comparten WS13 y WS11 y no solapan archivos (`errors/` vs `orientation/`). Integración conjunta: dos superficies read-only bajo `views/workspace/`; WS15 se validaría cuando existan ambos recibos per-delta y WS16 pueda ejecutar el recorrido humano. Si falta WS11, se detiene y registra el hueco según alcance.md, sin sustituto.

FUTURO
WS11 produce el contrato de errores y estados de red que WS15.1 consume. El receptor humano P01 (deltas graph_ui) emite G_UI_READ por delta concreto. WS13.1 aporta la lectura reutilizada. WS16 ejecuta la validación humana y mide tiempos; WS29 consume WS15 junto con WS24 para Changes. Ninguno de esos productos existe aún; WS15 no los sustituye.
