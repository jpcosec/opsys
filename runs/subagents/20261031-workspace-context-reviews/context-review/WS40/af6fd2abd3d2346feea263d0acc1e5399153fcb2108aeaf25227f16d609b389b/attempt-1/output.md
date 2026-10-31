## REFORMULACION
Propósito: definir un encargo de planificación para crear en `graph_ui` un generador reproducible del corpus Taller. Resultado: script/seed, fixtures y tests que crean tres repos temporales —dos con desk y uno sin desk—, stores y documentos, incluyendo Markdown no modelado, Code local y referencia rota; commits git reales, manifiesto JSON con roots/stores/commits/documentos clave, README de arranque y entrada mínima con enlaces a Board, FAQ y conocimiento; enlaces authored entre desks para UF08. Repo dueño: `graph_ui`. Límites: no toca desk real, no usa servidor fake, usa contrato WS11 y CLIs reales de deskops/sldb; plantillas WS17 opcionales; no implementa UI; promoción no autorizada.

## AMBIGUEDADES
ninguna.

## DRY-RUN
Lecturas: nodo WS40, guía, brief, alcance, decisiones, cobertura y contratos vecinos de WS11/WS08/WS16/WS17/WS41/gates; no reviso esos bloques ni ejecuto nada.

Cambios previstos: versionar generador y pruebas en `graph_ui`; producir corpus temporal, commits en repos temporales, manifiesto JSON e instrucciones; no escribir en desk real ni commitear corpus generado como registro competidor.

Dependencias: contrato WS11 y user-flows WS08; `G_UI_READ` por delta; CLIs verificados en WS02/WS03 por dependencia transitiva; plantillas WS17 solo después, sin bloquear el cierre inicial de WS40.

Validaciones futuras: ejecutar el comando dos veces y comprobar recreación aislada, commits git reales, manifiesto con roots/stores/commits/documentos clave y ausencia de escritura al desk real; verificar consumo por WS16/30 y regeneración posterior con plantillas WS17.

## FUTURO
WS17 aporta plantillas/índices y permite regenerar el corpus enriquecido; WS16 ejecuta la validación humana con el manifiesto; el receptor de `graph_ui` emite el recibo `G_UI_READ` por delta; la promoción fija TaskDoc, archivos, pills y preflight; WS30 integra índices.
