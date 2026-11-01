REFORMULACION
Propósito: planificar en graph_ui un delta de edición de campos del workspace con precondición de escritura y conflicto visible, reutilizando editores/API. Resultado: cambios en `frontends/mindmap/views/workspace/fields/` y tests que permitan guardar/recargar dato real, rechazar escritura obsoleta conservando el texto local y mostrar el conflicto; campos workflow-protected no editables. Repo dueño: graph_ui. Límites: consume endpoints del contrato WS12 sin cambiarlo; mutación solo en desk en modo manual exclusivo; otros modos read-only; no raw-source ni semántica nueva.

AMBIGUEDADES
ninguna

DRY-RUN
El ejecutor leería WS19.1, el contrato WS12, la evidencia/gate G_PAYLOAD_PRECONDITION de WS45, el workspace integrado, editores/API existentes y pruebas. Crearía el módulo de campos bajo el output_scope, lo integraría en la vista workspace, llamaría a los endpoints WS12 con la precondición fijada, conservaría el buffer local ante rechazo, mostraría el conflicto como tal, bloquearía campos protegidos y aplicaría la guarda de modo manual exclusivo/read-only. Añadiría pruebas de guardado/recarga, escritura obsoleta y campos protegidos. Dependencias: WS12 debe publicar representación de precondición, whitelist, endpoints, definición operativa y prueba de modo manual exclusivo; WS45 debe satisfacer G_PAYLOAD_PRECONDITION; G_WRITE_CONTRACT y G_UI_WRITE se evalúan por delta; G_HUMAN_READ se exige antes de habilitar mutaciones en UI, no para desarrollo/pruebas aisladas. Si falta contrato, endpoint, precondición o evidencia del modo, se detendría, registraría el hueco con dueño y dejaría la operación no disponible, sin sustituto. Un conflicto conservaría el texto; un fallo de backend se mostraría honestamente. Validación: pruebas focalizadas y recibo por delta.

FUTURO
WS12 fija los detalles del contrato; WS45 verifica la precondición; WS16 produce G_HUMAN_READ; el receptor P01 emite el acta por delta en graph_ui; WS19 cierra cuando WS19.1 y WS19.2 cumplan. Nada de esto se ejecuta aquí.
