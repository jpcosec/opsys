REFORMULACION
Encargo de planificación para implementar en graph_ui la presentación de errores de lectura y modo degradado del workspace. Resultado: estados visibles para referencia rota, documento ausente, modelo no importable, backend caído, fuente sin capacidad de edición y fallo CDN, con pruebas; reutiliza la lectura Markdown de WS13.1. Repo dueño: graph_ui. Límites: depende de WS13 y G_UI_READ; no implementa otro lector ni guardado; no promete offline; no inventa respuesta si falta backend; usa el contrato WS11; promoción no autorizada.

AMBIGUEDADES
Ninguna. WS11 produce el contrato de errores/red/CDN y WS13.1 la lectura reutilizable; G_UI_READ pendiente es intencional y se evalúa por delta.

DRY-RUN
Lecturas: input completo (guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS15.1, vecinos WS13/WS15 y gate G_UI_READ).
Cambios previstos: ninguno en esta revisión; futuros en `graph_ui/frontends/mindmap/views/workspace/errors/` y `tests/`.
Dependencias: WS13/WS13.1 para lectura Markdown; WS11 para errores de API, red sin respuesta y CDN; G_UI_READ por delta. Si falta contrato, detener y registrar el hueco.
Validaciones futuras: distinguir error de API/red sin respuesta y fallo CDN; reintento tras restaurar backend recupera lectura conservando pestañas/foco/historia; CDN con diagnóstico visible y prueba de no carga; límite read-only visible; no borrar historial ni fingir vacío. Sin ejecutar nada.

FUTURO
WS11 entrega el contrato de errores/red; WS13.1 aporta la lectura reutilizable; el receptor humano P01 emite acta G_UI_READ por delta con commit/blob; WS06 gestiona integración/evidencia; la promoción fijará TaskDoc, archivos y pruebas.
