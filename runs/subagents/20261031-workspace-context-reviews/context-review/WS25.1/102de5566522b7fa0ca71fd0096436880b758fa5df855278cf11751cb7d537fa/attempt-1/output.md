## REFORMULACION

Propósito: revisar WS25.1 como encargo de planificación, no como implementación. Resultado: nodo comprensible y acotado para construir en `graph_ui` la lectura de inbox, el ack y, solo si WS12 lo define, la respuesta local dentro del mismo desk. Repo dueño: `graph_ui`; salida prevista en `frontends/mindmap/views/workspace/inbox/`, endpoints autorizados por WS12 y `tests/`. Límites explícitos: no envío interdesk, ack no equivale a aprobación, no crea tarea implícita ni cron de triage, y la respuesta queda “no disponible” si WS12 no define esa operación. Depende de WS12 y requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT por delta.

## AMBIGUEDADES

ninguna.

La posible indefinición de “respuesta local” queda cubierta por la propia aceptación: “respuesta local solo si el contrato WS12 define esa operación, y si no se declara no disponible”. WS12 es el productor nombrado y el hueco tiene conducta prescrita, por lo que no obliga a inventar.

## DRY-RUN

Lecturas: `context-review-guide.md`, `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`, nodo WS25.1, gates y bloques de contrato WS12/WS25 usados solo como contexto. Cambios previstos: ninguno; esta revisión no modifica archivos ni promueve el nodo. Dependencias: contrato de operaciones WS12; G_WRITE_CONTRACT por delta; G_UI_WRITE mediante acta del receptor P01; G_HUMAN_READ producido por WS16. Validaciones futuras, sin ejecutar: preflight del TaskDoc de promoción, comprobación de ack persistente tras recarga mostrando el mensaje origen, verificación de respuesta local disponible/no disponible según WS12, aplicación de permisos del contrato y pruebas dentro de `tests/`.

## FUTURO

WS12 debe publicar la whitelist/operaciones aplicables a inbox, ack y eventual respuesta local. WS16 produce la evidencia de G_HUMAN_READ; el receptor P01 en `graph_ui` produce el acta por delta de G_UI_WRITE. La promoción sigue no autorizada y exige TaskDoc, archivos, pills, átomos, evidencia y preflight. La implementación y sus pruebas corresponden al ejecutor futuro, no a esta revisión.
