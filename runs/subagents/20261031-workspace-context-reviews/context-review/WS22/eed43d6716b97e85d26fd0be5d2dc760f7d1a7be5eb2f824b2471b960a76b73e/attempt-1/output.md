REFORMULACION
Propósito: que el Board real sea trabajo navegable en el workspace, sin sustituir el workflow Deskops. Resultado: tres representaciones —lista, tablero agrupado por estado y dependencias declaradas en el TaskDoc— que abren el mismo TaskDoc y comparten selección/links con el lector; estados y condiciones se leen de deskops (Board, lifecycle), no de dag.yaml. Repo dueño: graph_ui; salida en `frontends/mindmap/views/workspace/board/` y `tests/`. Límites: no drag-and-drop de status, no duplicar tareas, no presentar predicado satisfecho como test aprobado; promoción no autorizada.

AMBIGUEDADES
Ninguna. El nodo fija propósito, resultado, repo, límites, dependencias y aceptación comprobable. La forma exacta de las vistas, pills/átomos y escenarios queda delegada al TaskDoc de promoción; el contrato de Board corresponde a WS09/WS13, y la ausencia de contrato la resuelve alcance.md.

DRY-RUN
Lecturas: nodo WS22 y gate G_UI_READ en dag.yaml; guía, brief, alcance, decisiones, cobertura y reconciliacion; referencia a `task_file`. Cambios previstos: ninguno; esta revisión no ejecuta ni promueve. Dependencias: WS13 (lector, foco, links), WS09 (inventario/contrato de Board) y G_UI_READ con evaluación per_delta, cuyo recibo corresponde a WS22. Validaciones futuras: sobre TaskDoc real, comprobar que lista, tablero y dependencias abren el mismo TaskDoc; que estados/condiciones provienen de deskops; que no se duplican tareas ni se confunde predicado con test aprobado; validación humana en WS30.

FUTURO
WS13 produce el lector, foco y links; WS09 produce el inventario/contrato de Board; WS11 emite el acta de G_UI_READ por delta concreto; WS06 reconcilia al promover; el TaskDoc de promoción fija archivos, pills/átomos y escenarios; WS30 decide la aceptación humana; WS26 consume WS22. G_UI_READ permanece pendiente de forma intencional.
