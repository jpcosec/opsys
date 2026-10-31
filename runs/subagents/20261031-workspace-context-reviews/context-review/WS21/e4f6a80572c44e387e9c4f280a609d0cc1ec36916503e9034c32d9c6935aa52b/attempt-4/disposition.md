# Disposición WS21, ronda 2

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. error_reviewer: dag.yaml parameters.variant_rule: «Una variante añade sus depends_on/requires a los del nodo base; nunca los quita. Listas vacías significan que no añade nada.» La variante read_only con requires: [] no quita nada: siguen G_UI_WRITE y G_WRITE_CONTRACT del base. G_SOURCE nunca está en el base, solo lo añade editable, así que «No requiere G_SOURCE… read_only» no contradice.
2. corregido: WS21.scope -> nunca se descarta sin confirmación explícita de la persona usuaria; si no confirma, el buffer se conserva.
3. error_reviewer: WS21.scope: «Con pending no se prepara ni se promueve este nodo.» Con pending no hay ejecución ni aceptación que verificar; P04/WS07 resuelve el valor y WS12 acceptance añade «Tras WS07 source_mode ya no vale pending».
