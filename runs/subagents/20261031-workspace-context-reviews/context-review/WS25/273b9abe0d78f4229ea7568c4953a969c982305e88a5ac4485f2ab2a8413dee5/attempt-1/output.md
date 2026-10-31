REFORMULACION

Propósito: WS25 es un agregado de revisión, no una tarea ejecutable, para integrar en la UI de `graph_ui` la lectura/ack de inbox y la captura interna en drawer/protoátomo mediante operaciones autorizadas por WS12; «triage» no se define como capacidad separada. Resultado: agregado de salidas de WS25.1 y WS25.2; se cumple cuando ambos hijos cumplen su aceptación. Repo dueño: `graph_ui`; `output_base: graph_ui:repository_root/`; `output_scope` agregado. Límites: ack no es aprobación; sin envío interdesk; sin tarea implícita ni cron de triage; G_HUMAN_READ se exige antes de habilitar mutaciones en UI, no para desarrollo/pruebas aisladas de API. Depende de WS12 y sus hijos; gates por delta. Promoción no autorizada.

AMBIGUEDADES

ninguna

DRY-RUN

Lecturas: guía de revisión, nodo WS25, gates y fuentes de contexto suministradas; no se revisan contratos vecinos ni se leen archivos no incluidos. Cambios previstos: ninguno; solo revisión del encargo. Dependencias: WS12 como productor del contrato; WS25.1 y WS25.2 como hijos; G_WRITE_CONTRACT y G_UI_WRITE con evaluación `per_delta` y `accepted_scope_nodes` vacíos; G_HUMAN_READ producido por WS16. Validaciones futuras: comprobar aceptación de ambos hijos, recibos por delta, acta humana de lectura antes de habilitar mutaciones UI y ausencia de tarea implícita o envío interdesk. Nada ejecutado.

FUTURO

WS12 publica el contrato de operaciones; WS16 produce G_HUMAN_READ; el receptor P01 emite en `graph_ui` el acta G_UI_WRITE del delta concreto; WS12 o el responsable registra `accepted_scope_nodes`; un humano decide la promoción. WS25.1 y WS25.2 producen sus salidas y pruebas; WS30 podrá validar UF02 cuando corresponda.
