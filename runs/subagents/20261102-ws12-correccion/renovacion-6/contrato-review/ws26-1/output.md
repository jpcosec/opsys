REFORMULACION
WS26.1 debe implementar en graph_ui la preparación de un candidato en `desk/drawer/tasks/`, sin crear tarea activa ni tocar el Board. Resultado: UI de autoría con dos recorridos: candidato rastreado, guardado directo por `update` con `expected`, guarda de WS47 y admisión de WS48; candidato no rastreado, propuesta, handoff a `deskops edit task` y refresco verificable, sin escritura HTTP. Repo: graph_ui; alcance `frontends/mindmap/views/workspace/authoring/`, endpoints autorizados por WS12 y tests. Límites: no crear tarea activa/Board, no rastrear por reflejo, no ampliar S06, no inventar API, no editar `status/current_node/history/from_drawer`, no cerrar ni commitear. Depende de WS12, WS22, WS47 y WS48; consume `G_PAYLOAD_PRECONDITION`, `G_UI_WRITE`, `G_WRITE_CONTRACT`, `G_CLOSEOUT` y `G_HUMAN_READ`.

AMBIGUEDADES
1. «confirmado como TaskDoc, y si el store lo rastrea» (WS12, 4.4): no se define operación pública para saber si el store rastrea el candidato. Obligaría a inventar consulta o ruta de rastreo.
2. «endpoints autorizados por el contrato WS12» (WS26.1, `output_scope`): WS12 nombra `POST /save update` y el handoff sin HTTP, pero no fija la ruta graph_ui concreta ni su contrato de error. Obligaría a inventar nombres y forma del endpoint.
3. «referencias validadas (navegación autorizada, existencia, tipo PillDoc)» (WS26.1): el input no contiene las reglas de navegación autorizada. Obligaría a inventar resolución, alias y rechazos.

DRY-RUN
No es agregado: es un nodo de implementación. Un ejecutor futuro leería WS12 (3.3, 4.4, 6), WS22, WS47, WS48 y el código existente de authoring, `/api/save` y `deskops show task`. Añadiría vista/adaptador de autoría y pruebas; en recorrido A enviaría solo campos autorables con `expected`; en B generaría propuesta y comando solo tras las comprobaciones de selector, sin HTTP. Consumiría WS47 antes de habilitar documentos con contenido no declarado, WS48 antes de cualquier mutación y WS22 para lectura. Errores esperados: 409 sin perder buffer; selector coincidente sin comando; candidato sin rastreo no escribe. Validaría con tests de ambos recorridos, refresco, campos protegidos, pills y ausencia de escritura HTTP. Antes debe resolverse la ambigüedad de endpoint/rastreo.

FUTURO
WS47 entrega la guarda de contenido; WS48, la admisión; WS22, lectura/navegación. WS26.2 crea la tarea activa y la enruta. P01 registra el acta `G_UI_WRITE`; una persona decide `G_HUMAN_READ`. Root/planificación debe fijar endpoints y comprobación de rastreo.
