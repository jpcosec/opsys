# Disposición WS44, ronda 3

Propuestas de un agente Pi DeepSeek, revisadas por el coordinador antes de aplicar.

1. corregido: WS44.scope -> Las capabilities mínimas son las que auditoria/scion.md marque como requeridas por WS32/WS33; si no las mapea por nodo, WS44 se detiene y registra el hueco antes del prob
2. corregido: WS44.scope -> El solicitante registra en WS07 qué acceso read-only tiene el operador; sin ese registro no se ejecuta el probe.
3. corregido: WS44.acceptance -> G_SCION se satisface solo con respuesta pública real, identidad del operador y Hub, fecha, capabilities y actor registrados.
Ajuste del revisor: WS05 ahora marca las capabilities requeridas y WS07 registra el acceso read-only, porque el hueco estaba en quien las produce.
