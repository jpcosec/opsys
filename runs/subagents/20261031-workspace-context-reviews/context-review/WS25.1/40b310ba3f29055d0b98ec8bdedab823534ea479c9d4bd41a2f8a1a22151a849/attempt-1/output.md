## REFORMULACION

WS25.1 es un encargo de implementación UI: leer el inbox del desk y registrar ack o respuesta local usando solo operaciones autorizadas por el contrato de WS12. Resultado: vista en `frontends/mindmap/views/workspace/inbox/` con tests, persistencia tras recarga y permisos aplicados; sin envío interdesk, sin crear tareas implícitas ni cron de triage, y sin tratar ack como aprobación. Repo dueño: `graph_ui`. Depende de WS12 y WS16; requiere G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, hoy `pending`. Promoción no autorizada.

## AMBIGUEDADES

1. «registrar ack o respuesta local» / «sin envío interdesk». No define qué es una “respuesta local”: ¿contestación al emisor dentro del desk, nota local o cambio de estado? Tampoco sus campos ni destino, ni el store/API que provee los mensajes del inbox. WS12 se nombra para «endpoints autorizados», no para el modelo del inbox ni la semántica de respuesta; obligaría a inventar resultado y UI.

2. «Ack y respuesta local persisten tras recargar con origen visible». No define qué metadato constituye “origen” —autor, canal, documento, mensaje padre— ni cómo mostrarlo; obligaría a inventar el criterio de aceptación.

## DRY-RUN

Lecturas: nodo WS25.1, guía, brief, alcance, decisiones, cobertura; edges WS12/WS16 y gates. Cambios previstos: UI de inbox y tests dentro del `output_scope`; sin envío interdesk. Dependencias: contrato WS12 y acta WS16; gates pendientes intencionales. Validaciones futuras: persistencia de ack/respuesta tras recarga con origen visible; permisos del contrato aplicados; ausencia de tarea implícita/cron; G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT antes de mutar. No se ejecuta nada.

## FUTURO

WS12 debe producir whitelist/endpoints y G_UI_WRITE/G_WRITE_CONTRACT; WS16 produce G_HUMAN_READ. El humano resuelve las Pxx y confirma gates. La promoción exige changed files/pills/atoms/evidence y preflight task-only. WS25 cierra cuando WS25.1 y WS25.2 cumplan.
