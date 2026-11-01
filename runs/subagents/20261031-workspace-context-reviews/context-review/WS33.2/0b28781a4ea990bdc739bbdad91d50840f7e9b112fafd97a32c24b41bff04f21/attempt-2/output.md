## REFORMULACION
**Propósito:** registrar en deskops una decisión humana explícita —aprobar o pedir corrección— adoptada sobre un intento Scion, con actor humano identificado por el contrato WS12. **Resultado:** operación/adaptador, modelo o reporte y pruebas que persisten actor, referencia al intento y a su tarea, y resultado; no escribe estados validado/cerrado ni convierte `completed` del agente en aprobación. **Repo dueño:** deskops (`runtime/`, modelos/reportes, `tests/`). **Límites:** solo escribe la decisión por la operación que fije WS12; si falta contrato u operación, se registra hueco con dueño y no se crea sustituto. Requiere G_SCION y G_WRITE_CONTRACT; promoción no autorizada.

## AMBIGUEDADES
ninguna

## DRY-RUN
**Lecturas:** contrato WS12 (operación, campos, actor, revisión, errores); salida de WS32 (identidad de intento y vínculo con tarea); salida de WS33.1 (mensajes/resultados vinculados); evidencia de G_SCION producida por WS44; código existente `runtime/scion.py` y `services/closure.py` para no duplicar registro; esquema de RunDoc.

**Cambios previstos:** adaptador en `runtime/` que registra la decisión con actor, `intent_id`, `task_id`, resultado `aprobar|pedir_corrección` y texto obligatorio en corrección; validación que rechaza `completed` como aprobación; modelo/reporte asociado; pruebas focalizadas con fixture o doble local, sin tocar tablas Scion.

**Dependencias y gates:** WS32 y WS33.1 deben estar cumplidos; G_SCION verificado por WS44 antes de ejecutar; G_WRITE_CONTRACT `per_delta` para WS33.2 con recibo en `accepted_scope_nodes`.

**Errores esperados:** sin contrato WS12 → detener y registrar hueco con dueño; sin G_SCION → no ejecutar; intento inexistente o no resoluble → rechazar y no inventar vínculo; corrección sin texto → error; `completed` del agente → nunca aprobado.

**Validación esperada:** prueba de registro de aprobación y de corrección con actor, intento y tarea; rechazo de corrección vacía; rechazo de `completed` como aprobación; confirmación de que no escribe estados validado/cerrado ni modifica el cierre.

## FUTURO
WS33 cierra como agregado cuando WS33.1 y WS33.2 cumplen. WS34/WS36 consumen la decisión solo tras G_EXEC/G_SCION. WS44 produce G_SCION; WS12 produce el contrato; el receptor humano emite acta por delta y el operador Scion se designa al abordar el ramal E. La validez de la decisión se comprueba en uso humano real, no en este nodo.
