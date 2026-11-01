## REFORMULACION
Propósito: integrar delegación e intervención humanas en el workspace mediante el adaptador WS34 (dispatch/reply) y el registro de decisiones con WS33.2, con actor y evidencia visibles. Resultado: componentes en graph_ui, bajo `frontends/mindmap/views/workspace/execution/`, que invocan solo WS34, registran/ven decisiones y muestran error si faltan API o permisos; sin autoaprobación ni simulación. Repo: graph_ui; deskops solo por rutas/contratos autorizados. Límites: depende de WS34/WS35; requiere G_EXEC, G_SCION, G_UI_WRITE y G_WRITE_CONTRACT; no implementa adaptador ni registro. Nodo `implementation`, no agregado.

## AMBIGUEDADES
1. «registrar decisiones con WS33.2» frente a `output_scope`: «ruta fina hacia el adaptador WS34 autorizada por contrato WS12». Solo se autoriza ruta a WS34, no el canal hacia WS33.2; obligaría a inventar la ruta/operación de esa escritura o si WS34 la transporta.
2. «la revisión muestra actor humano y evidencia enlazada de WS33.1/WS33.2»: «revisión» no se define aquí (el glosario la trata como precondición de escritura); obligaría a inventar qué superficie de revisión existe y qué muestra.

## DRY-RUN
Lecturas: contrato/API WS34; contrato WS12 y operación de WS33.2; datos de WS33.1/WS33.2; vistas WS35; gates. Cambios: en `execution/`, acciones dispatch/reply que llamen solo a WS34; acción de decisión por la operación WS33.2; render de actor/evidencia; estados de error; tests. Dependencias: WS34, WS35 y, transitivamente, WS33/WS33.2; gates pendientes: sin recibo por delta no se habilita. Errores: adaptador ausente, permiso denegado, timeout, respuesta no vinculada; mostrar y testear. Validación: test de respuesta ligada al intento y operación confirmada; test de revisión con actor/evidencia; test de error sin API/permisos; sin autoaprobación. No se ejecuta nada.

## FUTURO
WS12 fija la operación de decisión; WS33.2 la implementa; WS34 publica el adaptador; G_SCION/WS44 y G_EXEC los produce el operador/humano; G_UI_WRITE se recibe por delta; WS37 valida con agente real. Son insumos/decisiones externas, no ambigüedad.
