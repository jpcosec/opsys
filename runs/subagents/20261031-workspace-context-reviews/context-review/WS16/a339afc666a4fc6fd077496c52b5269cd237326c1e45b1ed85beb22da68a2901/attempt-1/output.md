## REFORMULACION
WS16 es un nodo de validación, no de implementación: un humano real debe recorrer lectura y descubrimiento (UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque/ausencia de desk) sobre el corpus producido por WS40. El resultado esperado es un acta en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/` y la resolución del gate `G_HUMAN_READ`. El repo dueño es `graph_ui`. Límites: no crea corpus propio, no muta el baseline, no sustituye la aprobación humana y no implementa correcciones ante fallos; solo los registra.

## AMBIGUEDADES
ninguna

## DRY-RUN
Lecturas previstas: nodo WS16, guía, `validacion-humana.md`, `cobertura.md`, `user-flows.md`, brief/alcance/decisiones, manifiesto de WS40 y salidas de WS14, WS15, WS41 y WS08. Cambios previstos: redactar el acta de lectura con guion, versiones/commits, corpus, comandos, tiempos, capturas y decisión del participante; registrar fallos y dejarlos listos para que el responsable del repo afectado abra la corrección. Dependencias: manifiesto y corpus WS40, segundo desk y tercer repo sin desk, lectura multidesk WS41, búsqueda WS14, errores/orientación WS15 y user-flows WS08; participante humano según P08. Validaciones futuras: recorrido humano sin rutas memorizadas, aperturas y búsquedas medidas, diagnóstico de link roto/backend ausente, lectura del segundo desk sin mutación, arranque y ausencia de desk; pruebas técnicas reportadas por separado.

## FUTURO
Otro nodo o un humano debe: confirmar el participante y presupuestos de P08; ejecutar el corpus WS40 antes de la sesión; emitir la decisión humana que resuelve `G_HUMAN_READ`; abrir tareas de corrección en el repo dueño si hay fallo; aportar índices WS17 y publicación WS43 en fases posteriores; y habilitar edición/guardados en WS30, no en WS16.
