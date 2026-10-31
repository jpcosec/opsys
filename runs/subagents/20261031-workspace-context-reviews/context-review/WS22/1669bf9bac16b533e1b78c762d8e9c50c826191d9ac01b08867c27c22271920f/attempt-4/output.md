REFORMULACION

Propósito: encargo de implementación para que `graph_ui` renderice el Board real de deskops como trabajo navegable. Resultado: vista en `frontends/mindmap/views/workspace/board/` (más tests) que representa el Board como lista, tablero y dependencias, abriendo los TaskDoc y pills/átomos referenciados en el lector. Repo dueño: `graph_ui` (`output_base: graph_ui:repository_root/`). Límites: no reemplazar workflow con drag-and-drop de status; no duplicar tareas; no presentar predicado satisfecho como test aprobado; promoción no autorizada; integración delta o ticket existente, nunca duplicado paralelo. Depende de WS13 (lector) y WS09 (catálogo); requiere `G_UI_READ`.

AMBIGUEDADES

Ninguna.

DRY-RUN

Lecturas: guía, brief, alcance, decisiones, cobertura, reconciliación, nodo WS22, aristas WS13/WS09/WS26/WS30 y gates. Cambios previstos: ninguno; esta revisión no ejecuta ni promociona. Dependencias: WS13 y WS09; `G_UI_READ` (resolver WS11); transitivas por WS13. Validaciones futuras: acta de `G_UI_READ`; catálogo/contrato de Board de WS09; preflight task-only y precisión de archivos/pills/átomos/evidencia en promoción; validación humana WS30.

FUTURO

WS11 resuelve `G_UI_READ`; WS09 entrega el catálogo y contrato de Board; un humano o el nodo de promoción autoriza y fija el TaskDoc; WS30 valida; WS26 consume WS22. Las Pxx siguen pendientes y no se resuelven aquí.
