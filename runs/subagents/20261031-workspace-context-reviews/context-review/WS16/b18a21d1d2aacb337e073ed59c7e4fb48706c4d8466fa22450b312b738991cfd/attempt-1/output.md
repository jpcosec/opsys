## REFORMULACION

WS16 es un nodo de validación (`kind: validation`) de `graph_ui`. Su propósito es que una persona real recorra UF01, UF03 lectura, UF07 diagnóstico, UF08 lectura y UF10 arranque sobre el corpus y protocolo existentes, sin crear producto ni corpus propio. El resultado esperado es un acta con evidencia en `runs/subagents/workspace-documental-acceptance/lectura/acta.md`, tiempos y fallos, que resuelve o mantiene pendiente `G_HUMAN_READ`. Límites: consume el manifiesto de WS40; no implementa correcciones; no muta entre desks; no mide guardados; el agente no sustituye la aprobación humana; el gate habilita uso de mutaciones en UI, no desarrollo ni pruebas aisladas de API.

## AMBIGUEDADES

1. «supervisor del repo receptor atribuye el fallo por evidencia»: no se identifica al supervisor concreto ni el canal para entregarle el fallo; obligaría a inventar destinatario y forma de atribución.

2. «registra incidente/diagnóstico en repo/superficie antes de asignar nodo y abrir corrección»: no dice si registra WS16 o el supervisor, ni qué repo/superficie o artefacto cuenta como incidente; obligaría a inventar responsable y destino del registro.

## DRY-RUN

Un ejecutor futuro leería el manifiesto JSON de WS40 (roots, stores, commits, documentos clave), `validacion-humana.md`, `user-flows.md` y las decisiones P08. Prepararía el entorno con los dos desks temporales y el tercer repo sin desk ya generados, sin recrear corpus. Ejecutaría el guion UF01/UF03 lectura/UF07/UF08 lectura/UF10 usando búsqueda WS14, errores y modo degradado WS15 y lectura multidesk WS41; mediría al menos 20 aperturas, 10 búsquedas y el arranque. Escribiría únicamente el acta y soportes bajo `output_scope`, con versiones, comandos, timestamps, capturas y observaciones; no tocaría código ni corpus. Validaría que la persona completa el recorrido sin rutas memorizadas, que link roto y backend ausente muestran origen, y que un umbral P08 superado queda registrado como fallo con gate pendiente. Guardados quedan fuera hasta WS30.

## FUTURO

El supervisor del repo receptor atribuye el fallo y abre la corrección; WS30 prueba guardados; WS17 enriquece navegación y WS43 publica el desk real; una persona decide cualquier revisión explícita de umbrales; `G_HUMAN_READ` se resuelve con el acta versionada.
