REFORMULACION
WS27 es un nodo agregado de implementación en `graph_ui` cuyo encargo es integrar en el workspace la revisión de cambios y evidencia junto a la TaskDoc. Resultado: salidas de WS27.1 (diff Git e historial read-only por repo/tarea) y WS27.2 (evidencia declarada/encontrada/verificada). Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: “Agregado no ejecutable”; no escribe ni revierte; no muestra hallazgos de integridad del store; promoción no autorizada. Depende de WS13, WS12 y sus hijos; requiere G_UI_READ.

AMBIGUEDADES
Ninguna.

DRY-RUN
WS27 no se ejecuta: termina cuando WS27.1 y WS27.2 cumplen su aceptación. Lecturas: contrato del nodo, aceptación de hijos, WS13 (lector/workspace, historia y foco), WS12 (canal/operaciones), G_UI_READ y reglas de alcance. Cambios propios: ninguno. WS27.1 produce la vista de diff/historial en `frontends/mindmap/views/workspace/diff/` y tests; consume rutas del contrato WS11 y `TaskDoc.references/files`, y entrega diff e historial read-only acotados al repo y tarea. WS27.2 produce evidencia en `frontends/mindmap/views/workspace/evidence/` y tests; consume la correspondencia WS12 y `closeout verify`, y entrega estados distintos declarada/encontrada/verificada, con apertura de soporte o declaración de no soportado. No hay transferencia entre hijos: ambos transfieren sus salidas al agregado. Validación conjunta: ambas aceptaciones satisfechas, recibos G_UI_READ por delta, salidas coexistentes junto a la TaskDoc, sin escritura/commit, sin confundir evidencia ausente/fallida con verificada, y diff limitado a rutas/repos resolubles. Errores esperados: repo/ruta no resoluble => no disponible; comando/reporte ausente => no verificable; contrato faltante => detenerse y registrar hueco.

FUTURO
WS28 y WS35 consumen WS27; P01 emite recibos G_UI_READ por delta; la promoción e implementación quedan a autorización humana posterior.
