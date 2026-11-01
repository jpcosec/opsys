REFORMULACION
WS36 es un nodo de implementación en graph_ui que integra delegación e intervención humanas. Propósito: que la persona despache/responda solo mediante el adaptador WS34 y registre decisiones con WS33.2, con actor y evidencia visibles. Resultado: vista en frontends/mindmap/views/workspace/execution/ y tests, incluida una ruta fina al adaptador autorizada por contrato WS12. Límites: no autoaprobación ni simulación; ausencia de API/permisos debe mostrarse como error; gates G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT siguen pendientes; promoción no autorizada.

AMBIGUEDADES
ninguna.

DRY-RUN
Un ejecutor futuro leería el nodo, task_file, WS12, WS34, WS33.2, WS35 y estado de gates. Crearía/modificaría UI y tests en el output_scope de graph_ui: invocación exclusiva del adaptador WS34 para dispatch/reply; llamada a la operación de WS33.2 para registrar la decisión; presentación de actor humano y enlaces a evidencia WS33.1/WS33.2; estado de error ante API/permisos ausentes. Consumiría el adaptador de WS34, la vista/trazabilidad de WS35 y el registro de WS33.2, sin sustituirlos. Si falta contrato, API o permiso, se detendría y mostraría error, según reglas comunes; no inventaría sustituto. Validaría con tests: respuesta ligada al intento, operación confirmada, decisión con actor/evidencia, error visible y ausencia de autoaprobación/simulación. La promoción exigiría TaskDoc/preflight de solo tarea y recibos por delta de G_UI_WRITE/G_WRITE_CONTRACT, además de G_EXEC/G_SCION.

FUTURO
WS12 fijará operaciones, campos, revisión esperada y ruta fina; WS34 entregará el adaptador y su confirmación; WS33.2 fijará el registro de decisión; WS35 entregará lectura/trazabilidad; los resolvers emitirán recibos por delta; WS37 hará la validación humana real. No son ambigüedades de este nodo.
