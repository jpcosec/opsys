REFORMULACION
Propósito: entregar en graph_ui el alta/baja de relaciones permitidas por contrato dentro del workspace, usando API real y la precondición de escritura que fije WS12, sin definir semántica de relaciones en el componente. Resultado: interacción en `frontends/mindmap/views/workspace/relations/`, endpoints autorizados por WS12 y `tests/`; alta/baja persisten tras recargar y las operaciones no permitidas o con revisión obsoleta muestran error visible. Repo dueño: graph_ui. Límites: no tocar campos workflow-protegidos; no duplicar el ticket `editing` (`delta_or_existing_ticket; never_parallel_duplicate`); no habilitar uso de mutaciones en UI sin G_HUMAN_READ; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Nodo de ejecución, no agregado. Un ejecutor leería `dag.yaml` (WS19, WS19.1, WS19.2, gates), el contrato WS12 en `contratos/operaciones.md`, el contrato WS11, el ticket `editing` y `reconciliacion.md`; comprobaría Board y solapamiento. Con WS12 cerrado, tomaría whitelist de relaciones, endpoints/canal, representación de precondición y efectos por delta. Añadiría vistas y controladores bajo `views/workspace/relations/`, conectaría alta/baja a endpoints autorizados, aplicaría la precondición y mostraría rechazos; añadiría pruebas en `tests/`. Consumiría G_WRITE_CONTRACT (WS12), G_PAYLOAD_PRECONDITION (evidencia de WS45), G_HUMAN_READ (acta WS16) antes de habilitar mutaciones UI y G_UI_WRITE (acta P01 por delta). Si falta contrato, endpoint o precondición: detenerse, registrar hueco con repo dueño y no crear sustituto; la operación queda no disponible. Validación esperada: alta persiste tras recargar; baja persiste; relación no permitida rechazada con error visible; revisión obsoleta rechazada sin cambio visible; pruebas aisladas de API pueden avanzar antes del acta de lectura. La promoción fijará archivos, pruebas y textos.

FUTURO
WS12 publica contrato, whitelist, endpoints y precondición; WS45 aporta G_PAYLOAD_PRECONDITION; WS16 produce G_HUMAN_READ; el receptor P01 produce G_UI_WRITE por delta; WS06/promoción decide extender el ticket `editing` o crear delta nuevo, y el TaskDoc fija archivos, escenarios y textos.
