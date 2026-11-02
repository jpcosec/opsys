REFORMULACION
Propósito: integrar en el workspace la delegación e intervención humanas sobre ejecución Scion. Resultado: UI de graph_ui que invoca exclusivamente el adaptador público WS34 para dispatch/reply y registra la decisión humana mediante la operación de WS33.2; la revisión muestra actor humano y evidencia enlazada. Repo dueño: graph_ui. Límites: cambios en `frontends/mindmap/views/workspace/execution/` y `tests/`, con ruta fina al adaptador WS34 autorizada por WS12; sin autoaprobación, simulación ni sustitución de API/permisos ausentes.

AMBIGUEDADES
ninguna.

DRY-RUN
Lecturas: contrato WS12 del adaptador WS34; salidas WS34.1/.2; implementación WS35; operación/evidencia de WS33.1/WS33.2; estado de G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT, con recibos per-delta de WS36.
Cambios previstos: añadir en `execution/` la integración UI y la ruta fina al adaptador WS34; invocar solo dispatch/reply; registrar decisión con WS33.2; mostrar respuesta vinculada al intento, operación confirmada, actor y evidencia; mostrar error si faltan API/permisos; tests.
Dependencias: WS34 agregado completo, WS35 y, transitivamente, WS33/WS33.1/WS33.2. Si falta contrato, API, permiso o recibo de gate: detenerse, registrar hueco con dueño y dejar la operación no disponible; no crear sustituto.
Validación esperada: tests de vínculo respuesta-intento y confirmación; revisión con actor humano/evidencia; error visible por ausencia de API/permisos; ausencia de autoaprobación/simulación.

FUTURO
WS34 entrega el adaptador y sus hijos; WS35 la vista de ejecución; WS33.2 la operación de decisión y actor; WS12 fija contrato/canal; el solicitante/designee resuelve G_EXEC/G_SCION y los recibos per-delta de G_UI_WRITE/G_WRITE_CONTRACT. WS37 validará después con agente real; no es requisito de este nodo.
