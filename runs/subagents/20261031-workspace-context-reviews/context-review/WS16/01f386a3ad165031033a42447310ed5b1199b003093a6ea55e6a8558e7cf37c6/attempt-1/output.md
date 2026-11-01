## REFORMULACION
WS16 es un nodo de validación, no de implementación: una persona real recorre UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque sobre el corpus WS40, siguiendo `validacion-humana.md`. El resultado es evidencia y acta en `graph_ui:runs/subagents/workspace-documental-acceptance/lectura/acta.md`, que resuelve `G_HUMAN_READ`. Repo dueño: `graph_ui`. Límites: no crea corpus propio, no implementa correcciones, no muta entre desks, no mide guardados y no sustituye la aprobación humana.

## AMBIGUEDADES
1. «supervisor del repo receptor atribuye el fallo por evidencia»: no se identifica al supervisor ni cómo se designa; el ejecutor tendría que inventar el actor que atribuye el fallo.
2. «registra incidente/diagnóstico en repo/superficie antes de asignar nodo»: «superficie» y la ubicación del incidente no están definidas; obligaría a inventar repo, ruta y formato del registro.

## DRY-RUN
Un ejecutor futuro leería `dag.yaml` (WS16 y vecinos), `validacion-humana.md`, `cobertura.md`, `user-flows.md` y el manifiesto JSON de WS40. Ejecutaría el generador WS40 para preparar los desks temporales y el tercer repo sin desk; comprobaría que WS14, WS15 y WS41 están disponibles según sus contratos. Conduciría el recorrido humano: entrada/búsqueda, apertura de soporte, cambio de representación, retorno, diagnóstico de link roto y backend ausente, lectura del segundo desk y arranque sin desk. Mediría 20 aperturas y 10 búsquedas, registraría tiempos, ayudas y fallos; no mediría guardados. Escribiría el acta en la ruta de evidencia y la incluiría en el commit atómico de la tarea de validación. Si falta el manifiesto, un contrato o una capacidad dependiente, se detendría y registraría el hueco sin crear sustituto. Validación esperada: la persona completa el guion sin rutas memorizadas ni correcciones verbales; si supera umbrales P08 o hay fallo, el gate queda pendiente y se registra para corrección.

## FUTURO
La persona firmante decide la aceptación del recorrido; el supervisor del repo receptor atribuye fallos; otro nodo implementa correcciones si procede. `G_HUMAN_READ` se resuelve solo con acta versionada. WS30 medirá guardados y WS17/WS43 aportarán índices y publicación real.
