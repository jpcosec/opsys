## REFORMULACION
WS25 es un nodo agregado, no ejecutable, del repo `graph_ui`. Su propósito es integrar en la UI el triage de mensajes —lectura, ack y respuesta local— y la captura interna hacia drawer o protoátomo, usando solo operaciones autorizadas por el contrato WS12. El resultado es el agregado de las salidas de WS25.1 y WS25.2. Límites: no confundir ack con aprobación; no crear tareas implícitas; no enviar entre desks; no inventar API, modelo o wrapper si WS12 no lo autoriza.

## AMBIGUEDADES
Ninguna. La aceptación del agregado es comprobable mediante sus hijos y el alcance queda delimitado por WS12, los gates y las reglas comunes de ejecución.

## DRY-RUN
Un ejecutor futuro no parchea WS25 directamente: comprueba que WS25.1 y WS25.2 cumplen su aceptación.

WS25.1 debe entregar la UI de inbox y ack/respuesta local en `frontends/mindmap/views/workspace/inbox/`, con endpoints autorizados y tests. Transfiere al agregado: ack persistente tras recarga, mensaje origen visible, respuesta solo si WS12 la define y, en caso contrario, declaración de no disponible; sin tarea implícita ni cron.

WS25.2 debe entregar la UI de captura en `frontends/mindmap/views/workspace/capture/`, con destino explícito, endpoints autorizados y tests. Transfiere: captura persistente en el destino elegido, origen tipado —ruta o mensaje— visible tras recarga, ausencia de tarea implícita y control de colisiones según contrato.

Dependencias consumidas: contrato WS12, `G_HUMAN_READ` para uso de mutaciones, `G_UI_WRITE` por delta y `G_WRITE_CONTRACT` por efecto. Si falta contrato o permiso, se detiene y se registra el hueco con repo dueño; no se crea sustituto. Validación conjunta: ambas aceptaciones, rutas y pruebas de hijos, cobertura del alcance de WS25 y ausencia de solapamiento. Un hijo incompleto bloquea el agregado.

## FUTURO
WS30 validará UF02 con recorrido humano. WS16 produce el acta de `G_HUMAN_READ`; el receptor P01 emite recibos por delta para `G_UI_WRITE`; WS12 produce `G_WRITE_CONTRACT`. La promoción exige TaskDoc y preflight posteriores, fuera de esta revisión.
