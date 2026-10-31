REFORMULACION
WS04 es un encargo de planificación de deskops: inventariar el estado observable de graph_ui (Board, tareas y código), identificar sesiones y solapamientos, y reconciliar el SPEC externo y el encargo que hubiera, dejando la correspondencia en auditoria/ui.md. Resultado: auditoria/ui.md con tareas externas (path, estado, hash SHA256, alcance), solapamientos y reconciliación del SPEC (coincidencias, discrepancias, ausencias con path/hash). Repo dueño: deskops. Límites: solo lectura de graph_ui; no cambiar tareas ni Board; no ejecutar UI; output_scope único; WS01 como dependencia. Los bloques edge WS01/WS06 no se revisan.

AMBIGUEDADES
1. «mapear a deltas existentes los nodos de este plan que toquen graph_ui (...) registrando la correspondencia en auditoria/ui.md». La aceptación exige tareas externas, solapamientos, SPEC y encargo, pero no una entrada por nodo del plan ni cómo marcar “sin delta”. Obligaría a inventar el criterio y la evidencia de completitud del mapeo.
2. «y cualquier encargo aportado al ejecutar». Define cuándo no hay encargo, pero no qué comparar ni con qué categorías si existe. Obligaría a inventar su tratamiento y salida.

DRY-RUN
Lecturas: dag.yaml/plan, brief, alcance, decisiones, cobertura, reconciliacion, task-ws04.md; Board, tareas, código y git status/herdr de graph_ui; SPEC en el path indicado; encargo opcional. Cambios previstos: crear/actualizar auditoria/ui.md; ningún cambio en Board ni tareas. Dependencias: WS01, acceso de lectura a graph_ui, SPEC y archivos de tarea. Validaciones futuras: path/estado/hash/alcance por tarea; solapamientos por tarea o archivos; correspondencia por nodo; SPEC con path/hash; registro de encargo o “no hubo”; output limitado a auditoria/ui.md.

FUTURO
WS06 usará la correspondencia para proponer deltas por repo; WS07 designa responsables y WS11/12 aceptan lectura/mutación; la promoción fija TaskDoc. El solicitante puede aportar el encargo o designar actor; las Pxx no se aprueban aquí.
