REFORMULACION
Propósito: integrar en graph_ui la verificación de cierre y el handoff posterior. Resultado: una vista en `frontends/mindmap/views/workspace/review/` que usa `deskops closeout verify` por el canal del contrato WS12, muestra faltantes, permite preparar el cierre por CLI o solicitud al coordinador y refresca el estado; no cierra ni hace commit desde HTTP. Repo dueño: graph_ui. Límites: handoff no equivale a cierre; sin commit/close HTTP; sin terminal embebido genérico; gates humanos y por delta.

AMBIGUEDADES
1. «ofrecer handoff explícito con evidencia». No se define qué evidencia debe acompañar el handoff ni cómo se comprueba que es correcto. La aceptación solo exige mostrar faltantes y confirmar un cierre externo. Obliga a inventar el conjunto de evidencia (salida de verify, faltantes, comando preparado, task ID) y el criterio de éxito del handoff.
2. «Sin terminal embebido genérico.» No queda claro si prohíbe todo terminal o solo uno genérico. Un terminal específico de closeout podría ejecutar CLI desde la UI, contradiciendo el handoff y «No commit/close desde HTTP en baseline». Obliga a decidir si se permite ejecución embebida, con riesgo de exceder alcance.
3. «G_HUMAN_READ aplica porque es una acción de escritura del baseline» frente a «No commit/close desde HTTP en baseline» y el alcance de solo verificar/preparar. Obliga a inventar cuál sería esa acción de escritura de WS28 o si basta el handoff; si se toma literal, podría exigir implementar una mutación no prevista.

DRY-RUN
Lecturas: input, guía, brief, alcance, decisiones, `dag.yaml` (WS28, WS27, WS12, WS30, gates). Cambios previstos: vista de revisión, invocación de verify mediante adapter WS12, visualización de faltantes, preparación de comando/solicitud y refresco de estado. Dependencias: WS27 y WS12; G_CLOSEOUT satisfecho; G_HUMAN_READ pendiente de WS16; G_UI_WRITE y G_WRITE_CONTRACT pendientes por delta. Validaciones futuras: TaskDoc de promoción, aceptación UF05 con `deskops show task` y commit externo, recibos por delta y prueba de ausencia de terminal ejecutable. Sin ejecutar.

FUTURO
WS12 publica contrato y política de coordinador; WS16 produce el acta de G_HUMAN_READ; P01 acepta G_UI_WRITE por delta; WS27 entrega diff/evidencia; CLI o coordinador externo ejecuta el commit; WS30 valida UF05; el TaskDoc fija archivos, textos y escenarios.
