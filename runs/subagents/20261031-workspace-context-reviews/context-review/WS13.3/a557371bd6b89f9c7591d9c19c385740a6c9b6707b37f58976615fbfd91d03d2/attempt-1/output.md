REFORMULACION
Propósito: encargar a `graph_ui` un delta de UI para abrir documentos en pestañas/divisiones, cambiar documento activo y volver conservando foco e historia. Resultado: disposición local de sesión, dos documentos lado a lado y restauración de documento/foco/origen. Repo dueño: `graph_ui`; salidas en `frontends/mindmap/views/workspace/layout/` y `tests/`. Límites: no persistir disposición tras recargar, no tratarla como documento compartido, no duplicar workspace ni sustituir el lector de WS13.1; `G_UI_READ` sigue pendiente y la promoción no está autorizada.

AMBIGUEDADES
1. «Volver sigue el orden inverso de navegación.» No define qué acciones crean entrada de historia: ¿abrir documento, cambiar de pestaña, activar una división o varias? Obliga a inventar qué apila y desapila “volver”, y por tanto el criterio comprobable de historia.
2. «Pestañas, dos documentos lado a lado» no aclara si cada división tiene su propio conjunto de pestañas o si hay uno global. Obliga a inventar el modelo de disposición y cómo se abren/cierran pestañas entre divisiones.
3. «Abrir, cambiar y cerrar pestañas» no define qué documento queda activo al cerrar la pestaña activa ni si se permite cerrar la última. Obliga a inventar una transición de estado que la aceptación no cubre.

DRY-RUN
Lecturas previstas: contrato WS11, acta `G_UI_READ`, base de WS13.1 y `task-ws13-3.md`. Cambios previstos: componentes de layout/pestañas/divisiones e historia en `frontends/mindmap/views/workspace/layout/`, más pruebas en `tests/`. Dependencias: WS11, WS13.1 y `G_UI_READ` pendiente. Validaciones futuras: apertura/cambio/cierre de pestañas, dos documentos en divisiones, documento activo, atrás en orden inverso, foco y origen por documento asistido. Sin ejecutar nada.

FUTURO
WS11 produce contrato y acta de `G_UI_READ`; WS13.1 aporta lector/foco base; la promoción fijará archivos y escenarios en TaskDoc; una persona resuelve P07 y autoriza promoción. No son ambigüedades de este nodo.
