REFORMULACION
Propósito: implementar en graph_ui el alta y baja de relaciones permitidas por el contrato WS12 en el workspace, usando API real y la precondición de escritura que WS12 fije, sin definir semántica de relaciones en el componente. Resultado: UI bajo `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y tests; aceptación: alta/baja persisten y se confirman tras recargar, y relación no permitida o revisión obsoleta se rechaza con error visible. Repo dueño: graph_ui. Límites: depende de WS12; gates G_HUMAN_READ, G_PAYLOAD_PRECONDITION, G_UI_WRITE y G_WRITE_CONTRACT; solapa con el ticket de edición (serie, nunca duplicado paralelo); promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Nodo ejecutable (delivery), no agregado. Un ejecutor futuro leería `dag.yaml` (WS19.2), el contrato WS12 en `contratos/operaciones.md` (whitelist por campo/modelo, adapter y representación de precondición), WS11 para lectura, `reconciliacion.md` (C-13/C-14) y el código de graph_ui: `persistence.py` (`save`/`expected`), `connect-dialog.js`, `workspace-view.js`, `workspace_routes.py`; comprobaría el ticket de edición y sus tests. Cambios previstos: alta/baja en `views/workspace/relations/` contra endpoints autorizados, sin semántica propia; tests; integración como delta o extensión del ticket de edición, nunca en paralelo. Dependencias: contrato WS12, G_WRITE_CONTRACT por delta, G_PAYLOAD_PRECONDITION (WS45) y G_UI_WRITE (receptor P01); G_HUMAN_READ (WS16) solo antes de habilitar mutaciones en UI; desarrollo y pruebas aisladas de API pueden avanzar. Validación: store temporal real, persistencia tras recarga, rechazo visible de relación no permitida y revisión obsoleta; si falta contrato o API se registra hueco con repo dueño, sin sustituto.

FUTURO
WS12 publica whitelist, adapter y representación de precondición; WS45 verifica G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 de graph_ui emite G_UI_WRITE y G_WRITE_CONTRACT por este delta; WS19 cierra cuando cierran WS19.1 y WS19.2; los dependientes consumen WS19.
