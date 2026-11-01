## REFORMULACION

**Propósito:** revisar WS25 como encargo de planificación, no como implementación. WS25 es un nodo `aggregate` cuyo objeto es agrupar la integración en UI de mensaje/ack y captura interna (drawer/protoátomo) mediante operaciones autorizadas por contrato.

**Resultado:** un agregado no ejecutable que se satisface cuando WS25.1 y WS25.2 cumplen su aceptación; sus dependientes siguen apuntando a WS25.

**Repo dueño:** `graph_ui`.

**Límites:** no confundir ack con aprobación; no enviar entre desks; no crear tarea implícita ni API/modelo por reflejo; mutaciones en UI sujetas a `G_HUMAN_READ`, `G_UI_WRITE` y `G_WRITE_CONTRACT` por delta. El nodo delega archivos, textos y pruebas al TaskDoc de promoción.

## AMBIGUEDADES

Ninguna.

El título menciona “triage”, pero el alcance y los hijos concretan sus dos efectos (ack/respuesta local y captura), sin exigir al ejecutor inventar un tercero. Las dependencias y gates son coherentes con la guía: los gates `per_delta` se evalúan por recibo del efecto concreto, y el agregado no ejecuta ni requiere aprobación conjunta.

## DRY-RUN

- **Lecturas previstas:** nodo WS25, hijos WS25.1/WS25.2 y aristas WS12/WS30 en `dag.yaml`; guía de revisión; `brief.md`, `alcance.md`, `decisiones.md`, `cobertura.md`.
- **Cambios previstos:** ninguno; revisión de solo lectura.
- **Dependencias:** contrato de operaciones WS12 (canal, campos, actor, revisión, errores y pruebas); aceptación de ambos hijos; recibos por delta de `G_UI_WRITE` y `G_WRITE_CONTRACT`; `G_HUMAN_READ` producido por WS16.
- **Validaciones futuras (no ejecutadas):** aceptación agregada al cerrar hijos; prueba de persistencia de ack y captura tras recarga; control de colisiones; validación humana UF02/03/04/05 en WS30.

## FUTURO

- WS12 debe publicar el contrato por operación, incluida la composición/wrapper para captura directa a drawer o el hueco con productor Deskops.
- El receptor P01 emite el acta de recepción por delta en `graph_ui`; Executor solo enlaza.
- WS16 produce el acta de lectura que habilita el uso de mutaciones en UI.
- WS25.1 y WS25.2 implementan y prueban sus efectos; WS30 valida manualmente el recorrido.
- La promoción fijará archivos, textos y escenarios dentro de la aceptación ya definida.
