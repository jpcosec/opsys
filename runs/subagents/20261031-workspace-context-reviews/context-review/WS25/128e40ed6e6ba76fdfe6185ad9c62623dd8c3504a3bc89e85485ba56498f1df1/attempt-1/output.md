## REFORMULACION
**Propósito:** revisar WS25 como encargo de planificación, no como implementación. WS25 es un nodo `aggregate` de graph_ui que agrupa la UI de mensaje/ack y captura interna hacia drawer o protoátomo.
**Resultado:** agregado no ejecutable; se satisface cuando WS25.1 y WS25.2 cumplen su aceptación. No produce artefacto propio distinto de las salidas de sus hijos.
**Repo dueño:** `graph_ui`, con `output_base: graph_ui:repository_root/`.
**Límites:** operaciones permitidas por el contrato WS12; ack no equivale a aprobación; sin envío interdesk; sin tarea implícita ni cron de triage; captura con destino elegido explícitamente.
**Dependencias:** WS12 (contrato de operaciones), WS16 (lectura humana) y los hijos WS25.1/WS25.2. Gates: G_HUMAN_READ, G_UI_WRITE y G_WRITE_CONTRACT, todos pendientes y con resolutor declarado.

## AMBIGUEDADES
Ninguna.

Las posibles dudas quedan cubiertas por el propio input: la aceptación del agregado está definida; el repo y los límites son explícitos; la ausencia de una operación de respuesta se resuelve declarándola no disponible; y las decisiones Pxx pendientes tienen actor humano y no se aprueban aquí. La repetición de los hijos en `depends_on` es coherente con la semántica de agregado y no obliga a inventar nada.

## DRY-RUN
**Lecturas previstas (sin ejecutar):** nodo WS25 y contratos de vecinos en `dag.yaml`; guía; brief; alcance; decisiones; cobertura; gates.
**Cambios previstos:** ninguno sobre el plan ni el repo. Solo se emite este informe de revisión.
**Dependencias:** WS12 debe publicar la whitelist de operaciones y efectos; WS16 debe producir el acta G_HUMAN_READ; G_UI_WRITE requiere aceptación del delta por el responsable graph_ui designado.
**Validaciones futuras:** aceptación separada de WS25.1 y WS25.2; persistencia tras recarga; permisos del contrato; WS30 valida UF02 y la edición/operación manual. No se ejecuta ninguna prueba en este nodo.

## FUTURO
- WS12 produce el contrato de operaciones y la representación del origen de captura.
- WS16 produce el acta de lectura humana; un humano real la aprueba.
- El solicitante o quien designe resuelve P01/P03/P04/P06/P07 y designa responsables.
- El responsable de graph_ui acepta el delta de mutación (G_UI_WRITE).
- La promoción fijará archivos, TaskDoc, pills y evidencia; hoy está `not_authorized`.
- WS30 aporta la validación manual completa; una observación no equivale a aceptación.
